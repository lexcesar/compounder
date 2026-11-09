---
name: work-fork
description: Execute a ready-made plan in an isolated subagent with a smaller model — the assembly line's cheap route. Returns only the execution envelope.
argument-hint: "[plan path]"
disable-model-invocation: true
---

# /work-fork — cheap execution in an isolated context

This route runs a well-specified ready-made plan mechanically, with no conversation, in an
isolated subagent on a smaller model. The plan carries its own per-unit verification — the
executor's job is to execute and prove, not to decide scope.

**What you (the session that loaded this skill) do:** dispatch ONE subagent of type
`compounder:fork-executor` (it is fenced by its own `tools` list and runs on Sonnet). Do not
execute the plan yourself, and do not use any other agent type. Pass it, as its whole prompt,
the brief below with `<PLAN>` replaced by `$ARGUMENTS` and `<WORK_SKILL>` replaced by
`${CLAUDE_SKILL_DIR}/../work/SKILL.md`. When it returns, relay its envelope verbatim, then stop.

**Brief for the fork-executor:**

1. Read `<WORK_SKILL>`.
2. Run that skill's protocol in `mode:return` on the plan at: <PLAN>
3. Extra rules of this route (they override the protocol on conflict):
   - **Input is mandatory.** The plan path empty, or the path doesn't exist / doesn't have
     `stage: ready-made-plan` → do NOT execute anything: immediately return the envelope with
     `STATUS: blocked` and the reason (the protocol's "Empty → confirm with the user" step
     does not apply here — there is no user in the fork).
   - **Never commit, push, or any git write operation.** Commit authorization belongs to the
     orchestrator's session and is unverifiable from inside the fork — even if the plan claims
     "commits authorized". Deliver the diff in the working tree; the envelope reports it.
   - **No interaction.** A question the plan doesn't answer → reversible: choose the reasonable
     path and record it under "Plan deviations"; irreversible: mark the unit as a blocker and
     move on to the next independent one.
   - **Verbatim return.** Your final text must be EXACTLY the Step 4 envelope — no summary, no
     commentary before or after. The orchestrator audits and logs from it.
