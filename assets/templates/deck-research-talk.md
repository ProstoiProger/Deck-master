---
title: "{{title_yaml}}"
subtitle: "<venue or seminar>"
event: research-talk
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <authors, affiliation>
date: {{date}}
rubric:
  - {id: R1, text: <novelty>, weight: 25}
  - {id: R2, text: <rigor of evaluation>, weight: 35}
  - {id: R3, text: <evidence>, weight: 25}
  - {id: R4, text: <clarity>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <venue>
notes: <20 seconds: the claim in one sentence>

---
# <Gap as a takeaway: what existing work cannot do>
layout: problem
rubric: R1
stat: <number> | <size of the gap>
source: <paper, table or experiment>
notes: <60 seconds: motivation>
<the problem in one sentence>
- <what is missing in prior work>

---
# <Method in one sentence>
layout: pipeline
rubric: R1, R2
notes: <90 seconds: only what is needed to read the results>
- <Step 1> | <caption>
- <Step 2> | <caption>
- <Step 3> | <caption>

---
# <Main result as a takeaway>
layout: chart_insight
rubric: R3
chart: bar
source: <experiment file>
takeaway: <effect size with uncertainty>
notes: <90 seconds>
| <Variant> | <Metric> |
|---|---|
| <baseline> | <n> |
| <ours> | <n> |

---
# <Comparison across datasets as a takeaway>
layout: comparison
rubric: R2
highlight: 4
source: <experiment file>
notes: <90 seconds: seeds, tests, intervals>
| Dataset | <Baseline A> | <Baseline B> | Ours |
|---|---|---|---|
| <d1> | <n> | <n> | **<n>** |

---
# <Limits and open questions>
layout: impact
rubric: R2
notes: <60 seconds>
## Limits
- <limit>
## Open
- <question>

---
# Questions?
layout: closing
rubric: R4
notes: <10 seconds>
- <code and paper link>
