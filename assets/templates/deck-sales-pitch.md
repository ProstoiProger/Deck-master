---
title: "{{title_yaml}}"
subtitle: "<customer name and the outcome you offer>"
event: sales-pitch
theme: {{theme}}
lang: en
minutes: {{minutes}}
team: <account team>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <fit to the client>, weight: 30}
  - {id: R2, text: <value>, weight: 30}
  - {id: R3, text: <proof>, weight: 20}
  - {id: R4, text: <price and next step>, weight: 20}
---
# {{title}}
layout: title
eyebrow: <client, date>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Client's problem as a takeaway, in their words>
layout: problem
rubric: R1
stat: <number> | <cost of the problem to them>
source: <client data, call notes or study>
notes: <40 seconds: show that you listened>
<one sentence on what hurts today>
- <symptom 1>

---
# <What changes for the client>
layout: solution
rubric: R2
image: <path to a product screenshot, optional>
notes: <40 seconds: outcome first, product second>
<one line outcome>
- <benefit 1>
- <benefit 2>
- <benefit 3>

---
# Four things the product does for you
layout: feature_grid
rubric: R2
notes: <40 seconds: map each feature to one client pain>
- <Feature> | <one line outcome>
- <Feature> | <one line outcome>
- <Feature> | <one line outcome>
- <Feature> | <one line outcome>

---
# <Proof: a customer like you>
layout: quote
rubric: R3
author: <name>
role: <role, company>
notes: <30 seconds: the result they got, with a number from the case study>
> <the customer's words>

---
# <Pricing as a takeaway: pay for what you use>
layout: pricing
rubric: R4
highlight: 2
notes: <40 seconds: recommend one plan and say why>
- <Plan 1> | <price> | <feature>; <feature>
- <Plan 2> | <price> | <feature>; <feature>; <feature>
- <Plan 3> | <price> | <feature>; <feature>

---
# <Rollout as a takeaway: live in n weeks>
layout: roadmap
rubric: R4
notes: <30 seconds: what you need from the client in week one>
- Week 1 | <milestone> | <detail>
- Week 3 | <milestone> | <detail>
- Week 6 | <milestone> | <detail>

---
# Next step: <one concrete action and date>
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
