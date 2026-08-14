---
name: lfg
description: Full autonomous pipeline — plan, execution, simplification, review, and local closure with adversarial gates.
disable-model-invocation: true
argument-hint: "[feature description | plan path] [send:pr]"
---

# /lfg — autopilot with truth gates

Input: `$ARGUMENTS`

Execute the phases IN ORDER. No gate is self-attested: gate = an executed command or a verifier
agent — never "I trust it's ok". Between phases, narrate in 1 line what closed and what opens.

**Closure rule (read before starting):** delivery is LOCAL. Local commit only if the user
authorized commits (AUTONOMY.md/CLAUDE.md or a request). Push/PR ONLY if `$ARGUMENTS` contains
`send:pr` or the user explicitly ordered it in this session. Without authorization: leave the
diff in the working tree and report. Never bypass this.

## Phase 0 — Contract (2 min, don't skip)
- Does `docs/goals/ACTIVE.md` exist? Use it as the contract.
- Otherwise: derive a mini-contract from the arguments (goal in 1 sentence + 2–5 CHECKABLE
  acceptance criteria + non-goals) and write it to `docs/goals/ACTIVE.md`. Ambiguity that changes
  the outcome in an autonomous pipeline → pick the reasonable option, DECLARE it in the contract
  under "Declared assumptions".
- Argument is a path to a ready plan? Validate Phase 1's gate and skip to Phase 2.

## Phase 1 — Plan
Invoke the `plan` skill with the contract/description (headless: no menus).
**GATE 1:** the plan file exists in `docs/plans/` AND every unit has its own verification AND the
cited paths exist (`ls` them). Failed → invoke `plan` again pointing at the exact gap.
Failed 2× → STOP and report what's missing; don't improvise an implementation without a plan.

## Phase 2 — Work
Invoke the `work` skill with the plan path (`mode:return` — no delivery tail).
**GATE 2 (adversarial):** dispatch the `adversarial-verifier` agent with the return envelope
("done" claims + cited evidence). It confirms by execution: does the suite run? do units
marked done have the behavior? Any REFUTED → go back to `work` with the list of
refutations (1 retry). If it persists → STOP, report the real state + handoff.

## Phase 3 — Simplification (mandatory on a code diff)
Skip ONLY if the diff is exclusively docs/config (no executable code). Any code touched →
invoke `simplify` ALWAYS (preserves behavior, suite green before/after), including on a small
diff. AI tends to leave scaffolding — a new helper with no caller, a speculative branch, an
orphan import: the planer exists exactly for that, and Phase 4's review should judge already-clean
code. Don't commit here.

## Phase 4 — Review
Invoke `review` in `apply` mode over the full diff. It applies only safe-class fixes
and reruns the suite; SEVERE non-applicable findings come back in the list.
**GATE 3:** a confirmed, unapplied SEVERE finding remains → do not proceed to closure: record the
findings in `docs/plans/<plan>-residuals.md`, report, and STOP (the decision is the user's).

## Phase 5 — Closure
1. Check the contract: each acceptance criterion verified NOW (command/observation), not from memory.
2. Apply the Closure rule (top). With `send:pr` authorized: named branch, commit(s)
   with a clear message, push, PR citing contract + evidence; then `gh pr checks --watch`,
   up to 3 CI fix cycles (fix the cause, never weaken a test); CI red after
   3 → record it in the PR and stop.
3. Archive the contract (`docs/goals/archive/`), with a `## Result` section holding the evidence.

## Phase 6 — Compound-lite
Don't run the full capture on your own (expensive). List 1–3 learning candidates in 1 line each
("X cost time because Y — worth documenting?") in the final report, suggesting `/compound`.

## Final report (format)
```
RESULT: <delivered locally | PR open | stopped at phase N>
Contract: <criterion → ✅/❌ + evidence (command → summarized output)>
Diff: <N files, ~N lines> | Suite: <before → after> | Not tested: <or "nothing">
Residuals: <pending findings/risks or "none">
Learning candidates: <1–3 lines>
```

## Failure protocol (applies in every phase)
Same failure 2× → new hypothesis, never an identical 3rd attempt. 3 dead hypotheses or an external
blocker → STOP: real state + what each failure proved + recommended next step. A pipeline that
stalls and reports well is a partial success; a pipeline that pretends to finish is a total failure.
