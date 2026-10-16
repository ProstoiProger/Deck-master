---
title: "{{title_yaml}}"
subtitle: "<one line: the system and the decision requested>"
event: architecture-review
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <requirements fit>, weight: 25}
  - {id: R2, text: <trade-offs>, weight: 25}
  - {id: R3, text: <risks>, weight: 20}
  - {id: R4, text: <operability>, weight: 15}
  - {id: R5, text: <decision>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <system> design review
notes: <15 seconds: system, author, status>

---
# <The problem and the requirements that shape the design>
layout: problem
rubric: R1
stat: <number> | <the scale or limit that drives the design>
source: <requirements document>
notes: <40 seconds: the requirements that matter most>
<one sentence on why the current system cannot meet them>
- <requirement 1>
- <requirement 2>

---
# <Design as a takeaway: how the pieces fit>
layout: architecture
rubric: R1, R2
notes: <60 seconds: follow one request through the layers>
- <Layer>: <component>, **<key component>**, <component>
- <Layer>: <component>, <component>
- <Layer>: <component>, <component>

---
# <Data model as a takeaway>
layout: schema
rubric: R2
relations: <table.key -> table.key>
notes: <40 seconds: ownership, consistency, growth>
## <table one>
- <column> | <type> | primary key
- <column> | <type>
## <table two>
- <column> | <type> | foreign key
- <column> | <type>

---
# <Technology choices as a takeaway>
layout: tech_stack
rubric: R2
notes: <40 seconds: why each choice over the alternative>
- Language: <a>, <b>
- Data: <a>, <b>
- Infra: <a>, <b>

---
# <Alternatives as a takeaway: why this option wins>
layout: comparison
rubric: R2
highlight: 3
notes: <45 seconds: criteria and weights>
| Criterion | <Option A> | <Option B> |
|---|---|---|
| <criterion> | <value> | **<value>** |
| <criterion> | <value> | **<value>** |

---
# <Risks as a takeaway: three risks need an owner>
layout: risk
rubric: R3
notes: <35 seconds: likelihood, impact, mitigation>
- <Risk> | <level> | <level> | <mitigation>
- <Risk> | <level> | <level> | <mitigation>

---
# <Readiness as a takeaway: what is needed to run it>
layout: checklist
rubric: R4
notes: <35 seconds: monitoring, on-call, rollback, security>
- <Check> | <status> | <note>
- <Check> | <status> | <note>
- <Check> | <status> | <note>

---
# <Rollout as a takeaway>
layout: roadmap
rubric: R5
notes: <30 seconds: phases and gates>
- Now | <milestone> | <detail>
- Next | <milestone> | <detail>
- Later | <milestone> | <detail>

---
# Decision requested
layout: closing
rubric: R5
notes: <15 seconds: approve, approve with changes, or send back>
- <decision needed>
- <contact>
