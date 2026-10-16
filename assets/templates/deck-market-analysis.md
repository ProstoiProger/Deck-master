---
title: "{{title_yaml}}"
subtitle: "<one line: how big the market is and where we fit>"
event: market-analysis
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <team or presenter>
date: {{date}}
rubric:
  - {id: R1, text: <market size and growth>, weight: 30}
  - {id: R2, text: <competitor view>, weight: 25}
  - {id: R3, text: <positioning>, weight: 25}
  - {id: R4, text: <recommendation>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <market> analysis
notes: <15 seconds: the market and why it matters now>

---
# <Summary as a takeaway: the market is big enough and we can win a niche>
layout: exec_summary
rubric: R4
notes: <40 seconds: size, competition, where to play, what to do>
- Situation | <market today>
- Complication | <the competitive pressure>
- Resolution | <where to play>
<one line recommendation>

---
# <Market size as a takeaway>
layout: market
rubric: R1
source: <market report or model>
notes: <40 seconds: how each number was built>
- TAM | <value> | <definition>
- SAM | <value> | <definition>
- SOM | <value> | <definition>

---
# <Growth as a takeaway: where the market is heading>
layout: chart_insight
rubric: R1
chart: line
source: <report or dataset>
takeaway: <the so-what in one sentence>
notes: <40 seconds: growth rate and the drivers behind it>
| <Year> | <Value> |
|---|---|
| <year> | <n> |
| <year> | <n> |

---
# <Competitors as a takeaway: nobody covers all the must-haves>
layout: feature_matrix
rubric: R2
highlight: 4
notes: <45 seconds: where each competitor is strong and weak>
| Feature | <Competitor A> | <Competitor B> | Us |
|---|---|---|---|
| <feature> | <yes/no> | <yes/no> | <yes/no> |
| <feature> | <yes/no> | <yes/no> | <yes/no> |

---
# <Positioning as a takeaway: the strengths outweigh the threats>
layout: matrix
rubric: R3
notes: <45 seconds: one point per quadrant>
## Strengths
- <point>
## Weaknesses
- <point>
## Opportunities
- <point>
## Threats
- <point>

---
# <Risks as a takeaway>
layout: risk
rubric: R3, R4
notes: <30 seconds: top risks to the recommendation>
- <Risk> | <level> | <level> | <mitigation>
- <Risk> | <level> | <level> | <mitigation>

---
# Recommendation and next steps
layout: closing
notes: <20 seconds: the recommendation and who decides>
- <recommendation>
- <contact>
