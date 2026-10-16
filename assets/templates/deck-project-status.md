---
title: "{{title_yaml}}"
subtitle: "<project name and reporting period>"
event: project-status
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <project lead>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <progress>, weight: 40}
  - {id: R2, text: <risks>, weight: 30}
  - {id: R3, text: <decisions needed>, weight: 30}
---
# {{title}}
layout: title
eyebrow: <project, period>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Status as a sentence: on track, at risk or late, and why>
layout: exec_summary
rubric: R1
source: <tracker export>
notes: <45 seconds: colour first, reason second>
- Situation | <where the project is>
- Complication | <what slipped or is at risk>
- Resolution | <what we do about it>
<the decision or help you need>

---
# <N> of <M> milestones are on track
layout: scorecard
rubric: R1
source: <tracker export>
notes: <60 seconds: red and amber rows only>
- <Milestone or metric> | <actual> | <target> | green | <note>
- <Milestone or metric> | <actual> | <target> | amber | <note>
- <Milestone or metric> | <actual> | <target> | red | <note>

---
# <Plan as a takeaway: what finishes when>
layout: gantt
rubric: R1
periods: <P1>, <P2>, <P3>, <P4>
notes: <45 seconds: what moved since the last report>
- <Task> | 1 | 2 | <owner>
- <Task> | 2 | 3 | <owner>
- <Task> | 4 | 4 | <owner>

---
# <N> risks need your attention
layout: risk
rubric: R2
notes: <45 seconds: owner and date for each>
- <Risk> | medium | high | <mitigation, owner>
- <Risk> | high | medium | <mitigation, owner>

---
# Decisions needed
layout: closing
rubric: R3
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
