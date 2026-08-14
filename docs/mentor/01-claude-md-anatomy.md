# 01 — Anatomy of the ideal CLAUDE.md

## The fundamental economy
CLAUDE.md is loaded in EVERY session, forever. Every line pays context rent for eternity — and
context spent on instruction is context missing for reasoning. Everything follows from this:

> **A line only enters CLAUDE.md if removing it would worsen some observable behavior.**

It's not "useful information about the project". It's "instruction that changes action". The
difference kills or saves the file: "we use PostgreSQL" changes no action at all (the model sees it
in docker-compose); "dates always in UTC in the database; conversion only at the edge" changes
actions every day.

## The sections, in order of value per token

1. **Commands** — the highest value-per-token content there is. A wrong test command wastes
   minutes per session; a right one saves the discovery every time. Include: tests (suite and
   single file), lint/typecheck, build, run locally. And the meta-rule: "never guess; confirm at
   the source" — because commands change and CLAUDE.md goes stale.

2. **Invariants** — the absolute rules ("never X"). Few and truly absolute: a block of 20
   invariants teaches the model to ignore the whole block (if everything is critical, nothing is).
   Max ~7, each one testable: "never edit a merged migration" (checkable), not "be careful with migrations" (vague).

3. **30-second architecture map** — where what lives and the typical flow of a request/action.
   It is NOT architecture documentation: it's the minimum for the model to open the right file on
   the first try instead of the fourth.

4. **Non-inferable conventions** — only what reading the code does NOT reveal. "We use single
   quotes" is inferable (and the linter already handles it); "service X is generated, edit the template in Y" is not.

5. **Conditional pointers** — the technique that solves the "I want to give lots of context but
   can't pay for it" dilemma: a `situation → read this file` table. The deep knowledge lives in
   `docs/`, costs zero by default, and loads exactly when it's relevant. That's how this entire
   kit works (progressive disclosure).

6. **Work cycle** — one line with the expected loop (understand → plan → act → verify →
   report → learn). A cheap anchor that reduces the two most common flow errors: acting without
   understanding and reporting without verifying.

## Anti-patterns (each one seen in the wild)

| Anti-pattern | Why it kills | Fix |
|---|---|---|
| Mirroring what the code says | Pays rent for free information; and goes stale | Delete; the model reads the code |
| Vague rule ("write clean code") | Changes no concrete decision | Make it testable or delete |
| Architecture essay (3 pages) | Costs dearly every session; nobody carries 3 pages in their head | 6-line map + pointer to docs/ |
| Changelog/project history | History is not instruction | git log already exists |
| Public tool tutorial ("how to use git") | The model knows; training covered it | Delete |
| Dead rule (references something removed) | Worse than useless: teaches that the file lies | Prune via `/retro` |
| Begging tone ("PLEASE ALWAYS REMEMBER!!") | Inflated emphasis = everything becomes noise | Dry imperative; strength comes from clarity |

## Quality test for the whole file
1. **Line test:** for each line — "if I delete this, what behavior gets worse?" No answer → delete.
2. **Size test:** past ~120 lines → something is in the wrong place (it probably should be a
   pointer to docs/).
3. **Newcomer test:** does a competent model that only read this file complete the first task
   without tripping over a known gotcha? If there's an uncovered gotcha that ALREADY caused rework, a line is missing.
4. **Dust test:** does any line reference a file/command/folder that no longer exists? The whole
   file lost its credibility — prune now.

## Maintenance: the file is alive
The ideal CLAUDE.md on day 1 is reasonable; on day 90, sharp — IF `/retro` feeds it. Flow:
user correction → distilled rule → "does it apply to the whole project and is it stable?" → it goes
in (respecting the line test). And in the reverse direction: a rule that never fires → goes out. The
size should oscillate around the same point; only growing is a symptom of accumulation, not learning.
