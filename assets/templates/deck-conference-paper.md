---
title: "{{title_yaml}}"
subtitle: "<venue and track>"
event: conference-paper
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <authors, affiliation>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <novelty>, weight: 25}
  - {id: R2, text: <soundness>, weight: 35}
  - {id: R3, text: <significance>, weight: 25}
  - {id: R4, text: <clarity>, weight: 15}
---
# {{title}}
layout: title
eyebrow: <venue, year>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Claim as a takeaway>
layout: abstract
rubric: R1
source: <paper>
keywords: <k1>, <k2>, <k3>
notes: <45 seconds: the abstract in your own words>
- Background | <one sentence>
- Methods | <one sentence>
- Results | <one sentence with a number>
- Conclusion | <one sentence>

---
# <Gap as a takeaway>
layout: problem
rubric: R1
stat: <number> | <size of the gap>
source: <paper or table>
notes: <45 seconds>
<the problem in one sentence>
- <what is missing in prior work>

---
# <Method in one sentence>
layout: pipeline
rubric: R2
notes: <75 seconds>
- <Step 1> | <caption>
- <Step 2> | <caption>
- <Step 3> | <caption>

---
# <Core idea as a formula>
layout: equation
rubric: R1
math: <LaTeX, for example \hat{y}=\sigma(w^{T}x+b)>
notes: <60 seconds: say what each symbol means>
<one line on intuition>
- <symbol> | <meaning>
- <symbol> | <meaning>

---
# <Main result as a takeaway>
layout: figure
rubric: R2
chart: line
source: <experiment file>
caption: <caption with unit and number of seeds>
notes: <75 seconds>
- <observation 1>
- <observation 2>
| <X> | <Ours> | <Baseline> |
|---|---|---|
| <x1> | <n> | <n> |
| <x2> | <n> | <n> |

---
# <Robustness as a takeaway: it holds on both datasets>
layout: figures2
rubric: R2
image: <path to panel a>
image2: <path to panel b>
caption: <caption a>
caption2: <caption b>
takeaway: <what both panels show together>
notes: <60 seconds>

---
# <Comparison with baselines>
layout: comparison
rubric: R2
highlight: 4
source: <experiment file>
notes: <60 seconds>
| Dataset | <Baseline A> | <Baseline B> | Ours |
|---|---|---|---|
| <d1> | <n> | <n> | **<n>** |

---
# <Limits and open questions>
layout: impact
rubric: R3
notes: <45 seconds>
## Limits
- <limit>
## Open
- <question>

---
# References
layout: references
notes: <skip>
- <Author (year). Title. Venue.>
- <Author (year). Title. Venue.>

---
# Questions?
layout: closing
rubric: R4
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
