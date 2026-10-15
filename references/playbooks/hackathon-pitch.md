# Playbook: hackathon pitch

**Preconditions**: a prototype or a concrete idea exists; judged on impact, innovation, feasibility, demo; 3 to 5
minutes.

## Steps

1. **Profile and rubric**: time, slide cap, criteria with weights (`protocol/1-brief.md`).
2. **Message**: "Who gets what change, shown by what" in one sentence (`protocol/2-story.md`).
3. **Scaffold**: `python scripts/cli.py new --event hackathon --out decks/pitch.md`, theme `midnight-navy` or
   `deep-space` (`obsidian-craft` for playful briefs).
4. **Fill in this order**: demo slide and screenshot first, then problem, evidence, architecture, roadmap, title, closing.
5. **Evidence**: one metric against a baseline with a `source:`; if there is no measurement, show a user quote or
   a timed task and say what it is.
6. **Notes and time**: notes for every slide, total under the budget; demo gets the largest share.
7. **QA**: lint, previews, trace, two timed rehearsals, a backup recording (`protocol/5-qa.md`).
8. **Q&A prep**: `communication/judge-qa.md`, three backup slides after the closing slide.

## Examples

| Situation | Adjustment |
|---|---|
| no working demo yet | show a clickable prototype or screenshots; say "prototype"; do not fake a live run |
| 2-minute pitch | 5 slides: problem, solution, demo, evidence, ask |
| team of three | split slides by speaker, write handovers in notes |

## Traps

- Features instead of pain; the team slide before the problem.
- Invented traction. Say "pilot with 40 students" only if it happened.
- No ask at the end.

## Output

The deck source, `.pptx`, `.pdf`, speaker script, Q&A prep, the traceability table and the rebuild command.
