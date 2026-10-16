---
title: "{{title_yaml}}"
subtitle: "<one line: what it does and for whom>"
event: demo-day
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <wow of the demo>, weight: 30}
  - {id: R2, text: <clarity of the problem>, weight: 25}
  - {id: R3, text: <technical depth>, weight: 25}
  - {id: R4, text: <completeness and next steps>, weight: 20}
---
# {{title}}
layout: cover_poster
eyebrow: <event name>
subtitle: <team name and track>
notes: <10 seconds: team and the one sentence promise>

---
# <The challenge as a how-might-we question>
layout: hmw
rubric: R2
question: <How might we help ... do ... without ...?>
notes: <20 seconds: who has this problem and why it is hard>
- Who | <the person and their situation>
- Constraint | <what makes it hard>
- Success | <what good looks like, measurable>

---
# <Solution as a takeaway: what changes for the user>
layout: solution
rubric: R2, R3
image: <path to a screenshot, optional>
notes: <25 seconds: what it does and the clever part>
<one line solution>
- <benefit 1>
- <benefit 2>
- <benefit 3>

---
# Demo: <the user goal> in <n> steps
layout: demo
rubric: R1
image: <path to a screenshot, the backup if the live demo fails>
notes: <60 seconds: do the live demo; say what you click before you click>
- <step 1>
- <step 2>
- <step 3>

---
# <Evidence as a takeaway: it works>
layout: kpi
rubric: R3, R4
source: <run log or file with these numbers>
notes: <20 seconds: measured how, against what>
- <number> | <metric> | <baseline or context>
- <number> | <metric> | <baseline or context>
- <number> | <metric> | <baseline or context>

---
# Try it, read it, build on it
layout: links
rubric: R4
cta: <one line: what you want the judges to do next>
notes: <15 seconds: where to find everything, then stop>
- Demo | <address> | <note>
- Code | <repository address> | <licence>
- Slides | <address> | <format>
