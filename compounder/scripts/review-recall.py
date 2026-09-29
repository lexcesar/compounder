#!/usr/bin/env python3
"""Recall of one /compounder:review run against a golden list of known defects.

A review run is judged by what it found on a frozen target, not by impression: run-to-run
variance is larger than the effect of most changes, so a change to a skill or agent is accepted
on a measured number over several runs. Never writes anything. Python 3.9 stdlib only.

Usage:
  review-recall.py <golden.json> <session-id-prefix | transcript.jsonl | report.md>
  review-recall.py --json ...        machine-readable output
  review-recall.py --all-text ...    score every long assistant message of a transcript
                                     (for a run that stopped before its final report)
  review-recall.py --agreement <golden.json> <run> <run> [<run>...]
                                     severity agreement across runs

A finding matches a defect when ONE report item satisfies EVERY regex of the defect.
Exit 2: the transcript has no final report. Any missing or malformed input is an error,
never a score of zero.
"""
import glob
import json
import os
import re
import sys

REPORT_MARK = re.compile(r"\b(VERDICT|VEREDITO|VEREDICTO)\b")
SECTIONS = (   # first match wins; order matters
    ("refuted", re.compile(r"DISCARDED|DESCARTAD|REFUTED|REFUTAD", re.I)),
    ("suspicion", re.compile(r"SUSPICION|SUSPEIT|INCONCLUS", re.I)),
    ("minor", re.compile(r"^MINOR\b", re.I)),
    ("other", re.compile(r"COVERAGE|COBERTURA|VERDICT|VEREDI|REVIEW (READY|PRONT)|NEXT STEP|PR[OÓ]XIMO PASSO"
                         r"|ULTRA:|ESCOPO|SCOPE|CORRIGIDOS", re.I)),
    ("confirmed", re.compile(r"CONFIRM", re.I)),
)
LEVEL_NAMES = {"SEVERE": "SEVERE", "GRAVE": "SEVERE", "MEDIUM": "MEDIUM", "MEDIO": "MEDIUM",
               "MÉDIO": "MEDIUM", "MINOR": "MINOR"}
TAG = re.compile(r"\[?\b(SEVERE|GRAVE|MEDIUM|M[EÉ]DIO|MINOR)\b\]?", re.I)
TAG_START = re.compile(r"^\s*[*_`]*\[(SEVERE|GRAVE|MEDIUM|M[EÉ]DIO|MINOR)\]", re.I)
MARKER = re.compile(r"^(\s*)(\d+[.)]|[-*•]|\|)\s+")
# sub-bullets that detail the finding above them, whatever their indent
LABEL = re.compile(r"[*_`]*(cen[aá]rio|scenario|fix|corre[cç][aã]o|realismo|junto|agravante|nota|note"
                   r"|frequ[eê]ncia|a[cç][aã]o|escopo|ressalva|proof|prova|evid[eê]nc|evidence"
                   r"|o que acontece|alcance|suggested)\b", re.I)
EMPTY = re.compile(r"(none|nada|nenhum\w*|n/?a|0|[-–—])$", re.I)   # "MINOR: none" is not a finding
TAG_WINDOW = 40      # a level counts when it opens a line; deeper in the text it is commentary
DEFAULT_LEVEL = {"minor": "MINOR", "suspicion": "SUSPICION", "confirmed": "UNRATED", "refuted": "REFUTED"}


def load_golden(path):
    with open(path, encoding="utf-8") as fh:
        g = json.load(fh)
    for d in g["defects"]:
        d["_re"] = [re.compile(p, re.I) for p in d["all"]]
    return g


def heading_of(line):
    """Section a heading line opens, or None. A heading is a short line that is not a finding and
    is decorated, opens with an upper-case word, or ends in a colon or question mark."""
    if MARKER.match(line) or TAG_START.match(line) or len(line) > 160:
        return None
    text = re.sub(r"^[#*_`>\s]+", "", line)
    decorated = line.lstrip().startswith(("#", "*"))
    shouted = re.match(r"[A-ZÀ-Ú]{4,}\b", text)
    closes = text.rstrip(" *_`").endswith((":", "?"))
    if not text or not (decorated or shouted or closes):
        return None
    for name, rx in SECTIONS:
        if rx.search(text[:60]):
            return name
    return None


def items_of(report):
    """Report split into findings: (section, text). A finding owns its deeper-indented lines, its
    labelled sub-bullets, and, when it opens with a bold title, the bullets under that title.
    Prose between findings is not a finding."""
    items, section, cur, indent, blank = [], "other", None, 0, False

    def close():
        nonlocal cur
        if cur is not None and cur[1].strip():
            items.append((cur[0], cur[1].strip()))
        cur = None

    for line in report.splitlines():
        if not line.strip() or line.strip().startswith("```"):
            blank = True
            continue
        h = heading_of(line)
        if h:
            close()
            section, blank = h, False
            rest = line.split(":", 1)[1] if ":" in line else ""
            if rest.strip(" *_") and not EMPTY.match(rest.strip(" *_.`")):
                cur, indent = [section, rest], -1      # findings written on the heading line
            continue
        m = MARKER.match(line)
        label = m and LABEL.match(line[m.end():])
        if m and not label and (cur is None or len(m.group(1)) <= indent):
            close()
            cur, indent = [section, line], len(m.group(1))
        elif m and cur is not None:
            cur[1] += "\n" + line
        elif TAG_START.match(line):
            close()
            cur, indent = [section, line], 0
        elif line.lstrip().startswith(("**", "#")):
            close()
            cur, indent = [section, line], -1          # bold title: the bullets below belong to it
        elif cur is not None and (not blank or line[:1].isspace()):
            cur[1] += "\n" + line
        else:
            close()                                    # prose
        blank = False
    close()
    return items


def level_of(section, text):
    if section in ("refuted", "suspicion"):
        return DEFAULT_LEVEL[section]
    for line in text.splitlines():
        m = TAG.search(line[:TAG_WINDOW])
        if m:
            return LEVEL_NAMES[m.group(1).upper()]
    return DEFAULT_LEVEL[section]


def score(report, golden):
    matched, refuted, unmatched, seen = [], [], [], set()
    for section, text in items_of(report):
        if section == "other":
            continue
        ids = [d for d in golden["defects"] if all(rx.search(text) for rx in d["_re"])]
        snippet = re.sub(r"\s+", " ", text)[:140]
        level = level_of(section, text)
        if not ids:
            if section != "refuted":
                unmatched.append({"level": level, "text": snippet})
            continue
        for d in ids:
            row = {"id": d["id"], "title": d["title"], "weight": d["weight"], "level": level, "text": snippet}
            if section == "refuted":
                refuted.append(row)
            elif d["id"] not in seen:
                seen.add(d["id"])
                matched.append(row)
    matched.sort(key=lambda r: r["id"])
    refuted = [r for r in refuted if r["id"] not in seen]
    return {"target": golden.get("target"), "recall": len(matched), "total": len(golden["defects"]),
            "matched": matched, "refuted": refuted, "unmatched": unmatched,
            "missed": [d["id"] for d in golden["defects"] if d["id"] not in seen]}


def agreement(scores):
    """Severity agreement over several runs: of all placements of defects found in two or more
    runs, the share that carries that defect's most common level."""
    per = {}
    for s in scores:
        for m in s["matched"]:
            lv = m["level"] if m["level"] in ("SEVERE", "MEDIUM", "MINOR") else "OTHER"
            per.setdefault(m["id"], {"SEVERE": 0, "MEDIUM": 0, "MINOR": 0, "OTHER": 0})[lv] += 1
    per = {k: v for k, v in per.items() if sum(v.values()) >= 2}
    if not per:
        raise ValueError("no defect was found in two or more runs: agreement is undefined")
    agree = sum(max(v.values()) for v in per.values())
    placements = sum(sum(v.values()) for v in per.values())
    return {"agree": agree, "placements": placements, "share": agree / placements,
            "per_defect": dict(sorted(per.items()))}


def texts_of(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if not isinstance(rec, dict) or rec.get("type") != "assistant":
                continue
            for b in (rec.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "text":
                    out.append(b.get("text", ""))
    return out


def report_of(arg, all_text):
    if os.path.exists(arg) and not arg.endswith(".jsonl"):
        with open(arg, encoding="utf-8") as fh:
            return fh.read()
    if arg.endswith(".jsonl") and os.path.exists(arg):
        path = arg
    else:
        hits = glob.glob(os.path.expanduser("~/.claude/projects/*/%s*.jsonl" % arg))
        if len(hits) != 1:
            sys.exit("%d transcripts match %r, need exactly one" % (len(hits), arg))
        path = hits[0]
    texts = texts_of(path)
    if all_text:
        long_ones = [t for t in texts if len(t) > 250]
        if not long_ones:
            sys.exit("no assistant text in " + path)
        return "\n\n".join(long_ones)
    reports = [t for t in texts if REPORT_MARK.search(t)]
    if not reports:
        sys.stderr.write("no final report in %s (run stopped early? try --all-text)\n" % path)
        sys.exit(2)
    return reports[-1]


def main():
    argv = sys.argv[1:]
    as_json, all_text, agree = "--json" in argv, "--all-text" in argv, "--agreement" in argv
    argv = [a for a in argv if a not in ("--json", "--all-text", "--agreement")]
    if agree and len(argv) >= 3:
        golden = load_golden(argv[0])
        try:
            a = agreement([score(report_of(x, all_text), golden) for x in argv[1:]])
        except ValueError as e:
            sys.exit(str(e))
        if as_json:
            print(json.dumps(a))
            return
        print("severity agreement over %d runs: %d of %d placements (%.0f%%)" % (
            len(argv) - 1, a["agree"], a["placements"], 100 * a["share"]))
        for k, v in a["per_defect"].items():
            print("  %-4s SEVERE %d  MEDIUM %d  MINOR %d  other %d" % (k, v["SEVERE"], v["MEDIUM"], v["MINOR"], v["OTHER"]))
        return
    if len(argv) != 2:
        sys.exit(__doc__.split("Usage:")[1].split("\n\n")[0])
    golden = load_golden(argv[0])
    s = score(report_of(argv[1], all_text), golden)
    if as_json:
        print(json.dumps(s))
        return
    print("target %s — recall %d of %d" % (s["target"], s["recall"], s["total"]))
    for r in s["matched"]:
        print("  %-4s %-9s (weight %-6s) %s" % (r["id"], r["level"], r["weight"], r["title"]))
    print("missed: " + (" ".join(s["missed"]) or "-"))
    for r in s["refuted"]:
        print("  refuted by the run: %s %s" % (r["id"], r["title"]))
    if s["unmatched"]:
        print("unmatched findings (adjudicate by hand; a real one enters the golden list):")
        for u in s["unmatched"]:
            print("  [%s] %s" % (u["level"], u["text"]))


if __name__ == "__main__":
    main()
