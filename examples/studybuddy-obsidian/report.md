# Report: StudyBuddy game-style pitch

## Profile

| Field | Value | Status |
|---|---|---|
| Task | trim `inputs/long-deck.md` to 5 minutes and at most 8 slides, rebuild as a game presentation | fact (prompt) |
| Theme | `obsidian-craft` (dark obsidian, purple, IT cyan highlights) | fact (prompt) |
| Components | boss, crafting, hud, advancements, team, demo | fact (prompt asked for game components) |
| Characters | Steve, Alex, Villager, Pig as the team; Alex and Steve as mascots; 14 hostile mobs as decoration | fact (prompt) |
| Use | personal demo day, non-commercial | fact (prompt) |
| Rubric | R1 Impact 30, R2 Innovation 20, R3 Feasibility 25, R4 Demo 25 | fact (original deck) |

## Deliverables

- `studybuddy.md` (source), `studybuddy.pptx`, `studybuddy.pdf`, `preview.png`, `cut.md` (what was cut and why).
- Rebuild: `python scripts/cli.py build examples/studybuddy-obsidian/studybuddy.md --out build`.

## Verification (actually run)

- `cli.py lint`: 0 findings.
- `cli.py trace`: R1 slides 2, 5; R2 slides 3, 4; R3 slide 7; R4 slides 4, 5; all met.
- `cli.py timing`: 4.8 of 5 minutes (explicit `time:` values, the demo at 55 seconds).
- Numbers compared with `inputs/long-deck.md`: every number on the slides and in the notes appears there.
- Previews viewed: all 8 slides, no overflow; the mob decoration changes on every slide and never covers content.
- The PPTX re-read with python-pptx: 8 slides, notes on each, pictures present. Not opened in PowerPoint itself.

## Assumptions and open risks

- The characters belong to Mojang/Microsoft. This deck is for personal, non-commercial use: do not publish the PPTX, PDF or
  preview, and do not reuse the look in a company or promotional deck without asking again (`references/design/entities.md`).
- Fonts: the PDF embeds Inter, JetBrains Mono and Press Start 2P; the PPTX needs them installed or PowerPoint substitutes.
- The pilot is small (40 students); the stats slide and the notes call it a promising pilot, not proof.
- The demo slide's screenshot is synthetic; run the live demo once on the stage laptop.
