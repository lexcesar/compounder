---
name: handoff
description: Generates a handoff document for the next session (actual state with evidence, next step executable in 1 minute, traps, pending decisions). Use when closing a session with work still open.
argument-hint: "[optional - extra context for the handoff]"
---

# /handoff — passing the baton

Extra context from the user (if any): `$ARGUMENTS`

The next session (you yourself, tomorrow, with zero context) will only know what this document says.
Write for a competent colleague who saw NOTHING of this conversation.

Template: the project's `docs/templates/handoff.md` if it exists; otherwise `template.md` next to
this skill (`${CLAUDE_PLUGIN_ROOT}/skills/handoff/template.md`). Save to
`docs/handoffs/YYYY-MM-DD-HHMM.md` (create the folder if needed).

Quality rules — what separates a useful handoff from a useless one:
1. **State is what IS, not what should be.** "Tests: 47/49 passing; the 2 failing ones are
   pre-existing (names + evidence)" — never "tests ok".
2. **Done only with evidence.** Each completed item cites its proof (command run, file, output).
   An item without proof goes under "in progress", not "done".
3. **The next step is executable in 1 minute.** "Continue the refactor" is useless.
   "Run `pnpm test src/billing` and fix the clock mock in `tests/helpers.ts:34`" is useful.
4. **Traps are worth gold.** Everything that cost time to discover and is written down nowhere:
   a command that needs an env var, initialization order, a flaky test, a misleading API.
5. **Pending decisions with full context:** situation, options, consequences, your recommendation
   and why — so the user can decide without reconstructing the discussion.
6. **Do not copy file contents** — point to `path:line`. The document is a map, not a suitcase.

After saving: show the user the file path and a 3-line summary.
If `docs/goals/ACTIVE.md` exists, update the state of its criteria there too.
