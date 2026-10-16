---
title: "{{title_yaml}}"
subtitle: "<one line: what happened and what we change>"
event: postmortem
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <facts and timeline>, weight: 30}
  - {id: R2, text: <root causes>, weight: 30}
  - {id: R3, text: <what went well>, weight: 15}
  - {id: R4, text: <actions with owners>, weight: 25}
---
# {{title}}
layout: title
eyebrow: <incident id> post-mortem
notes: <15 seconds: blameless format, scope, severity>

---
# <Summary as a takeaway: impact, cause, fix>
layout: exec_summary
rubric: R1
source: <incident record>
notes: <40 seconds: what users saw, for how long, what fixed it>
- Situation | <what users saw>
- Complication | <the cause>
- Resolution | <the fix>
<one line: the main lesson>

---
# <Timeline as a takeaway: detection took longer than the fix>
layout: timeline
rubric: R1
source: <incident log>
notes: <60 seconds: walk the timeline, mark detection and recovery>
- <time> | <event> | <detail>
- <time> | <event> | <detail>
- <time> | <event> | <detail>
- <time> | <event> | <detail>

---
# <Impact as a takeaway>
layout: chart_insight
rubric: R1
chart: area
source: <metrics export>
takeaway: <the so-what in one sentence>
notes: <40 seconds: error rate or latency during the incident>
| <Time> | <Value> |
|---|---|
| <t> | <n> |
| <t> | <n> |

---
# <Causes as a takeaway: three factors combined>
layout: matrix
rubric: R2, R3
notes: <60 seconds: one point per quadrant, no names>
## What went wrong
- <point>
## Why it was not caught
- <point>
## What went well
- <point>
## Where we got lucky
- <point>

---
# <Actions as a takeaway: owners and dates>
layout: kanban
rubric: R4
notes: <45 seconds: each action with an owner and a date>
## To do
- <action> | <owner>
## Doing
- <action> | <owner>
## Done
- <action> | <owner>

---
# <Prevention as a takeaway: how we will know next time>
layout: checklist
rubric: R4
notes: <30 seconds: monitors, tests and runbooks to add>
- <Safeguard> | <todo> | <owner or date>
- <Safeguard> | <todo> | <owner or date>
- <Safeguard> | <todo> | <owner or date>

---
# Questions?
layout: closing
notes: <10 seconds: where the full write-up lives>
- <address of the write-up>
- <contact>
