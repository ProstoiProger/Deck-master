# deck-master

A presentation skill for AI coding agents (Claude Code, Codex, Cursor, Copilot, Gemini CLI, Windsurf and any tool
that reads `AGENTS.md`). It turns a brief, a project or analysis results into a finished **PPTX, PDF and web (HTML)** deck with
speaker notes, a time plan and requirement traceability. It covers every common kind of presentation: **scientific
talks and defenses, hackathons and datathons, investor pitches, business reviews and strategy, lectures and workshops,
tech talks, portfolios and case studies, assignments**. 33 events, 44 themes (42 formal, grouped by scope) and 87 layouts, including 3D, glass and HUD looks.
Decks are **formal by default**; the Minecraft and gamified styles (dark obsidian, light classic, characters such as Steve
and Creeper) are used only when the prompt asks for them.


## Quick start

```
python -m pip install -r scripts/requirements/pptx.txt -r scripts/requirements/pdf.txt -r scripts/requirements/charts.txt -r scripts/requirements/preview.txt
python scripts/install_check.py core pptx pdf charts preview

python scripts/cli.py new --list                                      # 33 events: scope, slide cap, minutes, default theme
python scripts/cli.py new --event hackathon --out decks/pitch.md      # scaffold, fill the <placeholders>
python scripts/cli.py themes --scope business                         # themes for a scope
python scripts/cli.py lint decks/pitch.md                             # readability, numbers, notes, time, rubric
python scripts/cli.py build decks/pitch.md --out build                # .pptx, .pdf and .html (--pptx, --pdf, --html pick)
python scripts/cli.py serve build/pitch.html                          # open the web version (N notes, O overview, P presenter window)
python scripts/cli.py preview decks/pitch.md --out build/preview --sheet   # PNGs to look at
python scripts/cli.py trace decks/pitch.md                            # every rubric item on a slide?
```

Try a finished example: `python scripts/cli.py build examples/investor-pitch-venture/routely.md --out build` (then `cli.py serve build/routely.html`; the page adapts: slides on large screens, a reading view on phones). Each example
folder has a `preview.png` contact sheet (`examples/README.md`).

## Using it through an agent

Install once, then ask in plain words:

```
python scripts/install.py --agent claude --scope user        # or codex, cursor, copilot, gemini, windsurf, agents
```

- "Use deck-master: build a 5-minute hackathon pitch from `brief.md` and `runs/`."
- "Build a 12-minute seminar talk from my results, scientific tone." / "Make a seed pitch deck from these facts." / "Quarterly review for the board."
- "Make it a Minecraft-style game presentation, dark obsidian, with Steve and Alex on the team slide." (game styles only on request)
- "Restyle `decks/pitch.md` with the boardroom theme."
- "Trim this deck to 5 minutes and list what you cut."
- "Review my deck against the rubric: trace, lint, previews."

## What is inside

| Path | Content |
|---|---|
| `SKILL.md` | the operating protocol, prime directives, routing, modes (single source of truth) |
| `references/` | protocol, ops, event modes, communication, design, playbooks, domain cards, `extending.md` |
| `scripts/cli.py`, `scripts/deckkit/` | CLI and package: parser, 87 layouts in 12 families, PPTX, PDF and web (HTML) backends, themed charts, lint |
| `assets/themes/` | IT and data: `midnight-navy`, `ultraviolet-core`, `graphite-cyan`, `deep-space`, `terminal-slate`, `cloud-light`, `aurora-mesh`, `datablue`, `matrix-green`, `synthwave`, `cobalt-pop`, `blueprint`, `cyber-hud`, `glass-dusk`, `liquid-light`; science: `academic`, `conference-dark`, `clinical`, `quantum-teal`, `deep-ocean`, `petrol`; business: `boardroom`, `consulting`, `ledger`, `startup-bright`, `venture-dark`, `signal-yellow`, `coral-market`, `harbor`, `navy-gold`, `sunset-mesh`; education: `chalkboard`, `forest`, `terracotta`, `sage`, `lavender`; portfolio and creative: `editorial`, `portfolio-mono`, `portfolio-warm`, `swiss`, `plum`, `ember`; game (on request): `obsidian-craft`, `classic-craft` |
| `assets/templates/` | event deck skeletons, profile, brief intake, Q&A prep, traceability, speaker notes, rubric map |
| `assets/presets/` | event presets (slide caps, minutes), font families |
| `assets/fonts/` | Inter, JetBrains Mono, Source Serif 4, Playfair Display, Montserrat, Press Start 2P (SIL OFL); Latin and Cyrillic covered, Kazakh checked per font |
| `examples/` | seven finished presentations (PPTX and PDF): hackathon, research talk, investor pitch, business review, portfolio, and two game-style ones |
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

## Game themes: components and mobs (only when asked)

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

`examples/` holds seven finished presentations, each with its prompt, inputs, PPTX, PDF and report
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
