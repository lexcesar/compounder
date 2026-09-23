#!/usr/bin/env python3
"""Unit tests for dispatch-cost.py. Run: python3 compounder/scripts/test_dispatch_cost.py"""
import importlib.util
import json
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("dc", os.path.join(HERE, "dispatch-cost.py"))
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)


def rec(mid, model, inp=0, w5=0, w1h=0, read=0, out=0, split=True):
    usage = {
        "input_tokens": inp,
        "cache_creation_input_tokens": w5 + w1h,
        "cache_read_input_tokens": read,
        "output_tokens": out,
    }
    if split:
        usage["cache_creation"] = {"ephemeral_5m_input_tokens": w5, "ephemeral_1h_input_tokens": w1h}
    return {"type": "assistant", "uuid": "u-" + mid + str(out),
            "message": {"id": mid, "model": model, "usage": usage}}


def write_jsonl(lines):
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as fh:
        for l in lines:
            fh.write(l if isinstance(l, str) else json.dumps(l))
            fh.write("\n")
    return path


class PriceFor(unittest.TestCase):
    def test_longest_prefix_wins_regardless_of_table_order(self):
        self.assertEqual(dc.price_for("claude-opus-5-5"), dc.PRICES["claude-opus-5-5"])
        self.assertEqual(dc.price_for("claude-opus-5"), dc.PRICES["claude-opus-5"])
        self.assertEqual(dc.price_for("claude-fable-5-1"), dc.PRICES["claude-fable-5"])

    def test_unknown_model_is_none(self):
        self.assertIsNone(dc.price_for("<synthetic>"))


class TurnsOf(unittest.TestCase):
    def test_dedup_by_message_id_keeps_last_record(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", out=10), rec("m1", "claude-sonnet-5", out=25)])
        turns = dc.turns_of(p)
        self.assertEqual(len(turns), 1)
        self.assertEqual(turns[0]["output"], 25)

    def test_cache_write_split_by_ttl(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", w5=100, w1h=900)])
        t = dc.turns_of(p)[0]
        self.assertEqual((t["write_5m"], t["write_1h"], t["write"]), (100, 900, 1000))

    def test_missing_split_counts_as_1h(self):
        # Claude Code writes 1h caches; old transcripts without the split field are priced as such.
        p = write_jsonl([rec("m1", "claude-sonnet-5", w1h=500, split=False)])
        t = dc.turns_of(p)[0]
        self.assertEqual((t["write_5m"], t["write_1h"]), (0, 500))

    def test_non_dict_json_line_is_skipped(self):
        p = write_jsonl(["null", "[1,2]", rec("m1", "claude-sonnet-5", out=3)])
        self.assertEqual(len(dc.turns_of(p)), 1)


class ClassifyTurn1(unittest.TestCase):
    def t(self, write, read, inp=0):
        return {"write": write, "read": read, "input": inp}

    def test_fresh_below_ceiling(self):
        self.assertEqual(dc.classify_turn1(self.t(18_000, 0))[0], "fresh")

    def test_same_model_fork_reads_parent_cache(self):
        self.assertEqual(dc.classify_turn1(self.t(2_000, 150_000))[0], "fork:same-model")

    def test_cross_model_fork_rewrites_parent_context(self):
        self.assertEqual(dc.classify_turn1(self.t(150_000, 0))[0], "fork:cross-model")

    def test_boundary_at_ceiling_is_fresh(self):
        self.assertEqual(dc.classify_turn1(self.t(dc.FRESH_CEILING, 0))[0], "fresh")


class Analyze(unittest.TestCase):
    def test_root_session_row_is_not_classified_as_a_dispatch(self):
        p = write_jsonl([rec("m1", "claude-fable-5-1", w1h=60_201)])
        r = dc.analyze(p, {})
        self.assertEqual(r["agent"], "session")
        self.assertEqual(r["turn1"], "root")

    def test_subagent_row_is_classified(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", w1h=18_000)])
        r = dc.analyze(p, {"agentType": "x"})
        self.assertEqual(r["turn1"], "fresh")

    def test_usd_prices_1h_writes_at_2x_and_5m_at_1_25x(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", inp=1_000_000, w5=1_000_000, w1h=1_000_000,
                             read=1_000_000, out=1_000_000)])
        inp, read, out = dc.PRICES["claude-sonnet-5"]
        expected = inp + inp * 1.25 + inp * 2 + read + out
        self.assertAlmostEqual(dc.analyze(p, {})["usd_est"], expected, places=6)

    def test_usd_is_priced_per_turn_not_by_majority_model(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", inp=1_000_000),
                         rec("m2", "claude-sonnet-5", inp=1_000_000),
                         rec("m3", "claude-opus-5", inp=1_000_000)])
        expected = 2 * dc.PRICES["claude-sonnet-5"][0] + dc.PRICES["claude-opus-5"][0]
        self.assertAlmostEqual(dc.analyze(p, {})["usd_est"], expected, places=6)

    def test_model_tie_is_deterministic(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", inp=1), rec("m2", "claude-opus-5", inp=1)])
        seen = {dc.analyze(p, {})["model"] for _ in range(20)}
        self.assertEqual(seen, {"claude-opus-5"})  # ties break alphabetically

    def test_zero_token_unknown_model_turn_does_not_void_usd(self):
        p = write_jsonl([rec("m1", "<synthetic>"), rec("m2", "claude-sonnet-5", inp=1_000_000)])
        self.assertAlmostEqual(dc.analyze(p, {})["usd_est"], dc.PRICES["claude-sonnet-5"][0], places=6)

    def test_unknown_model_with_tokens_voids_usd(self):
        p = write_jsonl([rec("m1", "claude-unknown-9", inp=5)])
        self.assertIsNone(dc.analyze(p, {})["usd_est"])


class Misses(unittest.TestCase):
    def test_drop_over_threshold_is_flagged_and_exact_threshold_is_not(self):
        turns = [{"read": 100_000}, {"read": 80_000}, {"read": 60_000}]
        self.assertEqual(dc.misses(turns), [(3, 80_000, 60_000)])


class ProjectDir(unittest.TestCase):
    def test_dots_and_slashes_map_to_dashes_like_claude_code(self):
        d = dc.project_dir_for("/Users/x/Projetos/alexcesar.com/portfolio")
        self.assertTrue(d.endswith("/.claude/projects/-Users-x-Projetos-alexcesar-com-portfolio"))


if __name__ == "__main__":
    unittest.main()
