---
stage: ready-made-plan
date: 2026-09-17
origin: Cognition "Fusion" post (lead + sidekick exchange briefs, never conversations) → question "what does our fork route actually cost vs a fresh brief?"
---

# Dispatch cost measurement + token counting for the assembly line

## Problem
The fork route (`/compounder:work-fork`, `context: fork`, executor on sonnet) inherits the
orchestrator's whole conversation. The parent's prompt cache is per model, so a sonnet fork
cannot read a fable/opus cache: turn 1 re-tokenizes and re-writes the entire parent context at
1.25× sonnet input price, then every later turn re-reads it. A fresh agent with a brief pays
only system prompt + brief. Nobody has measured the gap; ROUTES.md has no cost column.

Two API features shipped that touch this: `count_tokens` (free, model-specific) and cache
diagnostics (beta, `diagnostics.previous_message_id` in the request body). The second cannot be
wired into Claude Code's own requests — the harness owns the body. What CAN be observed is the
per-turn `usage` block in every transcript (`~/.claude/projects/<proj>/<session>/subagents/*.jsonl`).

## Units

### U1 — `compounder/scripts/dispatch-cost.py` (transcript-level cache diagnostics)
Python 3.9 stdlib. Input: session id, transcript path(s), or nothing (newest session of the cwd
project). For each subagent transcript: agentType, model, turns, Σ input / cache_write /
cache_read / output, turn-1 shape, estimated USD at API list prices, and cache-miss flags
(cache_read drops >20% between consecutive turns of one agent — the transcript analog of the
API's `messages_changed`/expiry). Turn-1 classification:
- `fresh` — cache_creation ≲ 60k, cache_read ≈ 0 (system + brief)
- `fork:same-model` — cache_read ≫ cache_creation (parent cache re-used)
- `fork:cross-model` — cache_creation ≫ 60k and cache_read ≈ 0 (parent context rewritten)
Verification: run on session `ff1a490e` of site-axia → the two `fork` agents classify
`fork:same-model` with inherited ≈215k/137k; explorers classify `fresh`.

### U2 — `compounder/scripts/count-tokens.sh <file>... [--model M]`
curl `POST /v1/messages/count_tokens`, one call per file, model default `claude-sonnet-5`
(the executor's tokenizer). Key from `ANTHROPIC_API_KEY` or Keychain item of the same name.
Prints `tokens<TAB>file`. Verification: run on the toy plan and on `fork-executor.md`; a
non-existent file exits non-zero with a message.

### U3 — Experiment: fork vs fresh brief on one toy plan, same session
Toy plan `docs/plans/2026-09-17-toy-fork-cost-probe.md` (one unit writing a scratch file, one
WebFetch fence probe). Route A: `Agent` tool → `compounder:fork-executor` (sonnet) with the
work-fork body as brief (fresh context). Route B: user types `/compounder:work-fork <toy plan>`
(real fork). Then `dispatch-cost.py` on this session compares both. Result goes to the
ROUTES.md evolution record with numbers.

### U4 — ROUTES.md: optional cost fields in the dispatch log + pointer to the script
Add `tokens_in`, `tokens_cache_read`, `tokens_cache_write`, `tokens_out`, `usd_est` as optional
keys in the logging-duty schema; one line naming `dispatch-cost.py` as the source.

## Out of scope
- API cache diagnostics on Claude Code traffic (needs a local proxy that threads
  `previous_message_id`; decision pending — see plan notes).
- Changing the fork route itself. Measure first.

## Regression checklist
- `btw-hook.sh` untouched; `hooks.json` untouched.
- Skills list unchanged (no new skill; scripts only).
- `dispatch-cost.py` never writes; `count-tokens.sh` never prints the key.
- `/compounder:work-fork` still returns the envelope verbatim (U3 proves it).

## Discarded approaches
1. **Estimate with `count_tokens` on the parent transcript.** Can't see the harness's system
   prompt/tools, and the cache write/read split is what matters. Transcript `usage` is the bill.
2. **Local proxy injecting `diagnostics` into Claude Code's requests.** Only path to the real
   beta, but ~100 lines of SSE passthrough, OAuth+beta-header interaction unknown, and the
   question at hand (fork vs fresh) is answered by `usage` alone. Deferred, not rejected.
3. **Python `anthropic` SDK for count_tokens.** Not installed, Python 3.9, no `uv` — a new dep
   for one free HTTP call. curl + jq is the plugin's existing stack.
