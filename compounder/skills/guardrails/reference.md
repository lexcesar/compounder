# Guardrails — the four layers

A limit is not a shackle — it is what BUYS autonomy. A user without trustworthy fences watches
every step; a user with hard fences truly delegates inside them.

Design rule: **every limit goes into the hardest layer that can hold it.** A hard layer does not
depend on the model remembering, obeying, or even reading.

**1. `.claude/settings.json` — mechanical (the rail).** Permission patterns evaluated by the
tool, not by the model:
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
(every useless confirmation trains the user to approve without reading). Everything that IS
expressible as a command/file pattern belongs here.

**2. Hooks — programmatic (the alarm).** Scripts that run before/after tools; they block by
code, not by static pattern. Example — protecting merged migrations (in `settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "python3 scripts/hooks/protect_migrations.py" }]
    }]
  }
}
```
The script reads the call's JSON from stdin; exit code 2 blocks (stderr becomes feedback to the
model). Use it for conditional rules a static pattern cannot express. Cost: a broken hook disrupts
everything — only propose it when the user wants that level of maintenance.

**3. `CLAUDE.md` §Invariants — judgment (the doctrine).** Rules that require understanding:
"never edit a merged migration; create a new one", "PII never in logs". The model must judge
them — the SECOND line of defense, never the only one, for anything catastrophic. Always a
testable sentence: "never/always X when Y", nothing like "be careful with".

**4. `AUTONOMY.md` — criterion (the zones).** Classifies FAMILIES of decision (reversible?
blast radius? contract?) into 🟢 act / 🟡 act and announce / 🔴 ask first. It covers the case
nobody foresaw.

**Defense in depth:** the same critical risk appears in ≥ 2 layers. Secrets: deny in settings
(hard) + invariant in CLAUDE.md (doctrine) + `.gitignore` (out of git's reach).

## Boundaries beyond permissions (frequently forgotten)
- **Data:** what never leaves the machine (not in a subagent briefing, not in an external service
  prompt, not in an artifact URL)? PII, keys, production dumps.
- **Environments:** how to tell dev from staging from production HERE — and the rule "when in
  doubt about which environment, it's production".
- **Budget:** cost ceiling per session (tokens, paid API calls, agents dispatched).
- **Time/scope:** "investigations have a timebox of X; after that, report the state".

## Evolution: incident becomes fence
Near-miss or accident → mandatory question "which layer would have stopped it?" → the fence goes
into THAT layer. The inverse too: an `ask` the user has approved 100% of the time for weeks →
propose downgrading it to `allow`.

## Anti-patterns
| Anti-pattern | Consequence | Fix |
|---|---|---|
| Everything in doctrine, nothing mechanical | One distracted model breaks through everything | Critical risk → layer 1 always |
| Everything in `ask` | Approval fatigue; user approves without reading | `ask` only for what deserves a human pause |
| Fence without a why | Nobody dares remove it; eternal clutter | Why written down alongside |
| Someone else's guardrail | Generic deny-list from the internet | Interview: the risks are THIS project's |
