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
import re
import sys

# USD per million tokens: input, cache read, output. API list prices. Cache writes are a
# multiple of input on every model: 5m TTL = 1.25x, 1h TTL = 2x (Claude Code writes 1h).
PRICES = {
    "claude-fable-5": (10.0, 0.25, 50.0),
    "claude-opus-5-5": (4.0, 0.2, 20.0),
    "claude-opus-5": (5.0, 0.5, 25.0),
    "claude-opus-4-8": (5.0, 0.5, 25.0),
    "claude-opus-4-7": (5.0, 0.5, 25.0),
    "claude-sonnet-5": (2.0, 0.2, 10.0),
    "claude-sonnet-4-6": (3.0, 0.3, 15.0),
    "claude-haiku-4-5": (1.0, 0.1, 5.0),
}
WRITE_5M, WRITE_1H = 1.25, 2.0
FRESH_CEILING = 60_000      # tokens: a subagent's system prompt + brief rarely exceeds this
MISS_DROP = 0.20            # cache_read falling by more than this between turns = miss


def price_for(model):
    for key in sorted(PRICES, key=len, reverse=True):   # longest prefix wins: opus-5-5 before opus-5
        if model.startswith(key):
            return PRICES[key]
    return None


def usd_of(t):
    """Price one turn at its own model, or None when the model is unknown and had tokens."""
    p = price_for(t["model"])
    if p is None:
        return None if any(t[k] for k in ("input", "write", "read", "output")) else 0.0
    inp, read, out = p
    return (t["input"] * inp + t["write_5m"] * inp * WRITE_5M + t["write_1h"] * inp * WRITE_1H
            + t["read"] * read + t["output"] * out) / 1e6


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
            if not isinstance(rec, dict) or rec.get("type") != "assistant":
                continue
            msg = rec.get("message") or {}
            u = msg.get("usage") or {}
            mid = msg.get("id") or rec.get("uuid")
            if mid not in by_id:
                order.append(mid)
            write = u.get("cache_creation_input_tokens", 0) or 0
            split = u.get("cache_creation") or {}
            write_5m = split.get("ephemeral_5m_input_tokens", 0) or 0
            # no TTL split in the record → Claude Code's default, 1h
            write_1h = split.get("ephemeral_1h_input_tokens", write - write_5m) or 0
            by_id[mid] = {
                "model": msg.get("model", "?"),
                "input": u.get("input_tokens", 0) or 0,
                "write": write,
                "write_5m": write_5m,
                "write_1h": write_1h,
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
    model = max(sorted(set(models)), key=models.count)   # ties break alphabetically, not by hash seed
    agent = meta.get("agentType", "session")
    if agent == "session":
        kind, base = "root", turns[0]["write"] + turns[0]["read"] + turns[0]["input"]
    else:
        kind, base = classify_turn1(turns[0])
    tot = {k: sum(t[k] for t in turns) for k in ("input", "write", "read", "output")}
    per_turn = [usd_of(t) for t in turns]
    usd = None if None in per_turn else sum(per_turn)
    return {
        "file": path,
        "agent": agent,
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


def project_dir_for(cwd):
    # Claude Code names the project dir by replacing every non-alphanumeric byte of the cwd with "-"
    return os.path.join(os.path.expanduser("~/.claude/projects"), re.sub(r"[^A-Za-z0-9-]", "-", cwd))


def resolve(args):
    paths = []
    if not args:
        proj = project_dir_for(os.getcwd())
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
