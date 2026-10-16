---
title: "{{title_yaml}}"
subtitle: "<one line: the question and the headline finding>"
event: data-viz-report
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <insight quality>, weight: 30}
  - {id: R2, text: <visual clarity>, weight: 25}
  - {id: R3, text: <method soundness>, weight: 20}
  - {id: R4, text: <actionability>, weight: 25}
---
# {{title}}
layout: cover_split
eyebrow: <event or audience>
subtitle: <the question and the headline answer in one line>
notes: <15 seconds: the question and the answer in one breath>

---
# <The finding in one sentence>
layout: statement
rubric: R1
source: <data file>
notes: <30 seconds: the number that frames the report>
- <lead-in> | <key number or phrase> | <what it means>

---
# <Dashboard as a takeaway: the picture in six tiles>
layout: bento
rubric: R1, R2
source: <data file>
notes: <45 seconds: big number first, then trend, rate and note>
- stat | <number> | <what it measures> | <context>
- spark | <label> | <n>,<n>,<n>,<n>,<n> | <latest value>
- ring | <percent> | <label> | <target>
- bars | <label> | <n>,<n>,<n>,<n> | <note>
- text | <headline> | <one sentence>

---
# <Composition as a takeaway: where the volume sits>
layout: treemap
rubric: R1
source: <data file>
notes: <40 seconds: the biggest areas and what they have in common>
- <Name> | <value>
- <Name> | <value>
- <Name> | <value>
- <Name> | <value>

---
# <Flow as a takeaway: where people drop out>
layout: sankey
rubric: R1, R3
source: <data file>
notes: <45 seconds: follow the widest band, then the leaks>
- <Source> | <Target> | <value>
- <Source> | <Target> | <value>
- <Source> | <Target> | <value>

---
# <Rhythm as a takeaway: when activity happens>
layout: activity_grid
rubric: R2
source: <data file>
values: <seven numbers per week, comma separated>
caption: <what one square means>
notes: <35 seconds: the busiest and quietest periods>
- <number> | <label>
- <number> | <label>

---
# <Goals as a takeaway: how close the numbers are>
layout: gauges
rubric: R3
source: <data file>
notes: <35 seconds: each gauge against its goal>
- <Metric> | <value> | <maximum> | <note>
- <Metric> | <value> | <maximum> | <note>
- <Metric> | <value> | <maximum> | <note>

---
# <Actions as a takeaway: three findings, three moves>
layout: insight_cards
rubric: R4
source: <data file>
notes: <45 seconds: finding, evidence, action for each card>
- <Finding> | <number> | <what the number measures> | <action>
- <Finding> | <number> | <what the number measures> | <action>
- <Finding> | <number> | <what the number measures> | <action>

---
# Reproduce it
layout: links
rubric: R3
notes: <10 seconds: notebook, data card, slides>
- Notebook | <address> | <runtime>
- Data card | <address> | <licence>
- Slides | <address> | <format>
