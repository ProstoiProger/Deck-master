---
title: "{{title_yaml}}"
subtitle: "<project, client and year>"
event: case-study
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <name or team>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <problem framing>, weight: 25}
  - {id: R2, text: <process>, weight: 30}
  - {id: R3, text: <outcome>, weight: 30}
  - {id: R4, text: <role clarity>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <case study, year>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Project name: outcome in a few words>
layout: case_header
rubric: R4
image: <path to a hero image>
role: <your role>
year: <year>
client: <client>
tools: <tool>, <tool>
notes: <30 seconds>
<one sentence summary>

---
# <Problem as a takeaway: who struggled with what>
layout: problem
rubric: R1
stat: <number> | <what it measures>
source: <research, analytics or interview notes>
notes: <45 seconds>
<one sentence on why it mattered>
- <finding>

---
# <Process as a takeaway: four steps from insight to launch>
layout: process
rubric: R2
notes: <60 seconds>
- <Step> | <what you did> | <who>
- <Step> | <what you did> | <who>
- <Step> | <what you did> | <who>

---
# <Design as a takeaway>
layout: gallery
rubric: R2
notes: <45 seconds>
- <image path> | <caption>
- <image path> | <caption>
- <image path> | <caption>
- <image path> | <caption>

---
# <Redesign as a takeaway>
layout: before_after
rubric: R3
notes: <45 seconds>
- <image path> | Before
- <image path> | After
<one line on the effect>

---
# <Outcome as a takeaway>
layout: kpi
rubric: R3
source: <analytics file>
notes: <40 seconds>
- <number> | <metric> | <context>
- <number> | <metric> | <context>

---
# <Client words>
layout: quote
rubric: R3
author: <name>
role: <role, company>
notes: <20 seconds>
> <testimonial>

---
# Thank you
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
