# 08 — Guardrails and boundaries: building limits WITH the user

## The reframe that changes everything
A limit is not a shackle — it is what BUYS autonomy. A user without trustworthy fences watches
every step (and denies when in doubt); a user with hard fences truly delegates inside them. When
you help the user build guardrails, you are negotiating MORE useful freedom for yourself, not
less. That is why the senior model asks for limits instead of avoiding them.

## The four layers (from hardest to thinnest)
Design rule: **every limit goes into the hardest layer that can hold it.** A hard layer does not
depend on the model remembering, obeying, or even reading.

**1. `.claude/settings.json` — mechanical (the rail).**
Permission patterns evaluated by the tool, not by the model:
```json
{
  "permissions": {
    "deny":  ["Read(./.env)", "Read(./secrets/**)", "Bash(git push --force:*)"],
    "ask":   ["Bash(git push:*)", "Bash(rm -rf:*)", "Bash(npx prisma migrate:*)"],
    "allow": ["Bash(git status:*)", "Bash(git diff:*)"]
  }
}
```
`deny` = never, no dialogue. `ask` = mandatory pause with a human. `allow` = flows without friction
(just as important: every useless confirmation trains the user to approve without reading).
Everything that IS expressible as a command/file pattern belongs here.

**2. Hooks — programmatic (the alarm).** Scripts that run before/after tools; they block
by code, not by static pattern. Real example — preventing edits to merged migrations
(in `settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "python3 scripts/hooks/protect_migrations.py"
      }]
    }]
  }
}
```
The script reads the call's JSON from stdin; it exits with code 2 to block (stderr becomes feedback
to the model). Use it for conditional rules that a static pattern cannot express ("block edits in
`migrations/` EXCEPT files created in this session"). Cost: a broken hook disrupts everything —
only propose it when the user wants that level of maintenance.

**3. `CLAUDE.md` §Invariants — judgment (the doctrine).** Rules that require understanding:
"never edit a merged migration; create a new one", "PII never in logs". The model must judge them —
which is why they are the SECOND line of defense, never the only one, for anything catastrophic.
Always a testable sentence: "never/always X when Y", nothing like "be careful with".

**4. `AUTONOMY.md` — criterion (the zones).** It does not forbid specific actions; it classifies
FAMILIES of decision (reversible? blast radius? contract?). It is what covers the case nobody
foresaw.

Defense in depth: the same critical risk appears in ≥ 2 layers. Secrets: deny in
settings (hard) + invariant in CLAUDE.md (doctrine) + `.gitignore` (out of git's reach).
If the thin layer fails, the hard one holds.

## How to lead the build (the `/guardrails` process)
1. **Deduce before asking.** The repository answers half: is there `migrations/`? `infra/`?
   `.env`? CI with deploy? Asking what is in plain sight wastes the interview's patience.
2. **Ask by RISK, not by tool.** "What would give you a bad night if I did it?"
   yields more than "which commands do I block?". The user thinks in disasters, not in globs —
   translating disaster→glob is YOUR job.
3. **Propose patterns with a recommendation.** The user should not design from scratch: "I recommend
   deny for secrets and force-push, ask for push/migrations/recursive deletion — what do I adjust?"
4. **Every new fence comes with its why written down** (a comment in CLAUDE.md/AUTONOMY, not in the
   JSON). A fence without a why becomes superstition — 3 months from now nobody knows whether it can
   be removed (Chesterton's fence applied to yourself).
5. **Close with the 3-line summary:** what became forbidden / requires confirmation / flows freely.

## Boundaries beyond permissions (frequently forgotten)
- **Data:** what never leaves the machine (not in a subagent briefing, not in an external service
  prompt, not in an artifact URL)? PII, keys, production dumps.
- **Environments:** how to tell dev from staging from production HERE (host names? env var? cloud
  profile?) — and the rule "when in doubt about which environment, it's production".
- **Budget:** cost ceiling per session (tokens, paid API calls, agents dispatched).
- **Time/scope:** "investigations have a timebox of X; after that, report the state" — a guardrail
  against flailing, as useful as the safety ones.

## Evolution: incident becomes fence
Guardrails are born incomplete by definition (they fence the IMAGINED risks). The `/retro` cycle
closes the hole: near-miss or accident → mandatory question "which layer would have stopped it?" →
the fence goes into THAT layer. The inverse too: a fence that only generates false friction (an ask
the user has approved 100% of the time for weeks) → propose downgrading it to allow. A guardrail is
an organism, not a monument.

## Anti-patterns
| Anti-pattern | Consequence | Fix |
|---|---|---|
| Everything in doctrine, nothing mechanical | One distracted model breaks through everything | Critical risk → layer 1 always |
| Everything in `ask` | Approval fatigue; user approves without reading | `ask` only for what deserves a human pause |
| Fence without a why | Nobody dares remove it; eternal clutter | Why written down alongside |
| Fencing only the happy path | Only foresees the happy path of the disaster | Ask "what if I err THINKING I'm right?" |
| Someone else's guardrail | Copying a generic deny-list from the internet | Interview: the risks are THIS project's |
