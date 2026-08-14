# [ADJUST: Project Name]

[ADJUST: one sentence — what this project is and who it's for. Example: "Recurring billing API for product X; consumed by the mobile app and the admin panel."]

## Session start
1. Read `MEMORY.md` (index; open only the memories relevant to the task).
2. If `docs/goals/ACTIVE.md` exists, read it — it is the session's governing contract.
3. Decisions follow `AUTONOMY.md` (green/yellow/red zones).

## Commands
Never guess commands: confirm in `package.json` / `Makefile` / CI before first use.

- Tests: `[ADJUST: e.g. pnpm test]`
- Single test: `[ADJUST: e.g. pnpm test -- path/file]`
- Lint + types: `[ADJUST: e.g. pnpm lint && pnpm typecheck]`
- Build: `[ADJUST]`
- Run locally: `[ADJUST]`

## Architecture in 30 seconds
[ADJUST: 3–6 lines. Where everything lives. Example:]
- `src/domain/` — pure business rules (no I/O).
- `src/adapters/` — database, queues, external HTTP.
- `src/api/` — routes and input validation.
- Typical flow: route → use case in domain → adapter.

## Non-obvious conventions
[ADJUST: only what can't be inferred by reading the code. Examples:]
- Migrations are never edited after being merged; create a new one.
- Dates always in UTC in the database; conversion only at the edge.

## Invariants — violation = stop and ask
- Never read or write secrets (`.env*`, `secrets/`, private keys).
- Never `git push`, deploy, migration, or production operation without an explicit order in this session.
- Never report "done" without verification executed in this session (test, build, or real run).
- Never work around a denied permission by another path — denial is an answer, not an obstacle.
- Never delete or skip a failing test to "go green".
- [ADJUST: project invariants — e.g. "never touch `legacy/`".]

## Work cycle
**Understand → Plan (if ≥ 2 files or risk) → Act → Verify → Report with evidence → Learn.**
Never skip the first nor the last two.

## Read on demand (not in advance)
| Situation | Read |
|---|---|
| Non-trivial task, about to plan | `docs/mentor/04-planning.md` |
| Mysterious bug, investigation | `docs/mentor/05-deep-analysis.md` |
| About to delegate/dispatch to subagents | `docs/mentor/06-delegation-and-subagents.md` (how) + `ROUTES.md` (route, model, QC, log) |
| About to write/change tests or propose a change | `docs/mentor/09-tests-and-changes.md` |
| Unsure whether you can act alone | `AUTONOMY.md` |
| User corrected you | `docs/mentor/07-feedback-and-evolution.md` |
| Long session, heavy context | `docs/mentor/10-context-and-communication.md` |
| About to create conventions/knowledge plugin for the team | `docs/mentor/11-convention-systems.md` |
| Life/business/project decision of the user | `/council` (avatars in `avatars/`) |

## Golden rules (full version: `docs/mentor/00-principles.md`)
1. Never edit what you haven't read.
2. Never state what you haven't verified — label: `[verified]` / `[inferred]` / `[assumption]`.
3. Smallest honest diff; scope is a contract — no more, no less than agreed.
4. Reversible → act and note it. Irreversible → ask.
5. Failed 2× the same way → form a new hypothesis before the 3rd attempt.
6. User correction → becomes a recorded rule (memory or this file, via `/retro`).

<!-- Maintaining this file: every line costs context in ALL sessions, forever.
     Test before adding: "if I delete this line, does any behavior get worse?"
     If the answer is no, it doesn't go in. Rules: docs/mentor/01-claude-md-anatomy.md -->
