---
title: "{{title_yaml}}"
subtitle: "<one line: what we learned and what to change>"
event: ux-research
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <method>, weight: 20}
  - {id: R2, text: <insights>, weight: 30}
  - {id: R3, text: <evidence>, weight: 25}
  - {id: R4, text: <recommendations>, weight: 25}
---
# {{title}}
layout: title
eyebrow: <study name> research readout
notes: <15 seconds: the question and the method in one sentence>

---
# <The research question>
layout: hmw
rubric: R1
question: <How might we ...?>
notes: <30 seconds: why this question, who took part, how many sessions>
- Who | <participants and how they were recruited>
- Constraint | <method limits, sample size>
- Success | <the decision this research informs>

---
# <Who we studied>
layout: persona
rubric: R1
name: <first name, age>
role: <role or situation>
facts: <fact> | <fact> | <fact>
quote: <one line from a session>
notes: <30 seconds: the main user type the data points to>
## Goals
- <goal>
## Frustrations
- <frustration>
## Needs
- <need>

---
# <Journey as a takeaway: the journey breaks at one step>
layout: journey
rubric: R2
notes: <45 seconds: walk the stages, show the low point>
- <Stage> | <what the user does> | <1 to 5> | <opportunity>
- <Stage> | <what the user does> | <1 to 5> | <opportunity>
- <Stage> | <what the user does> | <1 to 5> | <opportunity>
- <Stage> | <what the user does> | <1 to 5> | <opportunity>

---
# <Three insights explain most of the friction>
layout: insight_cards
rubric: R2, R3
source: <study notes or analytics>
notes: <45 seconds: each insight with its evidence>
- <Insight> | <number> | <what the number measures> | <change to make>
- <Insight> | <number> | <what the number measures> | <change to make>
- <Insight> | <number> | <what the number measures> | <change to make>

---
# <In their words>
layout: quote
rubric: R3
author: <participant label, not a real name>
role: <context>
notes: <20 seconds: why this quote matters>
> <quote from a session>

---
# <Task success as a takeaway>
layout: kpi
rubric: R3
source: <usability test results>
notes: <30 seconds: how it was measured>
- <number> | <metric> | <context>
- <number> | <metric> | <context>
- <number> | <metric> | <context>

---
# <Recommendations as a takeaway: fix three things first>
layout: checklist
rubric: R4
notes: <40 seconds: priority and owner for each>
- <Change> | <todo> | <owner or date>
- <Change> | <todo> | <owner or date>
- <Change> | <todo> | <owner or date>

---
# <Next steps as a takeaway>
layout: roadmap
rubric: R4
notes: <25 seconds: what we test next>
- Now | <step> | <detail>
- Next | <step> | <detail>
- Later | <step> | <detail>

---
# Questions?
layout: closing
notes: <10 seconds>
- <where the full report lives>
- <contact>
