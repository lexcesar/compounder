---
name: slfg
description: Let the swarms fucking go — the /lfg pipeline with research, review, and verification in a parallel SWARM.
disable-model-invocation: true
argument-hint: "[feature description] [send:pr] [budget:released]"
---

# /slfg — the swarm

Input: `$ARGUMENTS`

Same contracts, gates, and closure rule as `/lfg` (read the `lfg` skill first — it is the
constitution; this skill only swaps the execution ENGINE for parallelism). Differences below.

## Cost and consent
The swarm costs 3–10× `/lfg`. If `$ARGUMENTS` does not contain `budget:released`, announce the
estimate ("~N agents: research 3, review 4–6, verification 1 per finding") and ask for an ok
BEFORE firing.

## Capabilities: detect and degrade gracefully
1. **Best case** — `Workflow` tool available (deterministic orchestration): use it for the
   fan-outs below (pipeline per item, no unnecessary barriers).
2. **Normal case (Opus/Sonnet/Haiku)** — subagent tool (`Task`/`Agent`): fire each wave's agents
   in ONE SINGLE message (multiple calls together = true parallelism). Never in series.
3. **No subagents** — become sequential `/lfg` and say so.

## Phase 1' — Swarm research (before the plan)
3 `researcher` agents in parallel, distinct and independent lenses:
- A: codebase patterns in the area (files, conventions, existing utilities).
- B: institutional memory — `docs/solutions/`, `CONCEPTS.md`, previous `docs/plans/`, memories.
- C: contracts and consumers — who calls what will change, existing tests, API surfaces.
Each returns a dossier ≤40 lines with `file:line`. The Phase 1 plan is written from the
3 dossiers (cite them). Sample 2 citations from each before trusting (one false → redo that lens).

## Phase 2' — Work
Plan units are executed IN SEQUENCE by default (parallel edits collide). Parallelize only if the
plan declares units with no file intersection AND there is real isolation (worktrees); when in
doubt, sequential — the swarm is for READING and JUDGING in parallel, not for writing.

## Phase 4' — Swarm review
Wave 1 (parallel): 4 reviewers (`correctness-reviewer`, `security-reviewer`,
`simplicity-reviewer`, `tests-reviewer`) over the same diff.
Dedup (you, no agent): merge findings at the same `file:line`; corroboration between reviewers
raises the severity by 1 level.
Wave 2 (parallel): every SEVERE/MEDIUM finding goes to an `adversarial-verifier` instructed to
REFUTE it. Survives = confirmed; refuted = dies. (This filters the plausible-but-false — the
specific poison of agent-based review.)
Application: as in `/lfg` Phase 4 (safe class + suite).

## Phases 5'/6' — identical to /lfg
Local closure by default; compound-lite in the report.

## Report: add the swarm line
```
Swarm: <N agents: research X, review Y, verification Z> | refuted in Wave 2: <N>
```
A refuted finding does NOT appear as a problem in the report — at most as "discarded in
verification".

## Golden rules of the swarm
1. Full briefing in every agent (it is born without your conversation): goal, context, negative
   scope, return format. Agent came back with garbage once → fix the briefing, not the agent.
2. Parallel waves only for INDEPENDENT work; results that feed each other = separate phases.
3. No secrets in briefings.
4. You are the synthesis bottleneck: agents collect and judge; the one who integrates, decides,
   and SIGNS is you. "The agent said so" does not exist in the final report.
