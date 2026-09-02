# 02 — Living memory

## The mental model
You wake up amnesiac every session. Memory (`MEMORY.md` + `memory/`) is the letter that
yesterday-you left for today-you. Two implications:
1. Write for someone who didn't see the conversation — no implicit context, no "today's problem".
2. The letter competes with everything else for your reading time — every useless memory dilutes the useful ones.

Architecture: `MEMORY.md` is the INDEX (one line per memory; loaded/read at session start);
`memory/*.md` are the facts (one file = one fact; opened only when relevant). Never invert this:
content in the index bloats the fixed cost of every session.

## Memory file format
```markdown
---
name: short-kebab-slug
description: one sentence — used to decide relevance without opening the file
metadata:
  type: user | feedback | project | reference
---

The fact, in 1–5 lines, absolute dates.

**Why:** what happened that generated this memory (the evidence).
**How to apply:** the concrete behavior change.
```
The `description` is the most important field: it's how future-you decides whether or not to open it.
Vague description = invisible memory.

## The four types and each one's yardstick
- **user** — who the user is: role, expertise, communication and decision preferences.
  Yardstick: would it help calibrate ANY future response? ("prefers diffs to long explanations").
- **feedback** — corrections and confirmations about HOW to work. The most valuable type. Always
  with **Why** and **How to apply**. Record the distilled rule, not the incident
  (see `docs/mentor/07-feedback-and-evolution.md`).
- **project** — project state and decisions that are NOT spilled into the code/git: long-term
  goals, constraints agreed verbally, who decides what.
- **reference** — external pointers: dashboard URLs, tickets, internal docs. Only the pointer
  and when it was seen; external content changes.

## What NEVER to record
- **What the repository already records** — code structure, fixes made (git log), CLAUDE.md
  content. Duplicated memory GOES STALE and starts to lie.
- **Task ephemera** — "test X is failing today". Tomorrow it's a lie; that's `/compounder:handoff`
  business, not memory.
- **Secrets** — never, in any form.
- **Trivia** — "user said hi in Portuguese". The temptation to record too much is failure
  mode #1: memory is signal, and signal is defined by what it refuses to include.

## Writing discipline (in this order, always)
1. **Search before creating.** Does a memory on the subject already exist? UPDATE it (and its description).
   A duplicate is worse than absence: two versions diverge and you don't know which one to trust.
2. **Absolute dates.** "Last week" rots; "2026-07-06" doesn't.
3. **Link related ones** with `[[slug]]` — a web retrieves better than a list.
4. **Index.** A file without a line in `MEMORY.md` doesn't exist.

## Reading discipline
- Session start: read the INDEX; open only the memories whose description touches the task.
- A retrieved memory is a hypothesis, not current fact: it records what was true WHEN WRITTEN.
  If it points to a command/file/decision, confirm it still exists before acting on it.

## Memory death (as important as birth)
Delete (file + index line) when: the memory proved wrong; the feedback was superseded by a newer
one; what it points to no longer exists. In doubt between pruning and keeping a suspicious memory:
verify it now or delete — keeping it "just in case" is how the 40-line indexes where nobody finds
anything are born.

## Example — bad vs. good
❌ `memory/todays-bug.md`: "Fixed the parser bug by adding trim() on line 42."
(Ephemeral, already recorded in git, no general rule.)

✅ `memory/feedback-parser-real-inputs.md`, type feedback:
"Parser inputs come from customer spreadsheets: whitespace, BOM and mixed encoding are the NORMAL
case, not the exception. **Why:** 2026-07-06, fix only accepted after covering those cases; the
first 'clean' version was rejected. **How to apply:** when touching parsing/validation in this
project, test with a real sample from `fixtures/` before declaring it done."
