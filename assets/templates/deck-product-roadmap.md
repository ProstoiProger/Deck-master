---
title: "{{title_yaml}}"
subtitle: "<one line: the year in one sentence>"
event: product-roadmap
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <alignment with goals>, weight: 30}
  - {id: R2, text: <clarity of priorities>, weight: 25}
  - {id: R3, text: <feasibility>, weight: 25}
  - {id: R4, text: <risks and dependencies>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <period> roadmap
notes: <15 seconds: scope of the roadmap and who it is for>

---
# <Summary as a takeaway: what we will ship and why>
layout: exec_summary
rubric: R1
notes: <40 seconds: situation, what we will do, what we ask>
- Situation | <where we are>
- Complication | <what blocks us>
- Resolution | <the plan>
<one line recommendation or decision needed>

---
# <Goals as a takeaway: the outcomes the roadmap serves>
layout: okr
rubric: R1
source: <OKR file>
notes: <40 seconds: each objective and its key results>
## <Objective one>
- <Key result> | <current> | <target>
- <Key result> | <current> | <target>
## <Objective two>
- <Key result> | <current> | <target>
- <Key result> | <current> | <target>

---
# <Priorities as a takeaway: three bets this period>
layout: roadmap
rubric: R2
notes: <40 seconds: the order and why>
- Now | <bet one> | <detail>
- Next | <bet two> | <detail>
- Later | <bet three> | <detail>

---
# <The plan fits in the period>
layout: gantt
rubric: R3
periods: Q1, Q2, Q3, Q4
notes: <40 seconds: dependencies and owners>
- <Task> | 1 | 2 | <owner>
- <Task> | 2 | 3 | <owner>
- <Task> | 3 | 4 | <owner>

---
# <Work in flight as a takeaway: where the board stands>
layout: kanban
rubric: R3
notes: <30 seconds: what is done, what is moving, what waits>
## To do
- <task> | <owner>
## Doing
- <task> | <owner>
## Done
- <task> | <owner>

---
# <Risks as a takeaway: three risks need an owner>
layout: risk
rubric: R4
notes: <30 seconds: each risk and its mitigation>
- <Risk> | <level> | <level> | <mitigation>
- <Risk> | <level> | <level> | <mitigation>

---
# <Success metrics as a takeaway: how we will know>
layout: kpi_table
rubric: R1, R4
source: <metrics file>
notes: <30 seconds: baseline and target for each metric>
- <Metric> | <value> | <delta> | <status> | <note>
- <Metric> | <value> | <delta> | <status> | <note>

---
# Decisions we need today
layout: closing
notes: <20 seconds: the asks and the date for the next review>
- <decision needed>
- <contact>
