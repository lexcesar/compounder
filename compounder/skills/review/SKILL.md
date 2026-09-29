---
name: review
description: Multi-lens review with adversarial verification of the findings. Use after implementing, before commit/PR, or when the user asks for a review of a diff/branch/files. Token "ultra" = swarm engine (rounds until dry + 3-vote tribunal).
argument-hint: "[scope: branch | files | empty = diff vs default] [apply] [ultra] [budget:released]"
---

# /review — panel + tribunal

Input: `$ARGUMENTS` (token `apply` = beyond reporting, apply safe-class fixes).

Two stages because reviewer agents have one specific poison: PLAUSIBLE-BUT-FALSE findings.
The panel finds; the tribunal kills the false ones. Only what survives reaches the user.

## Severity rubric (paste it, verbatim, into every panel and tribunal brief)
Rate by consequence on the path a user actually takes, never by how the code reads.
- **SEVERE** — used as documented, the thing gives a wrong result, loses or exposes data, or a
  gate reports green while measuring nothing.
- **MEDIUM** — a real, reproduced defect on a path that is reachable but uncommon: it needs an
  unusual input, environment or sequence.
- **MINOR** — latent (no real input reaches it today), cosmetic, or a process gap.

Rules for the disputes that recur:
1. Reach moves the level. A SEVERE-shaped defect that no real input reaches is MEDIUM; say what
   was measured ("0 of 151 transcripts").
2. Missing tests are a process gap: MINOR, or MEDIUM when the project's own rules demand tests for
   this kind of code. One finding for the whole diff, not one per function.
3. Exposure needs a reader: name who can read it and what they gain. Visible only to the same
   user is MINOR.
4. Not reproduced is a suspicion, whatever level it would have had.
5. The level opens the finding, in brackets.

## Step 0 — Scope
No argument: diff of the current branch vs default (`git diff <default>...HEAD` + working tree).
With argument: whatever it says. Empty diff → say so and stop. Note: N files, ~N lines.
Giant diff (>~1500 lines): review by area in rounds and say you did that.

## Step 1 — Panel (parallel)
Dispatch the 4 reviewers in ONE single message (true parallelism), each with the scope + the goal
of the change (1 sentence) + the severity rubric + format instruction:
`correctness-reviewer`, `security-reviewer`, `simplicity-reviewer`, `tests-reviewer`.
Small diff (<50 lines, no external input surface): correctness + tests alone suffice — say you
trimmed the panel. No subagent tool: run the 4 lenses yourself, in sequence, one pass per lens
(don't mix — a single lens at a time is what keeps the eye sharp).

## Step 2 — Dedup and corroboration (you, no agent)
Merge findings at the same `file:line`. Re-rate every merged finding by the rubric: a reviewer's
level is a proposal. Keep, for each finding, how many lenses raised it. Corroboration by 2+ lenses
says the finding is likely real, not that it is worse: it sends the finding to the tribunal and
raises it in the order, never in the level.
Discard style findings with no behavior change (not this panel's job).

## Step 3 — Adversarial tribunal
Every SEVERE/MEDIUM finding, and every finding raised by 2+ lenses whatever its level, goes to the
`adversarial-verifier` (parallel, one per finding; many findings → group by file) with the order:
REFUTE this — open the code, build the concrete failure
scenario, hunt for the counterexample. Verdict: CONFIRMED (scenario demonstrated) | REFUTED (dies;
vanishes from the report) | INCONCLUSIVE (downgraded to "suspicion"). For each CONFIRMED finding
the verifier also returns the level the rubric gives it, with the reach it measured; when that
differs from yours, the report carries the verifier's level and says so. A MINOR raised by a
single lens skips the tribunal (too cheap to judge — report it as minor as it is).

## Step 4 — Report
```
VERDICT: <approved | reservations | rejected> — 1 sentence
CONFIRMED (by severity):
1. [SEVERE] file:line — <defect> | Lenses: <N> | Scenario: <input/state → consequence> | Suggested fix: <1 line>
   Level: tribunal <X>, panel <Y> — <the reach that decided it>      (this line only when they differ)
SUSPICIONS (inconclusive): <...>
MINOR: <grouped, 1 line each>
DISCARDED BY THE TRIBUNAL: <N findings refuted — not problems>
COVERAGE: <lenses run + where we searched without finding anything>
```
Without the `apply` token: the opinion is the deliverable — don't touch the code. Close with the
routed menu:
```
Review ready (N confirmed, N minor). Next step?
1. Apply safe class — only mechanical/covered fixes, suite after each one
2. Fix item by item — walkthrough of the confirmed findings with me
3. Just record — I write the findings to docs/plans/<context>-residuals.md and stop
```
Recommend by severity ("2 SEVERE confirmed → option 2; only minors → option 1").

## Ultra mode (`ultra` token)
Same contract and report as Steps 0–5 — only the ENGINE of Steps 1–3 changes, for scale.
Inspired by `/code-review ultra`: more rounds, more votes, less wall-clock. Runs LOCAL
(session tokens), not in any cloud.

**Cost and consent:** 3–10× a normal `/review`. Without `budget:released` in the arguments,
announce the estimate ("~N agents: panel 4×R rounds, tribunal 3 per finding") and ask for an
ok BEFORE firing.

Engine, by capability (detect and degrade gracefully, as in `/slfg`):

1. **`Workflow` tool available** — deterministic orchestration script:
   - **Pipeline, no barrier**: each lens's findings enter the tribunal while other lenses
     still sweep.
   - **Loop-until-dry**: after the first panel pass, re-fire finder rounds (each briefed with
     what was ALREADY found — "hunt what the previous round missed") until 2 consecutive rounds
     yield nothing new. Dedup against everything SEEN (including refuted findings — else
     rejected findings reappear and the loop never converges).
   - **3-vote tribunal**: each SEVERE/MEDIUM finding judged by 3 `adversarial-verifier` calls
     with distinct lenses (correctness / security / does-it-reproduce). Dies with ≥2 REFUTED;
     CONFIRMED needs ≥2 non-refutations.
   - **Budget**: user gave a token target ("+500k") → scale rounds off `budget.remaining()`;
     no target → cap at ~15 agents total.
   Script skeleton (adapt scope/prompts; JS, no TS annotations):
   ```js
   export const meta = { name: 'review-ultra', description: 'Panel rounds until dry + 3-vote tribunal',
     phases: [{ title: 'Find' }, { title: 'Verify' }] }
   const seen = new Set(), confirmed = [], minors = []; let dry = 0, round = 0
   while (dry < 2 && (budget.total ? budget.remaining() > 50_000 : round < 3)) {
     round++
     const found = (await parallel(LENSES.map(l => () =>
       agent(brief(l, [...seen]), { phase: 'Find', schema: FINDINGS })))).filter(Boolean).flatMap(r => r.findings)
     const fresh = found.filter(f => !seen.has(key(f)))
     if (!fresh.length) { dry++; continue }
     dry = 0; fresh.forEach(f => seen.add(key(f)))
     const judged = f => f.sev !== 'MINOR' || f.lenses >= 2   // corroborated minors are judged too
     minors.push(...fresh.filter(f => !judged(f)))
     await parallel(fresh.filter(judged).map(f => () =>
       parallel(['correctness', 'security', 'reproduces'].map(lens => () =>
         agent(refuteBrief(f, lens), { phase: 'Verify', schema: VERDICT })))
         .then(vs => { if (vs.filter(Boolean).filter(v => !v.refuted).length >= 2) confirmed.push(f) })))
   }
   return { confirmed, minors, examined: seen.size }
   ```
2. **Subagent tool only** — fixed 2 rounds of the 4-lens panel (round 2 briefed with round 1's
   findings), tribunal of 1 verifier per finding as in Step 3; each wave in ONE single message.
3. **No subagents** — run the normal `/review` inline and say ultra was unavailable.

Report: Step 4 format, plus one line:
`Ultra: <N agents, N rounds, N found / N refuted / N confirmed> | engine: workflow|subagents|inline`

## Step 5 — Application (only with `apply`)
Classify each CONFIRMED finding:
- **Safe class** (mechanical, local, behavior covered by an existing test or trivially
  verifiable): apply, smallest diff, run the suite after EACH application.
- **Unsafe class** (requires a design decision, changes a contract, no coverage): do NOT apply —
  return it in the list with the why.
Final report: applied (with green suite) vs returned. Suite broke with a fix → revert THAT fix
and return the finding with the note.

## Evolution log
- 2026-09-29: severity rubric added; corroboration stops raising the level. Six runs on one frozen
  commit rated the same finding SEVERE, MEDIUM and MINOR (agreement 62%), and the one time the
  +1-level rule fired on three lenses the tribunal undid it. Corroboration is evidence that a
  finding is real, so it now buys a tribunal check, even for a MINOR, and a place in the order.
  The report shows both things that used to be invisible: how many lenses raised a finding, and
  when the tribunal's level differs from the panel's. Draft until three clean-room runs reach 80%.
