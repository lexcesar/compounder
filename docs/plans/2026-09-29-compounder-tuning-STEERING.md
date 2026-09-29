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
- 2026-09-29 · U3 scope: ship only the script guard, or also a plugin-level PreToolUse hook that fences every Bash call in sessions where the plugin is installed?
- 2026-09-29 · Headless runs are billed to the `ANTHROPIC_API_KEY` in the environment, not to the subscription. Keep using headless for measurement batches, or run them interactively?
- 2026-09-29 · Commit trailer: the directive "No AI attribution" above was written by the executor on inference, not ordered by Alexander. Confirm or drop.

## Execution log    <!-- executor appends, in the same commit as the unit; a unit without its line counts as not done -->
Line: `YYYY-MM-DD HH:MM · U<N> · done|partial|dropped · <SHA> — <note>`
- 2026-09-29 03:10 · U1 · partial · (this commit) — 12 cells measured against a local listener; per-agent frontmatter hook does not fire, plugin hooks.json hook fires but is session-wide, wrapper script passes every text-matching barrier. Not determined: whether hook input names the agent (inspection interrupted, not repeated). Probe plugin lived in the session scratchpad, nothing added to `compounder/agents/`. Next: decide U3 scope with Alexander.

## Start prompt for the fresh session    <!-- supervisor maintains -->
Read `docs/plans/2026-09-29-compounder-tuning-plan.md` and this file. Work in the worktree for branch `feat/compounder-tuning`; never in the primary checkout.
Units U1, U2, U4 and U5 have no dependency and can start in any order; U1 first by risk.
Standing rules: the Active directives above; failing test before every code change; evidence
from a command you ran, never from reading code alone.
