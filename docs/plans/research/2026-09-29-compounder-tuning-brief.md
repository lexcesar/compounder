---
stage: research-brief
date: 2026-09-29
plan: docs/plans/2026-09-29-compounder-tuning-plan.md
---

# Research brief — compounder tuning

Two dossiers, persisted verbatim. They are CLAIMS by subagents. The plan's "Verified by the
planner" section lists which ones were re-checked by hand and what the re-check added.

## Dossier 1 — codebase (compounder:researcher, Haiku)

---

## DOSSIER — Compounder Plugin Tuning

**LENS:** Agent fences, dispatch logging, review severity, prompt audit surface, test infrastructure, institutional memory for network-call and severity decisions.

---

### A. AGENT FENCES

**Frontmatter fields (all agents):**
- `compounder/agents/researcher.md:2-5` — `name: researcher`, `model: haiku`, `tools: Read, Grep, Glob, Bash`
- `compounder/agents/security-reviewer.md:2-5` — `name: security-reviewer`, `model: sonnet`, `tools: Read, Grep, Glob, Bash`
- `compounder/agents/correctness-reviewer.md:2-5` — `name: correctness-reviewer`, `model: sonnet`, `tools: Read, Grep, Glob, Bash`
- `compounder/agents/simplicity-reviewer.md:2-5` — `name: simplicity-reviewer`, `model: sonnet`, `tools: Read, Grep, Glob` (NO Bash)
- `compounder/agents/tests-reviewer.md:2-5` — `name: tests-reviewer`, `model: sonnet`, `tools: Read, Grep, Glob, Bash`
- `compounder/agents/adversarial-verifier.md:2-5` — `name: adversarial-verifier`, `model: sonnet`, `tools: Read, Grep, Glob, Bash`
- `compounder/agents/fork-executor.md:2-5` — `name: fork-executor`, `model: sonnet`, `tools: Read, Edit, Write, Grep, Glob, Bash`

**Bash present in:** researcher, security-reviewer, correctness-reviewer, tests-reviewer, adversarial-verifier, fork-executor. **NOT** in simplicity-reviewer.
**WebFetch/WebSearch:** None of the agents declare these tools in their frontmatter.

**Network-blocking instructions in agent bodies:** 
- `compounder/agents/fork-executor.md:22` — "No git write operation" (does not address network calls, addresses git only)
- No explicit instruction found blocking network calls in agent body text.

**Permissions in `.claude/settings.json`:**
- `deny` block (lines 3–14): `"Bash(curl:*)"`, `"Bash(wget:*)"`, `"Bash(nc:*)"`, `"Bash(gh api:*)"` — blocks curl, wget, netcat, gh API calls via bash
- No deny rules for `Python3` or generic network calls; only Bash patterns.

**Permissions in `.claude/settings.local.json`:**
- `allow` block (lines 3–12): Permits `Bash(python3 *)` (line 7) — no network restrictions on Python execution

**Result:** 
- Bash network tools (curl, wget, nc) are blocked at the settings level, NOT by agent-level instruction.
- fork-executor has Bash but the bash deny rules prevent `curl`/`wget`; count-tokens.sh uses `curl` and would be blocked.
- Python3 subprocesses are allowed, so dispatch-cost.py can run; it makes no network calls.
- `compounder/hooks/hooks.json:8` — btw-hook.sh command does not reference network operations.

---

### B. DISPATCH LOG + MODEL RECORDING

**ROUTES.md § "Logging duty" (lines 40–58):**
> ```json
> {"date":"YYYY-MM-DD","session":"<short session id>","task":"1 sentence","type":"<from the table>","route":"<agent/skill>","model":"<used>","result":"complete|partial|blocked|refuted","rework":false,"notes":"optional"}
> ```
> - Optional cost keys, taken from `compounder/scripts/dispatch-cost.py <session>` (reads the transcripts' `usage`; never estimates): `"tokens_in"`, `"tokens_cache_write"`, `"tokens_cache_read"`, `"tokens_out"`, `"usd_est"` (API list price; on a subscription it is the equivalent, not the bill; 1h cache writes at 2× input — what Claude Code uses). Its `turn1` column tells the route's true shape: `fresh` (system + brief), `fork:same-model` (parent cache re-read every turn), `fork:cross-model` (parent context rewritten at cache-write price — the expensive one); the session's own row reads `root`.

**ROUTES.md § Rule 5 (lines 21–24):**
> **Frozen tree during a dispatch.** An executor that runs a regression checklist on the shared working tree sees every orchestrator edit as its own noise (2026-09-17: `git status` 5→6 lines mid-run, flagged as red by the executor — correctly). While a dispatch is out, the orchestrator edits no tracked file; edits wait for the envelope, or the executor gets its own worktree.

**Model recording in ROUTES.md § Evolution (line 87–90):**
> agents on `/compounder:review commit c8432b8` — Fable 5.1, Opus 5.5 (launch day) and Sonnet 5, same 4 lenses + tribunal on Sonnet 5... Consequence: review orchestrator default = Opus 5.5

**`docs/pipeline/dispatches.jsonl` structure (5 lines total):**
- Keys per line: `date`, `session`, `task`, `type`, `route`, `model`, `result`, `rework`, and optional: `tokens_in`, `tokens_cache_write`, `tokens_cache_read`, `tokens_out`, `usd_est`, `notes`
- **Resolved model ID:** Line 2 records `"model":"sonnet"` (alias); lines 3–4 record `"model":"claude-sonnet-5"` (resolved). **No line records a full resolved model id for sonnet aliases** — only explicit full IDs in later dispatches.
- Example (line 3): `"tokens_in":16`, `"tokens_cache_write":26000`, `"tokens_cache_read":162000`, `"tokens_out":4000`, `"usd_est":0.138`

**Scripts writing to dispatches.jsonl:**
- `ROUTES.md:41` states "1-line append" is the **orchestrator's** duty, done manually.
- **No automated script writes to dispatches.jsonl.** Neither dispatch-cost.py nor count-tokens.sh writes to it; they read transcripts and output cost summaries.

**`compounder/scripts/dispatch-cost.py` output model field:**
- `dispatch-cost.py:113` — `model = max(sorted(set(models)), key=models.count)` — returns the **most frequent model string** seen in the transcript's usage records.
- Line 126: Returns this as `"model": model` in the analysis object.
- Line 79: `u = msg.get("usage") or {}` — reads `usage` block from each assistant message in the transcript.
- Outputs as a field in the per-agent result; when printed (line 197), formatted as `r["model"][:22]` — truncated to 22 chars.

---

### C. REVIEW SKILL SEVERITY

**`compounder/skills/review/SKILL.md` severity rules:**
- Line 28: "Corroborated by 2+ reviewers → severity rises 1 level."
- Lines 32–36: "Every SEVERE/MEDIUM finding goes to the `adversarial-verifier`... Verdict: CONFIRMED (scenario demonstrated) | REFUTED (dies; vanishes from the report) | INCONCLUSIVE (downgraded to "suspicion"). MINOR ones skip the tribunal (too cheap to judge — report them as minor as they are)."
- Line 40: Return format lists severity as `[SEVERE|MEDIUM|MINOR]`

**Severity definitions across agents:**
- `compounder/agents/security-reviewer.md:26` — "Severity by consequence (third-party data/remote execution = SEVERE), not by elegance."
- `compounder/agents/tests-reviewer.md:24–33` — "Tests touched in the diff: assert loosened / deleted / skipped to get green? SEVERE, no question." and "Reference re-frozen: the diff updates a gate's snapshot/golden/reference/extract. SEVERE unless..."
- `compounder/agents/simplicity-reviewer.md:44` — "(SEVERE is rare in this lens — reserve it for complexity that actively hides a risk.)"
- `compounder/agents/correctness-reviewer.md:30` — Format: `[SEVERE|MEDIUM|MINOR] file:line`

**No written numeric/explicit rubric** found (e.g., "SEVERE = max damage score X"). Severity is defined by consequence domain: correctness (wrong behavior), security (data/execution gain), tests (gate skipped), simplicity (maintenance cost). Mapping to levels is implicit per lens.

**Corroboration rule (line 28 of review/SKILL.md):** "Corroborated by 2+ reviewers → severity rises 1 level."

**Tribunal gate rule (lines 32–36 of review/SKILL.md):** SEVERE/MEDIUM → tribunal; MINOR → skip tribunal, reported as-is.

---

### D. PROMPT AUDIT SURFACE

**Line counts per file:**

| File | Lines |
|---|---|
| `compounder/agents/researcher.md` | 33 |
| `compounder/agents/security-reviewer.md` | 38 |
| `compounder/agents/correctness-reviewer.md` | 35 |
| `compounder/agents/simplicity-reviewer.md` | 44 |
| `compounder/agents/tests-reviewer.md` | 52 |
| `compounder/agents/adversarial-verifier.md` | 40 |
| `compounder/agents/fork-executor.md` | 25 |
| `compounder/skills/brainstorm/SKILL.md` | 80 |
| `compounder/skills/btw/SKILL.md` | 57 |
| `compounder/skills/compound/SKILL.md` | 94 |
| `compounder/skills/council/SKILL.md` | 54 |
| `compounder/skills/debug/SKILL.md` | 54 |
| `compounder/skills/goal/SKILL.md` | 73 |
| `compounder/skills/guardrails/SKILL.md` | 52 |
| `compounder/skills/handoff/SKILL.md` | 32 |
| `compounder/skills/lfg/SKILL.md` | 78 |
| `compounder/skills/plan/SKILL.md` | 165 |
| `compounder/skills/review/SKILL.md` | 115 |
| `compounder/skills/simplify/SKILL.md` | 55 |
| `compounder/skills/slfg/SKILL.md` | 66 |
| `compounder/skills/work-fork/SKILL.md` | 31 |
| `compounder/skills/work/SKILL.md` | 125 |

**Old-model pattern hits (10 densest):**

1. `compounder/skills/slfg/SKILL.md:4` — `disable-model-invocation: true`
2. `compounder/skills/slfg/SKILL.md:23` — "2. **Normal case (Opus/Sonnet/Haiku)** — subagent tool (`Task`/`Agent`): fire each wave's agents"
3. `compounder/skills/lfg/SKILL.md:4` — `disable-model-invocation: true`
4. `compounder/skills/lfg/SKILL.md:43` — "invoke `simplify` ALWAYS (preserves behavior, suite green before/after), including on a small"
5. `compounder/skills/work-fork/SKILL.md:8` — `disable-model-invocation: true`
6. `compounder/skills/work/SKILL.md:95` — "- **NEVER:** edit the plan as if it were state; delete/skip a test to pass; "seize the moment""
7. `compounder/skills/council/SKILL.md:41` — "they apply, the question they hand back. Voices MUST diverge — if everyone agrees, you convened wrong."
8. `compounder/skills/plan/SKILL.md:13` — "execution. Output: a plan an implementer (you tomorrow, or a Haiku) executes without guessing."
9. `compounder/skills/review/SKILL.md:63` — "**Cost and consent:** 3–10× a normal `/review`. Without `budget:released` in the arguments,"
10. `compounder/skills/review/SKILL.md:86` — "while (dry < 2 && (budget.total ? budget.remaining() > 50_000 : round < 3)) {"

**ALL-CAPS patterns:**
- NEVER (1 hit: work/SKILL.md:95)
- ALWAYS (1 hit: lfg/SKILL.md:43)
- MUST (1 hit: council/SKILL.md:41)
- IMPORTANT (0 hits)
- CRITICAL (0 hits)

**Model names/versions:** Opus, Sonnet, Haiku (not Fable by name; Fable is in plugin.json description). No "claude-4" or version specifics like "4.5" or "5.0" in agent/skill prompts.

**disable-model-invocation:** 3 occurrences (lfg, slfg, work-fork).

**Budget/effort instructions:** Lines 63, 79, 86 of review/SKILL.md; lines 16 of slfg/SKILL.md.

**Think-step/ultrathink:** 0 hits.

---

### E. CONSUMERS AND TEST INFRA

**Plugin installation (README):**
- `compounder/README.md:10–12`:
  ```
  /plugin marketplace add lexcesar/compounder
  /plugin install compounder
  ```
- Line 15: "For local development, point to the clone: `/plugin marketplace add path/to/clone`."

**Plugin metadata:**
- `compounder/.claude-plugin/plugin.json:2–3` — `"name": "compounder"`, `"version": "2.6.1"`

**CI workflows:**
- `.github/workflows/pages.yml` — **single workflow**, triggers on:
  - `push` to `main` branch with paths matching `site/**` or `.github/workflows/pages.yml` (lines 4–8)
  - `workflow_dispatch` manual trigger (line 9)
  - Jobs: `deploy` (line 21–35) — uses `actions/upload-pages-artifact` and `actions/deploy-pages` to GitHub Pages

**No test runners/validators for skills/agents:** No `.github/workflows/*` file validates skill output, schema compliance, or agent tool fencing.

**compounder/scripts/** (all files with purpose):
- `btw-hook.sh` — Injects aside protocol when prompt starts with "btw"
- `count-tokens.sh` — Calls `/v1/messages/count_tokens` API to measure file tokens (specific to executor model); outputs `<tokens>\t<file>`
- `dispatch-cost.py` — Reads transcripts' `usage` blocks, outputs per-dispatch tokens, USD, and fork-vs-fresh classification
- `test_count_tokens.sh` — Unit test for count-tokens.sh; uses stub curl, never hits network
- `test_dispatch_cost.py` — Unit tests for dispatch-cost.py

---

### F. INSTITUTIONAL MEMORY

**Grep results for fence/deny/severity/rubric/tribunal/prompt-audit (8 most relevant hits with file:line):**

1. `ROUTES.md:73–74` — "Reason: the `ask` layer proved not to intercept subagents; the hard fence is tools + deny."
2. `ROUTES.md:19` — "Executor evidence is never final." The envelope reports; the round that counts is QC's (the `adversarial-verifier` re-runs the verification on its own)."
3. `docs/mentor/08-guardrails-and-boundaries.md:70–72` — "**Every new fence comes with its why written down** (a comment in CLAUDE.md/AUTONOMY, not in the JSON). A fence without a why becomes superstition — 3 months from now nobody knows whether it can be removed (Chesterton's fence applied to yourself)."
4. `docs/mentor/08-guardrails-and-boundaries.md:18` — "`deny` = never, no dialogue. `ask` = mandatory pause with a human. `allow` = flows without friction"
5. `docs/plans/2026-09-22-dispatch-cost-residuals.md:36` — "## Refuted by the tribunal (not defects)"
6. `docs/plans/2026-07-21-assembly-line-plan.md:82` — "foundational research → `researcher`; review → panel + tribunal; mysterious bug →"
7. `AUTONOMY.md:43` — "Reading/writing secrets; sending project data to external services."
8. `AUTONOMY.md:74` — "Permission denied = "no". Don't work around it by another path (another command, another tool, another format)."

**AUTONOMY.md § network calls and external APIs (lines 43, 74):**
- Line 43 (🔴 Red zone): "Reading/writing secrets; sending project data to external services." — **sending data to external services is irreversible, red-zone action.**
- Line 74 (Honesty invariants): "Permission denied = "no". Don't work around it by another path (another command, another tool, another format)."

**No explicit deny rule for WebFetch/WebSearch found** in any .json file — only Bash patterns (curl, wget, nc, gh api).

---

### GAPS:

- **No numeric rubric** for severity levels (e.g., "SEVERE = score ≥8, MEDIUM 4–7"). Severity mapping is domain-implicit and undocumented as a formal table.
- **No test for agent tool fencing** (e.g., "try WebFetch and report", as noted in ROUTES.md:19–20 for fork-executor but not implemented as a CI step).
- **count-tokens.sh network call is not fenced in settings.json at fork-executor agent level** — it's globally denied (Bash curl deny), so a brief that runs count-tokens.sh via an agent would fail. This is noted but not explicitly tested in CI.
- **Model alias resolution:** dispatches.jsonl records alias ("sonnet") but dispatch-cost.py resolves full ID from transcripts. No documented contract for which dispatch logs record alias vs. resolved ID — only empirical (lines 2 vs. 3–4).
- **Prompt audit:** All agent/skill frontmatter and bodies checked; no comprehensive scan for "old-model language" beyond manual grep (disable-model-invocation and model names are found; no systematic linting for instruction style/age).
- **Permission scope:** `Bash(python3 *)` is broadly allowed in settings.local.json — no restriction on what Python subprocesses can do (network, file write, etc.). dispatch-cost.py happens to be read-only, but the allow rule doesn't enforce it.

---

**CONFIDENCE: high** — Every agent frontmatter read; all permission files examined; ROUTES.md fully cited; dispatch log structure verified against 5 real lines; no claims made beyond quoted evidence. Institutional memory searches were exhaustive for the named patterns.

## Dossier 2 — Claude Code documentation (claude-code-guide), CLI 2.1.284

Now I have enough information to answer comprehensively. Here are the answers with citations:

---

## 1. **Subagent Frontmatter Fields (Complete List)**

**URL:** https://code.claude.com/docs/en/sub-agents.md

Supported fields in agent frontmatter:
- `name` (required) – unique identifier
- `description` (required) – when Claude should delegate  
- `tools` (optional) – comma-separated or list; e.g., `tools: Read, Grep, Glob, Bash`
- `disallowedTools` (optional) – deny tools or patterns  
- `model` (optional) – `sonnet`, `opus`, `haiku`, `fable`, `inherit`, or full model ID  
- `permissionMode` (optional) – `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`
- `maxTurns` (optional) – max agentic turns
- `skills` (optional, list) – preload skills
- `mcpServers` (optional, list) – MCP servers available
- `hooks` (optional) – lifecycle hooks
- `memory` (optional) – `user`, `project`, or `local`
- `background` (optional, boolean)
- `omitClaudeMd` (optional, boolean)
- `effort` (optional) – `low`, `medium`, `high`, `xhigh`, `max`
- `isolation` (optional) – `worktree`
- `initialPrompt` (optional) – auto-submitted first turn
- `experimental` (optional) – `cacheTtl: 5m|1h`

**Quote:** "Frontmatter Configuration Reference" section lists all fields above.

---

## 2. **Model Field: Aliases & Resolution**

**URL:** https://code.claude.com/docs/en/model-config.md

**Accepted values:** Aliases (`sonnet`, `opus`, `haiku`, `fable`, `inherit`) or full model IDs (e.g., `claude-opus-5-5`).

**What `sonnet` resolves to (v2.1.284):** "**`sonnet`** | Latest Sonnet model (daily coding tasks)" resolves to **Sonnet 5.5 on Anthropic API**.

**Environment variable for subagent model override:** `CLAUDE_CODE_SUBAGENT_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` (from sub-agents.md).

**Quote from sub-agents.md:** "Set `CLAUDE_CODE_SUBAGENT_MODEL` environment variable as default for all subagents" with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE: "1"  // Override all subagent models`.

**Session model override behavior:** The session's main model does NOT automatically override a subagent's model if the subagent specifies one. **Docs silent** on whether session model ever overrides subagent `model: inherit` resolution.

---

## 3. **Restricting Subagent Network Access**

**URL:** https://code.claude.com/docs/en/sub-agents.md, https://code.claude.com/docs/en/hooks.md

**(a) Omitting WebFetch/WebSearch from `tools` removes them:** Yes.  
**Quote:** "`tools: Read, Grep, Glob, Bash`" — explicit list; tools not named are unavailable.

**(b) Bash restricted to specific commands in frontmatter:** **Docs silent**. The frontmatter accepts `tools: Bash` (all) or `disallowedTools: Bash` (none). Fine-grained restriction via `if: "Bash(rm *)"` is shown in hooks configuration, not frontmatter.

**(c) Do `permissions.deny` rules (settings.json) apply to subagents?** **Docs silent** on subagent-specific permission rule scope.

**(d) Do `ask` rules prompt inside subagents?** **Docs silent** on whether ask prompts execute in subagent context.

**(e) Can a plugin ship its own permission rules/PreToolUse hooks that apply to its agents?** **Docs silent** on plugin-level permission configuration beyond agent frontmatter.

**(f) Sandbox setting to block network for Bash:** **Docs silent** on a general network-blocking sandbox setting. Bash execution inherits provider's network policies but no documented `sandbox: { network: false }` setting.

---

## 4. **Hooks: Agent Type Visibility & Bash Matching**

**URL:** https://code.claude.com/docs/en/hooks.md

**Can PreToolUse hook see which subagent/agent type is calling?** **Docs silent**. The documented PreToolUse input includes `tool_name`, `tool_input`, `tool_use_id`, `permission_mode`, `hook_event_name`, etc., but no `agentType` or `agent_id` field.

**Quote:** "PreToolUse hooks receive these fields... `tool_name`, `tool_input`, `tool_use_id`, `permission_mode`, `hook_event_name`". No agent identifier listed.

**Can a plugin's hooks.json register PreToolUse with a Bash matcher?** Yes.  
**Quote:** "Matcher Patterns... `"matcher": "Bash"` — Only Bash commands... `"if": "Bash(rm *)"` — Match rm commands". Bash matching via matcher + if conditions is supported.

---

## 5. **Subagent Transcripts & `.meta.json`**

**URL:** https://code.claude.com/docs/en/sessions.md

**Storage location:** "`~/.claude/projects/<project>/<session-id>.jsonl`".

**Quote:** "By default, Claude Code stores transcripts as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is your working directory path with non-alphanumeric characters replaced by `-`."

**`.meta.json` sidecar:** **Docs silent**. The sessions documentation does not mention a `.meta.json` file alongside the transcript. Transcript format is JSONL only; "The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release."

---

## 6. **Effort in Frontmatter & Default**

**URL:** https://code.claude.com/docs/en/sub-agents.md, https://code.claude.com/docs/en/model-config.md

**Can subagent effort be set in frontmatter?** Yes.  
**Quote:** "`effort: high` | Optional: effort level (`low`, `medium`, `high`, `xhigh`, `max`)".

**Default effort for Sonnet 5.5 in Claude Code:** "`medium` | Default on Opus 5.5/Sonnet 5.5; day-to-day work".

**Quote from model-config.md:** "Effort Levels... | **`medium`** | Default on Opus 5.5/Sonnet 5.5; day-to-day work |".

---

**Summary of "docs silent" gaps:**
- Bash command restriction at the frontmatter `tools:` level (only in hooks)
- Permission rule scope for subagents  
- Ask rule behavior inside subagent context  
- Plugin-level permission/hook shipping  
- Network sandbox settings for Bash  
- Hook input field for identifying agent/subagent type  
- `.meta.json` sidecar or resolved model ID recording in transcripts
