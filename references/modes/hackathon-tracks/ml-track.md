# ML track deck

Judged on predictive quality, the validity of the evaluation and the business use of the predictions.

## Slides (6 to 8, 3 to 5 minutes)

| # | Slide | Layout | Content |
|---|---|---|---|
| 1 | Title | `title` | case name, team |
| 2 | The decision | `problem` | who acts on the score and what it costs when wrong |
| 3 | Data and validation | `pipeline` | unit, target, split that mirrors use, leakage checks |
| 4 | Result | `kpi` or `comparison` | metric against a simple baseline, with spread across folds or seeds |
| 5 | Decision rule | `chart_insight` | threshold or ranking cut, cost curve or lift chart |
| 6 | Why it can be trusted | `bullets` | explanations, calibration, stability over time |
| 7 | Path to production | `architecture` | latency, monitoring, owner |
| 8 | Closing | `closing` | repo, contact |

## Numbers to show

Official metric and the business metric, kept separate; the baseline; spread (folds, seeds); latency if it is a
constraint. Every number has a `source:` pointing to the run log.

## Likely questions

How do you know it works on new data? Where could leakage hide? What threshold and why? What if the data drifts?
Use `communication/judge-qa.md`.

## Traps

A leaderboard score as the only evidence; hiding the split; ignoring the decision rule.
