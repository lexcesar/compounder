---
name: debug
description: Root-cause investigation for bugs — reproduce, competing hypotheses, bisection, fix with a red-green test. Use when the input is broken behavior, not a feature.
argument-hint: "[bug description | error message | 'tests X are failing']"
---

# /debug — from symptom to cause, with proof

Input: `$ARGUMENTS`

**If the project has the `deep-analysis` skill (starter kit), invoke it — it is the full
doctrine behind this one.** The method below is the embedded version for projects without the kit.

## Phase 1 — Investigation
1. **Reproduce** before theorizing. Couldn't reproduce → record what you tried; "doesn't
   reproduce" is central data, not a license to guess.
2. **Read the ENTIRE error** — message, stack, and the FIRST failure in the log (the rest are cascade).
3. **What changed?** `git log` of the area, dependencies, config, data. A new bug in old code has
   a recent trigger.
4. **≥2 hypotheses BEFORE investigating the first**, each with a discriminating test defined
   BEFORE running ("if H1, I'll see X; if H2, I'll see Y"). A single hypothesis = anchoring.
5. **Bisect:** by layer (is the data right at boundary N?), by time (the commit that
   introduced it), by data (smallest input that still fails). Each check cuts ~half.
6. **One change at a time** — and NO "drive-by" fixes during the investigation (they contaminate
   the evidence).
7. Keep 3 separate lists: FACTS (with source), INFERENCES, ASSUMPTIONS. Stuck? The cause is
   almost always in an untested assumption — promote it to a hypothesis.
8. **Cause ≠ symptom:** ask "why" until you hit a decision/config/premise. Patching where it
   blew up (`if null` at the crash site) hides the defect and spreads it.

## Phase 2 — Fix (only after the cause is demonstrated)
1. **Test that reproduces the bug** — see it RED (the bisection's minimal case = the ideal test).
2. **Minimal fix, at the cause.**
3. **Green** — the new test + the whole suite (compare against baseline if known).

## Phase 3 — Delivery
```
ROOT CAUSE: <decision/config/premise> — decisive evidence: <command→output | file:line>
Chain: <symptom ← link ← link ← cause>
Fix: <what changed, N lines> | Regression: <new test> | Suite: <X/Y>
Prevention: <what would block recurrence: test, guardrail, invariant — proposed or applied>
Confidence: high|medium|low — <what would overturn it>
```
If the request was DIAGNOSIS only: deliver Phase 1 + the PROPOSED fix (diff in a block, not
applied) and stop.

## Stop conditions
3 dead hypotheses or budget blown → STOP and deliver the 3 lists + hypotheses tested +
best suspect ranked + the next test you would run. That is a valuable deliverable; flailing is not.
Root bug belongs to a third party (lib, service) → evidence + minimal workaround + where to report.

## Afterwards
Bug cost > 30 min or will recur → suggest `/compound` (the investigation is fresh — now is when
it becomes an asset). Non-trivial fix → suggest `/review` before committing.
