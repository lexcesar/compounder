#!/usr/bin/env python3
"""Unit tests for review-recall.py. Run: python3 compounder/scripts/test_review_recall.py"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "review-recall.py")
GOLDEN = os.path.join(HERE, "..", "..", "docs", "pipeline", "golden", "c8432b8.json")
spec = importlib.util.spec_from_file_location("rr", SCRIPT)
rr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rr)

REPORT = """**VERDICT: reservations.** The cost estimate is below the real one.

**CONFIRMED (by severity)**

1. **[SEVERE]** `dispatch-cost.py:63,99` — cache write priced at a fixed 1.25x rate.
   - Scenario: 19,248 records carry `ephemeral_1h_input_tokens`.
   - Fix: price the 1h write at 2x.
2. **[MEDIUM]** `count-tokens.sh:32` — the API key goes in curl's argv.
   - Scenario: `ps -axww` showed the key during the call.

**SUSPICIONS (inconclusive)**
- A finding about something nobody has listed yet, in `resolve()`.

**MINOR**
- `dispatch-cost.py:53`: a non-object JSON line (`null`) kills the run with `AttributeError`.

**DISCARDED BY THE TRIBUNAL:** 1 refuted.
- Empate de modelo muda entre execuções por hash seed: refutado, não reproduz.

**COVERAGE**
- Nothing found in shell injection. No tests were run against the API key in argv path.
"""


def golden():
    return rr.load_golden(GOLDEN)


def run(args, **kw):
    return subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, **kw)


def tmpfile(text, suffix):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w") as fh:
        fh.write(text)
    return path


class Score(unittest.TestCase):
    def test_matches_carry_the_level_the_report_gave(self):
        s = rr.score(REPORT, golden())
        found = {m["id"]: m["level"] for m in s["matched"]}
        self.assertEqual(found, {"G01": "SEVERE", "G06": "MEDIUM", "G08": "MINOR"})
        self.assertEqual(s["recall"], 3)
        self.assertEqual(s["total"], 17)

    def test_nested_bullets_belong_to_their_item(self):
        # "1h" and "2x" sit in sub-bullets of finding 1; the match needs the whole item
        report = REPORT.replace("cache write priced at a fixed 1.25x rate", "cache write is priced wrong")
        self.assertIn("G01", {m["id"] for m in rr.score(report, golden())["matched"]})

    def test_refuted_and_coverage_sections_do_not_count(self):
        s = rr.score(REPORT, golden())
        self.assertNotIn("G04", {m["id"] for m in s["matched"]})   # only in DISCARDED
        self.assertEqual([r["id"] for r in s["refuted"]], ["G04"])
        self.assertEqual(sum(m["id"] == "G06" for m in s["matched"]), 1)   # COVERAGE line ignored

    def test_unmatched_findings_are_listed_for_adjudication(self):
        s = rr.score(REPORT, golden())
        self.assertEqual(len(s["unmatched"]), 1)
        self.assertIn("nobody has listed", s["unmatched"][0]["text"])
        self.assertEqual(s["unmatched"][0]["level"], "SUSPICION")

    def test_one_item_can_match_two_defects(self):
        report = "**CONFIRMED**\n1. [MEDIUM] `count-tokens.sh` — API key and body in argv; past ARG_MAX it fails.\n"
        self.assertEqual({m["id"] for m in rr.score(report, golden())["matched"]}, {"G06", "G07"})

    def test_report_without_findings_scores_zero(self):
        s = rr.score("**VERDICT: approved.**\n\n**COVERAGE**\n- four lenses, nothing found.\n", golden())
        self.assertEqual((s["recall"], s["unmatched"]), (0, []))

    def test_removing_a_golden_entry_lowers_the_score(self):
        g = golden()
        g["defects"] = [d for d in g["defects"] if d["id"] != "G01"]
        self.assertEqual(rr.score(REPORT, g)["recall"], 2)

    def test_portuguese_headings_and_levels(self):
        report = ("**VEREDITO: reservas.**\n\n**CONFIRMADOS**\n"
                  "1. **[GRAVE]** Sessão nova rotulada como fork:cross-model.\n\n"
                  "**DESCARTADOS PELO TRIBUNAL:** nada.\n")
        s = rr.score(report, golden())
        self.assertEqual([(m["id"], m["level"]) for m in s["matched"]], [("G02", "SEVERE")])


class Formats(unittest.TestCase):
    """Report shapes seen in real runs (calibration of 2026-09-29)."""

    def test_plain_headings_and_tagged_paragraphs_inside_a_code_block(self):
        report = ("```\nVERDICT: reservations — real bugs.\n\nCONFIRMED (by severity):\n\n"
                  "[SEVERE] dispatch-cost.py:92-99 — usd_est prices ALL tokens at one majority model.\n\n"
                  "[MEDIUM] count-tokens.sh:31 — API key passed as curl argv, visible in ps.\n\n"
                  "MINOR (grouped):\n- `--json` flag has no consumer.\n\n"
                  "DISCARDED BY THE TRIBUNAL: 0\n```\n")
        s = rr.score(report, golden())
        self.assertEqual([(m["id"], m["level"]) for m in s["matched"]], [("G03", "SEVERE"), ("G06", "MEDIUM")])
        self.assertEqual([u["level"] for u in s["unmatched"]], ["MINOR"])

    def test_menu_after_the_report_is_not_a_finding(self):
        report = ("**CONFIRMED**\n1. [MEDIUM] API key in curl argv.\n\n**MINOR**\n- `--help` uses sed.\n\n"
                  "Review pronta (1 confirmado, 1 minor). Próximo passo?\n"
                  "1. Aplicar só a classe segura.\n2. Corrigir item a item.\n3. Só registrar.\n")
        s = rr.score(report, golden())
        self.assertEqual(len(s["unmatched"]), 1)

    def test_labelled_sub_bullets_at_the_same_indent_stay_with_their_finding(self):
        report = ("**CONFIRMED**\n**B — classify_turn1**\n- [MEDIUM] `classify_turn1` tem um quadrante sem tratamento.\n"
                  "- Cenário: read e write ambos acima de 60k sai `fresh`.\n- Realismo: 0 de 151.\n- Fix: definir a fronteira.\n")
        s = rr.score(report, golden())
        self.assertEqual([m["id"] for m in s["matched"]], ["G11"])
        self.assertEqual(s["unmatched"], [])

    def test_level_word_deep_in_the_text_does_not_override_the_section(self):
        report = ("**MINOR**\n- Não há teste automatizado: `unittest` é stdlib. O tests-reviewer marcou SEVERE, "
                  "eu rebaixei.\n")
        self.assertEqual([(m["id"], m["level"]) for m in rr.score(report, golden())["matched"]], [("G09", "MINOR")])

    def test_a_dollar_amount_is_not_a_cache_read_price(self):
        report = "**CONFIRMED**\n1. [MEDIUM] Empate vira para fable e o estimado cai para US$ 240,25.\n"
        self.assertNotIn("G12", {m["id"] for m in rr.score(report, golden())["matched"]})


class Agreement(unittest.TestCase):
    def s(self, **levels):
        return {"matched": [{"id": k, "level": v} for k, v in levels.items()]}

    def test_share_of_placements_that_carry_the_modal_level(self):
        runs = [self.s(G01="SEVERE", G06="MEDIUM"), self.s(G01="SEVERE", G06="MINOR"),
                self.s(G06="MEDIUM", G09="MINOR")]
        a = rr.agreement(runs)
        # G01: 2 of 2; G06: 2 of 3; G09 found once, not counted
        self.assertEqual((a["agree"], a["placements"]), (4, 5))
        self.assertEqual(a["per_defect"]["G06"], {"SEVERE": 0, "MEDIUM": 2, "MINOR": 1, "OTHER": 0})
        self.assertNotIn("G09", a["per_defect"])

    def test_no_defect_found_twice_is_an_error_not_full_agreement(self):
        with self.assertRaises(ValueError):
            rr.agreement([self.s(G01="SEVERE"), self.s(G02="MINOR")])


class Cli(unittest.TestCase):
    def transcript(self, texts):
        lines = [json.dumps({"type": "assistant", "message": {"id": "m%d" % i, "content": [
            {"type": "text", "text": t}]}}) for i, t in enumerate(texts)]
        return tmpfile("\n".join(lines) + "\n", ".jsonl")

    def test_scores_the_last_report_in_a_transcript(self):
        p = self.transcript(["Panel dispatched.", REPORT])
        r = run(["--json", GOLDEN, p])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["recall"], 3)

    def test_plain_report_file_is_accepted(self):
        r = run(["--json", GOLDEN, tmpfile(REPORT, ".md")])
        self.assertEqual(json.loads(r.stdout)["recall"], 3)

    def test_transcript_without_a_report_is_an_error_not_a_zero(self):
        r = run([GOLDEN, self.transcript(["Verdict E arrived. Still waiting for F."])])
        self.assertEqual(r.returncode, 2)
        self.assertIn("no final report", r.stderr)

    def test_missing_golden_file_is_an_error(self):
        r = run(["/nonexistent/golden.json", tmpfile(REPORT, ".md")])
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")

    def test_golden_with_a_broken_regex_is_an_error(self):
        bad = tmpfile(json.dumps({"target": "x", "defects": [{"id": "B", "title": "t", "weight": "MINOR",
                                                              "all": ["("]}]}), ".json")
        r = run([bad, tmpfile(REPORT, ".md")])
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
