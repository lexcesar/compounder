# Plan: <short title>
Date: YYYY-MM-DD | Goal/contract: docs/goals/ACTIVE.md (or the verbatim request)

## Verifiable goal
<1 sentence; how we'll know it's finished (command/observation)>

## Recon performed
<!-- Proof that the plan is against reality: -->
- Files opened: `path`, `path` ...
- What already exists and will be reused: <...>
- Who consumes what will change (callers): <...>
- Constraints inherited from docs (STEERING, older plans, CLAUDE.md): quoted verbatim, `path:line`, re-checked against the current default branch: <...>

## Options considered
- **Chosen:** <A — 1 sentence> because <...>
- Rejected: <B> — <why it lost>

## Steps
<!-- Order: riskiest assumption first; irreversible step (if any) last. -->
- [ ] 1. <change> in `file(s)` — verification: <command/observation> — risk: <...>
- [ ] 2. ...

## Pre-mortem
If this plan fails, it will have been because:
1. <likely cause> → mitigation: <...>
2. <...> → <...>
3. <...> → I accept the risk.

## Regression checklist
<!-- One line per OUTPUT TARGET the project ships (static build, SSR/preview function, CI
     workflow, deployed URL, feed/sitemap endpoints) — per target, never per feature. A gate
     that exercises one build mode is blind to the other. -->
- [ ] <target> — still answers: <command or request → expected result>

## Out of scope
- <what will NOT be done; note it if encountered>

## Done criteria
- [ ] <checkable>
- [ ] Suite + typecheck green (compared to baseline: <state>)
