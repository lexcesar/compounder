#!/usr/bin/env python3
"""Unit tests for dispatch-cost.py. Run: python3 compounder/scripts/test_dispatch_cost.py"""
import importlib.util
import json
import os
import re
import subprocess
import sys
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
        self.assertEqual(dc.price_for("claude-fable-5-1"), dc.PRICES["claude-fable-5-1"])
        self.assertEqual(dc.price_for("claude-fable-5"), dc.PRICES["claude-fable-5"])

    def test_fable_5_and_5_1_differ_on_cache_read(self):
        self.assertEqual(dc.price_for("claude-fable-5")[1], 1.0)
        self.assertEqual(dc.price_for("claude-fable-5-1")[1], 0.25)

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

    def test_model_tie_is_deterministic_across_hash_seeds(self):
        # The hash seed is fixed per process, so the tie has to be tried in separate processes.
        p = write_jsonl([rec("m1", "claude-sonnet-5", inp=1), rec("m2", "claude-opus-5", inp=1)])
        seen = set()
        for seed in range(10):
            out = subprocess.run([sys.executable, SCRIPT, "--json", p], capture_output=True, text=True,
                                 check=True, env=dict(os.environ, PYTHONHASHSEED=str(seed))).stdout
            seen.add(json.loads(out.splitlines()[0])["model"])
        self.assertEqual(seen, {"claude-opus-5"})  # ties break alphabetically

    def test_zero_token_synthetic_record_is_not_a_turn(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5", read=100_000),
                         rec("m2", "<synthetic>"),
                         rec("m3", "claude-sonnet-5", read=100_000)])
        r = dc.analyze(p, {"agentType": "x"})
        self.assertEqual(r["turns"], 2)
        self.assertEqual(r["misses"], [])

    def test_zero_token_unknown_model_turn_does_not_void_usd(self):
        p = write_jsonl([rec("m1", "<synthetic>"), rec("m2", "claude-sonnet-5", inp=1_000_000)])
        self.assertAlmostEqual(dc.analyze(p, {})["usd_est"], dc.PRICES["claude-sonnet-5"][0], places=6)

    def test_unknown_model_with_tokens_voids_usd(self):
        p = write_jsonl([rec("m1", "claude-unknown-9", inp=5)])
        self.assertIsNone(dc.analyze(p, {})["usd_est"])


class Misses(unittest.TestCase):
    def test_drop_over_threshold_is_flagged_and_exact_threshold_is_not(self):
        turns = [{"read": 100_000, "write": 0}, {"read": 80_000, "write": 20_000},
                 {"read": 60_000, "write": 20_000}]
        self.assertEqual(dc.misses(turns), [(3, 80_000, 60_000)])

    def test_read_drop_without_rewrite_is_compaction_not_a_miss(self):
        turns = [{"read": 100_000, "write": 0}, {"read": 30_000, "write": 2_000}]
        self.assertEqual(dc.misses(turns), [])

    def test_read_drop_with_rewrite_is_a_miss(self):
        turns = [{"read": 100_000, "write": 0}, {"read": 30_000, "write": 100_000}]
        self.assertEqual(dc.misses(turns), [(2, 100_000, 30_000)])


class ProjectDir(unittest.TestCase):
    def test_dots_and_slashes_map_to_dashes_like_claude_code(self):
        d = dc.project_dir_for("/Users/x/Projetos/alexcesar.com/portfolio")
        self.assertTrue(d.endswith("/.claude/projects/-Users-x-Projetos-alexcesar-com-portfolio"))


class LogLine(unittest.TestCase):
    def documented_keys(self):
        routes = os.path.join(HERE, "..", "..", "ROUTES.md")
        text = open(routes, encoding="utf-8").read()   # a missing ROUTES.md is an error, not a skip
        section = text[text.index("## Logging duty"):]
        template = re.search(r"```json\n(\{.*?\})\n```", section, re.S).group(1)
        keys = set(json.loads(template))
        keys |= set(re.findall(r'`"(tokens_\w+|usd_est)"`', section))
        return keys

    def row(self):
        p = write_jsonl([rec("m1", "claude-sonnet-5-5", inp=16, w1h=17_565, read=134_211, out=1_587)])
        return dc.analyze(p, {"agentType": "compounder:fork-executor", "description": "toy plan"}), p

    def test_keys_match_what_routes_md_documents(self):
        r, p = self.row()
        self.assertEqual(set(dc.log_line(r)), self.documented_keys())

    def test_values_are_exact_and_model_is_the_resolved_id(self):
        r, p = self.row()
        line = dc.log_line(r)
        self.assertEqual((line["tokens_in"], line["tokens_cache_write"], line["tokens_cache_read"],
                          line["tokens_out"]), (16, 17_565, 134_211, 1_587))
        self.assertEqual(line["model"], "claude-sonnet-5-5")
        self.assertEqual(line["route"], "compounder:fork-executor")
        self.assertEqual(line["task"], "toy plan")

    def test_cli_prints_one_line_per_dispatch_and_skips_the_root_session(self):
        r, p = self.row()
        out = subprocess.run([sys.executable, SCRIPT, "--log-line", p], capture_output=True, text=True,
                             check=True).stdout
        self.assertEqual(out, "")   # a lone transcript without meta is the root session, not a dispatch


SCRIPT = os.path.join(HERE, "dispatch-cost.py")

if __name__ == "__main__":
    unittest.main()
