---
name: simplify
description: Take the plane to freshly written code while preserving behavior — YAGNI, duplication, premature abstraction. Use between implementing and reviewing, or on an area that keeps jamming changes.
argument-hint: "[scope: empty = branch diff | specific path]"
---

# /simplify — the plane

Input: `$ARGUMENTS`

Freshly written code carries scaffolding: speculative generality, layers that never paid for their
ticket, first-attempt names. This skill removes scaffolding WITHOUT changing behavior — it runs
between `/work` and `/review` so the review judges code that is already clean.

## Hard precondition
Run the scope's suite BEFORE. Red → STOP and report: simplifying on a broken base mixes "I just
broke it" with "it was already broken" and nobody can tell them apart anymore. (Pre-existing
failure documented in the `/work` baseline → ok, proceed, excluding it from the criterion.)

## Scope
Empty → branch diff vs default + working tree. Path → what was asked, BUT only simplify what the
recent change touched or what the user named — planing stable code that isn't yours is risk
without a mandate.

## Targets, in order of value
1. **Speculation (YAGNI):** parameter that only ever receives one value, branch that never runs,
   config for an imagined need, hook "for the future". Cut.
2. **Single-use abstraction:** interface with 1 implementation, wrapper that only forwards,
   3-line helper called once. Inline.
3. **New duplication:** the diff reinvented a utility the project already has → use the existing
   one. (2× duplication is still cheap; rule of three: abstract on the 3rd occurrence, not the 1st.)
4. **First-attempt names:** rename to what the thing IS now (local scope of the diff).
5. **Dead code from the diff:** orphan import, unread variable, comment narrating the obvious.
6. **Gratuitous depth:** nesting an early return resolves; double negative condition.

## Prohibitions
- Changing behavior (any "while I'm here, let me fix this" → note it as a residual, don't do it).
- Reformatting what wasn't touched.
- Abstracting "to make it elegant" — the plane REMOVES layers, it doesn't add them.
- Touching a test to accommodate it: a test that broke = behavior changed = revert the
  simplification (the exception: a test coupled to an implementation detail the inline
  eliminated — adjust the test and SAY so in the report).

## Hard postcondition
Suite + typecheck of the scope AFTER, green same as before. Any regression → revert the guilty
simplification (bisect if needed) before reporting.

## Report
```
Simplification: <N lines removed, N added> across <N files>
- <target>: <what left and why, 1 line each>
Behavior: preserved — suite <X/Y> before and after | typecheck clean
Residuals noted (untouched): <improvements that would require a behavior change, or "none">
```
Nothing to simplify? Say so in 2 lines — a plane with no work to do is a good sign, not a failure.
