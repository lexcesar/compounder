---
name: plan
description: Decide HOW to build — real code reconnaissance, compared options, units with their own verification. Use to plan implementation from requirements or a description.
argument-hint: "[requirements path | task description]"
---

# /plan — the HOW, against reality

Input: `$ARGUMENTS`

Central law: **a plan written before opening the files is fiction with numbered steps.**
If `docs/mentor/04-planning.md` exists in the project, it is the full doctrine; this skill is the
execution. Output: a plan an implementer (you tomorrow, or a Haiku) executes without guessing.

## Step 0 — Input and artifact
- Input is a doc with `stage: requirements` → you will ENRICH that file in place (one artifact
  per feature, requirements preserved at the top).
- Input is a loose description → create `docs/plans/YYYY-MM-DD-<slug>-plan.md`; derive minimal
  requirements (R1..Rn) from the description and declare assumptions. Ambiguity that changes the
  outcome → ask (one round, with recommendations) — except in a pipeline call (lfg/slfg): assume
  the reasonable thing and record it under "Assumptions".
- Trivial task (1–2 files, obvious path)? Say a formal plan is overhead and propose executing
  directly with a 5-line plan in the chat.

## Step 1 — Reconnaissance (the step that separates a plan from fiction)
1. OPEN the files that will be touched (small area) or dispatch 1 `researcher` (broad area).
   Researcher ran → persist its dossier verbatim at `docs/plans/research/<same-slug>-brief.md`
   and cite it in the plan: the executor reads the brief instead of re-exploring, and the
   dossier survives the session that produced it.
2. Grep the CONSUMERS of what will change — the surprise lives in the callers.
3. What already exists worth reusing? (a utility, a pattern, a model test to imitate)
4. Institutional memory: grep `docs/solutions/` for terms from the area; `CONCEPTS.md` for vocabulary.
5. **External knowledge:** an option that introduces an attribute/API/lib the repo has never used →
   read ITS official docs and check platform support (caniuse, version matrix) BEFORE proposing.
   An empirical test in one environment only proves that environment; the docs are what tell you
   where the option breaks.
6. **Work in flight:** open branches/PRs touching the same files (`git fetch` + `gh pr list`).
   Conflict in sight → declare the sequencing in the plan ("start after X merges" or "I accept
   resolving the conflict") and note that line anchors may shift by execution time.
**Litmus before proceeding:** every file the plan will cite was seen THIS session (by you or via
the researcher's dossier, with a sample checked).

## Step 2 — Decisions
For each non-obvious decision: ≥2 options, 1 sentence each, winner + why, loser + why.
Paste it into the plan ("Decisions" section). A decision with no recorded alternative = a reflex,
not a choice.

## Step 3 — Implementation units
Break it into U1..Un, each one deliverable and verifiable on its own:
```markdown
### U<N>: <what changes, in 1 sentence>
- Files: `path`, `path` (real, seen during reconnaissance)
- Change: <2–4 lines of intent — decisions, not finished code>
- Tests: <enumerated scenarios — the implementer does not invent coverage>
- Verification: <command/observation that proves THIS unit; unit creates a check (test/gate/
  probe) → name its red-proof: which mutation must make it fail>
- Risk: <what can go wrong here, if relevant>
- Depends on: <U<M> | nothing>
```
Order by RISK: the most dangerous assumption becomes U1 (a cheap spike that can invalidate the rest).
Irreversible step (migration, public contract): as late as possible, with a checkpoint before it.

## Step 4 — Armor
At the end of the file:
- **Pre-mortem:** "if this fails, it will have been because: 1) 2) 3)" + mitigation or "accepted".
- **Out of scope:** what does NOT go in (inherit the non-goals from the requirements).
- **Deferred to execution:** questions only running code can answer — named, not hidden.
- **Done:** final checkable criteria + "suite and typecheck green against the baseline".
Update the frontmatter: `stage: ready-made-plan`.

## Step 4b — Multi-session? Add a STEERING channel
Execution will span sessions, another agent, or a supervised external executor → create
`docs/plans/<same-slug>-STEERING.md` next to the plan and cite it in the plan header:
```markdown
# STEERING — <plan>
Async supervisor↔executor channel. Executor: re-read before EVERY unit and EVERY commit.
Concurrency: `git pull --rebase` before editing this file; each side touches only its own
sections — a stale-copy commit deletes the other side's newest lines.
## Active directives    <!-- supervisor writes, newest on top, binding -->
## Questions for supervisor    <!-- executor appends the blocker, takes the next independent unit — never waits -->
## Execution log    <!-- executor appends, in the same commit as the unit; a unit without its line counts as not done -->
Line: `YYYY-MM-DD HH:MM · U<N> · done|partial|dropped · <SHA> — <note>`
The note carries what the diff doesn't show: deviation from a directive (allowed — silent
deviation is not), findings outside the unit, what was deliberately left open, next unit.
```

## Step 5 — Quality gate (self-applied before delivering)
- [ ] Every unit has its own verification and real files.
- [ ] Test scenarios enumerated in the units that carry behavior.
- [ ] Decisions have a recorded rejected alternative.
- [ ] No absolute paths (always relative to the repo).
Any ❌ → fix it before showing.

## Step 6 — Handoff (routed menu)
Summary in the chat: goal, number of units, U1 (the risk spike), key decisions. Close with a
numbered menu where every option is an executable ACTION (whoever answers "1" has already
triggered work):
```
Plan ready at <path>. Next step?
1. /work <path> — implement now
2. /lfg <path> — autonomous to the end (gates preserved: commit/push only with your go)
3. Walkthrough — decide unit by unit with me
4. Adjust the plan — tell me what
```
Recommend ONE option with the why tied to the context ("1-file fix → option 1 is the most direct
path"). The autonomous option always declares the fence along with the engine.
(In a pipeline: return the path and stop — menus are for humans.)

## Evolution log
- 2026-08-13: persisted research brief (`docs/plans/research/`) and STEERING channel for
  multi-session plans, adopted from an audited external assembly line (client): the dossier
  died with the planning session, and cross-session execution had no directive/question/log
  channel — blockers meant waiting instead of taking the next independent unit.
- 2026-08-13: units that create checks must name their red-proof (with /work's prove-it-can-fail
  rule). Case: a parity gate in another project ran green while measuring nothing — dark-theme
  screenshots silently rendered light, caught only because light and dark baselines had identical
  checksums.
- 2026-07-13: added the "External knowledge" recon (official docs + platform support).
  Case: `hx-preserve` chosen and validated empirically in Chromium; the official htmx docs already
  said text input is not preservable — it broke on Safari, caught only in adversarial review.
