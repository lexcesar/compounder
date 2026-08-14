---
description: Turns a request into a verifiable goal contract (docs/goals/ACTIVE.md)
argument-hint: [goal in natural language] | status | done
---

# /goal — goal contract

User input: `$ARGUMENTS`

A goal without acceptance criteria is a wish. This command turns wish into contract.
The contract lives in `docs/goals/ACTIVE.md` and is the anchor for ALL decisions until it is closed.

## If the input is empty or `status`
Read `docs/goals/ACTIVE.md`. Report: the goal in 1 sentence, acceptance criteria with state
(✅ met with evidence / ⬜ pending / ⚠️ at risk), the next concrete step. If the file does not
exist, say there is no active goal and ask for one.

## If the input is `done`
1. Re-read `docs/goals/ACTIVE.md` and verify EACH acceptance criterion for real (run the test,
   open the file, execute the command). No checking ✅ from memory.
2. Criterion not met → report which ones and ask: close anyway (recording it as
   "not met") or keep working?
3. All met → move the file to `docs/goals/archive/YYYY-MM-DD-<slug>.md` (create the folder
   if needed), append a final `## Outcome` section with the evidence, and suggest running `/retro`.

## General case: the input is a new goal
1. If a non-archived `docs/goals/ACTIVE.md` already exists, warn and ask: replace it or archive first.
2. Do the MINIMUM reconnaissance needed to write real criteria (look at the cited code,
   confirm the targets exist). Do not start implementing.
3. If there is ambiguity that changes the outcome, ask — at most 3 questions, all at once,
   each with your recommendation. Ambiguity that does not change the outcome: assume the
   reasonable thing and declare it.
4. Write `docs/goals/ACTIVE.md` in this format:

```markdown
# Goal: <1 sentence, verb-first, observable outcome>
Created: <YYYY-MM-DD> | Original request: "<user's verbatim words>"

## Why (value)
<1–2 sentences: what problem it solves, for whom>

## Acceptance criteria
<!-- Each one CHECKABLE: a command that runs, a behavior that can be observed, a file that exists.
     Vague criteria like "clean code" or "works well" are forbidden. -->
- [ ] <criterion> — verification: <how to prove it>
- [ ] <criterion> — verification: <how to prove it>

## Non-goals (out of scope for this round)
- <what will NOT be done, to contain scope drift>

## Constraints
- <technical, time, compatibility limits>

## Declared assumptions
- <what was assumed without user confirmation>

## Known risks
- <risk> → <mitigation or "accepted">
```

5. Show the user the contract in summary (goal + criteria) and start the work.

## Standing rule while ACTIVE.md exists
Before any significant decision, ask yourself: **"does this serve the contract?"**
Work that serves no acceptance criterion and is not a prerequisite of one → don't do it,
or propose it as an explicit addition to the contract.
