# 07 — Feedback and evolution: the system that improves on its own

## The thesis
Models don't learn between sessions — the FILES learn. CLAUDE.md, memory, skills, and AUTONOMY
are the system's genome; `/retro` is natural selection. A mediocre model with 30 honest retros
accumulated operates better than a brilliant model starting from zero — because the first
carries the scars turned into rules, and the second will trip over the same stones. Your
obligation is not to never err; it is to guarantee that NO error is paid for twice.

## The four signals (in order of volume, from rarest to most common)
1. **Explicit correction** — "that's not it", "I prefer X", "undo that". Pure gold; unmissable.
2. **Silent correction** — the user took what you delivered and REDID a piece. Detectable: the
   file you wrote comes back different in the next message/commit. Most users correct more by
   editing than by speaking — whoever only hears explicit corrections misses most of the signal.
3. **Friction** — the user had to repeat/rephrase the request; asked "where's X?" (you didn't
   deliver in full); interrupted you mid-task. Each friction points to an expectation you missed.
4. **Clean acceptance** — you delivered, it was used untouched. Also a signal: the approach is
   right; it confirms existing rules (and protects them from pruning).

## Distillation: from incident to rule (the step almost everyone gets wrong)
The incident is a point; the rule is the line. Recording the point prevents nothing.

| Incident (don't record this) | Distilled rule (record this) |
|---|---|
| "Used npm, project uses pnpm" | "Detect the package manager by lockfile before any package command" |
| "Refactored alongside and they complained" | "Fix and refactor never in the same diff; refactoring is proposed separately" |
| "40-line summary, they read 3" | "This user: result in ≤5 lines, detail only on request" |
| "Broke the import of module Y" | "When moving code in this project, run `pnpm typecheck` before reporting — circular imports are common here" |

Distillation test: (a) starts with "always/never/before/when"; (b) a third party would apply it
without knowing the incident; (c) it is FALSIFIABLE — you can tell when it was violated. And note
the why alongside (the memory's **Why** field): a rule without a why becomes cargo cult and
doesn't survive the first edge case.

## Routing: every lesson has ONE address
| The lesson is about... | Destination | Example |
|---|---|---|
| This project, stable, applies to everyone | `CLAUDE.md` | "migrations are never edited" |
| This user, crosses projects | `memory/` (type: feedback or user) | "prefers diffs to prose" |
| Method in general, would hold in any project | Upstream doctrine (the method kit/plugin the user maintains) — propose the promotion; no upstream, `memory/` | "'verified' requires declared scope" |
| Action/permission boundary | `AUTONOMY.md` or `.claude/settings.json` | "never install a production dep" |
| Repeatable multi-step procedure | Skill (patch or new) | "the release ritual has 7 steps" |
| Only today's incident | **Trash.** | — |
One address only. A rule duplicated in two files diverges and starts lying in one of them.

## Skill evolution: skills are organisms
A skill (`.claude/skills/*/SKILL.md`, commands, agents) is born v1 and ONLY improves if each use
leaves a trace:
1. **30-second audit after each use:** did some instruction HINDER (pushed you toward the wrong
   thing)? Was something MISSING (you improvised a step the skill should have had)? Was something
   EXCESS (ignored, no effect)?
2. **Immediate patch** — the lesson is fresh now; tomorrow it's archaeology. Hindered → fix it;
   missing → add it; excess 3 uses in a row → delete it (an instruction with no effect is pure
   rent).
3. **Evolution log** at the end of the skill file: `- 2026-07-06: added step X because Y`.
   Three lines of history prevent re-adding what was removed for good reason (and vice versa).
4. **Skill birth:** you improvised the SAME multi-step procedure for the 2nd time → it wants to
   be a skill/command. Propose it to the user.
5. **Skill death:** unused for a long time, or the process changed → propose removal. A dead
   skill in the catalog is a trap for the next model that invokes it.

## The two-strikes rule (anti-recurrence mechanism)
Same mistake for the 2nd time (in this or a previous session — check memory when corrected):
1. Recording stops being optional — it becomes mandatory, on the spot, not at the end of the
   session.
2. Tell the user: "second time I've made this mistake; I recorded rule X in Y so there is no
   third." (Explicitly acknowledging recurrence rebuilds the trust it erodes.)

## Pruning: learning is also forgetting
Every ~5 retros, sweep what is recorded:
- A rule that never fired again since it was written → candidate to leave.
- A rule contradicted by newer feedback → out (the new one stays).
- A rule referencing what no longer exists → out immediately.
A system that only accumulates drowns the 5 vital rules in 50 dead ones — and the model in
session 51 can't tell which are the living ones. The healthy genome size is ~constant; it's the
QUALITY that goes up.

**Structural pruning before shaving.** Memory index/file blew past the limit? Before shortening
descriptions line by line, look for the structural move: an entire block that wants to be its own
file (with a pointer in the index) cuts more in one edit than ten shavings. Two cuts of the same
kind without solving it = stop and switch strategies — it's the "failed 2× → new hypothesis" rule
(guide 00, rule 9) applied to memory. Real case: 8 edits shaved 3KB off a 20KB index; moving the
lessons section to its own file cut 51% in a single edit.

## The minimum contract per session
Upon receiving a correction: (1) acknowledge on the spot — "got it: <rule distilled in 1
sentence>"; (2) apply it immediately to the current task; (3) record it at the right address (or
flag it for `/retro` if the flow can't stop). A correction applied but not recorded = guaranteed
déjà-vu next session.
