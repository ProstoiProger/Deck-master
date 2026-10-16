---
title: "{{title_yaml}}"
subtitle: "<decision the proposal supports>"
event: strategy-proposal
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <author, sponsor>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <recommendation>, weight: 25}
  - {id: R2, text: <logic>, weight: 25}
  - {id: R3, text: <evidence>, weight: 20}
  - {id: R4, text: <feasibility>, weight: 15}
  - {id: R5, text: <risks>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <client, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# <We should do X because Y>
layout: exec_summary
rubric: R1
source: <analysis file>
notes: <90 seconds: answer first, then the three reasons>
- Situation | <context the audience agrees with>
- Complication | <the problem or opportunity>
- Resolution | <your recommendation>
<the ask: decision, budget, date>

---
# <Where we stand: strengths outweigh threats, or not>
layout: matrix
rubric: R2
notes: <60 seconds: pick one item in each box that drives the choice>
## Strengths
- <item>
## Weaknesses
- <item>
## Opportunities
- <item>
## Threats
- <item>

---
# We can win <SOM> in <n> years
layout: market
rubric: R3
source: <market model>
notes: <60 seconds: assumptions behind each circle>
- TAM | <value> | <definition>
- SAM | <value> | <definition>
- SOM | <value> | <definition>

---
# <Options compared as a takeaway: option B fits best>
layout: feature_matrix
rubric: R2
highlight: 3
notes: <60 seconds: the criteria and how they were weighted>
| Criterion | <Option A> | <Option B> | <Option C> |
|---|---|---|---|
| <criterion> | no | yes | partial |
| <criterion> | yes | yes | no |

---
# <Steps from decision to result>
layout: process
rubric: R4
notes: <45 seconds: owners and hand-offs>
- <Step> | <what happens> | <owner>
- <Step> | <what happens> | <owner>
- <Step> | <what happens> | <owner>

---
# <Plan as a takeaway: first value in n months>
layout: gantt
rubric: R4
periods: <P1>, <P2>, <P3>, <P4>
notes: <45 seconds: the critical path>
- <Task> | 1 | 1 | <owner>
- <Task> | 2 | 3 | <owner>
- <Task> | 4 | 4 | <owner>

---
# <N> risks and how we hold them
layout: risk
rubric: R5
notes: <45 seconds: the one risk that could stop the plan>
- <Risk> | medium | high | <mitigation>
- <Risk> | low | medium | <mitigation>

---
# How we will know it works
layout: scorecard
rubric: R3
source: <baseline file>
notes: <40 seconds: baseline, target and the review date>
- <Metric> | <baseline> | <target> | amber | <how measured>
- <Metric> | <baseline> | <target> | amber | <how measured>

---
# Decision and next step
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
