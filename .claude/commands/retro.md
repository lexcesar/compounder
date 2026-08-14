---
description: Harvests the session's lessons and records each one in the right place (memory, CLAUDE.md, skill, AUTONOMY)
argument-hint: [optional - specific lesson to record]
---

# /retro — feedback that becomes rule

User input (specific lesson, if any): `$ARGUMENTS`

A correction that does not become a recorded rule will be repeated. This command is the evolution
mechanism of the entire system. Full method: `docs/mentor/07-feedback-and-evolution.md`.

## Step 1 — Harvest (sweep the current session)
List honestly, citing the moment it happened:
1. **Explicit corrections** — the user said "no", "not like that", "I prefer X", undid something of yours.
2. **Silent corrections** — the user redid or adjusted what you delivered.
3. **Your self-detected mistakes** — dead ends, wrong hypotheses, guessed commands,
   time lost by not having read something first.
4. **Confirmed wins** — approaches the user accepted without changes (they are signal too:
   they confirm existing rules).
5. **Assembly-line dispatches** — if `docs/pipeline/dispatches.jsonl` exists, read this
   session's lines (`session` field) and apply the lesson trigger and the promotion/demotion
   rules defined in `ROUTES.md` (Audit section — their single address).

Session with nothing in items 1–3? Say so and stop — an empty retro does not invent lessons.

## Step 2 — Distillation (the step that separates senior from junior)
For each item, extract the GENERAL RULE, not the incident:
- ❌ Incident: "I used npm but the project uses pnpm."
- ✅ Rule: "before any package command, detect the manager from the lockfile."
Test of a good rule: it would start with "always" or "never", and a third party would understand
it without knowing the incident.

## Step 3 — Destination (decision table)
| The lesson applies to... | Record in |
|---|---|
| This project, any session, anyone | `CLAUDE.md` (respecting the limit: a line only gets in if it changes behavior) |
| This user, across projects (preference, style) | `memory/` new file + a line in `MEMORY.md` |
| Method in general, would hold in ANY project | Upstream doctrine — the method kit/plugin the user maintains: propose the promotion (the lesson dies if it stays only in project memory). No upstream → `memory/` |
| Permission limit or autonomy decision | `AUTONOMY.md` (zones) or `.claude/settings.json` |
| Repeatable procedure with steps | Skill/command: patch the existing one or propose a new one |
| Wrong route/model for a dispatched task type | `ROUTES.md` (route table + evolution log) |
| Only applied to today's task | **Do not record it.** Accumulated noise kills the system. |

## Step 4 — Application
1. Show the user: lesson → distilled rule → destination file → proposed diff.
2. Apply what they approve (edits to kit files are 🟡 zone: act and announce; if the rule
   restricts YOU, you may apply it directly).
3. **Two-strikes rule:** the same mistake for the 2nd time across sessions → recording is
   mandatory, not optional — and mention in the summary that it was a repeat offense.

## Step 5 — Pruning (every ~5 retros or when you notice)
Recorded rules that never fired again, contradict newer feedback, or reference things that no
longer exist → propose deleting them. Dirty memory is worse than empty memory: it lies with confidence.
This includes routes: apply the route-pruning criterion defined in `ROUTES.md` itself (Audit).
