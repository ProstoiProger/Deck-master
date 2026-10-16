# Examples

Finished presentations, one per kind of request. Each folder holds the prompt a user would give, the material they attach
(`inputs/`), the deck source, the built **PPTX and PDF**, a contact-sheet preview and the final report. All data, names and
companies are fictional.

The skill builds **formal decks by default**. The two game examples exist because their prompts ask for Minecraft or a
gamified look; without such a request the skill never picks a game theme.

## Formal decks (default)

| Folder | Prompt in one line | Theme | Slides | Components used |
|---|---|---|---|---|
| `hackathon-pitch-midnight` | "5-minute hackathon pitch, jury scores impact, innovation, feasibility, demo" | `midnight-navy` | 8 | problem stat, solution, layered architecture, demo frame, KPI cards, roadmap |
| `research-talk-academic` | "12-minute seminar talk on my results, hypotheses before results" | `academic` | 10 | hypotheses with status chips, pipeline, factsheet, figure, comparison table, references |
| `investor-pitch-venture` | "10-minute seed pitch, investors score problem, market, traction, team, ask" | `venture-dark` | 11 | market circles, funnel, pricing cards, feature matrix, team, executive summary |
| `quarterly-review-boardroom` | "20-minute Q3 review for the executive committee, lead with the decision" | `boardroom` | 8 | executive summary, KPI scorecard, chart with so-what, risk register, Gantt |
| `portfolio-case-mono` | "10-minute design portfolio with one case study, monochrome and editorial" | `portfolio-mono` | 9 | profile, skill bars, timeline, case header, gallery, before and after, quote |

## Game decks (only when the prompt asks)

| Folder | Prompt in one line | Theme | Slides | Game components used |
|---|---|---|---|---|
| `studybuddy-obsidian` | "Trim our 10-minute deck to 5 minutes and rebuild it as a full Minecraft game presentation, dark obsidian, mobs on most slides" | `obsidian-craft` | 8 | boss, crafting, demo, hud, team, advancements, toast |
| `network-lesson-classic` | "8-minute networks lesson in a light classic Minecraft style, from my notes and lab results" | `classic-craft` | 11 | hotbar agenda, inventory, crafting, strata, trade, leaderboard, chat, hud, book, toast |

## Files in each folder

| File | Content |
|---|---|
| `prompt.md` | the prompt, what it exercises, what a good run does |
| `inputs/` | the files the user attached |
| `<name>.md` | the deck source (edit this, not the PPTX) |
| `<name>.pptx`, `<name>.pdf` | the finished presentation |
| `preview.png` | contact sheet of the slides |
| `report.md` | the final report: profile, deliverables, verification, assumptions |

## Rebuild or change a look

```
python scripts/cli.py build examples/investor-pitch-venture/routely.md --pptx --pdf --out build
python scripts/cli.py build examples/investor-pitch-venture/routely.md --pdf --out build --theme startup-bright
python scripts/cli.py preview examples/research-talk-academic/calibration.md --out build/preview --sheet
```

## Notes

- **The game decks embed Minecraft characters** from `assets/entities` (downloaded with `python scripts/cli.py entities fetch`).
  They belong to Mojang/Microsoft: personal, non-commercial use only. Do not publish those PPTX, PDF or preview files
  (`references/design/entities.md`); they are gitignored. Without the downloaded characters a deck still builds, without
  the mob decoration. The formal examples contain no third-party artwork and can be committed.
- The images in `portfolio-case-mono` and `hackathon-pitch-midnight` are illustrative mock-ups drawn for the examples.
- **Fonts**: the PDFs embed the bundled fonts; the PPTX files need them installed (`assets/fonts`).
- Components are listed in `references/design/layouts.md`; game components are described in `references/design/game-components.md`.
