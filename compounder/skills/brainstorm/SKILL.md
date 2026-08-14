---
name: brainstorm
description: Discover WHAT to build — the right questions in one round, output as a requirements doc. Use before planning features whose scope or value is still fuzzy.
argument-hint: "[idea or problem in natural language]"
---

# /brainstorm — the WHAT, before the HOW

Input: `$ARGUMENTS`

Goal: turn a vague idea into requirements a planner can execute without guessing.
Do NOT decide architecture or files here — that belongs to `/plan`.

## Step 0 — Is it worth it?
Request already small and clear (1 behavior, obvious acceptance)? Say: "this doesn't need a
brainstorm; I'll go straight to /plan" — and offer that. Brainstorming trivia is ceremony, and
ceremony kills the habit of using the funnel when it matters.

## Step 1 — Grounding before questions (cheap, mandatory)
1. Look at the repository in the idea's area (or dispatch 1 `researcher` if it's broad): what
   already exists? has something similar been done/tried?
2. Quick grep in `docs/solutions/` and `docs/plans/` for terms from the idea; read `CONCEPTS.md` if it exists.
Asking what the repo can answer burns the user's patience — every question of yours must be
something only THEY know.

## Step 2 — ONE round of questions (max 5)
Use the blocking question tool (AskUserQuestion; without it, a numbered list in chat).
All at once, each with your recommendation. Pick the 5 most likely to change the design:
1. **Real problem:** what pain triggers this? What happens today without the feature?
2. **User and frequency:** who uses it, how many times, with what urgency?
3. **Success:** how will we know it worked (numbers, observable behavior)?
4. **Non-goals:** what would be OUT even though it looks related?
5. **Constraints:** deadline, compatibility, sensitive data, what must not break?
Answers that contradict what you saw in the repo → point out the contradiction NOW (this is the
cheap moment).

## Step 3 — Write the requirements doc
`docs/plans/YYYY-MM-DD-<slug>-plan.md` (one artifact per feature; `/plan` enriches THIS file):
```markdown
---
stage: requirements
created: YYYY-MM-DD
---
# <Feature in 1 sentence>

## Problem
<the pain, with what you saw in the repo + what the user answered>

## Desired behavior
- R1: <observable, testable requirement>
- R2: ...

## Success criteria
- <checkable — a number or a behavior>

## Non-goals
- <explicit — the fence against drift>

## Constraints and known risks
- <...>

## Edge cases raised
- <empty/null, concurrency, permissions, volumes — the ones that matter HERE>

## Open questions (for the plan or for the user)
- <what went unanswered, and who answers it>
```
A good requirement = someone can write a test from it. "It should be fast" is not a requirement;
"p95 < 300ms on search" is.

## Step 4 — Handoff (routed menu)
Show the summary (problem + Rs + non-goals) and close with a numbered menu:
```
Requirements at <path>. Next step?
1. /plan <path> — decide the HOW now
2. Adjust requirements — tell me what
3. Park it — the idea didn't hold up (the file stays as a record of why)
```
Recommend ONE option with a why tied to what the round revealed ("criteria came out checkable
and no open questions → option 1"). An idea that died in brainstorm is a win for the funnel — say so.
