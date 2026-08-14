---
description: Interviews the user and generates layered guardrails (settings.json, invariants, autonomy)
argument-hint: [optional - specific area, e.g. "database"]
---

# /guardrails — build tailored boundaries

Requested focus (if any): `$ARGUMENTS`

Clear limits INCREASE useful autonomy: the more the user trusts the fences, the less they
need to watch every step. Full method: `docs/mentor/08-guardrails-and-boundaries.md`.

## Step 1 — Reconnaissance (before asking)
Look at the project and deduce what you can on your own: stack, available scripts, existence of
`.env*`, apparently sensitive directories (`migrations/`, `infra/`, `deploy/`), CI. Do not ask
what the repository already answers.

## Step 2 — Interview (one round, at most 7 questions, grouped)
Use AskUserQuestion/direct questions, always offering a recommended default:
1. **Untouchables:** which paths/files should I never modify? (suggest the ones you deduced)
2. **Secrets:** where do they live? (`.env`? vault? elsewhere)
3. **Forbidden vs. confirm-first commands:** deploy? migrations? push? recursive deletion?
4. **Environments:** is there any risk of me reaching staging/production from here? How do I tell them apart?
5. **Autonomy budget:** may I install dev-dependencies? create files? delete dead code?
6. **Sensitive data:** anything that must never leave this machine (not even in a subagent/service prompt)?
7. **Pace:** do you prefer that I ask more (safety) or push ahead more (speed)?

## Step 3 — Generate in layers
For each answer, choose the HARDEST layer that can hold it:
1. **`.claude/settings.json`** (`permissions.deny` / `ask` / `allow`) — mechanical, does not
   depend on the model remembering. Everything that can be a tool pattern goes here.
2. **`CLAUDE.md` → Invariants** — rules that require judgment ("never edit a merged migration").
   Testable sentence: starts with "never"/"always" + an observable condition.
3. **`AUTONOMY.md`** — zone adjustments (e.g.: user allowed dev-deps → move to 🟢;
   asked for more confirmations → move items to 🔴).
4. **Hook** (optional, only if the user wants programmatic protection) — propose the snippet from
   `docs/mentor/08-guardrails-and-boundaries.md` §Hooks, explaining what it blocks.

## Step 4 — Apply with transparency
Show ALL proposed diffs at once (settings.json, CLAUDE.md, AUTONOMY.md). Apply after
the ok. End with the 3-line summary: what became forbidden, what asks for confirmation, what was
freed up — and the sentence: "to revisit this in the future, run `/guardrails` again; to evolve
from incidents, `/retro` feeds these same layers."
