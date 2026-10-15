# Time budget

Two budgets: the time you have to make the deck, and the time the speaker has on stage.

## Contents

1. Making the deck
2. The talk
3. Checkpoints
4. Hackathon and datathon runbook
5. Trimming
6. Rules

---

## 1. Making the deck

Share of the deck-making time by phase. Adjust to the rubric: a demo-heavy rubric moves time from design to the demo.

| Phase | Hackathon | Datathon | Assignment | Research talk |
|---|---|---|---|---|
| Brief and profile | 5% | 5% | 10% | 5% |
| Story and outline | 15% | 15% | 15% | 20% |
| Build and fill | 30% | 30% | 35% | 30% |
| QA and fixes | 20% | 20% | 20% | 20% |
| Rehearsal and Q&A prep | 30% | 30% | 20% | 25% |

Across a whole event (analysis or build plus communication), plan about 30 percent of the time for communication in a
datathon and about 45 percent in a hackathon; protect it, because the pitch is what is judged.

## 2. The talk

| Event | Slides | Minutes | Spoken words (at 150 wpm) |
|---|---|---|---|
| Hackathon | 6 to 8 | 3 to 5 | up to about 750 |
| Datathon | about 10 | 5 to 7 | up to about 1050 |
| Assignment | 8 to 15 | 8 to 12 | about 1400 at 140 wpm |
| Research talk | 8 to 14 | 10 to 15 | about 1700 at 140 wpm |

Defaults live in `assets/presets/events.yaml`; the brief overrides them. Rule of thumb: one slide per minute,
title and closing slides 10 to 20 seconds, keep 10 percent in reserve for slips.

## 3. Checkpoints

| Checkpoint | Question | Action if no |
|---|---|---|
| Outline done | does every rubric item have a slide? | add or merge slides now |
| First build | does lint show no Critical or High? | fix before any polish |
| Previews viewed | would a stranger follow it in 5 seconds per slide? | cut words, enlarge numbers |
| Timed read-through | total within budget minus reserve? | cut slides, then words |

## 4. Hackathon and datathon runbook

For a 24-hour event the communication block starts early: outline by hour 12, first full build by hour 18,
feature or code freeze at hour 20, slides final and two rehearsals plus a backup recording from hour 20 to 23,
submit at 23. Adapt the hours to the real schedule.

## 5. Trimming

`cli.py timing deck.md` shows seconds per slide from notes or `time:`. To trim to N minutes: remove slides in the cut
order of `protocol/2-story.md`, then shorten notes, then move detail to an appendix. Do not raise the speaking pace.

## 6. Rules

- Never spend the last block of time on new content; spend it on rehearsal.
- Polish goes first when time runs out; the problem, evidence and demo never do.
- The demo gets its time from the budget, not from the Q&A.
