---
title: "{{title_yaml}}"
subtitle: "<course, assignment number>"
event: assignment
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <your name>
date: {{date}}
rubric:                  # copy every marking criterion from the handout, in its order
  - {id: R1, text: <criterion 1>, weight: 25}
  - {id: R2, text: <criterion 2>, weight: 25}
  - {id: R3, text: <criterion 3>, weight: 30}
  - {id: R4, text: <criterion 4>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <course name>
notes: <15 seconds: topic and what the audience will learn>

---
# What this presentation covers
layout: agenda
notes: <20 seconds: the agenda follows the marking criteria in order>
- <Part 1> | <what it answers>
- <Part 2> | <what it answers>
- <Part 3> | <what it answers>
- <Part 4> | <what it answers>

---
# <Requirements as a takeaway>
layout: bullets
rubric: R1
notes: <40 seconds>
<one-sentence summary of the task>
- <requirement or finding 1>
- <requirement or finding 2>
- <requirement or finding 3>

---
# <Method or design as a takeaway>
layout: pipeline
rubric: R2
notes: <60 seconds>
- <Step 1> | <caption>
- <Step 2> | <caption>
- <Step 3> | <caption>

---
# <Main result as a takeaway>
layout: chart_insight
rubric: R3
chart: bar
source: <file or log>
takeaway: <the so-what>
notes: <60 seconds>
| <Item> | <Value> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Comparison or evaluation as a takeaway>
layout: comparison
rubric: R3
highlight: 3
source: <file or log>
notes: <50 seconds>
| Aspect | <Option A> | <Option B> |
|---|---|---|
| <aspect> | <value> | **<value>** |

---
# <Conclusion as a takeaway, with limits>
layout: impact
rubric: R4
notes: <40 seconds>
## Done
- <what was achieved>
## Next
- <what remains>

---
# Questions?
layout: closing
notes: <10 seconds>
- <repo or report link>
