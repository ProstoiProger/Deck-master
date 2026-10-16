---
title: "{{title_yaml}}"
subtitle: "<degree, programme, supervisor>"
event: thesis-defense
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <author>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <relevance>, weight: 20}
  - {id: R2, text: <method>, weight: 25}
  - {id: R3, text: <results>, weight: 30}
  - {id: R4, text: <contribution>, weight: 25}
---
# {{title}}
layout: title
eyebrow: <university, programme, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# What this talk covers
layout: agenda
notes: <15 seconds>
- Problem
- Method
- Results
- Contribution

---
# <Research gap as a takeaway>
layout: problem
rubric: R1
stat: <number> | <size of the gap>
source: <paper, table or standard>
notes: <60 seconds: motivation and the question you answer>
<the research question in one sentence>
- <what prior work does not do>

---
# <Hypotheses and what the data says>
layout: hypotheses
rubric: R2
source: <results file>
notes: <60 seconds: state each hypothesis before the result>
<research question>
- H1 | <statement> | supported
- H2 | <statement> | supported
- H3 | <statement> | open

---
# <Method in one sentence>
layout: pipeline
rubric: R2
notes: <90 seconds: only what is needed to trust the results>
- <Step 1> | <caption>
- <Step 2> | <caption>
- <Step 3> | <caption>

---
# <Data used in the study>
layout: factsheet
rubric: R2
source: <dataset card>
notes: <45 seconds: size, period, target and split>
<one line on limitations>
- Rows | <n>
- Period | <dates>
- Target | <variable>
- Split | <how train and test were separated>

---
# <Main result as a takeaway>
layout: figure
rubric: R3
chart: line
source: <experiment file>
caption: <what the figure shows, with the unit>
notes: <90 seconds: effect size and uncertainty>
- <observation 1>
- <observation 2>
| <X> | <Ours> | <Baseline> |
|---|---|---|
| <x1> | <n> | <n> |
| <x2> | <n> | <n> |
| <x3> | <n> | <n> |

---
# <Comparison with prior work>
layout: comparison
rubric: R3
highlight: 4
source: <experiment file>
notes: <60 seconds: seeds, tests, intervals>
| Dataset | <Baseline A> | <Baseline B> | Ours |
|---|---|---|---|
| <d1> | <n> | <n> | **<n>** |

---
# <Contribution and limits>
layout: impact
rubric: R4
notes: <60 seconds: what is new, what is not shown>
## Contribution
- <contribution>
## Limits
- <limit>

---
# References
layout: references
notes: <skip: leave on screen for questions>
- <Author (year). Title. Venue.>
- <Author (year). Title. Venue.>

---
# Questions?
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
