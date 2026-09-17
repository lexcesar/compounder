# ROUTES.md — assembly line routing policy

The orchestrator (session model, full context) decides the route BEFORE dispatching work.
This file is the policy; it is alive — `/retro` corrects it with evidence from the dispatch log.

## Table rules
1. Maximum **6 task types**. Fine-grained taxonomy doesn't converge with few samples — to create
   a new type, merge two existing ones or prove ~10 dispatches that fit none.
2. Every cheap route has **mandatory QC** — the savings pay off at the gate, not on faith.
3. A route is a conscious decision: when torn between two, take the more expensive one. Dispatching
   too low costs rework; too high costs only tokens.
4. **Executor evidence is never final.** The envelope reports; the round that counts is QC's
   (the `adversarial-verifier` re-runs the verification on its own). The executor obeys plan
   text — trust in it comes from tool fencing, not faith in its report.
   Forensic fork audit: the transcript lives at
   `~/.claude/projects/<project>/<session-id>/subagents/agent-*.jsonl` and proves the model used,
   the prompt received (variables already expanded), and whether the return arrived verbatim. Agent
   type leaves NO record — to prove the fence, include a tool probe in the plan (e.g. "try
   WebFetch and report"): nonexistent = fence active.

## Route table

| Task type | Route | Model | Mandatory QC |
|---|---|---|---|
| Locate code (where is X, who calls Y, map an area) | `explorer` agent | haiku | orchestrator spot-checks a sample of the `file:line` results |
| Grounding research (pre-plan/brainstorm) | `compounder:researcher` agent | haiku | citations spot-checked by sample |
| Execute a ready-made plan (units with their own verification) | `/compounder:work-fork` skill | sonnet | `compounder:adversarial-verifier` over the envelope |
| Diff/branch review | `/compounder:review` (panel + tribunal) | session + sonnet panel | tribunal already built in |
| Check claims ("done", "passes", "no uses of Y") | `verifier` agent | sonnet | executed evidence is the QC itself |
| Mysterious bug, architecture, nebulous scope | **INLINE — never dispatch** | session | normal cycle |

[ADJUST: routes for personal/other-plugin agents — e.g. cavecrew-investigator in place of
explorer if the caveman plugin is installed.]

## Logging duty (the orchestrator's, right after each dispatch)
1-line append to `docs/pipeline/dispatches.jsonl`:

```json
{"date":"YYYY-MM-DD","session":"<short session id>","task":"1 sentence","type":"<from the table>","route":"<agent/skill>","model":"<used>","result":"complete|partial|blocked|refuted","rework":false,"notes":"optional"}
```

- Optional cost keys, taken from `compounder/scripts/dispatch-cost.py <session>` (reads the
  transcripts' `usage`; never estimates): `"tokens_in"`, `"tokens_cache_write"`,
  `"tokens_cache_read"`, `"tokens_out"`, `"usd_est"` (API list price; on a subscription it is the
  equivalent, not the bill). Its `turn1` column tells the route's true shape: `fresh` (system +
  brief), `fork:same-model` (parent cache re-read every turn), `fork:cross-model` (parent context
  rewritten at cache-write price — the expensive one). Size a brief or plan before dispatch with
  `compounder/scripts/count-tokens.sh --model <executor model> <file>`.
- `result` comes from the dispatchee's envelope/return; `refuted` = QC struck down the delivery.
- `rework: true` = the orchestrator (or a more expensive route) had to redo/complete it.
- Dispatch with no envelope/return = broken route: log it with `result:"blocked"` and say so in `notes`.
- Free-text fields (`task`/`notes`): never sensitive data — the file is versioned.

## Audit (via /retro)
- **Lesson trigger** (single address of this rule): `rework:true`, `result:"refuted"`
  or `result:"blocked"` → candidate lesson in `/retro`.
- **Model demotion:** same type with ≥2 reworks in the last ~10 dispatches → raise the
  route's model (cheap → sonnet → session) and record the change here with a date.
- **Savings promotion:** type with ~10 dispatches and no rework → try one step
  cheaper, keeping the QC.
- Route unused for ~5 retros → removal candidate (pruning).

## Evolution record
- 2026-07-21: creation — 6 types, fork route for ready-made plans (spike U1 of the plan
  `docs/plans/2026-07-21-assembly-line-plan.md`).
- 2026-07-21: post adversarial review — dedicated executor `fork-executor` (no WebFetch/Task),
  deny of network channels in settings.json, rule 4 (executor evidence is never final).
  Reason: the `ask` layer proved not to intercept subagents; the hard fence is tools + deny.
- 2026-07-21 (retro, session 45ed8dec): fork route leaves "experimental" — first real dispatch
  as a skill (line 2 of dispatches.jsonl): real fork, sonnet proven by transcript, verbatim
  envelope, tool fence confirmed by probe. Rule 4 gains the forensic audit technique.
