#!/usr/bin/env python3
"""Transcript-level cache diagnostics for Claude Code sessions and their subagents.

Reads the per-turn `usage` block that Claude Code writes to every transcript and answers:
what did each dispatch cost, was it a fresh brief or an inherited fork, and did the cache
miss between turns. Never writes anything. Python 3.9 stdlib only.

Usage:
  dispatch-cost.py                      newest session of the current project
  dispatch-cost.py <session-id-prefix>  that session (searched in every project dir)
  dispatch-cost.py <transcript.jsonl>...  explicit transcripts
  dispatch-cost.py --json ...           machine-readable output (one object per agent)
"""
import glob
import json
import os
import sys

# USD per million tokens: input, cache write (1.25x), cache read, output. API list prices.
PRICES = {
    "claude-fable-5-1": (10.0, 12.5, 0.25, 50.0),
    "claude-fable-5": (10.0, 12.5, 0.25, 50.0),
    "claude-opus-5": (5.0, 6.25, 0.5, 25.0),
    "claude-opus-4-8": (5.0, 6.25, 0.5, 25.0),
    "claude-opus-4-7": (5.0, 6.25, 0.5, 25.0),
    "claude-sonnet-5": (2.0, 2.5, 0.2, 10.0),
    "claude-sonnet-4-6": (3.0, 3.75, 0.3, 15.0),
    "claude-haiku-4-5": (1.0, 1.25, 0.1, 5.0),
}
FRESH_CEILING = 60_000      # tokens: a system prompt + brief rarely exceeds this
MISS_DROP = 0.20            # cache_read falling by more than this between turns = miss


def price_for(model):
    for key, p in PRICES.items():
        if model.startswith(key):
            return p
    return None


def turns_of(path):
    """One entry per API response. Claude Code writes one record per content block
    (thinking / text / tool_use) with the same `usage`; dedupe on message id, keep the
    last record (its output_tokens is the final count)."""
    by_id = {}
    order = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message") or {}
            u = msg.get("usage") or {}
            mid = msg.get("id") or rec.get("uuid")
            if mid not in by_id:
                order.append(mid)
            by_id[mid] = {
                "model": msg.get("model", "?"),
                "input": u.get("input_tokens", 0) or 0,
                "write": u.get("cache_creation_input_tokens", 0) or 0,
                "read": u.get("cache_read_input_tokens", 0) or 0,
                "output": u.get("output_tokens", 0) or 0,
                "ts": rec.get("timestamp", ""),
            }
    return [by_id[m] for m in order]


def classify_turn1(t):
    if t["read"] > FRESH_CEILING and t["read"] > t["write"]:
        return "fork:same-model", t["read"]
    if t["write"] > FRESH_CEILING and t["read"] < FRESH_CEILING:
        return "fork:cross-model", t["write"]
    return "fresh", t["write"] + t["read"] + t["input"]


def misses(turns):
    flagged = []
    for i in range(1, len(turns)):
        prev, cur = turns[i - 1]["read"], turns[i]["read"]
        if prev > 0 and cur < prev * (1 - MISS_DROP):
            flagged.append((i + 1, prev, cur))
    return flagged


def analyze(path, meta):
    turns = turns_of(path)
    if not turns:
        return None
    models = [t["model"] for t in turns]
    model = max(set(models), key=models.count)
    kind, base = classify_turn1(turns[0])
    tot = {k: sum(t[k] for t in turns) for k in ("input", "write", "read", "output")}
    p = price_for(model)
    usd = None
    if p:
        usd = (tot["input"] * p[0] + tot["write"] * p[1] + tot["read"] * p[2] + tot["output"] * p[3]) / 1e6
    return {
        "file": path,
        "agent": meta.get("agentType", "session"),
        "description": meta.get("description", ""),
        "model": model,
        "turns": len(turns),
        "turn1": kind,
        "turn1_base": base,
        "tokens": tot,
        "usd_est": usd,
        "misses": misses(turns),
    }


def meta_of(path):
    m = path[:-len(".jsonl")] + ".meta.json"
    if os.path.exists(m):
        with open(m, encoding="utf-8") as fh:
            try:
                return json.load(fh)
            except ValueError:
                return {}
    return {}


def project_dir_for_cwd():
    return os.path.join(os.path.expanduser("~/.claude/projects"), os.getcwd().replace("/", "-"))


def resolve(args):
    paths = []
    if not args:
        proj = project_dir_for_cwd()
        sessions = sorted(glob.glob(os.path.join(proj, "*.jsonl")), key=os.path.getmtime)
        if not sessions:
            sys.exit("no session transcript under " + proj)
        args = [sessions[-1]]
    for a in args:
        if a.endswith(".jsonl") and os.path.exists(a):
            paths.append(a)
            continue
        hits = glob.glob(os.path.expanduser("~/.claude/projects/*/%s*.jsonl" % a))
        if not hits:
            sys.exit("no transcript matches %r" % a)
        paths.extend(hits)
    expanded = []
    for p in paths:
        expanded.append(p)
        sub = os.path.join(p[:-len(".jsonl")], "subagents", "agent-*.jsonl")
        expanded.extend(sorted(glob.glob(sub), key=os.path.getmtime))
    return expanded


def fmt_k(n):
    return "%dk" % round(n / 1000) if n >= 1000 else str(n)


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    rows = [r for r in (analyze(p, meta_of(p)) for p in resolve(argv)) if r]
    if as_json:
        for r in rows:
            print(json.dumps(r))
        return
    hdr = "%-28s %-22s %5s  %-16s %9s %9s %9s %9s %8s  %s" % (
        "agent", "model", "turns", "turn1", "input", "write", "read", "output", "usd", "misses")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        t = r["tokens"]
        usd = "%.3f" % r["usd_est"] if r["usd_est"] is not None else "?"
        miss = ", ".join("t%d %s->%s" % (i, fmt_k(a), fmt_k(b)) for i, a, b in r["misses"]) or "-"
        print("%-28s %-22s %5d  %-16s %9s %9s %9s %9s %8s  %s" % (
            r["agent"][:28], r["model"][:22], r["turns"],
            "%s %s" % (r["turn1"], fmt_k(r["turn1_base"])),
            fmt_k(t["input"]), fmt_k(t["write"]), fmt_k(t["read"]), fmt_k(t["output"]), usd, miss))
        if r["description"]:
            print("    " + r["description"][:100])


if __name__ == "__main__":
    main()
