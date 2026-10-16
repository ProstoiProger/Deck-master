---
title: "{{title_yaml}}"
subtitle: "<period and unit under review>"
event: business-review
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <owner, unit>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <clear decision>, weight: 30}
  - {id: R2, text: <evidence>, weight: 30}
  - {id: R3, text: <risks>, weight: 20}
  - {id: R4, text: <next steps>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <period, unit, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Recommendation as a sentence: what you decide today>
layout: exec_summary
rubric: R1
source: <report or dashboard the numbers come from>
notes: <60 seconds: the decision first, the reasons second>
- Situation | <what happened this period>
- Complication | <what is off plan and why>
- Resolution | <what you propose>
<the decision you need, with an amount and a date>

---
# <N> of <M> KPIs are on track
layout: scorecard
rubric: R2
source: <bi export or spreadsheet>
notes: <90 seconds: only the red and amber rows deserve words>
- <Metric> | <actual> | <target> | green | <short reason>
- <Metric> | <actual> | <target> | amber | <short reason>
- <Metric> | <actual> | <target> | red | <short reason>

---
# <Main trend as a takeaway>
layout: chart_insight
rubric: R2
chart: line
source: <data file>
takeaway: <the so-what in one sentence>
notes: <60 seconds: what changed and since when>
| Period | <Series A> | <Series B> |
|---|---|---|
| <p1> | <n> | <n> |
| <p2> | <n> | <n> |
| <p3> | <n> | <n> |

---
# <Headline numbers as a takeaway>
layout: kpi
rubric: R2
source: <data file>
notes: <40 seconds: compare each to plan or last period>
- <number> | <metric> | <context>
- <number> | <metric> | <context>
- <number> | <metric> | <context>

---
# <N> risks need an owner this month
layout: risk
rubric: R3
notes: <60 seconds: say who owns each and by when>
- <Risk> | medium | high | <mitigation and owner>
- <Risk> | low | high | <mitigation and owner>
- <Risk> | high | medium | <mitigation and owner>

---
# <Plan as a takeaway: what lands in which quarter>
layout: gantt
rubric: R4
periods: Q1, Q2, Q3, Q4
notes: <45 seconds: dependencies and the first milestone>
- <Task> | 1 | 1 | <owner>
- <Task> | 1 | 2 | <owner>
- <Task> | 3 | 4 | <owner>

---
# Decisions needed
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
