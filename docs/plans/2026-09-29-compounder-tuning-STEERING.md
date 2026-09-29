# STEERING — compounder tuning
Async supervisor↔executor channel. Executor: re-read before EVERY unit, EVERY commit, and before
starting ANY fix that is not in the plan.
Concurrency: `git pull --rebase` before editing this file; each side touches only its own
sections — a stale-copy commit deletes the other side's newest lines.

Plan: `docs/plans/2026-09-29-compounder-tuning-plan.md`

## Active directives    <!-- supervisor writes, newest on top, binding -->
- 2026-09-29 · All plan work happens in the worktree `../fable-5-start-project.feat-compounder-tuning` (branch `feat/compounder-tuning`). The primary checkout stays on `main`, untouched. Decided by Alexander.
- 2026-09-29 · Execution mode is walkthrough: each unit is presented, decided and approved with Alexander before it starts.
- 2026-09-29 · No merge and no push on any branch without an explicit order from Alexander in the session. `fix/dispatch-cost-review` merge decision is suspended.
- 2026-09-29 · Measurement runs happen in the clean-room clone only, one fresh session per run. Never accept "apply fixes" or "record to file" inside the clone: either one becomes a spoiler for the next run.
- 2026-09-29 · State the estimated cost in USD before each batch of runs and wait for approval.
- 2026-09-29 · Network probes in U1 target `127.0.0.1` only.
- 2026-09-29 · Commits end with the `Claude-Session` line, as the repo history already does (19 of 31 commits). Decided by Alexander after checking the history.
- 2026-09-29 · Measurement runs are interactive, on the subscription. No headless `claude -p` batches: they bill the `ANTHROPIC_API_KEY` in the environment.

## Questions for supervisor    <!-- executor appends the blocker, takes the next independent unit — never waits -->
- 2026-09-29 · U3 scope: script guard shipped. Alexander answered "cerca no plugin"; the executor could not tell whether that means the guard that ships inside the plugin (done) or the session-wide PreToolUse hook. Hook NOT built until confirmed.

## Execution log    <!-- executor appends, in the same commit as the unit; a unit without its line counts as not done -->
Line: `YYYY-MM-DD HH:MM · U<N> · done|partial|dropped · <SHA> — <note>`
- 2026-09-29 03:10 · U1 · partial · (this commit) — 12 cells measured against a local listener; per-agent frontmatter hook does not fire, plugin hooks.json hook fires but is session-wide, wrapper script passes every text-matching barrier. Not determined: whether hook input names the agent (inspection interrupted, not repeated). Probe plugin lived in the session scratchpad, nothing added to `compounder/agents/`. Next: decide U3 scope with Alexander.

- 2026-09-29 04:05 · U3 · partial · (this commit) — script guard done: `count-tokens.sh` exits 4 without `COMPOUNDER_SEND=1`, red-proof by removing the guard. Hook fence not built: scope awaits confirmation (see Questions).

- 2026-09-29 04:10 · U4 · done · (this commit) — `dispatch-cost.py --log-line`, contract test reads the key list out of ROUTES.md; log lines 3–4 corrected to exact values and re-priced (0.138 → 0.177, 0.087 → 0.113). Lines 1–2 keep the alias `sonnet`: July transcripts not looked for.
- 2026-09-29 04:10 · U5 · done · (this commit) — four code defects closed with a failing test first (synthetic records, Fable 5 cache read, tie test across hash seeds, miss vs compaction). The fifth, key names, is U4. Deviation: U4 and U5 share one commit because both edit `dispatch-cost.py` and hunks were not split.

- 2026-09-29 05:20 · U2 · done · (this commit) — `review-recall.py` (recall, unmatched list, `--agreement`), golden list of 17, `clean-room.sh`. Calibration on five real runs: 8, 6, 12, 5, 11 of 17; severity agreement baseline 62%. Five scorer defects found by the calibration, each fixed test-first. Limit: anchors were written against these same runs; the next batch is the real test. Next: U6 needs three interactive clean-room runs, launched by Alexander.

## Start prompt for the fresh session    <!-- supervisor maintains -->
Read `docs/plans/2026-09-29-compounder-tuning-plan.md` and this file. Work in the worktree for branch `feat/compounder-tuning`; never in the primary checkout.
U1–U5 are done (U1 and U3 partial, see the log). Next is U6, which needs a batch of three interactive clean-room runs before and after the rubric.
Standing rules: the Active directives above; failing test before every code change; evidence
from a command you ran, never from reading code alone.
