---
title: "{{title_yaml}}"
subtitle: "<one line: the technology and what it makes possible>"
event: tech-showcase
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <vision>, weight: 25}
  - {id: R2, text: <technical credibility>, weight: 30}
  - {id: R3, text: <visual clarity>, weight: 20}
  - {id: R4, text: <proof>, weight: 25}
---
# {{title}}
layout: cover_poster
eyebrow: <event or product name>
subtitle: <one line: what it is and who it is for>
notes: <15 seconds: the promise in one breath>

---
# <A fact that frames the opportunity>
layout: statement
rubric: R1
source: <where the fact comes from>
notes: <30 seconds: why this matters now>
- <lead-in> | <key number or phrase> | <what it means>

---
# <The idea as a takeaway: what the object stands for>
layout: hero_3d
rubric: R1, R3
object: <orbs, ring, cube or stack>
notes: <35 seconds: one picture of the idea>
<one line idea>
- <point 1>
- <point 2>
- <point 3>

---
# <Architecture as a takeaway: layers you can replace>
layout: iso_stack
rubric: R2
highlight: 2
notes: <45 seconds: walk the layers from the user down>
- <Layer> | <what it does>
- <Layer> | <what it does>
- <Layer> | <what it does>
- <Layer> | <what it does>

---
# <Dashboard as a takeaway: the system at a glance>
layout: bento
rubric: R3, R4
source: <metrics file>
notes: <45 seconds: the big number first, then the small tiles>
- stat | <number> | <what it measures> | <context>
- spark | <label> | <n>,<n>,<n>,<n>,<n> | <latest value>
- ring | <percent> | <label> | <target>
- bars | <label> | <n>,<n>,<n>,<n> | <note>
- text | <headline> | <one sentence>

---
# <Reach as a takeaway: where it already runs>
layout: globe
rubric: R4
lat0: 30
lon0: 60
arcs: yes
notes: <35 seconds: the regions and what each proves>
- <Place> | <note> | <latitude> | <longitude>
- <Place> | <note> | <latitude> | <longitude>
- <Place> | <note> | <latitude> | <longitude>

---
# <Service levels as a takeaway: how close to the goals>
layout: gauges
rubric: R2, R4
source: <service report>
notes: <35 seconds: each gauge against its goal>
- <Metric> | <value> | <maximum> | <note>
- <Metric> | <value> | <maximum> | <note>
- <Metric> | <value> | <maximum> | <note>

---
# <Dependencies as a takeaway: one part everything relies on>
layout: network
rubric: R2
takeaway: <what the graph shows in one sentence>
notes: <35 seconds: the hub and why it is protected>
- <Part> -> <Part>
- <Part> -> <Part>
- <Part> -> <Part>

---
# <Command line as a takeaway: it runs end to end>
layout: terminal
rubric: R3
window: <tool name>
notes: <40 seconds: run it live or show the recording>
```
$ <command>
<output line>
OK <result>
```

---
# Try it, read it, build on it
layout: links
rubric: R4
cta: <one line: what you want the audience to do>
notes: <15 seconds: where to find everything>
- Demo | <address> | <note>
- Code | <address> | <licence>
- Docs | <address> | <note>
