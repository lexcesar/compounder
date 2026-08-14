---
name: deep-analysis
description: Methodical investigation of bugs and mysterious behavior. Use when the user reports an error with no obvious cause, unexpected behavior, "it worked yesterday", divergence between environments, or asks for a diagnosis/root-cause analysis.
---

# Deep analysis — investigation protocol

Goal: reach the CAUSE (not the symptom) with evidence, and state with what confidence.
Foundations and per-layer tactics: `docs/mentor/05-deep-analysis.md`.
Final output in the format of `docs/templates/analysis.md`.

## Mandatory sequence

**1. Reproduce before theorizing.**
Run what fails and see it with your own eyes. Couldn't reproduce? Record exactly what you
tried and treat "does not reproduce" as central data — do not move on pretending you reproduced it.

**2. Read the entire error. Literally entire.**
Message, full stack, the FIRST failure in the log (the following ones are usually cascade). The
answer is in the error text with humbling frequency. Copy the decisive excerpt into the analysis.

**3. Ask "what changed?"**
Recent `git log`, updated dependencies, config, data, environment. A new bug in old code
almost always has a recent change as its trigger.

**4. Write ≥ 2 hypotheses BEFORE investigating the first.**
A single hypothesis = guaranteed anchoring. For each one, define the discriminating test BEFORE
running it: "if H1 is true, I will see X; if false, I will see Y." Table:

| # | Hypothesis | If true, I will see | Test | Status |
|---|---|---|---|---|

**5. Trace the data, not the vibe.**
Follow the real value through the layers (input → transformation → output). Print/inspect at the
boundaries. "I think it's already wrong here" doesn't count; showing the wrong value at the
boundary does.

**6. Bisect the space.**
Each check must cut the search space in half: by layer (front/API/domain/database),
by time (mental or real `git bisect`), by data (what minimal input still fails?). Reduce to the
smallest case that reproduces.

**7. Symptom ≠ cause: ask "why" until you hit something primary.**
Where the error APPEARS is rarely where it is BORN. Stop asking when you reach a decision,
a config, or a premise — not another effect.

## Evidence accounting (mandatory in the output)
Keep three SEPARATE lists — mixing them is investigation mistake #1:
- **Facts** — observed in this session, with source (command + output, file:line).
- **Inferences** — deductions from the facts (say which ones).
- **Assumptions** — what you are assuming without having looked.

## Stop conditions
- **Cause found:** demonstrate it (the discriminating test confirmed it; ideally, a minimal case
  reproduces and the fix makes it pass). Deliver: root cause + evidence + proposed fix +
  prevention + confidence (high/medium/low + what would raise it).
- **3 dead hypotheses / budget exhausted:** stop and deliver the evidence accounting with your
  best suspect ranked. This IS a valuable deliverable — never stretch it with random attempts.

## Prohibitions
- Fixing things "in passing" during the investigation (changing the system contaminates the evidence).
- Two simultaneous changes to test one hypothesis.
- Concluding a cause by similarity to a known bug, without local evidence confirming it.
- If the request was a DIAGNOSIS: deliver the verdict and STOP. Applying the fix is a different request.
