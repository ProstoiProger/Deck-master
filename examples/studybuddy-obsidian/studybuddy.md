---
title: StudyBuddy - a planner students keep using
subtitle: Game-style demo day pitch in the obsidian theme
event: hackathon
game: true
theme: obsidian-craft
lang: en
minutes: 5
max_slides: 8
team: Team Crafters
date: 2026-10-24
mobs: [creeper, enderman, skeleton, witch, ghast, spider, blaze, warden, phantom, vex, shulker, evoker, guardian, magma-cube]
rubric:
  - {id: R1, text: Impact, weight: 30}
  - {id: R2, text: Innovation, weight: 20}
  - {id: R3, text: Feasibility, weight: 25}
  - {id: R4, text: Demo, weight: 25}
---
# StudyBuddy: a planner students keep using
layout: title
eyebrow: Demo day
mascot: alex
time: 25
notes: We are Team Crafters. StudyBuddy turns a study plan into small quests so students keep going. In five minutes we fight the problem, craft the product, show it working, and read the pilot stats. The characters on these slides are Minecraft characters used for a personal, non-commercial demo day.

---
# Boss fight: students abandon planners within two weeks
layout: boss
rubric: R1
boss: zombie
stat: 14 days | median time until students abandon a study planner
source: inputs/long-deck.md
time: 35
notes: In our survey of three hundred students, the median time until they abandoned a planner was fourteen days. Planners feel like homework about homework. This is the boss of our story, and it has three attack patterns: planners reward only at the end of term, they give no feedback during the week, and the plans are too big to start.
Planners are homework about homework.
- Rewards come only at the end of term
- No feedback during the week
- Plans are too big to start

---
# Craft it: a task, a timer and a reward make a quest
layout: crafting
rubric: R2
result: Quest | sword | one small, rewarded step
source: inputs/long-deck.md
time: 45
notes: This is our innovation, and it works like a crafting table. Take a study task, add a twenty five minute timer, add an experience reward, and you craft a quest. Finishing quests keeps a daily streak alive, and a rest token makes a missed day recoverable, so one bad day is not the end of the plan.
Three ingredients turn any study task into a quest.
- Study task | book
- 25 minute timer | torch
- XP reward | xp
- Rest token | apple

---
# Demo: a study task becomes a quest in three taps
layout: demo
rubric: R2, R4
image: inputs/assets/demo-ui.png
time: 55
notes: Here is the live flow. We pick a task from the plan, the app splits it into quests, and finishing a quest fills the experience bar. The streak and the rest token sit next to it. If the live demo fails, this screenshot shows the same screen.
- Pick a task from the plan
- The app splits it into quests
- Finishing a quest fills the XP bar

---
# Pilot stats: students finished more tasks and kept streaks
layout: hud
rubric: R1, R4
source: inputs/long-deck.md
time: 45
notes: In a two week pilot with forty students, seventy two percent of tasks were completed, against fifty one percent with a plain list. Thirty one of forty students kept a seven day streak, and the exit survey gave four point four out of five for would use again. These are small numbers, so we call this a promising pilot, not proof.
- 72% | tasks completed | heart | vs 51% with a plain list
- 31 of 40 | kept a 7 day streak | hunger | pilot group of 40
- 4.4 / 5 | would use again | xp | exit survey

---
# Four players built it in one weekend
layout: team
time: 30
notes: Dana built the quest splitter, Aigerim designed the streak and rest token, Timur built the web client, and Mira ran the pilot and the survey. Four people, one weekend, boring technology on purpose.
- Dana K. | Quest engine | built the splitter | steve
- Aigerim S. | Streaks | designed the rest token | alex
- Timur B. | Interface | built the web client | villager
- Mira L. | Pilot | ran the survey | pig

---
# Next advancements: a campus pilot with 200 students
layout: advancements
rubric: R3
source: inputs/long-deck.md
time: 35
notes: It is feasible because it is a thin web client on a small backend. The prototype is done. Next is a campus pilot in the spring with two hundred students, and after that we measure grades against a control group in the fall. We would like help from a student union to find the pilot group.
- Prototype | web client and small backend | sword | done
- Campus pilot | 200 students in spring | diamond | current
- Study | grades against a control group | trophy | locked

---
# Questions?
layout: closing
mascot: steve
achievement: Demo day survived
time: 20
notes: Thank you for listening. The code and the pilot data are in the repository, and we are happy to run the demo again.
- github.com/team-crafters/studybuddy
- crafters@example.org
