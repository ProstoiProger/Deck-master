---
title: "{{title_yaml}}"
subtitle: "<one line: what it does, for whom, why now>"
event: investor-pitch
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <company and founders>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <problem size>, weight: 20}
  - {id: R2, text: <market>, weight: 20}
  - {id: R3, text: <traction>, weight: 25}
  - {id: R4, text: <team>, weight: 15}
  - {id: R5, text: <the ask>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <company, round, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Problem as a takeaway: who loses how much money or time>
layout: problem
rubric: R1
stat: <number> | <what it measures>
source: <study, survey or your own data file>
notes: <30 seconds: the pain in the customer's words>
<one sentence on why today's way fails>
- <evidence 1>

---
# <Solution as a takeaway: what changes for the customer>
layout: solution
rubric: R1
image: <path to a product screenshot, optional>
notes: <30 seconds: what it does and why it is hard to copy>
<one line solution>
- <benefit 1>
- <benefit 2>
- <benefit 3>

---
# We can win <SOM> in year three
layout: market
rubric: R2
source: <market report or your bottom-up calculation>
notes: <40 seconds: how the three numbers were built, bottom-up first>
- TAM | <value> | <who is included>
- SAM | <value> | <the part you can serve>
- SOM | <value> | <the part you win in three years>

---
# <Traction as a takeaway: customers are already paying>
layout: funnel
rubric: R3
source: <CRM export or analytics file>
notes: <40 seconds: what each stage means, where the biggest drop is and what you do about it>
- <Stage 1> | <number> | <note>
- <Stage 2> | <number> | <note>
- <Stage 3> | <number> | <note>
- <Stage 4> | <number> | <note>

---
# <Pricing as a takeaway: how revenue grows with the customer>
layout: pricing
rubric: R2
highlight: 2
notes: <30 seconds: why the middle plan carries most revenue>
- <Plan 1> | <price> | <feature>; <feature>
- <Plan 2> | <price> | <feature>; <feature>; <feature>
- <Plan 3> | <price> | <feature>; <feature>

---
# We cover what the alternatives miss
layout: feature_matrix
rubric: R2
highlight: 4
notes: <30 seconds: pick the two rows that decide a purchase>
| Feature | <Competitor A> | <Competitor B> | Us |
|---|---|---|---|
| <capability> | no | yes | yes |
| <capability> | partial | yes | yes |
| <capability> | no | no | yes |

---
# <Milestones as a takeaway: what the money buys in 18 months>
layout: roadmap
rubric: R5
notes: <30 seconds: tie each milestone to a number you will report>
- Now | <milestone> | <detail>
- Next | <milestone> | <detail>
- Later | <milestone> | <detail>

---
# <Team as a takeaway: we have done this before>
layout: team
rubric: R4
notes: <30 seconds: why this team, in one fact per person>
- <Name> | <Role> | <one proof point>
- <Name> | <Role> | <one proof point>
- <Name> | <Role> | <one proof point>

---
# We are raising <amount> to reach <milestone>
layout: exec_summary
rubric: R5
source: <financial model>
notes: <30 seconds: the ask, the use of funds and the date by which you want an answer>
- Situation | <where the company is today>
- Complication | <what blocks faster growth>
- Resolution | <what the funds change>
<the ask in one sentence: amount, use, timing>

---
# Questions?
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
