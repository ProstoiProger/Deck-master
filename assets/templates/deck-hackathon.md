---
title: "{{title_yaml}}"
subtitle: "<one line: what it does and for whom>"
event: hackathon
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team name>
date: {{date}}
rubric:                  # copy the judging criteria from the rules page; weights if given
  - {id: R1, text: <impact>, weight: 30}
  - {id: R2, text: <innovation>, weight: 20}
  - {id: R3, text: <feasibility>, weight: 25}
  - {id: R4, text: <demo and user experience>, weight: 25}
---
# {{title}}
layout: title
eyebrow: <event name>
notes: <15 seconds: team, the one sentence promise>

---
# <Problem as a takeaway: who loses what, how much>
layout: problem
rubric: R1
stat: <number> | <what the number measures>
source: <where the number comes from: file, page, run log>
notes: <20 seconds: the pain in the user's words>
<one sentence on why today's way fails>
- <evidence 1>
- <evidence 2>

---
# <Solution as a takeaway: what changes for the user>
layout: solution
rubric: R1, R2
image: <path to a product screenshot, optional>
notes: <25 seconds: what it does and what is new about it>
<one line solution>
- <benefit 1>
- <benefit 2>
- <benefit 3>

---
# <How it works in three layers>
layout: architecture
rubric: R3
notes: <25 seconds: only the parts that make it feasible>
- <Layer>: <component>, **<key component>**, <component>
- <Layer>: <component>, <component>

---
# Demo: <the user goal> in <n> steps
layout: demo
rubric: R4
image: <path to a screenshot>
notes: <45 seconds: do the live demo; this is the backup if it fails>
- <step 1>
- <step 2>
- <step 3>

---
# <Evidence as a takeaway: it works>
layout: kpi
rubric: R1, R3
source: <run log or file with these numbers>
notes: <25 seconds: measured how, against what baseline>
- <number> | <metric> | <baseline or context>
- <number> | <metric> | <baseline or context>
- <number> | <metric> | <baseline or context>

---
# <Next steps as a takeaway: path to real users>
layout: roadmap
rubric: R1, R3
notes: <20 seconds: what is needed to pilot>
- Now | <milestone> | <detail>
- Next | <milestone> | <detail>
- Later | <milestone> | <detail>

---
# Questions?
layout: closing
notes: <10 seconds: thank the jury, point to the code and the demo>
- <repo link>
- <contact>
