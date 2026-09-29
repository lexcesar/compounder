---
stage: research-result
date: 2026-09-29
plan: docs/plans/2026-09-29-compounder-tuning-plan.md
unit: U2
---

# U2 — scorer calibration and the baseline it produced

`compounder/scripts/review-recall.py` scored the five review runs that have a final report,
against `docs/pipeline/golden/c8432b8.json` (17 defects).

## Recall
| Run | Session | Orchestrator | Reviewers | Recall | Hand count before the scorer |
|---|---|---|---|---|---|
| series 1 | `7350eef8` | Opus 5.5 | Sonnet 5 | 8 of 17 | 6 of the first 9, plus 2 found later |
| series 1 | `3cae8abd` | Sonnet 5 | Sonnet 5 | 6 of 17 | 5 of the first 9, plus 1 |
| series 2 | `11fd9f40` | Sonnet 5.5 | Sonnet 5.5 | 12 of 17 | 12 |
| series 2 | `f803e4c4` | Opus 5.5 | Sonnet 5 | 5 of 17 | 5 |
| series 2 | `b2ef4310` | Fable 5.1 | Sonnet 5 | 11 of 17 | 8, counted before the run had finished |

Not scored: series 1 Fable 5.1 (`4157e1c2`). That session went on to discuss every other run,
so its text is contaminated as a source. Its report counted 5 of the first 9 by hand.

Series 1 ran with the fixes absent but in the primary checkout; series 2 ran in the clean room.
The two series are not interchangeable as samples of one configuration.

## Severity agreement — baseline for U6
`review-recall.py --agreement` over the five runs: **25 of 40 placements, 62%**. Target after the
rubric: 80%.

| Defect | SEVERE | MEDIUM | MINOR | other |
|---|---|---|---|---|
| G03 majority-model pricing | 2 | 2 | 0 | 0 |
| G04 model tie | 1 | 2 | 1 | 0 |
| G06 key in argv | 0 | 4 | 1 | 0 |
| G09 no tests | 1 | 1 | 2 | 0 |
| G11 classify_turn1 gaps | 0 | 3 | 0 | 2 |

The rest of the table is in the command output. "No tests" and the model tie are the two
defects rated at three different levels.

## What the calibration fixed in the scorer
Each became a test before the fix.
1. A report written inside a code block, with plain headings and findings as tagged paragraphs,
   scored 0. It now scores 6.
2. The routed menu after the report ("1. Apply safe class…") was counted as three findings.
3. Sub-bullets labelled Scenario, Fix or Realism at the same indent split a finding in two.
4. A level word deep in the text ("the reviewer marked it SEVERE, I downgraded") overrode the
   section the finding was filed under.
5. "US$ 240,25" matched the pattern for a 0.25 cache read price.

## Limits
- Anchors are keyword regexes in Portuguese and English. A finding phrased in an unforeseen way
  lands in the unmatched list, which is read by hand after every batch.
- The scorer counts a defect as found at any level, including suspicion. Weighting by level is
  not implemented.
- Calibrating on the same five runs the anchors were written against overstates how well the
  scorer will read a sixth. The first new batch is the real test.
