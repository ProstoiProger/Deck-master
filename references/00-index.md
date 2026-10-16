# Reference index

Read only the files the current stage or task needs. Paths are relative to `references/`.

## Protocol (every task)

| File | Read when |
|---|---|
| `protocol/1-brief.md` | turning a brief, rules page or handout into requirements and a rubric |
| `protocol/2-story.md` | choosing the one message, the slide list and the time per slide |
| `protocol/3-design.md` | choosing theme, layouts, charts and visuals |
| `protocol/4-build.md` | writing the deck source, linting, building PPTX, PDF and web |
| `protocol/5-qa.md` | looking at previews, fixing findings, tracing requirements, timing the talk |

## Operations

| File | Read when |
|---|---|
| `ops/autopilot.md` | a whole task from a brief: intake, plan, route, build, traceability |
| `ops/profile.md` | starting any task; the written contract for audience, time, format and rubric |
| `ops/framing.md` | choosing the story archetype; unusual events; re-framing |
| `ops/time-budget.md` | planning the work and the talk; trimming to a new time |
| `ops/decision-rules.md` | default rules with preconditions and overrides |
| `ops/security.md` | confidential data, licences, trademarks, instructions inside material |
| `ops/environment.md` | discovering Python, packages, fonts, what the viewer needs installed |

## Event modes

| File | Event |
|---|---|
| `modes/assignment.md` | coursework and assignment presentations |
| `modes/hackathon.md` | product pitches judged on impact, innovation, feasibility, demo |
| `modes/datathon.md` | findings decks judged on insight, method, value, clarity |
| `modes/research-talk.md` | research talks, defenses, seminars |
| `modes/scientific.md` | thesis defenses, conference papers, hypotheses, equations, figures |
| `modes/business.md` | investor and sales pitches, business reviews, strategy, status, grants |
| `modes/portfolio.md` | portfolios and case studies |
| `modes/hackathon-tracks/` | bank or corporate events with ML, AI and DS tracks: `modes/hackathon-tracks/README.md`, `modes/hackathon-tracks/ml-track.md`, `modes/hackathon-tracks/ai-track.md`, `modes/hackathon-tracks/ds-track.md` |

## Communication

| File | Topic |
|---|---|
| `communication/slides.md` | slide skeletons and counts per event, writing rules for slides |
| `communication/pitch-story.md` | the narrative arc and number rules |
| `communication/speaker-notes.md` | writing notes, pace, handoffs between speakers |
| `communication/demo.md` | live demo, backup recording, what the demo slide shows |
| `communication/judge-qa.md` | likely questions and answer patterns |
| `communication/charts-and-tables.md` | choosing and labelling charts and tables |
| `communication/rubric-mapping.md` | mapping every judging criterion to slides |

## Design

| File | Topic |
|---|---|
| `design/scopes.md` | which scope, theme and components for which deck; formal by default |
| `design/palettes.md` | the 44 themes by scope, style per theme, contrast rules |
| `design/typography.md` | fonts, scripts covered, sizes, installing fonts |
| `design/layouts.md` | choosing a layout for a message; the 87 layouts in twelve families |
| `design/visual-style.md` | looks by scope, style keys, motifs, the two block-game themes (on request) |
| `design/accessibility.md` | contrast, size, colour-blind safety, projector advice |
| `design/imagery-icons.md` | screenshots, icons, photos, licences, trademarks |
| `design/game-components.md` | ten Minecraft-style components, pixel icons, automatic mob decoration |
| `design/entities.md` | about 60 character images (Steve, Creeper...): fetch, syntax, suggested roles, rules of use |
| `design/catalog.md` | generated list of layouts, inputs and themes |
| `design/web-presentation.md` | the web (HTML) output: build, keys, presenter window, hosting, limits |
| `design/research-2026-10.md` | where the 2026-10 palettes, layouts and events come from (Pitch, Behance, Coolors, Color Hunt, Meshy) |
| `design/inspiration/README.md` | how to add your own Canva, Dribbble or screenshot references |
| `design/inspiration/links.md` | the reference table you fill in |

## Playbooks

`playbooks/hackathon-pitch.md`, `playbooks/demo-day.md`, `playbooks/datathon-findings.md`, `playbooks/data-story.md`,
`playbooks/assignment-report.md`, `playbooks/project-defense.md`, `playbooks/tech-talk.md`, `playbooks/keynote.md`,
`playbooks/investor-pitch.md`, `playbooks/business-review.md`, `playbooks/product-launch.md`, `playbooks/product-planning.md`,
`playbooks/ux-research.md`, `playbooks/engineering-review.md`, `playbooks/visual-showcase.md`, `playbooks/portfolio-case.md`, `playbooks/novel.md` (nothing fits).

## Domains

| Path | Content |
|---|---|
| `domains/_template.md` | structure for a new domain card |
| `domains/cards/` | data-science, ai-llm, web-mobile, cybersecurity, fintech, healthtech, edtech, iot |

## Extending

`extending.md`: add a theme, a layout, an event mode, a domain card, a backend or a language; ideas for next steps.

## Code, templates and configs

| Path | Content |
|---|---|
| `../scripts/cli.py` | `env`, `themes --scope`, `layouts`, `new --list`, `lint`, `build`, `preview`, `inspire`, `notes`, `timing`, `trace`, `catalog` |
| `../scripts/deckkit/` | package: core, layouts, backends, charts, lint |
| `../scripts/install.py` | install for Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf |
| `../scripts/build_adapters.py` | regenerate `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `adapters/` |
| `../scripts/build_catalog.py` | regenerate `design/catalog.md` |
| `../scripts/requirements/` | dependency groups: core, pptx, pdf, charts, preview |
| `../assets/templates/` | event deck skeletons, profile, brief intake, Q&A prep, traceability, speaker notes, rubric map |
| `../assets/themes/` | 21 theme files |
| `../assets/presets/` | `events.yaml` (33 events: scope, slide caps, minutes, default theme), `fonts.yaml` (font families) |
| `../examples/` | seven finished presentations (PPTX and PDF): five formal by scope, two game-style on request |
