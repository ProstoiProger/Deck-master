# Rubric mapping

Judges and markers score what they can find. Map every criterion to at least one slide and say it in their words.

## Steps

1. Copy the criteria with weights into the front matter:
   ```
   rubric:
     - {id: R1, text: Impact on the user problem, weight: 30}
     - {id: R2, text: Innovation, weight: 20}
   ```
2. Tag slides: `rubric: R1, R2`. A slide may serve several criteria; a criterion should have at least one slide.
3. Allocate by weight: a 30 percent criterion gets roughly 30 percent of the slides and time.
4. Run `python scripts/cli.py trace deck.md`: a NOT MET row is a Critical finding and exits 1.
5. Use the criterion's own words in at least one slide title or the notes.

## Table

Use `assets/templates/rubric-map.md`:

| Id | Criterion | Weight | Slides | Evidence on slide | Time (s) |
|---|---|---|---|---|---|
| R1 | Impact | 30 | 2, 6, 7 | stat 40 min; kpi 2 s | 90 |
| R2 | Innovation | 20 | 3 | streaming scoring | 60 |

## Hidden criteria

Many juries also score clarity, teamwork and reproducibility without listing them. Cover them anyway: a clean
structure, visible handovers, a repo link and a rebuild command.

## When there is no rubric

Ask for one. If none exists, use the event preset's `judged_on` list in `assets/presets/events.yaml`, mark the
criteria as assumptions in the profile, and say so in the report.
