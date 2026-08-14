---
name: compound
description: Capture the session's learning and file each lesson at the right address (docs/solutions/, CLAUDE.md, memory, CONCEPTS.md). Use after solving something that cost time. Refresh mode to prune the library.
argument-hint: "[learning context | refresh]"
---

# /compound — interest on knowledge

Input: `$ARGUMENTS`

The compounding thesis: the first solution costs an investigation; documented AT THE RIGHT
ADDRESS, the next occurrence costs minutes. The classic mistake is capturing expensively
(ceremony → capture skipped) or capturing everything (noise → an unreadable library). This skill
distills and routes. Cheap enough to run EVERY time something cost time.

## `refresh` mode (input = "refresh")
Sweep `docs/solutions/**/*.md`: for each doc, do the cited paths/symbols still exist
(quick grep)? Is the solution still how the project does it? → Propose per doc: keep / update
(diff) / retire (move to `docs/solutions/archive/` with a reason note). Apply after ok.
A library that lies is worse than an empty one. Done.

## Step 1 — Harvest (with `$ARGUMENTS` as a hint; otherwise, sweep the session)
What in this session: took > 15 min to figure out? surprised you (the system wasn't what it
seemed)? was a user correction? will recur if not written down? List candidates, 1 line each.
Nothing qualifies → say so and stop. An empty compound doesn't invent lessons.

## Step 2 — Value bar (per candidate)
Record ONLY if: (a) it will save real time in a plausible future occurrence AND (b) it isn't
derivable from the code/git AND (c) you can write "when X, do Y because Z". Failed any one → trash.

## Step 3 — Routing (one address per lesson)
| The lesson is... | Address | Form |
|---|---|---|
| Reusable technical solution (solved bug, library gotcha, pattern that worked) | `docs/solutions/<category>/<slug>.md` | Solution doc (below) |
| Stable project rule ("never X here") | `CLAUDE.md` | 1 line, line-test: only goes in if it changes behavior |
| User preference/style | Memory (`memory/` + index) | Distilled rule + Why + How to apply |
| Domain term with local meaning | `CONCEPTS.md` (create it if missing) | Term + definition in 1–3 sentences |
| Repeatable multi-step procedure | Patch to an existing skill/command, or proposal for a new one | Proposed diff |
Solution categories: `bugs/`, `integration/`, `performance/`, `conventions/`, `infra/` (create
on demand; don't create empty taxonomy).

## Step 4 — Anti-duplicate (before writing)
Grep `docs/solutions/` for the lesson's terms. A doc on the subject already exists → UPDATE it
(and note `updated: YYYY-MM-DD`). Duplicates diverge and start lying.

## Solution doc (fixed format, ~20 lines — fits in the searcher's head)
```markdown
---
title: <1 symptom-oriented sentence — how someone would search for this>
date: YYYY-MM-DD
category: bugs|integration|performance|conventions|infra
tags: [<module>, <lib>, <symptom>]
---
## Symptom
<what is observed — paste the literal error if there is one (it's what the future will grep)>
## Cause
<the primary cause, 2–4 lines>
## Solution
<what fixes it, with file:line or command>
## Prevention
<test/guardrail/rule that prevents recurrence — or "none viable">
## References
<commits, PRs, links, related docs>
```

## Step 5 — Close the loop
1. Show: lesson → address → proposed text. Apply what's approved (rules that constrain only
   you: apply directly and announce).
2. Compounding only compounds if it gets READ: confirm the consumers exist — this plugin's
   `/brainstorm`, `/plan`, and `/debug` already grep `docs/solutions/` and `CONCEPTS.md`. If the
   project's CLAUDE.md doesn't yet mention `docs/solutions/`, propose the discovery line:
   "Before investigating an error or planning in a new area: grep `docs/solutions/` (solution
   library) and check `CONCEPTS.md` (vocabulary)."
3. Recurrence of an already-recorded lesson that was NOT consulted → the problem is discovery,
   not content: improve `title`/`tags` (symptom-oriented) instead of writing another doc.
