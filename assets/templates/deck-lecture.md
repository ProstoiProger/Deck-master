---
title: "{{title_yaml}}"
subtitle: "<course, week and topic>"
event: lecture
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <lecturer>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <learning goals>, weight: 30}
  - {id: R2, text: <examples>, weight: 30}
  - {id: R3, text: <structure>, weight: 20}
  - {id: R4, text: <pacing>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <course, week>
notes: <15 seconds: who you are and the one sentence promise>

---
# What you will be able to do after this lecture
layout: agenda
rubric: R1
notes: <60 seconds: state the learning goals, then the order>
- <Goal 1> | <how you will practise it>
- <Goal 2>
- <Goal 3>

---
# <Part 1: the idea>
layout: section
number: 01
notes: <10 seconds>
<one line on what this part covers>

---
# <Idea as a takeaway sentence>
layout: bullets
rubric: R1
notes: <3 minutes: explain with one example>
<lede: the idea in one sentence>
- <point 1>
- <point 2>
- <point 3>

---
# <Formal definition in one line>
layout: equation
rubric: R2
math: <LaTeX>
notes: <3 minutes: derive or motivate it>
<one line of intuition>
- <symbol> | <meaning>
- <symbol> | <meaning>

---
# <Example as a takeaway>
layout: figure
rubric: R2
chart: bar
source: <data or textbook page>
caption: <caption>
notes: <3 minutes: walk through the example>
- <what to notice>
| <Item> | <Value> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Three approaches compared>
layout: columns
rubric: R3
notes: <2 minutes: when to use which>
## <Approach A>
- <point>
## <Approach B>
- <point>
## <Approach C>
- <point>

---
# <A quote worth remembering>
layout: quote
author: <name>
role: <source>
notes: <30 seconds>
> <quote>

---
# Summary and what to read next
layout: references
rubric: R4
notes: <60 seconds: recap the goals, assign the reading>
- <Author (year). Title.>
- <Author (year). Title.>

---
# Questions?
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
