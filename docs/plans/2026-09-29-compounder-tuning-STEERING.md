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
- 2026-09-29 · No AI attribution in commits or PR text.

## Questions for supervisor    <!-- executor appends the blocker, takes the next independent unit — never waits -->

## Execution log    <!-- executor appends, in the same commit as the unit; a unit without its line counts as not done -->
Line: `YYYY-MM-DD HH:MM · U<N> · done|partial|dropped · <SHA> — <note>`

## Start prompt for the fresh session    <!-- supervisor maintains -->
Read `docs/plans/2026-09-29-compounder-tuning-plan.md` and this file. Work in the worktree for branch `feat/compounder-tuning`; never in the primary checkout.
Units U1, U2, U4 and U5 have no dependency and can start in any order; U1 first by risk.
Standing rules: the Active directives above; failing test before every code change; evidence
from a command you ran, never from reading code alone.
