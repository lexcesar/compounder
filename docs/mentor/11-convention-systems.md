# 11 — Convention systems that compound

Distilled from `opten-conventions` — a system created from scratch by Alexander Cesar to guide
AI agents in a real team (C#/Umbraco/TypeScript/SCSS), generalized here for ANY stack.
What follows is the method behind that repository: how to turn team conventions into
permanent agent capability. The lessons apply to whoever builds the next system of this kind.

## The fifteen laws (mined from a system that worked in production)

**1. Mine rules from evidence, not opinion.** The conventions came from analyzing 40+ PRs
merged by 4 people — not from a style guide imagined a priori. A rule without ballast in
real work becomes bureaucracy; a rule mined from real corrections has a proven hit rate.
Corollary: record the rule's ORIGIN ("based on N occurrences") — it is what justifies keeping it.

**2. Close the compounding loop.** The cycle that gives the thing its name: human correction in a
PR → saved as a feedback artifact → becomes a permanent rule in the reviewer agent → the next piece
of work is born already knowing. A correction pays once; without the loop, it pays every week. (It
is this kit's `/retro` applied to team conventions.)

**3. Three activation layers for three needs.** The same knowledge serves itself three
ways: **skill** (passive knowledge, carried along while writing — "advice" mode),
**reviewer agent** (active judgment over finished work — "audit" mode), **command**
(multi-step workflow triggered by the user — "action" mode). Don't pick one: the mirror pattern
encodes the SAME rule as advice AND as audit — the writer doesn't need to remember to ask for
review in order to be protected.

**4. Every rule with a contrastive pair.** `CORRECT:` / `WRONG:` side by side, minimal, is the
fastest way to make a rule unambiguous for human and model alike. Abstract prose without the pair
is a rule every reader interprets differently.

**5. Shift-left: apply at the moment of action.** A convention applied at commit time (a command
that composes the right message) costs zero correction; the same convention policed at review
costs a whole cycle. The reviewer becomes the safety net for what automation doesn't cover, not
the front line.

**6. Warn, don't block (by default).** A governance agent that is "warn-only — report findings,
never block" preserves human authority and builds trust in the system much faster than
a gate that stalls work. Blocking is an explicit opt-in by the organization, never the author's default.

**7. The orchestrator sees what no specialist sees.** The unique value of running reviewers in
parallel under a coordinator: inconsistencies BETWEEN domains (the markup says X, the script expects Y;
the style defines a class the behavior never uses). A single-file reviewer will never catch that.

**8. Deterministic where possible, LLM where needed.** In the same review pass: greps and scripts
for objective facts ("does the token exist in the source of truth?", "is the component registered?") and
agents only for judgment. A fact via text search is cheaper AND more reliable.

**9. Fixed rules and heuristics are separate skills.** A domain with a right answer → table of
rules. A domain with real tradeoffs (git strategies, e.g.) → a matrix `situation → strategy →
why` + anti-patterns with an alternative + the 10-second checklist before a destructive action:
"Is it reversible? Has it been pushed? Is there a simpler way?". Capturing JUDGMENT ≠ capturing a rule.

**10. A numeric threshold where judgment would be vague.** "If more than N units behind, suggest X"
makes consistent and auditable what "use common sense" leaves to chance. Every recurring judgment
deserves its explicit threshold.

**11. The system governs its own maintenance.** A meta-doc (the CLAUDE.md OF the conventions
repository) with: a release checklist (version, changelog, README in sync), a template for
"how to add a new unit of knowledge". Without it, the system drifts from its own standard
by the third contribution.

**12. Short always loaded; heavy on demand.** Every topic follows `SKILL.md` (lean, always
in context) + `references/*.md` (catalogs, diagrams — loaded only when needed).
It is the same economy as guide 01 applied to plugins.

**13. Placeholders in everything shared.** Examples with `moduleXxx`, `MyController` —
NEVER a real project/client name in the generic layer. The specific lives only in the consumer's
local override layer, which has explicit priority over the plugin. (Two wins: portability and
zero client-information leakage.)

**14. Non-goals next to the goals.** Every tool declares what it deliberately does NOT
do ("does not push, does not create branches, does not use amend"). It is the boundary that prevents
scope creep and lets the user know what is still their responsibility.

**15. Vaccinate the reviewer against inventing problems.** Literal instruction in the agent: "if the
code is clean, say so — do not invent issues". The LLM's natural bias is to always find something;
without the vaccine, the system trains the team to ignore the reviewer.

## Structural patterns worth imitating
- Root split by function: `agents/<purpose>/`, `commands/<namespace>/`, `skills/<topic>/`, `docs/plans/`.
- Namespace prefix on every distributed artifact (`myteam-*`) — avoids collisions for whoever installs.
- Dated, typed plan (`YYYY-MM-DD-type-slug-plan.md`) separate from the changelog: the plan records
  the REASONING, the changelog records the RESULT.
- Identical skeleton per artifact type: every reviewer has the same sections (role → process →
  rules with pairs → output format → closing); adding a new one is filling in a template.
- Identify which artifact is "the truth that survives" in the team's flow (with squash-merge, it is
  the PR title) and concentrate the rigor THERE, not where it is convenient.
- Isolate the most expensive trap in its own section ("CRITICAL: …"), outside the list of minor
  rules — the 4-hour mistake must not share a paragraph with the 4-minute one.

## Relation to the rest of the kit
This guide is 02-living-memory + 07-feedback-and-evolution applied at TEAM scale and packaged as an
installable product: memory becomes versioned skills, `/retro` becomes the PR feedback loop,
guardrails become reviewers. Whoever masters guides 01–10 and this one can build, for
any team and any stack, what opten-conventions was for its own.
