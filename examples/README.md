# Examples

Finished game-style presentations: each folder has the prompt a user would give, the material they attach (`inputs/`), the
deck source, the built **PPTX and PDF**, a contact-sheet preview and the final report. All data and names are fictional.

| Folder | Prompt in one line | Theme | Slides | Game components used |
|---|---|---|---|---|
| `studybuddy-obsidian` | "Trim our 10-minute deck to 5 minutes and rebuild it as a full Minecraft game presentation, dark obsidian, mobs on most slides" | `obsidian-craft` | 8 | boss, crafting, demo, hud, team, advancements, toast |
| `network-lesson-classic` | "8-minute networks lesson in a light classic Minecraft style, from my notes and lab results" | `classic-craft` | 11 | hotbar agenda, inventory, crafting, strata, trade, leaderboard, chat, hud, book, toast |

`studybuddy-obsidian` is the flagship: its prompt, the cut list (`cut.md`), the report and the deck show the intended look.

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
python scripts/cli.py build examples/studybuddy-obsidian/studybuddy.md --out build
python scripts/cli.py build examples/studybuddy-obsidian/studybuddy.md --out build --theme classic-craft
python scripts/cli.py preview examples/network-lesson-classic/lesson.md --out build/preview --sheet
```

## Notes

- **The decks embed Minecraft characters** from `assets/entities` (downloaded with `python scripts/cli.py entities fetch`). They
  belong to Mojang/Microsoft: personal, non-commercial use only. Do not publish these PPTX, PDF or preview files
  (`references/design/entities.md`). Without the downloaded characters a deck still builds, without the mob decoration.
- **Fonts**: the PDFs embed Inter, JetBrains Mono and Press Start 2P; the PPTX files need them installed (`assets/fonts`).
- The components are described in `references/design/game-components.md`; their inputs are listed in `references/design/catalog.md`.
