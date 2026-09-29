---
stage: ready-made-plan
date: 2026-09-29
origin: orchestrator A/B series on `/compounder:review commit c8432b8` (series 1, 2026-09-22; series 2 clean room, 2026-09-29)
research: docs/plans/research/2026-09-29-compounder-tuning-brief.md
steering: docs/plans/2026-09-29-compounder-tuning-STEERING.md
branch: feat/compounder-tuning (stacked on fix/dispatch-cost-review)
---

# Compounder tuning — measure first, then fence, calibrate and prune

## Problem
Six review runs on one frozen commit showed where the plugin is fragile, not which model is best:
1. Two tribunal verifiers made real calls to the Anthropic API against the brief's instruction.
2. The `sonnet` alias moved from Sonnet 5 to Sonnet 5.5 (Claude Code 2.1.284) and nothing recorded it.
3. The same finding ("no tests") was rated SEVERE, MINOR, SEVERE ×3 and refuted, depending on the run.
4. Skills and agents were written for the previous model generation; nobody has measured what is now dead weight.
5. Run-to-run variance was larger than the orchestrator effect, so no change to the plugin can be judged by one run.

## Requirements
- **R1** A plugin reviewer or verifier cannot send data to an external host by accident, and the barrier ships with the plugin.
- **R2** Every dispatch log line carries the model id that actually ran, never an alias.
- **R3** Severity is assigned from a written rubric shared by panel, orchestrator and tribunal.
- **R4** Every prompt change to a skill or agent is accepted or rejected by a measured recall number on a frozen target, not by impression.
- **R5** The five defects still open on `fix/dispatch-cost-review` are closed.
- **R6** Defaults that depend on unmeasured claims (second panel pass, review orchestrator) change only after an isonomic retest.

## Assumptions (to confirm — see Handoff)
- **A1** (confirmed 2026-09-29) Work runs in a dedicated worktree on branch `feat/compounder-tuning`, stacked on `fix/dispatch-cost-review`; the primary checkout stays on `main`. The merge/push decision for the fix branch stays suspended with the user. Nothing here is merged or pushed without an explicit order.
- **A2** Threat model for R1 is the obedient agent making a mistake, not an adversary. A reviewer is not trying to exfiltrate; it reaches for the real script because the brief did not stop it.
- **A3** Budget for measurement runs is approved per batch, stated in USD at list price before each batch.
- **A4** The shipped plugin keeps `model: sonnet` (alias). The alias delivered Sonnet 5.5 for free.

## Verified by the planner (not taken from the dossiers)
| Claim | Check | Result |
|---|---|---|
| Deny list blocks `curl`, `wget`, `nc`, `gh api` | parsed `.claude/settings.json` | true, and the file is tracked in git |
| Verifiers reached the network | grepped Bash tool calls in the series 2 verifier transcripts | a verifier ran `count-tokens.sh` with `ANTHROPIC_API_KEY=dummy-not-real`; `curl` ran as a child of the script, so the prefix deny never matched |
| The fence ships with the plugin | listed `compounder/` and read `compounder/hooks/hooks.json` | false: the plugin ships one `UserPromptSubmit` hook and no permission rule; the deny list is project-local |
| Review skill has no rubric | read `compounder/skills/review/SKILL.md:26-37` | true: one corroboration rule, one tribunal gate, no criteria per level |
| Log records aliases | parsed `docs/pipeline/dispatches.jsonl` | lines 1–2 `sonnet`, lines 3–4 `claude-sonnet-5` |
| Alias pin variable | series 2 transcripts | `ANTHROPIC_DEFAULT_SONNET_MODEL` pinned subagents under Opus 5.5 and Fable 5.1, not under Sonnet 5.5 |

## Decisions

**D1 — Where the network fence lives.**
- (a) Instruction in the agent body. Lost: series 2 shows verifiers crossing an instruction; the kit's own rule is "the hard fence is tools + deny" (`ROUTES.md:74`).
- (b) More prefixes in the project deny list. Lost: not shipped with the plugin, and any wrapper script bypasses a prefix match.
- (c) Guard inside the scripts that talk to the network: `count-tokens.sh` refuses to send unless `COMPOUNDER_SEND=1` is set by the caller. Won for the known path: it travels with the plugin, costs five lines, and fails closed.
- (d) Per-agent `PreToolUse` hook (frontmatter `hooks`) that rejects Bash commands reaching for the network. Candidate for the general path; whether it fires for plugin subagents is unknown (docs silent) and is settled by U1.
- Chosen: (c) now, (d) if U1 proves it fires. (c) alone is accepted if (d) fails.

**D2 — How model identity is recorded.**
- (a) Pin full model ids in agent frontmatter. Lost: gives up free upgrades (A4).
- (b) Read the resolved id from the transcript's `usage` records, which `dispatch-cost.py` already does. Won: no new mechanism, the source is what actually ran.

**D3 — Where the rubric lives.**
- (a) Copy into each of the five agent files. Lost: five copies drift.
- (b) One section in `compounder/skills/review/SKILL.md`, injected by the orchestrator into every panel and tribunal brief. Won: single source, and the orchestrator applies the same text in Step 2.

**D4 — How a prompt change is judged.**
- (a) Read the diff and decide. Lost: variance between runs exceeded the effect of swapping the orchestrator.
- (b) Frozen target + golden list of known defects + recall per run, three runs per configuration. Won: it is the only option that separates a change from noise.

**D5 — Matching findings to the golden list.**
- (a) LLM judge. Lost for now: adds a model, a cost and its own variance to the instrument.
- (b) Deterministic anchors per defect (file, line range, keyword regex) plus a list of unmatched findings for manual adjudication. Won: reproducible; the unmatched list is how new defects enter the golden list.

## Implementation units

### U1: Probe which barriers stop a plugin subagent in Claude Code 2.1.284
- Files: `docs/plans/research/2026-09-29-fence-probes.md` (new), `compounder/agents/` (throwaway probe agent, deleted at the end of the unit)
- Change: a probe agent attempts six things against a local listener on `127.0.0.1` (never an external host): `curl` direct; `curl` inside a wrapper script; `python3 -c` with `urllib`; the same three with a frontmatter `hooks` PreToolUse guard; with `disallowedTools`; with a plugin-level `hooks.json` PreToolUse matcher. Record for each: blocked, prompted, or passed, and whether the hook input names the agent.
- Tests: none (spike). Output is the result table.
- Verification: the listener's access log is the ground truth. A row is "blocked" only if the log shows no request.
- Risk: the probe agent is cached by the session's plugin registry; run each configuration in a fresh session.
- Depends on: nothing

### U2: Frozen target, golden list and recall scorer
- Files: `compounder/scripts/review-recall.py` (new), `compounder/scripts/test_review_recall.py` (new), `docs/pipeline/golden/c8432b8.json` (new), `compounder/scripts/clean-room.sh` (new)
- Change: the golden file lists the 17 known defects of `c8432b8`, each with id, file, line range, keyword regex and weight. The scorer takes a session id, extracts the final report from the transcript, and prints matched ids, severity given, unmatched findings and recall. `clean-room.sh` rebuilds the isolated clone (`--no-local --single-branch`, remote removed) and prints the launch command with `CLAUDE_CODE_SUBAGENT_MODEL` set to a full id.
- Tests: scorer against the six existing transcripts reproduces the hand-scored table (12, 5, 8 for series 2); a report with no findings scores 0; a finding matching two golden ids counts once for each; a transcript with no report exits non-zero.
- Verification: `python3 compounder/scripts/test_review_recall.py`. Red-proof: delete one golden entry and the series 2 Sonnet 5.5 score must drop from 12. Fail-closed: a missing golden file or transcript is an error, never recall 0.
- Risk: keyword anchors too loose inflate recall. Mitigation: each anchor needs file match AND keyword match.
- Depends on: nothing

### U3: Network guard in the plugin's own scripts, plus the hook fence if U1 allows
- Files: `compounder/scripts/count-tokens.sh`, `compounder/scripts/test_count_tokens.sh`, `compounder/agents/*.md` (frontmatter only), `compounder/README.md`, `AUTONOMY.md`
- Change: `count-tokens.sh` exits 4 with a one-line reason unless `COMPOUNDER_SEND=1`. If U1 shows frontmatter hooks fire, the six Bash-holding agents get a PreToolUse guard script; the reason for the fence is written in `AUTONOMY.md` next to line 43.
- Tests: without the variable the stub curl is never invoked and exit is 4; with it, current behaviour is unchanged; key and body stay off argv (existing assertions).
- Verification: `bash compounder/scripts/test_count_tokens.sh`. Red-proof: remove the guard and the "never invoked" assertion fails. Fail-closed: variable set to anything other than `1` refuses.
- Risk: breaks the documented manual use in `ROUTES.md:53-54`. The unit updates that line.
- Depends on: U1

### U4: Resolved model and exact values in the dispatch log
- Files: `compounder/scripts/dispatch-cost.py`, `compounder/scripts/test_dispatch_cost.py`, `ROUTES.md`, `docs/pipeline/dispatches.jsonl`
- Change: `dispatch-cost.py --log-line` prints one ready-to-append JSON object per dispatch with the keys `ROUTES.md` documents and exact integers. `ROUTES.md` logging duty says `model` is the resolved id from that output. Lines 3–4 of the log are corrected to exact values (18000 → 17565, 2000 → 1587); lines 1–2 keep `sonnet` with a note, because the transcripts that could resolve them are from July and may be gone.
- Tests: `--log-line` key set equals the documented key set; values are integers equal to the transcript sums; model is the full id.
- Verification: unit tests, then `--log-line` on session `f803e4c4` compared by hand against `--json`. This unit changes a contract the docs describe, so it adds a test that parses the key list out of `ROUTES.md` and compares it with the script's output keys.
- Risk: editing a versioned log. The corrected lines are a data fix, recorded in the commit message.
- Depends on: nothing

### U5: Close the five defects open on the fix branch
- Files: `compounder/scripts/dispatch-cost.py`, `compounder/scripts/test_dispatch_cost.py`
- Change: zero-token `<synthetic>` records are excluded from turns and from miss detection; Fable 5 cache read is 1.00 and Fable 5.1 is 0.25, as separate rows; the tie test runs the script in subprocesses with `PYTHONHASHSEED` 0..9; a read drop counts as a miss only when the same turn's cache write rises.
- Tests: one failing test per defect first. Synthetic record between two 100k reads yields no miss; `price_for("claude-fable-5")` differs from `claude-fable-5-1`; ten seeds give one model; read 100k→30k with write 2k is not a miss, with write 100k it is.
- Verification: `python3 compounder/scripts/test_dispatch_cost.py`. Red-proof for the tie test: restore `max(set(models))` and at least one seed must fail.
- Risk: miss semantics change numbers already quoted in `ROUTES.md`. Re-run on the cited sessions and note any difference.
- Depends on: nothing (key names are U4)

### U6: Severity rubric in the review skill
- Files: `compounder/skills/review/SKILL.md`, `compounder/agents/adversarial-verifier.md`
- Change: a rubric section with criteria per level, written by consequence and reach: SEVERE = wrong result or exposure on the normal path; MEDIUM = real defect on a reachable but uncommon path; MINOR = latent, cosmetic or process gap. Absence of tests is a process gap: MINOR by default, MEDIUM when the repo's own rules require them. The orchestrator pastes the rubric into each brief and the verifier returns the level it would assign.
- Tests: none at code level (prompt text).
- Verification: three clean-room runs scored with U2. For golden defects found in two or more runs, the same level in at least 80% of cases. **Baseline, measured 2026-09-29 on the five runs with a final report: 25 of 40 placements, 62%** (`review-recall.py --agreement`).
- Risk: the rubric flattens everything to MEDIUM. The check reports the level distribution, not only agreement.
- Depends on: U2

### U7: Prompt audit of skills and agents
- Files: `compounder/skills/*/SKILL.md` (15), `compounder/agents/*.md` (7), `docs/plans/research/2026-09-29-prompt-audit.md` (new)
- Change: follow the audit procedure bundled with the `claude-api` skill (`prompt-audit`), targets Sonnet 5.5 for agents and Opus 5.5 for orchestration. Deliver the report and a proposed diff. Apply only the `review` skill and the five review agents in this plan, because they are the only ones U2 can measure.
- Tests: none at code level.
- Verification: three runs before, three after, same configuration. Accept when mean recall does not fall and the worst run does not fall. Otherwise revert that file.
- Risk: the recon found little legacy emphasis (one `NEVER`, one `ALWAYS`, one `MUST`), so the gain may be small. The unit states that outcome plainly if it happens.
- Depends on: U2, U6

### U8: Isonomic retest and the two defaults
- Files: `ROUTES.md`, `compounder/skills/review/SKILL.md`
- Change: three runs each for Sonnet 5.5, Opus 5.5 and Fable 5.1 as orchestrator, subagents pinned by full id. Then decide from the numbers: review orchestrator default, and whether a second panel pass becomes the default for commits flagged critical. Rewrite the 2026-09-22 note in `ROUTES.md`: the cost argument stays, "sees more" leaves.
- Tests: none.
- Verification: U2 recall table with mean and range per configuration. A default changes only if the means differ by two defects or more and the ranges do not overlap.
- Risk: nine runs. State the cost before starting (A3). The series 2 totals were about 1.2, 3.1 and 5.2 USD per run.
- Depends on: U2, U6, U7

## Discarded approaches
1. **Pin every agent to a full model id in the shipped plugin.** Dies: the alias is what delivered Sonnet 5.5, and the run with 5.5 reviewers found the most. The defect was the missing record, not the moving alias.
2. **Fence by instruction or by a longer deny list.** Dies on evidence: an instruction was crossed twice, and a prefix deny does not see `curl` inside a script. The deny list also stays in the project and never reaches plugin users.
3. **Tune the prompts by reading them, ship, and watch.** Dies: one run cannot tell an improvement from variance. The same model found the top defect in one series and missed it in the next.
4. **Replace panel and tribunal with a single stronger reviewer.** Dies: the union of runs found 17 where single runs found 5 to 12. Diversity is what the data rewards. Also untested and a far larger change.
5. **LLM judge for scoring.** Deferred, not rejected: adds variance to the measuring instrument before the instrument exists.

## Open questions (hypotheses, not units)
- Reviewer effort: Sonnet 5.5 runs at `medium` in Claude Code; `effort: high` in agent frontmatter may raise recall. Testable with U2 after U8.
- Security lens model: higher-risk cyber tasks on Sonnet 5.5 fall back to Sonnet 5. Whether the security reviewer triggers it is unknown.

## Regression checklist
| Output target | Proof it still answers |
|---|---|
| Plugin loads from a local clone | fresh session, `/plugin marketplace add` with the clone path, all 15 skills and 7 agents listed |
| `btw` hook | prompt starting with `btw` still injects the aside protocol; `compounder/hooks/hooks.json` parses as JSON |
| `/compounder:review` end to end | one clean-room run reaches the routed menu |
| Script suites | `python3 compounder/scripts/test_dispatch_cost.py`, `test_review_recall.py`, `bash compounder/scripts/test_count_tokens.sh` |
| `dispatch-cost.py` default table | run with no arguments in this repo, non-empty table, exit 0 |
| Site deploy | `git diff main --stat -- site/ .github/` is empty |
| Docs match the tree | file tree in `compounder/README.md` lists every file in `compounder/scripts/` |
| Plugin version | `compounder/.claude-plugin/plugin.json` bumped once, at the end |

## Pre-mortem
1. **The scorer measures its own anchors.** Loose regex inflates recall and every change looks fine. Mitigation: two-condition match, red-proof in U2, unmatched list reviewed by hand each batch.
2. **Variance swallows every comparison.** Three runs may not separate configurations. Mitigation: the acceptance rule is fixed before the runs; an inconclusive result keeps the current default and is written down as inconclusive.
3. **Claude Code changes under the plan.** Alias, hook fields and env variables moved once already. Mitigation: U1's probes stay as a re-runnable note; each batch records the CLI version.

## Deviations recorded during execution
- **U1** used a throwaway plugin in the session scratchpad, not a probe agent inside `compounder/agents/`. Nothing was added to the plugin. Probes ran headless; from here on runs are interactive (directive in STEERING).
- **U2** tests use inline report fixtures, not the local transcripts: a suite that depends on one machine's session files is not a suite. The real sessions were scored as a calibration step and recorded in the research note.
- **U2** gained `--agreement`, which U6 needs for its verification.
- **U3** delivered the script guard only. D1 option (d) changed shape after U1: the per-agent hook does not fire, and the plugin-level hook is session-wide. It waits for a scope decision.
- **U4 and U5** share one commit: both edit `dispatch-cost.py`.
- **Golden list** item G12 replaced "tie test cannot fail" (a defect of the fix branch, absent from the target commit) with "Fable cache read price".

## Out of scope
- Merging or pushing any branch; publishing a plugin release.
- Tuning skills other than `review` (the audit reports on all, applies to one).
- Comparing against non-Claude models.
- Changing the landing page under `site/`.

## Deferred to execution
- Which barrier actually blocks a plugin subagent (U1).
- Whether `CLAUDE_CODE_SUBAGENT_MODEL` pins subagents when the main model is Sonnet 5.5 (first clean-room run in U2).
- Whether the July transcripts still exist to resolve log lines 1–2 (U4).

## Done
- [x] U1 table written, with the listener log as evidence. (`docs/plans/research/2026-09-29-fence-probes.md`; one question left undetermined)
- [x] Scorer reproduces the hand-scored series 2 table; all script suites green. (12 and 5 reproduced; Fable 5.1 scored 11 once its run had finished. `docs/plans/research/2026-09-29-recall-calibration.md`)
- [x] `count-tokens.sh` refuses without `COMPOUNDER_SEND=1`, proven by test.
- [x] Every line appended to `docs/pipeline/dispatches.jsonl` from now on carries a full model id. (`--log-line`; contract test against `ROUTES.md`)
- [ ] Rubric in the skill; severity agreement measured before and after, both numbers in this file.
- [ ] Audit report delivered; each applied prompt change has a before and after recall.
- [ ] `ROUTES.md` note of 2026-09-22 rewritten from the retest numbers.
- [ ] Regression checklist run line by line against the baseline.
