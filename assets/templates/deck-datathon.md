---
title: "{{title_yaml}}"
subtitle: "<one line: the question and the headline answer>"
event: datathon
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team name>
date: {{date}}
rubric:
  - {id: R1, text: <insight quality>, weight: 30}
  - {id: R2, text: <method soundness>, weight: 25}
  - {id: R3, text: <business value>, weight: 25}
  - {id: R4, text: <clarity>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <event name>
notes: <15 seconds: the question and the answer in one breath>

---
# <Problem as a takeaway: the decision that needs data>
layout: problem
rubric: R3
stat: <number> | <what it measures>
source: <data file or brief page>
notes: <30 seconds: who decides what with this analysis>
<the question, in the stakeholder's words>
- <data size and span>
- <unit of analysis>

---
# <Data and checks as a takeaway: why the numbers can be trusted>
layout: pipeline
rubric: R2
source: <notebook or data card>
notes: <30 seconds: cleaning, joins, split, leakage checks>
- <Clean> | <what was removed>
- <Join> | <what was joined>
- <Split> | <how it was split>
- <Model or test> | <method>
<one line on the strongest validity check>

---
# <Finding 1 as a takeaway sentence>
layout: chart_insight
rubric: R1
chart: bar
source: <file with the numbers>
takeaway: <the so-what in one sentence>
notes: <40 seconds: read the chart, name the effect and its size>
- <detail or interval>
| <Category> | <Value> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Finding 2 as a takeaway sentence>
layout: chart_insight
rubric: R1
chart: hbar
source: <file with the numbers>
takeaway: <the so-what in one sentence>
notes: <40 seconds>
| <Driver> | <Importance> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Method result as a takeaway: ours beats the baseline>
layout: comparison
rubric: R2
highlight: 3
source: <evaluation file>
notes: <35 seconds: metric, split, uncertainty>
| Metric | Baseline | Ours |
|---|---|---|
| <metric> | <n> | **<n>** |

---
# <Business value as a takeaway: what the decision is worth>
layout: kpi
rubric: R3
source: <impact estimate file>
notes: <35 seconds: assumptions behind the estimate>
- <number> | <metric> | <interval or assumption>
- <number> | <metric> | <interval or assumption>
<one line on the main assumption>

---
# <Limits and recommendation>
layout: impact
rubric: R2, R3
notes: <30 seconds: what we cannot claim, what to do next>
## What we can claim
- <claim>
## What we cannot claim
- <limit>

---
# Questions?
layout: closing
rubric: R4
notes: <10 seconds>
- <repo link>
- <contact>
