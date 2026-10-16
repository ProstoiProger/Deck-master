---
title: "{{title_yaml}}"
subtitle: "<one line: how the quarter went>"
event: okr-review
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <honest progress>, weight: 30}
  - {id: R2, text: <causes>, weight: 25}
  - {id: R3, text: <decisions needed>, weight: 25}
  - {id: R4, text: <next quarter focus>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <team> OKR review
notes: <15 seconds: period and scope>

---
# <Summary as a takeaway: what moved and what did not>
layout: exec_summary
rubric: R1
notes: <40 seconds: progress in three sentences>
- Situation | <where we started>
- Complication | <what slipped>
- Resolution | <what we will change>
<one line decision or ask>

---
# <Progress as a takeaway: how many objectives are on track>
layout: okr
rubric: R1
source: <OKR file>
notes: <50 seconds: each objective, read the bars left to right>
## <Objective one>
- <Key result> | <current> | <target>
- <Key result> | <current> | <target>
## <Objective two>
- <Key result> | <current> | <target>
- <Key result> | <current> | <target>
## <Objective three>
- <Key result> | <current> | <target>
- <Key result> | <current> | <target>

---
# <Metrics as a takeaway: what the numbers say>
layout: kpi_table
rubric: R1, R2
source: <metrics file>
notes: <40 seconds: the metrics that moved most and why>
- <Metric> | <value> | <delta> | <status> | <note>
- <Metric> | <value> | <delta> | <status> | <note>
- <Metric> | <value> | <delta> | <status> | <note>

---
# <The main cause as a takeaway>
layout: chart_insight
rubric: R2
chart: waterfall
source: <analysis file>
takeaway: <the cause in one sentence>
notes: <40 seconds: what drove the miss or the win>
| <Step> | <Value> |
|---|---|
| =<Start> | <n> |
| <Driver> | <n> |
| =<End> | <n> |

---
# <Risks as a takeaway: what could still derail the quarter>
layout: risk
rubric: R3
notes: <30 seconds: owners and dates>
- <Risk> | <level> | <level> | <mitigation>
- <Risk> | <level> | <level> | <mitigation>

---
# <Next quarter as a takeaway: three commitments>
layout: checklist
rubric: R3, R4
notes: <30 seconds: what we commit to and what we drop>
- <Commitment> | <todo> | <owner or date>
- <Commitment> | <todo> | <owner or date>
- <Commitment> | <todo> | <owner or date>

---
# Decisions we need
layout: closing
notes: <15 seconds: the asks and the date of the next review>
- <decision needed>
- <contact>
