---
name: work
description: Execute a plan with a baseline, per-unit tracking, and real evidence. Use to implement plans from docs/plans/ or clear build requests.
argument-hint: "[plan path | description] [mode:return]"
---

# /work — execution with evidence

Input: `$ARGUMENTS` (token `mode:return` = called by a pipeline: no menus, no delivery tail,
ends at the structured envelope).

## Step 0 — Triage
- Plan path → read the frontmatter: `stage: ready-made-plan` → proceed. `stage: requirements` →
  stop: "this needs `/plan` first" (in a pipeline, return that error).
- Empty → take the most recent ready-made plan from `docs/plans/` and CONFIRM with the user.
- Loose description → small, clear scope: 5-line plan in the chat and execute; large/nebulous:
  recommend `/brainstorm` or `/plan` (the user decides).

## Step 1 — Preparation (never skip)
1. **Baseline:** discover the project's commands (CLAUDE.md → package.json/Makefile; never
   guess) and RUN the area's suite + typecheck. Record: "baseline: X/Y, pre-existing failures: ...".
2. **Branch:** on the default branch and commits authorized → create a branch with a meaningful
   name. Commits not authorized → work in the working tree and say so.
3. **Tracking:** create one task (TaskCreate; without the tool, a checklist in the chat) per unit
   U1..Un.
4. Read from the plan: "Deferred to execution" (your questions to resolve) and "Out of scope"
   (your fence).
5. **Research brief** cited by the plan (`docs/plans/research/`) → read it BEFORE opening code;
   no independent broad exploration — the brief is the map. A cited fact looks stale → verify
   that specific fact and record the deviation.
6. **STEERING** cited by the plan (or `<plan-slug>-STEERING.md` beside it) → re-read before
   EVERY unit and EVERY commit; active directives override plan order. Blocked → write the
   question there and take the next independent unit, never wait. Each finished unit gets its
   log line (format in the file) in the same commit — without commits, at unit close. A unit
   without its line counts as not done.

## Step 2 — Per-unit loop (U1 → Un, plan order)
For each unit: mark in progress → reread section U<N> → implement the SMALLEST honest diff
following the local dialect → the unit's test scenarios become real tests (new behavior: watch
the test FAIL before the implementation when the cost allows) → run the unit's VERIFICATION (the
plan's) → passed: mark done with 1-line evidence; narrate in the chat
("U2 ✅ — 3 files, test X green").
- **The unit CREATES a check (test, gate, probe, verification script) → prove it can go RED
  before trusting its green:** mutate the reference or break the input, watch it fail with a
  meaningful diff, revert. A check that cannot fail is decoration — the most dangerous kind of
  green is one that measures nothing.
- **Plan doesn't match reality** (file changed, premise fell): small deviation → note it in your
  execution note and continue; STRUCTURAL deviation → stop the unit and report "the plan expected
  X, reality is Y, I propose Z" (in a pipeline: record it and choose the reasonable path if
  reversible; otherwise stop).
- **Failed 2× the same way → new hypothesis.** 3 dead hypotheses in the same unit → the unit
  becomes a BLOCKER in the envelope; move on to the next independent unit, if any.
- **NEVER:** edit the plan as if it were state; delete/skip a test to pass; "seize the moment"
  to refactor outside the scope (note it as a residual).

## Step 3 — Final verification
ENTIRE suite + typecheck/lint + build (if it exists). Compare with the baseline: a regression
that is YOURS → fix it before reporting. Clean the scene: debug prints, orphan imports, scratch
files.

## Step 4 — Return envelope (mandatory, both modes)
```
STATUS: complete | partial | blocked
Units: U1 ✅ <1-line evidence> | U2 ✅ ... | U3 ❌ <blocker: what each attempt proved>
Files: <list> (~N lines)
Suite: baseline X/Y → now X'/Y' | typecheck: <state>
Not tested: <what + why + risk> | Residuals/notes: <...>
Plan deviations: <or "none">
```
Normal mode: envelope + "next: `/simplify` and `/review`". `mode:return`: envelope and STOP
(no commit, no menu — the tail belongs to the caller).
Honesty rule above all: STATUS `complete` requires every unit with verification executed IN THIS
session. A well-reported partial > a false complete — no exception.
