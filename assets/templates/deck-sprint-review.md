---
title: "{{title_yaml}}"
subtitle: "<one line: what we delivered this sprint>"
event: sprint-review
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <demo of done work>, weight: 35}
  - {id: R2, text: <metrics>, weight: 25}
  - {id: R3, text: <blockers>, weight: 20}
  - {id: R4, text: <next sprint>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <team> sprint <n> review
notes: <15 seconds: sprint goal and dates>

---
# <Numbers as a takeaway: what the sprint moved>
layout: kpi_table
rubric: R2
source: <tracker or analytics export>
notes: <40 seconds: the three metrics that moved most>
- <Metric> | <value> | <delta> | <status> | <note>
- <Metric> | <value> | <delta> | <status> | <note>
- <Metric> | <value> | <delta> | <status> | <note>

---
# Demo: <what is new> in <n> steps
layout: demo
rubric: R1
image: <path to a screenshot>
notes: <120 seconds: show the finished work, one story at a time>
- <step 1>
- <step 2>
- <step 3>

---
# <Board as a takeaway: what is done and what is carried over>
layout: kanban
rubric: R1
notes: <40 seconds: done, carried over, dropped>
## To do
- <story> | <owner>
## Doing
- <story> | <owner>
## Done
- <story> | <owner>

---
# <Trend as a takeaway: velocity or quality over sprints>
layout: chart_insight
rubric: R2
chart: line
source: <tracker export>
takeaway: <the so-what in one sentence>
notes: <40 seconds: the trend and the reason>
| <Sprint> | <Value> |
|---|---|
| <s> | <n> |
| <s> | <n> |

---
# <Blockers as a takeaway: two things we need help with>
layout: risk
rubric: R3
notes: <35 seconds: each blocker and who can unblock it>
- <Blocker> | <level> | <level> | <what we need>
- <Blocker> | <level> | <level> | <what we need>

---
# <Next sprint as a takeaway>
layout: roadmap
rubric: R4
notes: <30 seconds: the sprint goal and the top stories>
- Now | <goal> | <detail>
- Next | <story> | <detail>
- Later | <story> | <detail>

---
# Questions?
layout: closing
notes: <10 seconds>
- <where the board lives>
- <contact>
