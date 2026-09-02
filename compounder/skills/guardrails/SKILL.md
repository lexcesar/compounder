---
name: guardrails
description: Interviews the user and generates layered guardrails — settings.json permissions (mechanical), CLAUDE.md invariants (judgment), AUTONOMY.md zones (criterion), optional hook. Use when setting up a project or after an incident.
argument-hint: "[optional - specific area, e.g. \"database\"]"
---

# /guardrails — build tailored boundaries

Requested focus (if any): `$ARGUMENTS`

Clear limits INCREASE useful autonomy: the more the user trusts the fences, the less they
need to watch every step. The four layers, defense in depth and the hook recipe: `reference.md`
next to this skill (`${CLAUDE_PLUGIN_ROOT}/skills/guardrails/reference.md`) — read it first.

## Step 1 — Reconnaissance (before asking)
Look at the project and deduce what you can on your own: stack, available scripts, existence of
`.env*`, apparently sensitive directories (`migrations/`, `infra/`, `deploy/`), CI with deploy,
existing `.claude/settings.json`, `CLAUDE.md`, `AUTONOMY.md`. Do not ask what the repository
already answers.

## Step 2 — Interview (one round, at most 7 questions, grouped)
Use AskUserQuestion/direct questions, always offering a recommended default. Ask by RISK
("what would give you a bad night if I did it?"), then translate disaster → pattern yourself:
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
   asked for more confirmations → move items to 🔴). No AUTONOMY.md in the project → propose
   creating one with three zones (🟢 act and note / 🟡 act and announce / 🔴 ask first) seeded
   from the answers.
4. **Hook** (optional, only if the user wants programmatic protection) — propose the snippet from
   `reference.md` §Hooks, explaining what it blocks and that a broken hook disrupts everything.

Every new fence carries its why (a comment in CLAUDE.md/AUTONOMY.md, not in the JSON); the same
critical risk appears in ≥ 2 layers.

## Step 4 — Apply with transparency
Show ALL proposed diffs at once (settings.json, CLAUDE.md, AUTONOMY.md). Apply after
the ok. End with the 3-line summary: what became forbidden, what asks for confirmation, what was
freed up — and the sentence: "to revisit this in the future, run `/compounder:guardrails` again;
to evolve from incidents, `/compounder:compound` feeds these same layers."
