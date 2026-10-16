# Playbook: UX research readout

**Preconditions**: sessions, interviews or tests were run; the audience is a product team that must change something; 10 to 12 minutes.
Event: `ux-research`.

## Steps

1. **Question and method**: `hmw` for the research question; one line with number of participants, how recruited, tasks.
2. **Who**: `persona` built from the data: goals, frustrations, needs, one real quote; fake faces are not evidence.
3. **Journey**: `journey` with four to six stages, the user's feeling from 1 to 5, and one opportunity per stage; the low point is the story.
4. **Insights**: `insight_cards` with up to three findings, each with its evidence number (task success, time, count of participants) and the change.
5. **In their words**: `quote` with a participant label, not a real name, and context.
6. **Measures**: `kpi` for task success, time on task, error rate, with `source:` and the sample size.
7. **Recommendations**: `checklist` ordered by impact with an owner; `roadmap` for what you test next.
8. **Scaffold**: `new --event ux-research` (theme `lavender`; `swiss` or `terracotta` for a quieter look).
9. **QA**: no participant is identifiable; every number has its n; recommendations follow from the findings; lint and previews.

## Traps

Percentages from five participants shown as if they were a survey; a persona invented from assumptions; quotes picked to please;
recommendations with no owner.

## Output

Deck source, `.pptx`, `.pdf`, speaker script, an appendix with the session guide and the raw tally.
