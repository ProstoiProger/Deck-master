# Judge Q&A

Replace the bracketed parts with your numbers from the run log. Template: `assets/templates/qa-prep.md`.

## Data and validation

| Question | Answer pattern |
|---|---|
| How do you know it works on new data? | validation mirrors use: [time split or group split]; out-of-time score [x] against development [y] |
| Could there be leakage? | we tested [single-feature screen, time order, group overlap]; the best single feature scores [x], not suspicious |
| How big is the data? | [n rows] over [period]; [what was removed and why] |
| Is the gain real or noise? | difference [x] with interval [a, b] over [k seeds or folds] |

## Model and method

| Question | Answer pattern |
|---|---|
| Why this method? | simplest option that met the goal; compared with [baseline]: [result] |
| What does it get wrong? | main error type [x] in [segment]; handled by [rule or review] |
| Can you explain a decision? | yes: top reasons per case, global drivers [list] |
| What if the data changes? | monitored with [metric]; retrain when [condition] |

## Product and business

| Question | Answer pattern |
|---|---|
| Who uses it and how? | [user] does [action] in [n] steps, replacing [today's way] |
| What is it worth? | [size] with assumptions [list]; interval [a, b] |
| How would you deploy it? | [architecture in one sentence]; latency [x]; owner [role] |
| What is the biggest risk? | [risk]; mitigated by [measure] |

## Responsibility

| Question | Answer pattern |
|---|---|
| Privacy and fairness? | no personal data in the demo; segments checked: [result]; limits: [list] |
| What did you not do? | [honest list]; next step [x] |
| Where did the data and images come from? | [sources and licences] |

## Rules

- Answer in 20 to 30 seconds; give the number first, the reason second.
- If you do not know, say what you would check and how; never improvise a number.
- Keep backup slides for the three likeliest questions in an appendix after the closing slide.
- Agree who answers which kind of question before going on stage.
