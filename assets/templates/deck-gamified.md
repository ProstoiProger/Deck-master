---
title: "{{title_yaml}}"
subtitle: "<one line: the quest>"
event: gamified
theme: {{theme}}
lang: en
game: true
minutes: {{minutes}}
team: <party name>
date: {{date}}
rubric:                  # copy the criteria from the brief; weights if given
  - {id: R1, text: <clarity>, weight: 40}
  - {id: R2, text: <story>, weight: 30}
  - {id: R3, text: <engagement>, weight: 30}
---
# {{title}}
layout: title
eyebrow: <event, level>
notes: <15 seconds: who you are and the one sentence promise>

---
# <Problem as a takeaway: the boss to beat>
layout: boss
rubric: R1
boss: zombie
stat: <number> | <what it measures>
source: <where the number comes from>
notes: <30 seconds>
<one line of lore>
- <attack 1>
- <attack 2>

---
# <Idea as a takeaway: ingredients make a result>
layout: crafting
rubric: R2
result: <Result> | sword | <note>
notes: <30 seconds>
- <Ingredient> | book
- <Ingredient> | torch
- <Ingredient> | xp

---
# <Architecture as world layers>
layout: strata
rubric: R2
notes: <30 seconds>
- <Layer>: <component>, **<key component>**
- <Layer>: <component>, <component>

---
# <Results as stats>
layout: hud
rubric: R3
source: <results file>
notes: <30 seconds>
- <value> | <label> | heart | <context>
- <value> | <label> | hunger | <context>
- <value> | <label> | xp | <context>

---
# <Features as an inventory>
layout: inventory
rubric: R2
notes: <30 seconds>
- <Item> | <detail> | sword | 1
- <Item> | <detail> | torch | 1
- <Item> | <detail> | xp | 1

---
# <Roadmap as advancements>
layout: advancements
rubric: R3
notes: <30 seconds>
- <Milestone> | <detail> | sword | done
- <Milestone> | <detail> | diamond | current
- <Milestone> | <detail> | trophy | locked

---
# <Comparison as a leaderboard>
layout: leaderboard
rubric: R3
source: <results file>
notes: <30 seconds>
- <Name> | <value> | zombie
- <Name> | <value> | villager
- <Name> | <value> | steve

---
# Questions?
layout: closing
notes: <10 seconds: thank the audience and point to what they can use next>
- <contact or link>
- <second link>
