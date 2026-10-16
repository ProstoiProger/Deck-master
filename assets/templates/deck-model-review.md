---
title: "{{title_yaml}}"
subtitle: "<one line: the model and the decision it supports>"
event: model-review
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <problem fit>, weight: 25}
  - {id: R2, text: <evaluation rigor>, weight: 30}
  - {id: R3, text: <known limits>, weight: 25}
  - {id: R4, text: <decision>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <model name> review
notes: <15 seconds: model, owner, version>

---
# <The decision this model supports>
layout: hmw
rubric: R1
question: <How might we ... using a model?>
notes: <30 seconds: the user of the prediction and the cost of an error>
- Who | <the person or system that uses the prediction>
- Constraint | <latency, fairness, data limits>
- Success | <the metric that matters to the business>

---
# <Data as a takeaway: what the model reads>
layout: schema
rubric: R2
relations: <table.key -> table.key>
notes: <35 seconds: sources, joins, leakage controls>
## <table one>
- <column> | <type> | primary key
- <column> | <type>
## <table two>
- <column> | <type> | foreign key
- <column> | <type>

---
# <Model result as a takeaway>
layout: model_card
rubric: R2, R3
source: <evaluation file>
notes: <45 seconds: facts, metrics, limits>
## Facts
- Task | <what it predicts>
- Model | <type and size>
- Data | <rows and period>
- Split | <how it was split>
## Metrics
- <metric> | <value> | <split>
- <metric> | <value> | <split>
- <metric> | <value> | <split>
## Limits
- <where it fails>

---
# <Comparison as a takeaway: it beats the baseline>
layout: comparison
rubric: R2
highlight: 3
source: <evaluation file>
notes: <40 seconds: metric, split, uncertainty>
| Metric | Baseline | Ours |
|---|---|---|
| <metric> | <n> | **<n>** |

---
# <Drivers as a takeaway: what the model relies on>
layout: chart_insight
rubric: R2
chart: lollipop
source: <explanation file>
takeaway: <the so-what in one sentence>
notes: <35 seconds: top drivers and whether they make sense>
| <Feature> | <Importance> |
|---|---|
| <a> | <n> |
| <b> | <n> |

---
# <Risks as a takeaway: three failure modes to watch>
layout: risk
rubric: R3
notes: <35 seconds: drift, bias, outages and the monitor for each>
- <Risk> | <level> | <level> | <mitigation>
- <Risk> | <level> | <level> | <mitigation>

---
# <Launch readiness as a takeaway>
layout: checklist
rubric: R3, R4
notes: <35 seconds: what is ready and what blocks>
- <Check> | <status> | <note>
- <Check> | <status> | <note>
- <Check> | <status> | <note>

---
# <Next steps as a takeaway>
layout: roadmap
rubric: R4
notes: <25 seconds: what happens after approval>
- Now | <milestone> | <detail>
- Next | <milestone> | <detail>
- Later | <milestone> | <detail>

---
# Decision requested
layout: closing
notes: <15 seconds: approve, approve with conditions, or reject>
- <decision needed>
- <contact>
