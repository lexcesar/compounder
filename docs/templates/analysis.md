# Analysis: <symptom in 1 sentence>
Date: YYYY-MM-DD | Request: "<verbatim>"

## Reproduction
<steps executed + observed result; or "not reproduced: tried X, Y — treated as given">

## Facts (with source)
- F1: <fact> — source: `command → output` | `file:line`
- F2: ...

## Inferences
- I1: from F1+F2, <deduction>

## Assumptions (not verified)
- S1: <what I'm assuming without having looked>

## Hypotheses
| # | Hypothesis | If true, I will see | Test performed | Status |
|---|---|---|---|---|
| H1 | ... | ... | ... | dead/alive/confirmed |
| H2 | ... | ... | ... | ... |

## Root cause
<the primary decision/config/premise — not another symptom>
Decisive evidence: <...>
Chain: symptom ← ... ← cause.

## Proposed fix
<diff in a code block, NOT applied (if the request was a diagnosis)>
Risk/reach: <...>

## Prevention
<regression test, guardrail, invariant — what prevents recurrence>

## Confidence
high | medium | low — <why; what would raise it; what would knock this conclusion down>
