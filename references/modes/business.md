# Mode: business

For investor and sales pitches, business and quarterly reviews, strategy proposals, project status and grant proposals.
Events: `investor-pitch`, `business-review`, `strategy-proposal`, `sales-pitch`, `project-status`, `grant-proposal`.
Themes: `boardroom`, `consulting`, `ledger` (numbers), `startup-bright` and `venture-dark` (pitches), `forest` (grants).

## What the audience judges

A decision-maker has little time. They judge whether the recommendation is clear, whether the evidence supports it, what
the risks are and what happens next.

## Story (answer first)

| Part | Slide | Layout |
|---|---|---|
| Answer | the recommendation or the ask, with amount and date | `exec_summary` |
| Evidence | KPIs against target; trend; the one number that explains the decision | `scorecard`, `kpi`, `chart_insight`, `big_number` |
| Market and position | size, competitors, where we win | `market`, `matrix`, `feature_matrix` |
| Traction | funnel from leads to paying | `funnel` |
| Offer | plans and prices | `pricing` |
| How | steps from decision to result | `process` |
| Plan | tasks, owners, quarters | `gantt`, `roadmap` |
| Risks | likelihood, impact, mitigation, owner | `risk` |
| People | who delivers | `team`, `org` |

Investor pitch order: problem, solution, market, traction, pricing, competition, roadmap, team, the ask. Business review
order: decision, scorecard, trend, drivers, risks, plan.

## Rules

1. The first content slide answers the question: what do you want from the audience, how much and by when.
2. Titles are action titles: "Approve 1.2 M for fraud tooling to protect the margin", not "Fraud".
3. Every number has a `source:`. Market sizes show the definition of each circle (TAM, SAM, SOM) and the method.
4. Scorecards use a word with each colour (`green`, `amber`, `red`); explain red and amber rows only.
5. Totals must add up: check that chart values sum to the scorecard figures before delivering.
6. Risks name an owner and a date; a risk without a mitigation is a finding, not a plan.
7. Prices and money show the currency and the period (per vehicle per month, per year).
8. Forward-looking numbers are labelled as plans or estimates; never present a forecast as a result.
9. Confidential figures stay local; do not upload the deck or data to external services without asking.

## Component choices

- Pick `boardroom` or `consulting` for conservative rooms, `ledger` when the deck is mostly numbers, `startup-bright` or
  `venture-dark` for pitches. Do not use game themes in business decks.
- `matrix` fits SWOT (`tone: swot`) or any four-way split (`tone: neutral`); `funnel` widths follow the values, so stages with
  tiny values keep a minimum width and show their number as a label.
- `gantt` periods are columns (`periods: Q1, Q2, Q3, Q4`); each row is `Task | first | last | owner`.
