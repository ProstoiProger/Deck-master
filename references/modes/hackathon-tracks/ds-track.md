# DS track deck

Judged on insight, method, value and communication: a deck with 3 to 7 findings, each with number, interval,
sample size, interpretation and action.

## Slides (about 10, 5 to 7 minutes)

| # | Slide | Layout | Content |
|---|---|---|---|
| 1 | Title | `title` | question and headline answer |
| 2 | The question | `problem` | stakeholder decision and one number |
| 3 | Data and checks | `pipeline` | cleaning, joins, split, leakage and quality checks |
| 4 to 6 | Findings | `chart_insight` | one finding per slide, one chart, takeaway sentence |
| 7 | Method versus baseline | `comparison` | simple versus chosen method, with interval |
| 8 | Value | `kpi` | size of impact with assumptions |
| 9 | Limits and recommendation | `impact` | can and cannot claim; what to do next |
| 10 | Closing | `closing` | repo, contact |

## Finding format

| Claim | Number | Interval or n | Why it matters | Action |
|---|---|---|---|---|
| Rain cuts leisure rides by a third | -34% | 95% interval, n = 214 stations | weekend rebalancing | add a weekend van shift |

## Statistics and causal care

Say whether the result is association or effect; if causal, name the design (experiment, difference in
differences) and its assumptions. Use time-ordered splits for forecasts. State multiple-comparison handling when
many findings were screened.

## Traps

Many charts, no recommendation; correlation read as cause; averages hiding segments; intervals missing.
