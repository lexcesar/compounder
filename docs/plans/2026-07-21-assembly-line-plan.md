---
stage: ready-made-plan
date: 2026-07-21
slug: assembly-line
---

# Audited assembly line — routing tasks by route/model with feedback

## Requirements (derived from the conversation)

- R1: The orchestrator (session model, full context) consults an **explicit routing policy**
  before dispatching work to a subagent/fork, instead of deciding ad hoc.
- R2: Every dispatch leaves an **auditable trail** (1 line in a structured log): route, model,
  result, rework.
- R3: `/retro` **mines the log** and proposes corrections to the policy — the route table is a
  living artifact, corrected by evidence, not frozen doctrine.
- R4: There is at least **one real cheap route** for heavy load: executing a ready-made plan in
  a subagent with a smaller model (`context: fork` + `model` in the skill's frontmatter).
- Declared assumptions: (a) the focus is token/context efficiency, not speed (stated by the
  user); (b) artifacts enter the kit as templates (with `[ADJUST]`), not just in personal use;
  (c) task taxonomy capped at ~6 types — low-volume statistics do not converge with a fine
  taxonomy.

## Reconnaissance (seen in this session)

- `compounder/skills/work/SKILL.md` — already has `mode:return` with a structured envelope
  (Step 4): it is the return contract a fork needs. Current frontmatter is minimal.
- `compounder/skills/lfg/SKILL.md` — the pipeline already dispatches `plan → work → simplify →
  review` with adversarial gates; it is the natural future consumer of the routes (out of scope here).
- `.claude/commands/retro.md` — Step 1 (harvest) and Step 3 (destination table) are the graft
  points; Step 5 (pruning) already covers the life cycle of the rules.
- `compounder/agents/` — researcher, 4 reviewers, adversarial-verifier: routes that already exist.
- Skill frontmatter supported (official doc, checked today): `context: fork`, `agent`,
  `model` (override only during the skill's execution), `effort`, `${CLAUDE_SKILL_DIR}`.
- `docs/pipeline/` and `ROUTES.md` do not exist — the names are free.

## Decisions

1. **Where the route policy lives.**
   - (a) A section in CLAUDE.md — always in context, but bloats every session and violates the
     rule "a line only gets in if it changes behavior".
   - (b) **`ROUTES.md` at the root (winner)** — same pattern as `AUTONOMY.md`: its own file,
     read on demand (new line in CLAUDE.md's "Read on demand" table), editable by
     `/retro` without touching CLAUDE.md.
   - (c) A `route` skill — rejected: routing is a consulted policy, not an invocable procedure.
2. **Log format.**
   - (a) Markdown table — readable, but concurrent appends and mining are worse.
   - (b) **JSONL in `docs/pipeline/dispatches.jsonl` (winner)** — append-only, `jq`/grep for
     mining, 1 line per dispatch.
3. **How the cheap route executes the `/work` protocol without duplicating the text.**
   - (a) Copy the skill body into the fork variant — rejected: two sources of truth diverge.
   - (b) **The fork reads the protocol from disk (winner)** — the `work-fork` body instructs:
     "read `${CLAUDE_SKILL_DIR}/../work/SKILL.md` and execute in `mode:return`".
4. **Who writes the log.** The orchestrator, by instruction in `ROUTES.md` itself (which it has
   just read in order to dispatch). Automatic hook rejected in THIS version: infra > discipline
   for validating the concept first (pre-mortem 1 covers the risk).

## Units

### U1: Spike — `work-fork` skill (the most dangerous assumption first)
- Files: `compounder/skills/work-fork/SKILL.md` (new)
- Change: frontmatter `context: fork`, `agent: general-purpose`, `model: sonnet`,
  `argument-hint: "[plan path]"`, `disable-model-invocation: true` (the route is the
  orchestrator's/user's decision, not auto-invocation). Short body: read
  `${CLAUDE_SKILL_DIR}/../work/SKILL.md`, execute the protocol in `mode:return` on the
  plan in `$ARGUMENTS`, return ONLY the Step 4 envelope.
- Tests: toy plan with 1 trivial unit (e.g.: create a file with fixed content +
  verification via `cat`) in a temporary `docs/plans/`.
- Verification: invoke `/compounder:work-fork <toy-plan>`; prove that (a) it ran in a
  subagent (the main context receives only the envelope), (b) the smaller model was used,
  (c) the envelope has STATUS/Units/Suite. Frontmatter field failing in the installed CLI
  version → record exactly which field and abort the dependent units (U2 switches the route
  to "manual Agent tool").
- Risk: `model`/`context` not supported in the local version; `${CLAUDE_SKILL_DIR}` not
  resolving inside a fork (deferred to execution).
- Depends on: nothing.

### U2: `ROUTES.md` — routing policy (kit template)
- Files: `ROUTES.md` (new, root), `CLAUDE.md` (1 line)
- Change: table with ≤6 task types → route → model → mandatory gate. Initial rows:
  locate code → `explorer`/haiku; execute ready-made plan → `work-fork` (U1);
  foundational research → `researcher`; review → panel + tribunal; mysterious bug →
  inline with the session model (never dispatch); `[ADJUST: personal agent routes]`. Every
  cheap route declares its QC (adversarial-verifier or executable verification). Sections:
  "Duty to log" (JSONL line format, when to record) and "Audit" (how `/retro` mines; model
  promotion/demotion rule by rework rate). In CLAUDE.md, a new line in the "Read on demand"
  table: "About to dispatch work to a subagent/fork | `ROUTES.md`".
- Tests: n/a (doc); litmus — every cited route exists (`compounder/agents/`, built-in agents,
  or U1).
- Verification: `grep` of the routes against `ls compounder/agents/` + the list of built-ins;
  CLAUDE.md diff of 1 line.
- Depends on: U1 (defines whether the ready-made-plan route is the fork or the fallback).

### U3: Dispatch log — schema + seed
- Files: `docs/pipeline/dispatches.jsonl` (new), schema documented inside `ROUTES.md` (U2)
- Change: fields `{"date","task","type","route","model","result","rework","notes"}`
  (`result`: complete|partial|blocked|refuted; `rework`: bool). Seed: the real line from
  U1's dispatch (the spike is the first audited record — immediate dogfood).
- Tests: n/a.
- Verification: `jq -c . docs/pipeline/dispatches.jsonl` parses every line without error.
- Depends on: U1 (generates the seed line), U2 (documented schema).

### U4: `/retro` mines dispatches
- Files: `.claude/commands/retro.md`
- Change: (a) Step 1 gains item 5 — "Dispatches: if `docs/pipeline/dispatches.jsonl` exists,
  read the session's lines; a route with `rework:true` or `refuted` becomes a candidate lesson";
  (b) Step 3's table gains a row — "Wrong route/model for the task type → `ROUTES.md`";
  (c) Step 5 (pruning) mentions routes: a route unused for ~5 retros → removal candidate.
- Tests: n/a (procedure doc).
- Verification: the diff shows the 3 grafts; a full read of retro.md confirms it does not
  contradict the existing steps.
- Depends on: U2, U3 (the cited file names must exist).

## Pre-mortem
If this fails, it will have been because:
1. **Nobody writes the log** (discipline, not automation). Mitigation: the duty to log lives in
   `ROUTES.md`, the file the orchestrator has just read in order to dispatch; if after ~3
   sessions the log is empty while dispatches happened → promote to a hook (phase 2, out of
   scope here).
2. **Taxonomy too fine, statistics never converge.** Mitigation: the 6-type cap written as a
   rule in `ROUTES.md` itself.
3. **Fork/model frontmatter does not work in the local CLI version.** Mitigation: U1 is a cheap
   spike and comes first; declared fallback (route via Agent tool with explicit `model`).

## Out of scope
- Automatic logging hooks; log dashboard/visualization.
- Changing `lfg`/`slfg` to use the routes (phase 2, after minimal statistics exist).
- Routing without a conscious orchestrator (auto-invocation of `work-fork` stays off).
- Routes for personal agents from outside the kit (cavecrew etc.) — they enter as `[ADJUST]`.

## Deferred to execution — resolved in the real test (2026-07-21, session 45ed8dec)
- Model alias in frontmatter: PROVEN — `model: sonnet` resolved to `claude-sonnet-5`
  (`model` field in the subagent's transcript).
- `${CLAUDE_SKILL_DIR}` in `context: fork`: PROVEN — substituted BEFORE the body reached the
  fork, expanding to the working-tree path (marketplace directory). The fork read the
  protocol via the variable's path; the relative fallback was never exercised and was pruned
  from the skill body. Note: the substitution also rewrites the fallback's guard text
  ("the literal text `${CLAUDE_SKILL_DIR}` appears above" becomes the expanded path),
  rendering it meaningless — one more reason for the pruning.
- Fork envelope: PROVEN intact — the final text of the fork's transcript is byte for byte
  equal to what the orchestrator received.

## Done
- [x] U1: fork executed the toy plan with a valid envelope and a smaller model — first via an
      equivalent simulation (Agent tool); then validated with the real `/compounder:work-fork`
      skill on 2026-07-21 (session 45ed8dec, plugin 1.1.1): real fork, sonnet proven, verbatim
      envelope, tools fence active (line 2 of dispatches.jsonl).
- [x] `ROUTES.md` at the root with ≤6 types, all pointing to existing agents (litmus via `ls`
      in the execution session, reconfirmed by the tests lens); pointer in CLAUDE.md.
- [x] `dispatches.jsonl` with ≥1 real line, `jq` parses (JQ_OK).
- [x] `retro.md` with harvest/destination/pruning aware of the log (3 grafts checked in review).
- [x] Suite/typecheck: n/a (the kit is pure markdown) — verification was each unit's litmus.
