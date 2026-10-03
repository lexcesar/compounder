---
stage: ready-made-plan
date: 2026-10-03
origin: review of deepseek-harness (github.com/deepseek-ai/deepseek-harness @ 5badb15009ae1756c3afe0ae0cef1faafc290ccc, MIT) — which of its development-method ideas the compounder should absorb
---

# Absorb four deepseek-harness method ideas into the compounder

## Problem
deepseek-harness (dsh) runs its own agent-driven development on an Agent Notes corpus and 15
repository skills. Four of its criteria close gaps in the compounder; its machinery (bilingual
note triplets, frozen-archive manifest, format gates) does not fit a plugin whose thesis is cheap
capture. This plan absorbs the criteria as short text inside existing skills, agents and one
mentor guide. No runtime code is ported: dsh is a TypeScript/Cordis harness, the compounder is
markdown skills plus shell hooks.

Upstream sources (read at the SHA above; quote by path, never by local clone path):
`.agents/skills/dsh-trim-cot-leakage/SKILL.md`, `.agents/notes/README.md`,
`.agents/skills/dsh-archive-agent-notes/SKILL.md`, `.agents/skills/agent-experience/SKILL.md`,
`.agents/skills/dsh-pre-push-checks/SKILL.md`, `.agents/skills/dsh-code-review/SKILL.md`.

## Requirements
- **R1 — Session-vantage test.** Review flags prose that only the authoring session can resolve;
  `/compound` applies the same test before writing. Dated incident anchors stay legal.
- **R2 — Decision lifecycle.** `/compound` gains a route for decisions with their rejected
  alternatives; capture checks supersession in the same pass; `refresh` classifies by future
  decision value, never by age or size; a rejected alternative stays only while still tempting.
- **R4 — Model-facing text.** `docs/mentor/11-convention-systems.md` gains the agent-experience
  rules (each fact once, drop constraints the model learns from the result, measure first-turn
  tokens).
- **R5 — Micro rules.** (a) `/work`: a filtered test run is evidence only after its report shows
  the expected tests were selected; (b) security lens: follow each denial path to the operation
  that executes it, including alternate callers; (c) simplicity lens: a new public member on a
  shared module with one consumer is API expansion.

## Reconnaissance (seen this session)
- `compounder/skills/compound/SKILL.md` — Step 3 routing table (no decision route), Step 4
  Anti-duplicate already greps `docs/solutions/` and updates in place (R2's same-subject case is
  covered; the partial-supersession case is not), `refresh` decides keep/update/retire by
  "do cited paths still exist".
- `docs/templates/adr.md` — has `Rejected alternatives` and `superseded by`, and **zero consumers**
  in the plugin or mentor guides (grep for `adr` / `templates/`). R2 gives it its first.
- `compounder/agents/simplicity-reviewer.md` — item 5 already covers "public that could be
  private"; R5c is one clause, not a new item. No prose/leakage check exists.
- `compounder/agents/security-reviewer.md` — item 3 covers client-only role checks, not alternate
  callers that bypass the checked path.
- `compounder/skills/work/SKILL.md` — prove-it-can-go-red and fail-closed rules already exist
  (Step 2); filtered-run selection count does not.
- `docs/mentor/11-convention-systems.md` — "The fifteen laws" are mined from opten-conventions;
  a law sourced from dsh would misattribute that heading → separate section.
- `.claude/commands/retro.md` — routes user corrections, not design decisions → untouched.
- Calibration set for R1: commit `3573914` removed session ids, local scratchpad paths and a
  private project name from plans and ROUTES.md, and **kept the dates** — known positives and the
  provenance rule in one diff.
- `${CLAUDE_PLUGIN_ROOT}/…` paths are already used inside SKILL.md text (guardrails, council,
  handoff) → `/compound` can point at the lens instead of copying its taxonomy.

## Work in flight
- `feat/compounder-tuning` (other worktree, 333a0fc) touches `compounder/skills/review/SKILL.md`,
  `compounder/agents/adversarial-verifier.md`, `compounder/README.md` (scripts tree only),
  `compounder/.claude-plugin/plugin.json`, `ROUTES.md`, `AUTONOMY.md`.
- `fix/dispatch-cost-review` (5484cd9) bumps `plugin.json` to 2.6.1.
- This plan avoids `review/SKILL.md` and `adversarial-verifier.md` entirely. Accepted conflicts:
  `plugin.json` version line (resolve to the highest version at merge) and `compounder/README.md`
  line 26 (different hunk from the tuning branch's tree edit — expected clean).

## Inherited constraints (verbatim)
- `CLAUDE.md:36` — "Never write personal notes into tracked files. In a public repository `memory/` and
  `MEMORY.md` hold only the format examples; real memory lives in Claude's auto-memory
  outside the repository."
- `CLAUDE.md:39` — "Never `git push`, deploy, migration, or production operation without an explicit order in this session."
- `CLAUDE.md:40` — "Never report "done" without verification executed in this session (test, build, or real run)."
- `docs/templates/adr.md:20` — "an ADR is written when the decision is expensive to reverse or will generate "why did
  we do it this way?" in 6 months. A trivial decision doesn't become an ADR."

## Decisions
- **D1 — Where decisions live.** Winner: new `/compound` route → `docs/decisions/YYYY-MM-DD-<slug>.md`,
  form = project's `docs/templates/adr.md` when present, else a 4-heading inline format. Why: a
  plan's Decisions section dies with the feature; `refresh` never sweeps `docs/plans/`.
  Lost: dsh's proposed/implemented/rejected tree — proposals already live in plans, a lifecycle
  tree is the ceremony the compounder exists to avoid. Lost: leave decisions in plans — buried
  per feature, invisible to the next planner's grep.
- **D2 — Can a recorded decision be edited?** Winner: facts that moved (paths, names, keys) are
  updated in place; the decision itself never — a changed decision is a new record that
  supersedes, both cross-linked (dsh rule). `adr.md`'s comment gains that line. Lost: adr.md's
  current "never edited after acceptance" — an immutable record with dead paths fails `refresh`'s
  own "a library that lies is worse than an empty one".
- **D3 — Where the session-vantage taxonomy lives.** Winner: inline in the simplicity lens (item 7,
  ~10 lines); `/compound` points to it via `${CLAUDE_PLUGIN_ROOT}/agents/simplicity-reviewer.md`.
  Lost: a 5th review lens — edits `review/SKILL.md` (collides with the tuning branch) and adds a
  dispatch to every review. Lost: a separate reference file — one more file for ~10 lines.
- **D4 — Adapting dsh's resolvability test.** dsh: "could a reader at HEAD resolve every reference
  and verify every claim?" Compounder rules deliberately carry dated client incidents
  ("client 2026-08-21, PR #73") whose PR the public reader cannot open. Winner: **every claim must
  stand without opening the reference; an unresolvable citation is legal only as provenance
  (dated incident), never as the support of a claim** ("per decision 7", "see session X").
  Lost: dsh's literal test — it would flag every evolution log in the plugin.
- **D5 — Where R4 goes in guide 11.** Winner: new section "Writing model-facing text" before
  "Relation to the rest of the kit", one source line naming dsh's agent-experience skill, pointing
  to law 12 instead of restating "minimal context first". Lost: law 16 — misattributes the
  opten-mined list. Lost: guide 01 — about CLAUDE.md anatomy, not tool/skill descriptions.
- **D6 — Verifying edited agent/skill text.** The session's plugin registry is frozen at session
  start, so `compounder:*` agents run their old text. Winner: A/B with a fresh general-purpose
  subagent briefed with the OLD text vs the NEW text over the same fixture; the delta is the
  evidence. Lost: `claude plugin eval` — needs a new eval suite (machinery beyond scope). Lost:
  restart and re-dispatch — proves wiring that this plan does not change (agent names unchanged).
- **D7 — Version.** 2.7.0 (new behavior in `/compound`), bumped in the last unit. Lost: bump per
  unit — four conflicting bumps with no release in between.

## Implementation units

### U1: Calibrate the session-vantage test against this repository (risk spike)
- Files: read-only — tracked tree via `git grep`; calibration via `git show 3573914`.
- Change: draft the item-7 text (test per D4, classes, keep list) in the plan's "U1 result"
  section below. Classes to cover: session ids / local absolute paths / private project names
  (the 3573914 class, absent from dsh); dead session citations (`decision N`, `§N` of an
  uncommitted draft, phase codes); change narration ("used to", "no longer", "this PR");
  review choreography ("rejected in review"); reviewer-addressed justification; hedges with no
  marker. Keep list: dated incident anchors, evolution logs, issue/PR references inside
  incident anchors, measured bounds, runtime old/new states, external standards.
- Tests: battery over the tracked tree — `git grep -nE` for
  `[0-9a-f]{8}-[0-9a-f]{4}-`, `session [0-9a-f]{7,}`, `/private/tmp/`, `/Users/`,
  `\(decision [0-9]`, `used to`, `no longer`, `this PR`, `in review`. Judge every hit by D4.
- Verification: the draft classifies all removed lines of `3573914` as leaks and ≥5 sampled dated
  anchors from `compounder/skills/plan/SKILL.md` evolution log and `work/SKILL.md` as keeps.
  Red-proof: append a known positive to a scratch copy of one file → battery reports it.
  Fail-closed: `git grep` outside a repository errors (not "0 hits") — confirm once.
- Risk: real leaks in the current public tree. Listed under "U1 result → residuals", NOT fixed
  here (separate commit, own approval).
- Depends on: nothing.

### U2: Simplicity lens — item 7 (session vantage) and the R5c clause
- Files: `compounder/agents/simplicity-reviewer.md`
- Change: item 7 from U1's draft, return format unchanged (findings use the existing
  `[MEDIUM|MINOR] file:line` line). Item 5 gains: "a new public member on a SHARED module
  (service, registry, util) whose only caller is one consumer belongs to that consumer".
  Calibration section gains: dated incident anchors are not findings.
- Tests (fixture diff in the scratchpad): 2 leaks (a session id in a doc; "rejected in review"
  in a comment), 2 legal anchors ("client 2026-08-21: …" rule line; an evolution-log line), 1
  new public method on a shared util called from one place.
- Verification: D6 A/B — OLD text flags neither leak class nor the shared-module method (or only
  the method); NEW text flags both leaks + the method and does not flag either anchor.
- Depends on: U1.

### U3: Security lens — denial paths and alternate callers (R5b)
- Files: `compounder/agents/security-reviewer.md`
- Change: item 3 gains one sentence: follow each denial to the operation that executes it, and
  check alternate callers (CLI, job, internal call, another route) that reach that operation
  without passing the check.
- Tests (fixture): route handler checks ownership; the same delete function is also called from a
  CLI script with no check.
- Verification: D6 A/B — NEW text reports the CLI path with an attack line; record whether OLD
  text already did (if yes, the clause is redundant → drop it and say so).
- Depends on: nothing.

### U4: `/work` — filtered runs must show what they selected (R5a)
- Files: `compounder/skills/work/SKILL.md` (Step 2 bullet list, next to the go-RED rule)
- Change: one bullet: a run narrowed by file/name filter counts as evidence only after its
  report shows the expected tests were selected — a filter that matches nothing, or is silently
  ignored and runs everything, is not focused evidence. Runner-agnostic wording; no exit-code
  claims.
- Tests: premise check — `python3 -m pytest -k nomatch` on a one-test scratch file reports 0
  selected; record the literal output line.
- Verification: the premise output recorded; bullet reads without runner-specific claims.
- Depends on: nothing.

### U5: `/compound` — decision route, supersession at capture, vantage rule, refresh rubric
- Files: `compounder/skills/compound/SKILL.md`, `docs/templates/adr.md`, `compounder/README.md`
  (line 26 route list only)
- Change: (a) Step 3 row: decision expensive to reverse, with its rejected alternatives →
  `docs/decisions/YYYY-MM-DD-<slug>.md`; form per D1; value bar quotes adr.md:20.
  (b) Step 4: grep covers `docs/decisions/` too; a new lesson that contradicts or partly
  supersedes another record → in the same pass, retire it or cross-link both; never left for
  `refresh`. (c) Before writing: apply the session-vantage test
  (`${CLAUDE_PLUGIN_ROOT}/agents/simplicity-reviewer.md`, item 7). (d) `refresh`: classify each
  record by future value — keep while its rejected alternative is still tempting, or it states a
  negative guarantee, ownership boundary or reintroduction condition; update moved facts, never
  the decision (D2); archive when complete and no longer guiding; delete when it only recorded a
  mechanical change. Never by age or size. Archived records are history, never cited as a
  current rule. (e) adr.md comment: the D2 line. (f) README:26 mentions the decision route.
- Tests (fixture repo in the scratchpad): `docs/solutions/` with one dead-path doc and one
  mechanical-only doc; `docs/decisions/` with one decision whose rejected alternative is still
  tempting, one superseded by a newer record, one complete and no longer guiding. Capture
  scenario: a new lesson contradicting an existing solution doc.
- Verification: D6 A/B on `refresh` — NEW classifies all five as expected (keep / update+supersede
  link / archive / delete / dead-path update-or-retire); OLD only judges path existence. Capture
  scenario: NEW retires or cross-links the contradicted doc in the same pass.
- Risk: ceremony creep (decisions recorded for trivial choices) → value bar quoted verbatim.
- Depends on: U2 (item-7 anchor must exist before compound points at it).

### U6: Guide 11 — "Writing model-facing text" (R4)
- Files: `docs/mentor/11-convention-systems.md`
- Change: new section per D5, ≤8 bullets: say each fact once (tool vs system prompt vs parameter);
  delete constraints the model learns from the result; behavior not implementation; parameter
  rules on the parameter; bounded outputs with ids/paths to fetch more, truncation marked;
  saving context only counts if it causes no extra reads; measure first-turn tokens before/after
  (the repo's `compounder/scripts/count-tokens.sh` lands with the tuning branch — reference it
  only if merged by execution time, else name the API generically). Source line.
- Tests: none (prose).
- Verification: section does not restate law 12; heading "The fifteen laws" unchanged;
  session-vantage battery from U1 over the section is clean.
- Depends on: nothing.

### U7: Version, validation, dogfood
- Files: `compounder/.claude-plugin/plugin.json`
- Change: 2.6.0 → 2.7.0.
- Verification: `claude plugin validate compounder` passes; U1 battery over `git diff main` is
  clean (this plan included — it must cite the upstream URL+SHA, never a scratchpad path;
  hits on the battery's own pattern list, here and in item 7, are sanctioned keeps);
  `git diff main --stat` lists only the files named in U2–U7 plus this plan.
- Depends on: U2–U6.

Commits: one per unit, conventional, explicit `git add <file>`.

## U1 result
<!-- executor fills: final item-7 text, battery hits with verdicts, residual leaks found in the tree -->

## Regression checklist
- Plugin manifest: `claude plugin validate compounder` → passes (before and after).
- Plugin install from working tree: after merge, a fresh session lists `compounder:simplicity-reviewer`,
  `compounder:security-reviewer`, `/compounder:compound`, `/compounder:work` (registry reloads
  only in a new session).
- Site (`site/`, GitHub Pages workflow): untouched — `git diff main --stat -- site .github` empty.
- Kit docs links: `docs/templates/adr.md` and guide 11 still render; no other file links into the
  edited anchors (grep `simplicity-reviewer.md` / `adr.md` after the change).

## Pre-mortem
1. The lens floods reviews with false positives on dated anchors → U1 calibration + explicit keep
   list + U2 A/B on legal anchors.
2. `/compound` grows ceremony: decisions recorded for trivial choices → adr.md:20 value bar quoted
   verbatim in the route row.
3. A/B over briefed subagents proves the text, not the installed agent → accepted (D6); names and
   wiring unchanged; regression line 2 covers loading.
4. Merge friction with the tuning branch → accepted: plugin.json version line, README hunk.

## Out of scope
- Item 3 of the review (repeat-tool loop hook) — separate experiment.
- dsh machinery: note triplets, frozen archive manifest, format gates, i18n, stacked PRs.
- `.claude/commands/retro.md`, `compounder/skills/review/SKILL.md`, `adversarial-verifier.md`.
- Fixing leaks U1 finds in the existing tree (listed only).
- Push.

## Deferred to execution
- Whether OLD security-lens text already catches the alternate-caller case (U3 may drop its clause).
- Whether `count-tokens.sh` is on main by U6.

## Done
- R1, R2, R4, R5 each traced to a unit whose A/B or premise evidence is recorded in the commit
  body or the U1 result section.
- `claude plugin validate compounder` green; U1 battery clean over the diff; regression checklist
  lines 1, 3, 4 checked (line 2 after merge).
