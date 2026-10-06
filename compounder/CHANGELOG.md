# Changelog

What changed in each release of the compounder plugin, written for the people who use it. Versions follow [Semantic Versioning](https://semver.org/).

## [2.7.0] — 2026-10-03
### Added
- `/compound` has a home for decisions: a choice that is expensive to reverse, with the alternatives it beat, goes to `docs/decisions/`, and `/plan` reads it before proposing an option the project already rejected.
- `/compound refresh` classifies each record by what it still guides — keep, update moved facts, archive, or delete — instead of only checking that cited paths exist.
- The simplicity reviewer flags prose only the authoring session can follow: session ids, local paths, private names, "rejected in review". Dated incident anchors stay.
- `/work` counts a filtered test run as evidence only after its report shows which tests were selected.
- Guide 11 of the kit gains rules for writing model-facing text: each fact once, and measure first-turn tokens before and after a change.
### Changed
- A changed decision is never edited in place: it gets a new record that supersedes the old one, and the ADR template uses the file path as the record's id.

[Release notes](https://compounder.alexcesar.com/changelog/2.7.0/)

## [2.6.0] — 2026-09-17
### Added
- `scripts/dispatch-cost.py` reads the token usage in Claude Code transcripts and reports, per dispatch, tokens, estimated cost, and whether the subagent started fresh or as a fork of the parent's context.
- `scripts/count-tokens.sh` sizes a plan or brief with the free token-counting endpoint before you hand it to an executor.
- The dispatch log described in `ROUTES.md` accepts optional cost fields.

## [2.5.0] — 2026-09-02
### Added
- `/compounder:goal`, `/compounder:handoff`, `/compounder:guardrails` and `/compounder:council` ship inside the plugin, so projects that install only the plugin get them too.
- Each one bundles its defaults (the council's 15 avatars, the handoff template, the guardrails reference); a project's own copies override them.
### Changed
- The kit keeps only `/retro` as a local command.

## [2.4.1] — 2026-08-21
### Changed
- `/plan` quotes constraints inherited from documents verbatim with `path:line` and re-reads them against the default branch the day the plan is written, so a paraphrased note cannot turn into a rule nobody wrote.

## [2.4.0] — 2026-08-21
### Added
- Data that deployed code also reads has a reader to protect: a write that changes its shape needs expand/contract or a merge-time write, plus proof that the default branch still builds against it.
- When you answer by number, `/work` echoes its reading first. A merge, push or datastore write never rides on a bare "do it", and each write is its own ask.
### Changed
- `/goal` hands off to `/compounder:work` when a plan exists instead of starting the work itself.
- `/work` reads the repository's PR convention before the first commit: granularity is the repo's rule, not the executor's.

## [2.3.0] — 2026-08-20
### Added
- Plans carry a regression checklist per output target (static build, preview function, deployed URL, feeds), not per feature.
- Writes to a live dataset, database or CMS require a snapshot, a concurrent-writer check, and writes scoped to the unit's own ids.
### Changed
- Merging into the default branch is a red-zone action — your own PR with green CI included — unless a written standing order names that class of PR.
- Re-freezing a gate's reference is a recorded plan deviation in its own commit, never bundled with code.

## [2.2.1] — 2026-08-19
### Added
- When an instruction collides with what a gate measures, the gate wins: `/work` runs the check, refuses loudly with evidence where the instruction came from, and delivers the instruction's intent by a path that stays green.

## [2.2.0] — 2026-08-18
### Added
- A check must also fail closed: when its own tool, API or input is missing it goes red or loud, never exits 0.
- `/compound refresh` audits enforcement: each "never/always" rule is classified as hard (a deny rule, hook or CI check) or instruction-only.
- The tests reviewer hunts ghost gates and configuration-as-data without a pinning test.
- `/work` follows a `human-input.md` protocol: claim an item, resolve it, mark it done with a link to the evidence, never reword the human's text.
- STEERING files gain a start prompt for a fresh session, and a finished plan with a human gate offers an acceptance report.
### Changed
- Units that change a contract regenerate the derived specs behind a CI no-diff gate.

## [2.1.0] — 2026-08-13
### Added
- A unit that creates a check must prove the check can go red before its green is trusted.
- Multi-session plans get a STEERING file: active directives, questions for the supervisor, and a per-unit execution log.
- Research dossiers persist as briefs in `docs/plans/research/`; executors read them instead of exploring again.
- `/compound explainer` turns the learnings library into an onboarding page: rule, incident, and a quiz.
### Changed
- Rules recorded in `CLAUDE.md` carry the dated incident that created them.

## [2.0.0] — 2026-08-13
### Changed
- The plugin is renamed from composto to compounder, and every skill, agent, command and document is in English: `/plano` → `/plan`, `/trabalhar` → `/work`, `/revisar` → `/review`, `/depurar` → `/debug`, `/simplificar` → `/simplify`.
- Existing installs must re-add the plugin as `compounder@<marketplace>`.
### Added
- MIT license.

## Before 2.0.0
From July 2026 the plugin shipped in Portuguese as **composto** (1.x): the brainstorm → plan → work → simplify → review → compound pipeline, the four-lens review panel with an adversarial verifier, the `lfg` and `slfg` autopilots, `btw` asides, and a cheap fork route for execution.
