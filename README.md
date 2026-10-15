# deck-master

A presentation skill for AI coding agents (Claude Code, Codex, Cursor, Copilot, Gemini CLI, Windsurf and any tool
that reads `AGENTS.md`). It turns a brief, a project or analysis results into a finished **PPTX and PDF** deck with
speaker notes, a time plan and requirement traceability. Built for assignments, hackathons and datathons; IT look by
default (navy, purple, dark gray), plus a light theme and two block-game themes (dark obsidian, light classic) with
characters such as Steve and Creeper as team avatars and mascots.

Structure and conventions mirror the `ds-master` skill: `SKILL.md` as the router, `references/` for knowledge,
`scripts/` for a tested CLI, `assets/` for templates and themes.

## Quick start

```
python -m pip install -r scripts/requirements/pptx.txt -r scripts/requirements/pdf.txt -r scripts/requirements/charts.txt -r scripts/requirements/preview.txt
python scripts/install_check.py core pptx pdf charts preview

python scripts/cli.py new --event hackathon --out decks/pitch.md      # scaffold, fill the <placeholders>
python scripts/cli.py lint decks/pitch.md                             # readability, numbers, notes, time, rubric
python scripts/cli.py build decks/pitch.md --out build                # .pptx and .pdf
python scripts/cli.py preview decks/pitch.md --out build/preview --sheet   # PNGs to look at
python scripts/cli.py trace decks/pitch.md                            # every rubric item on a slide?
```

Try a finished example: `python scripts/cli.py build examples/studybuddy-obsidian/studybuddy.md --out build`. Each example folder has a
`preview.png` contact sheet.

## Using it through an agent

Install once, then ask in plain words:

```
python scripts/install.py --agent claude --scope user        # or codex, cursor, copilot, gemini, windsurf, agents
```

- "Use deck-master: build a 5-minute hackathon pitch from `brief.md` and `runs/`."
- "Restyle `decks/pitch.md` with the obsidian-craft theme and put Steve and Alex on the team slide."
- "Trim this deck to 5 minutes and list what you cut."
- "Review my deck against the rubric: trace, lint, previews."

## What is inside

| Path | Content |
|---|---|
| `SKILL.md` | the operating protocol, prime directives, routing, modes (single source of truth) |
| `references/` | protocol, ops, event modes, communication, design, playbooks, domain cards, `extending.md` |
| `scripts/cli.py`, `scripts/deckkit/` | CLI and package: parser, 17 layouts, PPTX and PDF backends, themed charts, lint |
| `assets/themes/` | `midnight-navy`, `ultraviolet-core`, `graphite-cyan`, `deep-space`, `terminal-slate`, `cloud-light`, `obsidian-craft`, `classic-craft` |
| `assets/templates/` | event deck skeletons, profile, brief intake, Q&A prep, traceability, speaker notes, rubric map |
| `assets/presets/` | event presets (slide caps, minutes), font families |
| `assets/fonts/` | Inter, JetBrains Mono, Press Start 2P (SIL OFL); Latin, Cyrillic and Kazakh checked |
| `examples/` | finished game-style presentations (PPTX and PDF) with their prompts, inputs and reports |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `adapters/` | generated pointers for other agents |

## The deck source

One Markdown file; slides separated by `---`; a title, property lines, then the body:

```markdown
---
title: Atlas - fraud alerts in 2 seconds
event: hackathon
theme: midnight-navy
minutes: 5
rubric:
  - {id: R1, text: Impact, weight: 30}
---
# Fraud alerts arrive 40 minutes late
layout: problem
rubric: R1
stat: 40 min | median delay
source: bank-brief.pdf p.3
notes: Say the pain in the user's words.
- 3 of 4 cases are card-not-present
```

Every layout, its inputs and an example: `references/design/catalog.md` (generated).

## Game themes: components and mobs

The two game themes come with ten Minecraft-style components (boss fight, crafting table, inventory, hearts and XP bars,
advancement path, trade list, chat, ore strata, leaderboard, open book), an XP progress bar and a floor strip on every slide, and
automatic mob decoration (`references/design/game-components.md`).

## Characters (Steve, Creeper...)

```
python scripts/cli.py entities fetch      # downloads about 115 small PNGs into assets/entities (git-ignored)
```

Then `mascot: creeper` on title, closing or problem slides, a 4th team cell (`| steve`), or `Step | creeper` in a game-theme
agenda. Personal, non-commercial use only; the files are never committed or installed. Rules and the full list:
`references/design/entities.md`.

## Add your own references

Paste Canva or Dribbble links in `references/design/inspiration/links.md` and save screenshots to
`assets/inspiration/`. `python scripts/cli.py inspire --from-image assets/inspiration/x.png` measures the palette.
Only patterns are used, never artwork. See `references/design/inspiration/README.md`.

## Test it

```
python -m pytest scripts/tests -q          unit and integration tests
```

`examples/` holds finished game-style presentations, each with its prompt, inputs, PPTX, PDF and report
(`examples/README.md`).

## Extend it

New themes, layouts, event modes, domain cards, languages and backends:
`references/extending.md`. After any change: `python -m pytest scripts/tests -q`.

## Limits

- The PDF is drawn by this skill's own renderer and embeds the fonts. PowerPoint lays out PPTX text itself, so line
  breaks can differ slightly; check the PPTX once in the viewer you will use. The machine opening a PPTX needs the
  fonts installed (or use the PDF).
- Example numbers are illustrative (`sample: true`); real decks must cite real sources.
- Design observations from Canva and Dribbble are general patterns viewed in 2026-10, not copied designs.
- Game characters belong to Mojang/Microsoft and are fetched by you, for personal use; the repository ships none of them.
