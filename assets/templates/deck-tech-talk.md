---
title: "{{title_yaml}}"
subtitle: "<talk topic and the take-away>"
event: tech-talk
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <speaker>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <clarity>, weight: 30}
  - {id: R2, text: <technical depth>, weight: 30}
  - {id: R3, text: <demo>, weight: 20}
  - {id: R4, text: <take-aways>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <event, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# What we will cover
layout: agenda
notes: <15 seconds>
- Problem
- Design
- Demo
- Lessons

---
# <Problem as a takeaway: what broke or hurt>
layout: problem
rubric: R1
stat: <number> | <what it measures>
source: <incident report, benchmark or log>
notes: <90 seconds>
<one sentence>
- <evidence>

---
# <Design in layers>
layout: architecture
rubric: R2
notes: <3 minutes: follow one request through the layers>
- <Layer>: <component>, **<key component>**, <component>
- <Layer>: <component>, <component>

---
# Boring technology, on purpose
layout: tech_stack
rubric: R2
notes: <60 seconds: why each choice>
- Language: <a>, <b>
- Data: <a>, <b>
- Cloud: <a>, <b>

---
# Demo: <goal> in <n> steps
layout: demo
rubric: R3
image: <path to a screenshot>
notes: <4 minutes: live demo; this is the backup>
- <step 1>
- <step 2>
- <step 3>

---
# <Benchmark as a takeaway>
layout: chart_insight
rubric: R2
chart: hbar
source: <benchmark file>
takeaway: <so-what in one sentence>
notes: <2 minutes: setup and caveats>
| Variant | <Metric> |
|---|---|
| <baseline> | <n> |
| <ours> | <n> |

---
# <Trade-offs against the alternatives>
layout: comparison
rubric: R2
highlight: 3
source: <benchmark file>
notes: <2 minutes>
| Metric | <Alternative> | Ours |
|---|---|---|
| <metric> | <n> | **<n>** |

---
# <Lessons and what is next>
layout: roadmap
rubric: R4
notes: <90 seconds>
- Now | <lesson or milestone> | <detail>
- Next | <milestone> | <detail>
- Later | <milestone> | <detail>

---
# Questions?
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
