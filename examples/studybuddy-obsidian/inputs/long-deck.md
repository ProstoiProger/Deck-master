---
title: StudyBuddy - a planner students keep using
subtitle: Demo day, full 10-minute version
event: hackathon
theme: midnight-navy
minutes: 10
max_slides: 12
team: Team Crafters
date: 2026-10-24
sample: true            # illustrative numbers and fictional sources
rubric:
  - {id: R1, text: Impact, weight: 30}
  - {id: R2, text: Innovation, weight: 20}
  - {id: R3, text: Feasibility, weight: 25}
  - {id: R4, text: Demo, weight: 25}
---
# StudyBuddy: a planner students keep using
layout: title
eyebrow: Demo day
notes: We are Team Crafters. StudyBuddy turns a study plan into small quests so students keep going. In ten minutes we show the problem, the product, the pilot and the plan.

---
# Students quit planners within two weeks
layout: problem
rubric: R1
stat: 14 days | median time until students abandon a study planner
source: survey/export.csv#abandon
notes: In our survey of 300 students the median time until abandoning a planner was fourteen days. Planners feel like homework about homework.
Planners reward only at the end of term.
- No feedback during the week
- Plans are too big to start
- Nothing makes a missed day recoverable

---
# The market is large and reachable
layout: kpi
rubric: R1
source: market/sizing.md
notes: There are about 2.3 million university students in our region. We start with the 40 thousand in our own city, who we can reach through student unions.
- 2.3M | university students | in the region
- 40k | in our city | reachable first
- 6% | target share | in year one

---
# Today's alternatives each miss something
layout: comparison
rubric: R2
highlight: 4
source: market/competitors.md
notes: Paper planners and calendar apps have no feedback loop. Habit trackers have streaks but no study structure. StudyBuddy has both.
| Feature | Paper planner | Calendar app | StudyBuddy |
|---|---|---|---|
| Small steps | no | no | **yes** |
| Instant feedback | no | no | **yes** |
| Streak with rest day | no | no | **yes** |

---
# Every task becomes a short quest with instant feedback
layout: feature_grid
rubric: R2
notes: Four mechanics carry the product: quests of twenty five minutes, daily streaks with a rest token, an XP bar, and a party view so friends see progress.
- Quests | tasks split into 25 minute steps
- Streaks | daily chain with a rest token
- XP bar | progress you can see
- Party | friends see your streak

---
# A thin web client on a small backend keeps it feasible
layout: architecture
rubric: R3
notes: A web client, a small API, and a database. We chose boring parts so the team could finish in one weekend.
- Client: Web app, Phone view
- API: Auth, **Quest engine**, Streak service
- Data: Postgres, Event log

---
# Demo: a study task becomes a quest in three taps
layout: demo
rubric: R4
image: assets/demo-ui.png
notes: Here is the live flow. We pick a task, the app splits it into quests, and finishing one fills the XP bar.
- Pick a task from the plan
- The app splits it into quests
- Finishing a quest fills the XP bar

---
# Pilot students finished more tasks and kept their streaks
layout: kpi
rubric: R1, R4
source: pilot/results.csv
notes: In a two week pilot with 40 students, task completion rose and most kept a streak. These are small numbers, so we call it a promising pilot, not proof.
- 72% | tasks completed | vs 51% with a plain list
- 31 of 40 | kept a 7 day streak | pilot group
- 4.4 / 5 | would use again | exit survey
Pilot of 40 students over 14 days.

---
# Free for students, paid for universities
layout: bullets
rubric: R3
source: market/pricing.md
notes: Students use it for free. Universities pay four dollars per active student per year for analytics and integrations. At 6 percent of 40 thousand students that is about ten thousand dollars a year in the first city.
- Free tier for students
- 4 USD per active student per year for universities
- About 9,600 USD a year in the first city at the target share

---
# Four people, one weekend
layout: team
notes: Dana built the quest engine, Aigerim the streak logic, Timur the interface, and Mira ran the pilot.
- Dana K. | Quest engine | built the splitter
- Aigerim S. | Streaks | designed the rest token
- Timur B. | Interface | built the web client
- Mira L. | Pilot | ran the survey

---
# From weekend prototype to campus pilot
layout: roadmap
rubric: R3
notes: Next we add the party view, run a campus pilot in the spring, and measure grades against a control group.
- Now | Prototype | quests and streaks
- Spring | Campus pilot | 200 students
- Fall | Study | grades against a control group

---
# Questions?
layout: closing
notes: Thank you for listening.
- github.com/team-crafters/studybuddy
- crafters@example.org
