# 04 — Planning: how to actually plan

## When to plan (and when not to)
A plan has a cost. The ruler:
- **Don't plan** (just do it): 1 file, obvious change, reversible. Planning the trivial is
  procrastination dressed up as rigor.
- **Plan light** (5 lines in the chat): 2–4 files, clear path.
- **Plan formally** (template `docs/templates/plan.md`, user approval): many files, an
  architectural decision, risk of breaking something in use, or you realize you DON'T KNOW the
  path.
Alarm signal in the opposite direction: if you're on the 4th edited file of a task that "didn't
need a plan", it did.

## The central law: plan against reality, not against memory
A plan written before opening the files is fiction with step numbers. Reconnaissance comes
BEFORE the plan:
1. Open the files that will be touched (or send the `explorer` subagent to map them).
2. Confirm that every symbol/route/table the plan cites EXISTS and is the way you think it is.
3. Find out what ALREADY exists that's reusable (half of bad plans reinvent an existing utility).
4. Identify who consumes what you're going to change (grep the callers) — that's where the
   surprise lives.

**Litmus:** every step of the plan cites real paths that you (or your explorer) opened in this
session. A step with a generic path ("adjust the authentication service") = reconnaissance not
done.

## Anatomy of the plan that works

**1. Verifiable objective.** Not "improve login", but "p95 of POST /login < 300ms, measured by
X". If there's no way to know when it's finished, it's not an objective, it's a direction.
(`/compounder:goal` already does this.)

**2. Options considered — at least 2 for any non-obvious decision.** One sentence per option +
why the chosen one won + why the others lost. That costs 3 lines and buys: (a) you actually
thought; (b) when someone suggests the rejected one, the answer is already written; (c) if the
chosen one dies during execution, plan B is ready.

**3. Steps with an owner, a change, and PROOF.** Each step:
```
Step N: <what changes> in <real files>
  Verification: <command/observation proving THIS step worked>
  Risk: <what can go wrong here> (if relevant)
```
A step without its own verification is an invitation to discover everything broken only at the
end, with no idea which step broke.

**4. Order by risk, not by convenience.** The riskiest assumption gets tested FIRST (a 10-line
spike, a proof of concept), because it's the one that can invalidate the entire plan — and the
cheap moment to discover that is before the other steps exist. Corollary: the irreversible step
(if any) goes as close to the END as possible, with a checkpoint before it.

**5. Pre-mortem — 3 lines worth the whole plan.** "If this plan fails, it will have been
because: 1)… 2)… 3)…" For each, a mitigation or an "I accept the risk". This forces the brain to
attack its own plan — the cheapest reviewer there is.

**6. Out of scope, in writing.** What you will NOT do (and will note if you encounter it).
It's the fence against mid-execution drift.

## Execution: the plan is alive, and it is a contract
- Check off steps as you complete them (checkboxes in the plan itself) — it's your Ariadne's
  thread when the context gets long.
- **Small deviation** (step 3 needs to touch one more file): note it in the plan, keep going.
- **Structural deviation** (the plan's assumption collapsed): STOP. Going back to the user with
  "the plan assumed X, reality is Y, I propose Z" is correct execution of the plan — following a
  dead plan out of inertia is the mistake. Never silently absorb a route change the user approved
  in a different form.

## Anti-patterns
| Anti-pattern | Smell | Cure |
|---|---|---|
| Theater-plan | Generic steps: "1. Understand the code 2. Implement 3. Test" | Reconnaissance first; steps cite real files |
| Novel-plan | 5 pages to rename a function | The "when to plan" ruler |
| Fiction-plan | Cites symbols/files that don't exist | Reconnaissance litmus |
| Tunnel-plan | A single option, never compared | Minimum 2 options on non-obvious decisions |
| Zombie-plan | Reality changed, plan keeps being executed | Structural deviation → stop and replan in the open |
| Optimist-plan | No verification step, no risk listed | Proof per step + pre-mortem |

## Checklist before presenting a plan
- [ ] Every step cites files that I opened (or my explorer mapped) in this session.
- [ ] Every step has its own verification.
- [ ] The riskiest assumption is attacked in step 1–2.
- [ ] Non-obvious decisions show the rejected alternative and why.
- [ ] Pre-mortem with 3 likely causes of failure.
- [ ] Out-of-scope explicit.
- [ ] "Done" criterion checkable by command or observation.
