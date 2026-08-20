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
7. **Human-input file** (`human-input.md` / `HUMAN-INPUT.md` at the repo root) → the human's
   inbound backlog: claim an item before working it (the file's own convention), and when a
   unit resolves one, mark it `[X]` in the same commit with a deep link to the evidence (commit
   SHA, file, preview URL). Never delete or reword the human's text; an item outside the plan's
   scope stays unchecked — note it as a residual instead of absorbing it.
8. **Shared mutable resource** (live dataset, database, CMS, bucket) in the plan's path → before
   the FIRST write: snapshot/backup, then check for concurrent writers (last-writer/`_updatedAt`/
   mtime since your baseline). Resource moving under you → STEERING question, next independent
   unit; never seed over someone's in-flight edits. Writes stay scoped to the id shape the unit
   owns — another person's document is not yours to replace or delete.

## Step 2 — Per-unit loop (U1 → Un, plan order)
For each unit: mark in progress → reread section U<N> → implement the SMALLEST honest diff
following the local dialect → the unit's test scenarios become real tests (new behavior: watch
the test FAIL before the implementation when the cost allows) → run the unit's VERIFICATION (the
plan's) → passed: mark done with 1-line evidence; narrate in the chat
("U2 ✅ — 3 files, test X green").
- **The unit CREATES a check (test, gate, probe, verification script) → prove it can go RED
  before trusting its green:** mutate the reference or break the input, watch it fail with a
  meaningful diff, revert. A check that cannot fail is decoration — the most dangerous kind of
  green is one that measures nothing. Prove it fails CLOSED too: run it with its own tool/API/
  input absent (browser off PATH, token missing, fixture gone) — absence must be red or loud,
  never exit 0. A gate that skips silently when its dependency vanishes is a ghost gate.
- **A gate goes RED and the verdict is "the reference is stale, not the code" → re-freezing is
  a plan deviation, never a reflex.** Four parts, all required: (1) diff the reference and map
  every changed line to an intended change of THIS unit — one unexplained line means the code is
  wrong, not the reference; (2) the reference update lands in its OWN commit, titled as a
  re-freeze with the reason, never bundled with code; (3) it appears under "Plan deviations" in
  the envelope and in STEERING; (4) a known visible change that passed UNDER a tolerance is
  reported as a gate measuring less than it claims — name the tolerance. A re-freeze mixed into
  a code commit is indistinguishable from a gate silenced to pass.
- **Plan doesn't match reality** (file changed, premise fell): small deviation → note it in your
  execution note and continue; STRUCTURAL deviation → stop the unit and report "the plan expected
  X, reality is Y, I propose Z" (in a pipeline: record it and choose the reasonable path if
  reversible; otherwise stop).
- **An instruction (supervisor, STEERING, plan) collides with what a gate measures → the gate
  outranks the instruction.** Legitimate refusal has a strict shape, all four required: run the
  check instead of arguing; produce evidence anyone can re-verify; refuse LOUDLY (the evidence
  written where the instruction came from, never a silent swerve); deliver the instruction's
  INTENT by the path that doesn't lie. Never comply into a red — obeying a directive past a
  failing gate is the same failure as a silent deviation, wearing obedience.
- **Failed 2× the same way → new hypothesis.** 3 dead hypotheses in the same unit → the unit
  becomes a BLOCKER in the envelope; move on to the next independent unit, if any.
- **NEVER:** edit the plan as if it were state; delete/skip a test to pass; "seize the moment"
  to refactor outside the scope (note it as a residual).

## Step 3 — Final verification
ENTIRE suite + typecheck/lint + build (if it exists). Compare with the baseline: a regression
that is YOURS → fix it before reporting. Then the plan's **Regression checklist**, every line:
one run per OUTPUT TARGET the project ships (static build, SSR/preview function, deployed URL,
feeds), not only the mode your change targeted — a gate that exercises one build mode is blind
to the other, and "the function file exists" is not "the function answers". Clean the scene:
debug prints, orphan imports, scratch files.

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
A PR was opened (authorized push) → the unit ENDS there. Merging it — your own included, CI
green included — is AUTONOMY's red zone unless a written standing order names that PR class;
CI green is a precondition of a merge, never its authorization.
Plan fully done AND a human gate exists (STEERING supervisor, PM, client) → offer the acceptance
report: `docs/plans/<slug>-acceptance.md`, distilled FROM the execution log — per-unit evidence,
deviations named (a deviation declared is allowed; a silent one is not), decisions left open for
the gatekeeper. The human accepts against evidence, not against a chat scroll.
Honesty rule above all: STATUS `complete` requires every unit with verification executed IN THIS
session. A well-reported partial > a false complete — no exception.
