# 06 — Delegation and subagents: orchestrate without losing control

## Why delegate (the three valid reasons)
1. **Context economy** — the dominant reason. A 40-file sweep would cost your entire reasoning
   budget; the subagent burns ITS context and hands you back 20 lines of conclusion.
   You keep the map, not the files.
2. **Parallelism** — N independent investigations at the same time.
3. **Fresh eyes / adversarial role** — a reviewer without your attachment to your own solution
   finds what you don't want to see.

## When NOT to delegate
- Single lookup in a known location ("what's the type of field X in models.py") — faster yourself.
- A task that requires the accumulated context of the whole session (the agent is born without it).
- A task whose verification costs more than its execution — if trusting the result would require
  redoing it, delegating was theater.
- And the inverse of theater: **delegated → don't redo it.** Duplicating delegated work pays twice.
  Wait, then verify by sampling (below).

## The briefing law: the agent is born amnesiac
Delegation mistake #1, by a mile: assuming the subagent knows what you know. It has NOT seen the
conversation, the goal, the files you opened, the agreed conventions. A good briefing fits this
skeleton — and all the effort goes into items 2 and 4:

```
GOAL: <1 sentence, outcome, not activity>
CONTEXT YOU DON'T HAVE: <the session's essentials: what the project is, what has
  already been discovered, decisions already made that constrain the answer>
SCOPE: in: <...> | out: <what NOT to do/touch/propose>
EXPECTED RETURN: <EXACT format — path:line list, table, JSON, verdict+evidence.
  Your final text is data for me, not a message for a human.>
QUALITY: <what invalidates the answer: "a finding without the file opened doesn't count",
  "only claim 'doesn't exist' while listing the patterns you searched">
```

A return with no requested format = a 3-page essay you'll have to reprocess (paying the context
the delegation was supposed to save). The output contract is half the value of delegation.

## Orchestration patterns (from most common to most expensive)
1. **Single explorer** — map unknown territory before planning. (The `explorer` agent.)
2. **Fan-out of independent fronts** — N agents, each on one dimension (one per module; or per
   search mode: by name, by content, by config). Fire ALL of them together (parallel), never in
   series. Only worth it if the fronts are truly independent.
3. **Per-item pipeline** — each item goes through stages (find → transform → verify) without
   waiting for the other items. Use when the items don't talk to each other.
4. **Finder → adversarial verifier** — the finder's findings become a list of claims; the second
   agent (`verifier`/`critical-reviewer`) tries to KNOCK DOWN each one. Filters out the
   plausible-but-false, which is the agent-specific poison: findings that sound right.
5. **Panel of judges** — for design decisions: N agents propose approaches with different biases
   (simplicity-first, risk-first, performance-first); you synthesize from the winner + the best
   ideas of the others. Expensive; only for decisions that are worth it.

Synchronization barriers (waiting for ALL before proceeding) only when the next step needs the
complete set (dedup across findings, total count). Otherwise, pipeline — an unnecessary barrier
wastes the fast agents' time waiting for the slow one.

## Trust, but check (the reception protocol)
A subagent result is INPUT, not truth:
1. **Check the format** — did it come per the contract? Items with path:line?
2. **Sample** — open 2–3 of the cited locations. Do they match? One false citation = quarantine
   the whole batch (re-verify everything or re-delegate with a corrected briefing).
3. **Check the coverage** — did the agent say WHERE it searched and what it did NOT find? "Doesn't
   exist" without a list of searched patterns isn't information, it's hope.
4. **Never pass it through raw** — a subagent conclusion only reaches the user after going through
   you: filtered, sample-verified, and signed by YOU. "The subagent said" doesn't exist as an
   attribution of responsibility — the one reporting is you.

## Failures and economic sanity
- Agent came back empty/wrong ONCE → fix the BRIEFING (reread it through the eyes of someone who
  saw nothing; the failure is almost always there) and re-delegate ONCE. Failed again → do it
  yourself; re-delegating the same briefing 3× is the distributed version of "failed 2× → try the
  same thing a 3rd time".
- Cost rule of thumb: delegation has fixed overhead (spawn + briefing + reception). Worth it when
  the work avoided ≫ overhead — a 30-file sweep, yes; 3 greps, no. Batch small stuff into ONE
  agent instead of one agent per trifle.
- Secrets and sensitive data NEVER go into an agent briefing (the briefing is a prompt; it leaks
  like any text).

## Checklist before dispatching
- [ ] The agent has ALL the necessary context inside the briefing (test: would a stranger execute it?).
- [ ] Return format specified and verifiable.
- [ ] Negative scope stated ("don't propose fixes", "don't touch X").
- [ ] Parallel fronts are actually independent.
- [ ] Reception plan: what you'll sample in order to trust the result.
