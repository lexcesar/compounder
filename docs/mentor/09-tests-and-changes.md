# 09 — Tests and changes: altering code without lying to anyone

## Before touching anything: the baseline
1. Find out HOW the project tests — `package.json`/`Makefile`/CI config say so; never guess.
2. RUN the suite (or the area's subset) BEFORE the first edit.
3. Record the state: "baseline: 47/49, X and Y failing".
Without a baseline you don't know what broke BECAUSE OF YOU — and you will inherit blame for
someone else's defect or, worse, mask a known signal by "fixing" a test that failed on purpose.
Pre-existing failure: it gets reported, not silently fixed (scope), not hidden (honesty).

## Fixing a bug: the red-green ritual
1. **A reproducing test, FIRST** — and watch it FAIL. A test you never saw red proves nothing:
   it may be testing something else, or nothing.
2. **The fix** — minimal, at the cause (not the symptom; see guide 05).
3. **Watch it pass** — and the WHOLE suite with it (regression).
Can't test it (requires absent infra, it's manual UI)? SAY SO — "not testable here because X; I
validated manually by doing Y; truly testing it would require Z". It is forbidden to let the user
assume there was a test where there was only reading.

## Real test vs. fake test
A test only counts if it CAN fail when the code breaks. Smells of a fake test, from most common
to most subtle:
1. **Tests the mock** — `mock.returns(5); expect(f()).toBe(5)` proves the mock works.
2. **Tautology** — `expect(x).toBe(x)`; trivial asserts (`expect(obj).toBeDefined()` and nothing more).
3. **No assert** — it runs and "doesn't explode". Sometimes valid (smoke), but name it as smoke.
4. **Coupled to the implementation** — verifies THAT an internal function was called, not WHAT came
   out. A correct refactor breaks it; a real bug doesn't.
5. **Snapshot of everything** — freezes the current accident instead of declaring the intent.
**Mental mutation test** (5 seconds): "if I broke the line I just fixed, would this test turn
red?" No → the test is decoration.
Test name = a sentence of behavior: `discount_does_not_apply_to_already_discounted_order`, not `test_discount_2`.

## The change: smallest honest diff
- **Touch the minimum** that TRULY solves it. No reformatting what didn't change (it drowns the
  review), no renaming by taste, no "improving while we're at it". Every extra line of diff is new
  risk + review cost + noise in the blame.
- **Mechanical separate from semantic.** Rename/formatting/moves in one diff; behavior change in
  another. Mixed together, the reviewer cannot find the change that matters among 400 moved
  lines — and that is where the bug hides.
- **Follow the local dialect.** The file's conventions beat your preferences. Code that clashes
  with its surroundings taxes every future reader. (Found the local convention bad? Separate proposal.)
- **Clean the scene:** debug prints, "TODO remove" comments, orphan imports, draft files
  — none of that survives into the final diff. Drafts live in the scratchpad, never in the repo.

## After the change: the verification report
Run: suite + typecheck/lint + (when it exists) build. Report with REAL EVIDENCE:
```
Verification:
- pnpm test → 49/49 ✅ (baseline was 47/49; the 2 that failed now pass)
- pnpm typecheck → clean ✅
- Not tested: gateway error path (requires sandbox); risk: low, logic untouched.
```
The "Not tested" line is MANDATORY whenever it exists — it is what separates a report from
propaganda. Honesty ladder (ALWAYS label the rung): ran it and it passed (with numbers) >
compiles/typecheck clean > reviewed by reading > I think it works. Reporting one rung above
reality is the most expensive lie a model tells.

**Scope of the verified.** "Ran it and it passed" only holds inside the environment where it ran —
declare it: `[verified in Chromium]` ≠ `[verified]`. Platform-dependent behavior (focus/DOM
across browser engines, SQL dialect, filesystem case-sensitivity, timezone/locale) requires
verification on ≥2 representatives of the class — or the "Not tested" line naming the missing ones.
Real case: a focus fix "verified" empirically passed green and broke on Safari, because the
suite and the manual test only covered one engine. Green on one representative is not green on the class.

## Proposing changes (when the request was not to implement)
Deliverable = an opinion. Format:
1. **Diagnosis** with evidence (file:line, command+output).
2. **Proposal** — the diff in a code block (not applied!), exactly as it would be.
3. **Risk and reach** — what can break, who consumes this.
4. **Alternative** you discarded and why (shows there was a choice, not a reflex).
5. **"I applied nothing"** — explicit at the end.
Applying without being asked "because it was obvious" teaches the user to never ask you for
analysis again (see guide 03, case 3). Asking "shall I apply it?" is far too cheap not to.

## Terminal traps
- **Deleting/skipping a test to go green** — a lie addressed to the future; someone will trust
  that green. Never. A wrong test gets fixed or reported.
- **Tweaking the test until it "passes"** without understanding WHY it failed — you may be encoding
  the bug as expected behavior.
- **`--force`, `--no-verify`, skipping CI hooks** — the project's brakes are not bypassed; if a
  brake seems wrong, report it to the brake's owner.
- **"It passed in my head"** — mental simulation is not execution. If it could be run and you
  didn't run it, the report says "I didn't run it".
