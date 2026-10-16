---
title: "{{title_yaml}}"
subtitle: "<one line: who we sell to and how>"
event: go-to-market
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <target customer>, weight: 30}
  - {id: R2, text: <channels and pricing>, weight: 25}
  - {id: R3, text: <targets>, weight: 25}
  - {id: R4, text: <plan and owners>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <product> go-to-market
notes: <15 seconds: product, market and period>

---
# <Summary as a takeaway: one segment, two channels, one price>
layout: exec_summary
rubric: R1, R4
notes: <40 seconds: who, how, how much, by when>
- Situation | <where we are>
- Complication | <what blocks growth>
- Resolution | <the plan>
<one line ask>

---
# <Market size as a takeaway>
layout: market
rubric: R1
source: <market report or model>
notes: <35 seconds: how each number was built>
- TAM | <value> | <definition>
- SAM | <value> | <definition>
- SOM | <value> | <definition>

---
# <The customer we start with>
layout: persona
rubric: R1
name: <first name, age>
role: <role>
facts: <fact> | <fact> | <fact>
quote: <one line in the persona's words>
notes: <35 seconds: the buyer and the user, and what they care about>
## Goals
- <goal>
## Frustrations
- <frustration>
## Needs
- <need>

---
# <Pricing as a takeaway: one plan wins most deals>
layout: pricing
rubric: R2
highlight: 2
notes: <30 seconds: why this price>
- <Plan 1> | <price> | <feature>; <feature>
- <Plan 2> | <price> | <feature>; <feature>; <feature>
- <Plan 3> | <price> | <feature>; <feature>

---
# <Funnel as a takeaway: the trial step loses most prospects>
layout: funnel
rubric: R2, R3
source: <crm export>
notes: <40 seconds: stage by stage, where we focus>
- <Stage> | <n> | <note>
- <Stage> | <n> | <note>
- <Stage> | <n> | <note>
- <Stage> | <n> | <note>

---
# <Plan as a takeaway: launch in two quarters>
layout: gantt
rubric: R4
periods: Q1, Q2, Q3, Q4
notes: <35 seconds: milestones and owners>
- <Task> | 1 | 1 | <owner>
- <Task> | 1 | 2 | <owner>
- <Task> | 3 | 4 | <owner>

---
# <Targets as a takeaway: what success looks like>
layout: scorecard
rubric: R3
source: <plan file>
notes: <30 seconds: baseline and target for each metric>
- <Metric> | <actual> | <target> | <status> | <note>
- <Metric> | <actual> | <target> | <status> | <note>

---
# Decisions and next steps
layout: closing
notes: <20 seconds: what we need from the room>
- <decision needed>
- <contact>
