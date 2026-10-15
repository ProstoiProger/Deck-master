# Mode: datathon

Judged on the quality of insight, the soundness of the method, business value and clarity of communication. The
deck is a findings report delivered aloud: a few findings, each with number, interval, sample size, meaning and action.

## First hour (for the deck)

1. Read the rubric and write the weights into the front matter.
2. Write the question the stakeholder asked, in their words.
3. Decide how many findings fit: 3 to 5 for 5 to 7 minutes.
4. List the checks that make the numbers trustworthy: data cleaning, split, leakage, uncertainty.
5. Sketch the order: question, data and checks, findings, value, limits, recommendation.

## Skeleton

Use `assets/templates/deck-datathon.md` (about 10 slides, 5 to 7 minutes): title, problem, data and checks
(`pipeline`), finding 1 and 2 (`chart_insight`), method result (`comparison`), value (`kpi`), limits (`impact`),
next step (`roadmap`), closing.

## What wins juries

- One clear headline finding, repeated in the title and the closing.
- Each finding as: claim, number, interval or sample size, why it matters, what to do.
- Checks shown, not asserted: time-ordered split, leakage tests, comparison with a simple baseline.
- A recommendation with a size of impact and its assumptions.
- Limits stated before the jury finds them.
- Charts that make the finding visible in five seconds.

## Pitch numbers

Every number in the deck comes from the analysis log or a saved result file and carries a `source:`. Do not
re-compute in slides by hand.

## Time runbook

Slides, rehearsal twice and a backup PDF take the last 3 to 4 hours of a 24-hour event; protect that block
(`ops/time-budget.md`).

## Traps

- Ten charts and no finding.
- Model details first, the business question last.
- Correlation presented as cause.
- A recommendation with no size and no assumption.
- A dense appendix table on the main path.
