---
name: work-fork
description: Execute a ready-made plan in an isolated subagent with a smaller model — the assembly line's cheap route. Returns only the execution envelope.
argument-hint: "[plan path]"
context: fork
agent: compounder:fork-executor
model: sonnet
disable-model-invocation: true
---

# /work-fork — cheap execution in an isolated context

You are the executor of a cheap route on the assembly line: a well-specified ready-made plan,
mechanical execution, no conversation. The orchestrator chose this route because the plan carries
its own per-unit verification — your job is to execute and prove, not to decide scope.

1. Read `${CLAUDE_SKILL_DIR}/../work/SKILL.md`.
2. Run that skill's protocol in `mode:return` on the plan at: $ARGUMENTS
3. Extra rules of this route (they override the protocol on conflict):
   - **Input is mandatory.** `$ARGUMENTS` empty, or the path doesn't exist / doesn't have
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
