---
title: "{{title_yaml}}"
subtitle: "<role, city, specialty>"
event: portfolio
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <name>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <craft>, weight: 30}
  - {id: R2, text: <range>, weight: 25}
  - {id: R3, text: <process>, weight: 25}
  - {id: R4, text: <results>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <portfolio, year>
notes: <15 seconds: who you are and the one sentence promise>

---
# Hi, I <do what for whom>
layout: profile
rubric: R2
image: <path to a portrait>
email: <email>
web: <site>
notes: <45 seconds: who you are in one breath>
<bio in one or two sentences>
- Role | <role>
- Based in | <city>
- Experience | <years>

---
# What I work with
layout: skills
rubric: R2
notes: <30 seconds>
- <Skill> | 5
- <Skill> | 4
- <Skill> | 4

---
# <Career as a takeaway: from X to Y>
layout: timeline
rubric: R2, R3
notes: <60 seconds>
- <Year> | <Role> | <where and what>
- <Year> | <Role> | <where and what>
- <Year> | <Role> | <where and what>

---
# <Project name: outcome in a few words>
layout: case_header
rubric: R1
image: <path to a hero image>
role: <your role>
year: <year>
client: <client>
tools: <tool>, <tool>, <tool>
notes: <45 seconds: the brief and your part>
<one sentence on what the project did>

---
# <Screens as a takeaway: one flow>
layout: gallery
rubric: R1
notes: <45 seconds>
- <image path> | <caption>
- <image path> | <caption>
- <image path> | <caption>
- <image path> | <caption>

---
# <Before and after as a takeaway>
layout: before_after
rubric: R4
notes: <45 seconds: what you changed and the measured effect>
- <image path> | Before
- <image path> | After
<one line on the effect>

---
# <Client words>
layout: quote
rubric: R4
author: <name>
role: <role, company>
notes: <20 seconds>
> <testimonial>

---
# Let's work together
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
