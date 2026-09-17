# compounder — compound engineering, version 2

Spiritual successor to Every's [compound-engineering-plugin](https://github.com/everyinc/compound-engineering-plugin),
redesigned from scratch by Claude Fable 5 for modern Claude Code and to run well on **Fable, Opus,
Sonnet, and Haiku**. Same philosophy — *each unit of work should make the next one easier* — with different
engineering underneath.

## Installation

```
/plugin marketplace add lexcesar/compounder
/plugin install compounder
```

(For local development, point to the clone: `/plugin marketplace add path/to/clone`.)

## What changed from the original — and why

| Original (CE) | compounder | Why |
|---|---|---|
| 400–800-line skills with dozens of modes, flags, and menus | ~100-line skills, one happy path, decisions in the model | A small model drowns in a flag tree; lean, concrete instruction is what Haiku/Sonnet execute well |
| `/lfg` gates in prose ("check the structured return") | Gates executed by an `adversarial-verifier` agent that tries to REFUTE the evidence | Self-attestation is the #1 failure mode of an autonomous pipeline; a real gate is adversarial |
| Orchestration described in text, 0 standalone agents (multi-platform portability) | 7 real agents (`agents/`) + native use of Claude Code parallelism | A single target (Claude Code) allows using the platform for real instead of the lowest common denominator |
| `/slfg` removed | **`/slfg` resurrected** — a swarm with research fan-out, a reviewer panel, and adversarial verification in parallel; degrades gracefully when only the subagent tool is available | It was the feature that was worth the price; today's platform can take it |
| Push/PR by default on autopilot | **Local by default** — local commit only if authorized; push/PR only with `send:pr` or an explicit order | An autopilot that publishes on its own violates the reversible/irreversible rule (AUTONOMY.md) |
| 727-line `ce-compound`, multi-agent to write one doc | `/compound` distills and ROUTES: technical solution → `docs/solutions/`; project rule → CLAUDE.md; preference → memory; vocabulary → CONCEPTS.md; ephemeral → trash | The value is in the distillation and the right address, not in the ceremony; expensive capture = skipped capture |
| No aside mechanism | **`/btw`** + interception hook: speak mid-work without derailing anything | Talking during execution is how humans work; formalizing the aside unlocks real parallelism |
| Its own YAML config, headless modes by flag | Convention over configuration: `docs/plans/`, `docs/solutions/`, `BTW.md`, `CONCEPTS.md`; headless = the caller's decision | Less surface to break and fewer tokens to load |

What was **preserved** from the original, because it is excellent: the brainstorm → plan → work →
simplify → review → compound loop; the WHAT (requirements) / HOW (plan) separation; learnings as
searchable artifacts with frontmatter; `CONCEPTS.md` as living vocabulary; the rule that research
is done in the phase that needs it and flows into the next.

## Commands

| Command | Role |
|---|---|
| `/brainstorm <idea>` | Discover the WHAT: the right questions → requirements doc |
| `/plan [requirements\|description]` | Decide the HOW: real reconnaissance → plan with verifiable units |
| `/work [plan]` | Execute with a baseline, task tracking, and per-unit evidence |
| `/simplify` | Take the plane to the freshly written diff (preserving behavior) |
| `/review [scope] [ultra]` | Panel of 4 reviewers in parallel + adversarial verification of the findings; `ultra` = swarm engine (finder rounds until dry, 3-vote tribunal) |
| `/debug <bug>` | Root-cause investigation (uses the kit's `deep-analysis` skill, if present) |
| `/compound [context]` | Distill learnings and record each one at the right address; `refresh` to prune; `explainer` to generate an onboarding inoculation doc |
| `/lfg <feature>` | The entire pipeline, autonomous, with adversarial gates — local delivery |
| `/slfg <feature>` | The same, as a SWARM: research, review, and verification in parallel |
| `/btw <message>` | Mid-work aside: recorded, classified, without derailing |
| `/goal <goal> \| status \| done` | The WHAT as a contract: `docs/goals/ACTIVE.md` with checkable acceptance criteria, then hands off to `/plan` or `/work` |
| `/handoff [context]` | Handoff document for the next session: state with evidence, next step executable in 1 minute, traps |
| `/guardrails [area]` | 7-question interview → layered limits: `settings.json` permissions, CLAUDE.md invariants, AUTONOMY.md zones, optional hook |
| `/council <dilemma>` | Council of 15 avatars for life/project/venture decisions: 4 voices with one guaranteed contrarian, tension mapped; project `avatars/` overrides the bundled set |

Typical flow: `/goal` → `/brainstorm` → `/plan` → `/work` → `/simplify` → `/review` → `/compound`;
`/handoff` when a session closes with work open.
In a hurry and confident: `/lfg feature description`. In a hurry, confident, and with budget: `/slfg`.

## Integration with the starter kit

This plugin was designed to coexist with the kit (`CLAUDE.md`, `AUTONOMY.md`, `/retro`,
`docs/mentor/`, `avatars/`): when those files exist, the skills respect and cite them (e.g. `/lfg`
obeys the AUTONOMY.md zones; `/compound` uses `/retro`'s routing table; `/council` prefers the
project's `avatars/`; `/handoff` prefers `docs/templates/handoff.md`). Without the kit, the plugin
works on its own with safe built-in defaults.

Recommended line in the project's CLAUDE.md:

> Messages that arrive while I work: handle via the /btw protocol — acknowledge in 1 line,
> classify (parallelize now / do next / record in BTW.md), and only abandon the current task
> if the message explicitly says to stop.

## Anatomy

```
compounder/
├── .claude-plugin/plugin.json
├── skills/            # 15 lean skills (~100 lines each); council/ bundles the 15 avatars
├── agents/            # researcher, 4 reviewers, adversarial-verifier, fork-executor
├── hooks/hooks.json   # intercepts "btw ..." prompts and injects the aside protocol
└── scripts/
    ├── btw-hook.sh        # UserPromptSubmit hook behind /btw
    ├── dispatch-cost.py   # per-dispatch tokens/USD + fork-vs-fresh shape, read from transcripts' `usage`
    └── count-tokens.sh    # size a plan/brief with /v1/messages/count_tokens (free, model-specific)
```
