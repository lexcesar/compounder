# 05 — Deep analysis: investigation that reaches the cause

The operational protocol lives in the skill (`.claude/skills/deep-analysis/SKILL.md`); this guide
is the foundation — why each step exists and the tactics per situation. Standard output:
`docs/templates/analysis.md`.

## The three laws of investigation

**1. Evidence before theory.** Mistake #1 is recognizing a pattern ("this looks like that cache
bug") and rushing off to "fix" it. Patterns generate HYPOTHESES, never conclusions. A conclusion
requires LOCAL evidence: from this code, this execution, this session. The model that skips this
step fixes the bug it remembers, not the one that exists.

**2. One change at a time.** Each hypothesis test changes ONE thing and observes. Changed three
things and it worked? You don't know which one it was — and you probably introduced two
superstitious changes someone will be afraid to remove forever. (Corollary: an investigation is
not the time to fix anything "in passing" — every change contaminates the crime scene.)

**3. The space gets cut in half.** Efficient investigation is binary search, not a linear sweep.
Each check should eliminate ~half of the remaining space. If you're reading file after file "to
see if you find something", you're not investigating — you're strolling.

## Bisection tactics, by axis
- **By layer:** is the data right coming out of the database? → half eliminated. In the API
  response? → the other half. Typical boundaries: database → repository → domain → serialization →
  network → client.
- **By time:** did it work at commit X? `git bisect` (real or mental, over the `git log` of the
  touched area). New bug in old code = a recent change in code, dependency, config, or DATA.
- **By data:** what is the SMALLEST input that still reproduces? Cut fields, lines, flags until
  the bug disappears — the last piece removed points to the cause. The minimal case also becomes
  the regression test.
- **By environment:** only in production? The difference (env vars, version, real data,
  concurrency, timezone) is the suspect list — enumerate it explicitly instead of "must be the
  environment".

## Hypotheses: the anti-anchoring mechanism
Write ≥ 2 BEFORE investigating the first (law 7 of the principles). The subtle point: define the
discriminating test BEFORE running it — "if H1, I'll see X; if H2, I'll see Y". Whoever defines
the expected outcome after seeing the result always finds that the result confirms what they
already thought (it's the p-hacking of debugging). A dead hypothesis is PROGRESS: record what the
failure proved and cross it off — smaller space.

## The evidence ledger
Three separate lists, always:
- **Facts** — with source: `command → output`, `file:line`. Immutable.
- **Inferences** — "from F1+F3 I conclude that...". Valid as long as the facts sustain them.
- **Assumptions** — what you are assuming WITHOUT having looked ("I presume the cron runs").
The assumptions list is the most valuable: when the investigation stalls, the cause is almost
always hiding in an untested assumption. Stuck? Promote the oldest assumption to hypothesis and
test it.

## Symptom → cause: the chained "why"
`NullPointerException at line 80` → why null? → the repository returned empty → why? → the query
filters by tenant and the tenant comes in empty → why? → the middleware doesn't populate tenant
on webhook requests → **cause**: a design decision that didn't foresee webhooks. Stop at the
primary one (decision/config/premise). Fixing at line 80 (`if null return`) would hide the real
defect and leave it free to show up in the other 12 places that depend on the tenant.

## When to stop
- **Found it:** the discriminating test confirmed and, ideally, the minimal case reproduces → the
  fix makes it pass → the whole suite stays green. Deliver with labeled confidence: "high —
  reproduced, fixed, regression covered" vs "medium — evidence points to X, but I couldn't
  reproduce locally; I'd validate with Y".
- **Didn't find it (3 dead hypotheses / budget blown):** deliver the evidence ledger, hypotheses
  tested and dead, ranked suspect, and the next test you would run. That is worth a LOT: the next
  investigator (or you tomorrow) starts where you stopped, not from zero. Flailing disguised as
  persistence — trying random things for one more hour — is worth less than nothing.

## Anti-patterns
| Anti-pattern | What it looks like | What it is |
|---|---|---|
| Shotgun debugging | "I'll keep changing things until it passes" | Destroys evidence; produces a superstitious fix |
| Anchoring | "It can only be the cache" | One hypothesis becoming a conclusion without a discriminant |
| Fix-at-the-symptom | `if (x != null)` where it blew up | Hides the cause; spreads the defect |
| Confidence-by-analogy | "I've seen this error, it's always X" | Pattern without local evidence |
| Log blindness | Reading only the last line of the error | The first failure in the log is the one that matters |
| Sightseeing investigation | Reading files "to get familiar" | No check cuts the space |
