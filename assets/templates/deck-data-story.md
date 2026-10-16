---
title: "{{title_yaml}}"
subtitle: "<one line: the question and the headline answer>"
event: data-story
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <insight quality>, weight: 30}
  - {id: R2, text: <method soundness>, weight: 25}
  - {id: R3, text: <business value>, weight: 25}
  - {id: R4, text: <clarity and reproducibility>, weight: 20}
---
# {{title}}
layout: cover_split
eyebrow: <event or audience>
subtitle: <the question and the headline answer in one line>
notes: <15 seconds: the question and the answer in one breath>

---
# <The decision that needs data>
layout: statement
rubric: R3
source: <data file or brief page>
notes: <30 seconds: who decides what with this analysis>
- <lead-in> | <the key number or phrase> | <what it means for the decision>

---
# <Data and checks as a takeaway: why the numbers can be trusted>
layout: schema
rubric: R2, R4
relations: <table.key -> table.key>
notes: <35 seconds: where the data comes from, cleaning, joins, leakage checks>
## <table one>
- <column> | <type> | primary key
- <column> | <type>
## <table two>
- <column> | <type> | foreign key
- <column> | <type>

---
# <Three findings explain most of the outcome>
layout: insight_cards
rubric: R1, R3
source: <notebook or analysis file>
notes: <45 seconds: read the three findings left to right, then the actions>
- <Finding> | <number> | <what the number measures> | <action>
- <Finding> | <number> | <what the number measures> | <action>
- <Finding> | <number> | <what the number measures> | <action>

---
# <Finding 1 as a takeaway sentence>
layout: chart_insight
rubric: R1
chart: bar
source: <file with the numbers>
takeaway: <the so-what in one sentence>
notes: <40 seconds: read the chart, name the effect and its size>
| <Category> | <Value> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Finding 2 as a takeaway sentence>
layout: chart_insight
rubric: R1
chart: lollipop
source: <file with the numbers>
takeaway: <the so-what in one sentence>
notes: <40 seconds: what drives the outcome most>
| <Driver> | <Importance> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Model result as a takeaway: it beats the baseline on held-out data>
layout: model_card
rubric: R2
source: <evaluation file>
notes: <40 seconds: facts, metrics, then the limits>
## Facts
- Task | <what it predicts>
- Model | <type and size>
- Data | <rows and period>
- Split | <how it was split>
## Metrics
- <metric> | <value> | <split>
- <metric> | <value> | <split>
## Limits
- <where it fails>

---
# <Limits and recommendation>
layout: impact
rubric: R2, R3
notes: <30 seconds: what we can claim, what we cannot, what to do next>
## What we can claim
- <claim>
## What we cannot claim
- <limit>

---
# Reproduce it and read the code
layout: links
rubric: R4
notes: <10 seconds: where the notebook and the data card live>
- Notebook | <address> | <runtime>
- Data card | <address> | <licence>
- Slides | <address> | <format>
