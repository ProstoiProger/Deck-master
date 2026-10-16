---
title: "{{title_yaml}}"
subtitle: "<programme name and amount requested>"
event: grant-proposal
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <applicant organisation>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <need>, weight: 25}
  - {id: R2, text: <impact>, weight: 25}
  - {id: R3, text: <feasibility>, weight: 20}
  - {id: R4, text: <budget>, weight: 15}
  - {id: R5, text: <team>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <funder, programme, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# <The need as a takeaway: who is affected and how many>
layout: problem
rubric: R1
stat: <number> | <people or area affected>
source: <official statistics, survey or study>
notes: <45 seconds: the human side first, then the number>
<one sentence on why current efforts fall short>
- <evidence 1>

---
# <One number that makes the case>
layout: big_number
rubric: R1
source: <statistic source>
stat: <number> | <what it means>
notes: <30 seconds>
- <supporting point>
- <supporting point>

---
# <Our approach as a takeaway>
layout: solution
rubric: R2
notes: <45 seconds: what you will do and why it works here>
<one line approach>
- <activity 1>
- <activity 2>
- <activity 3>

---
# <Steps from funding to results>
layout: process
rubric: R3
notes: <45 seconds>
- <Phase> | <what happens> | <who>
- <Phase> | <what happens> | <who>
- <Phase> | <what happens> | <who>

---
# <Work plan as a takeaway: done in n months>
layout: gantt
rubric: R3
periods: <P1>, <P2>, <P3>, <P4>
notes: <45 seconds: milestones tied to reports to the funder>
- <Activity> | 1 | 2 | <owner>
- <Activity> | 2 | 3 | <owner>
- <Activity> | 4 | 4 | <owner>

---
# How we will measure success
layout: scorecard
rubric: R2
source: <baseline survey>
notes: <45 seconds: baseline, target and how you will collect the data>
- <Indicator> | <baseline> | <target> | amber | <method>
- <Indicator> | <baseline> | <target> | amber | <method>

---
# Where the money goes
layout: pricing
rubric: R4
notes: <40 seconds: share of the budget per line; co-funding if any>
- <Budget line> | <amount> | <what it covers>
- <Budget line> | <amount> | <what it covers>
- <Budget line> | <amount> | <what it covers>

---
# <N> risks and how we reduce them
layout: risk
rubric: R3
notes: <30 seconds>
- <Risk> | medium | high | <mitigation>
- <Risk> | low | medium | <mitigation>

---
# <Team as a takeaway: who delivers>
layout: team
rubric: R5
notes: <30 seconds>
- <Name> | <Role> | <relevant experience>
- <Name> | <Role> | <relevant experience>

---
# Thank you
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
