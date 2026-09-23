---
stage: residuals
date: 2026-09-22
origin: union of three `/compounder:review commit c8432b8` runs (orchestrator Fable 5.1 / Opus 5.5 / Sonnet 5; lenses + tribunal on Sonnet 5)
---

# dispatch-cost.py + count-tokens.sh — review residuals (union of 3 orchestrators)

Every item below was reproduced against real transcripts or a fixture in the Fable session
before being listed. "Found by" records which orchestrator's review surfaced it.

## Confirmed defects

| # | Sev | Where | Defect | Found by |
|---|---|---|---|---|
| 1 | SEVERE | `dispatch-cost.py` PRICES / `analyze` | Every cache write priced at 1.25× input. Claude Code writes with 1h TTL (2×). Session 4157e1c2: 131,578 write tokens, 100% `ephemeral_1h`, 0 in 5m → USD ~24% under. | Opus 5.5 |
| 2 | SEVERE | `classify_turn1` + `resolve` | Top-level session row (no `.meta.json`) is classified like a dispatch: write 60,201 / read 0 → `fork:cross-model`. 12/13 real sessions sit at 43k–63k, on the 60k edge. | Fable 5.1 |
| 3 | SEVERE | `analyze` :93-100 | All tokens priced at the majority model. ad89ccfa (197 fable-5 + 13 opus-4-8): 45.92 vs per-turn 41.69 (+10%). | Fable 5.1, Sonnet 5 |
| 4 | SEVERE | `analyze` :94 | `max(set(models), key=models.count)` — tie resolved by hash seed; same file gives different `model`/`usd_est` across runs. | Fable 5.1, Sonnet 5 (MEDIUM), Opus 5.5 (MINOR) |
| 5 | MEDIUM | `project_dir_for_cwd` | `replace("/", "-")` only; Claude Code also maps `.` → `-`. cwd `alexcesar.com/portfolio` → wrong dir, exit 1. | Opus 5.5 |
| 6 | MEDIUM | `count-tokens.sh` :31-35 | API key AND full body in curl argv: `ps` shows both cross-UID on this macOS; body also hits ARG_MAX (1 MiB) with a misleading "request failed". | all three (key); Opus 5.5 (body/ARG_MAX) |
| 7 | MEDIUM | `turns_of` :51-54 | Valid non-dict JSON line (`null`) → `AttributeError`, whole batch dies. Latent: never seen in real transcripts. | Sonnet 5 |
| 8 | SEVERE | (repo) | Zero tests for 5 pure stdlib functions; project rule mandates TDD for tools. | all three (severity disputed: Opus MINOR) |

## Suspicions (no real data)
- `classify_turn1`: read > 60k AND write > 60k with read < write → `fresh`. Mechanism exists, 0 hits in 121 transcripts. Not built for; pinned by a test only if the case shows up.
- `turns_of` :57 fallback `rec.get("uuid")` when `message.id` is missing would defeat dedup. 2372 assistant lines checked, 100% have `message.id`.

## Minor
- PRICES row `claude-fable-5-1` redundant with `claude-fable-5` (same tuple, prefix match). Prefix lookup depends on insertion order (`opus-5-5` before `opus-5`).
- `bash -x count-tokens.sh` echoes the key (same root as #6).
- `--json` has no in-repo consumer; ROUTES.md documents the keys manually.
- `<synthetic>` records count as turns (0 tokens).
- `--help` depends on header lines 2-4; `.meta.json` description printed with ANSI intact; `--model` without value trips `set -u`.

## Refuted by the tribunal (not defects)
- Session-prefix `../` traversal in `resolve()`: explicit-path mode already accepts any `.jsonl` by design; no automated caller (only ROUTES.md:47, manual). Hygiene at most.
- count-tokens.sh sends file content to the API: that is the documented function, operator-invoked on an operator-named file, no hook. Docs note at most.
- "claude-opus-5-5 cache read $0.20 is a typo": official docs confirm $0.20 (0.05× of $4).

## Fixed on branch `fix/dispatch-cost-review` (2026-09-22, red → green per item)
- #1 TTL split: PRICES is now (input, read, output); writes priced 5m = 1.25×, 1h = 2× from `usage.cache_creation`; a record without the split counts as 1h (Claude Code default — decision, not measured on old transcripts).
- #2 session row → `turn1: root`, never classified as a dispatch.
- #3 + #4 per-turn pricing summed; majority model chosen with alphabetical tie-break; a zero-token `<synthetic>` turn no longer voids the estimate.
- #5 `project_dir_for(cwd)` maps every non-alphanumeric byte to `-`.
- #6 key via `-H @<(printf …)`, body via stdin `--data-binary @-`. Stub-curl test proves neither is in argv. `bash -x` still shows the printf — accepted, operator-only.
- #7 non-dict JSON line skipped.
- #8 `compounder/scripts/test_dispatch_cost.py` (19 unittest) + `test_count_tokens.sh` (stub curl). No runner config: `python3 compounder/scripts/test_dispatch_cost.py && bash compounder/scripts/test_count_tokens.sh`.
- PRICES: redundant `claude-fable-5-1` row dropped; lookup takes the longest matching prefix.
Effect on real transcripts: tests-reviewer 0.152 → 0.217 USD (+43%, 1h writes); mixed session ad89ccfa 45.92 → 51.96; session 770f4a50 `fork:cross-model` → `root`.

## Still open
- Suspicions above (both-high `classify_turn1` branch, `uuid` fallback) — no data, no code.
- Minors: `--json` consumer, `<synthetic>` turn count, `--help`/ANSI/`--model` edge cases.
