# Scopes: which look and components for which deck

The skill covers many kinds of presentations. Each scope has its own themes, components and tone. This file is the
chooser; `design/palettes.md` has the colours and `design/layouts.md` the components.

## Contents

1. The default: formal
2. Scope table
3. Choosing the theme
4. Choosing the components per scope
5. When the user asks for a game look
6. Mixing and overriding

---

## 1. The default: formal

Unless the user asks otherwise, build a formal deck: a readable theme from the table below, plain components, no
characters, no pixel fonts. Game and Minecraft styles exist (`obsidian-craft`, `classic-craft`, ten game components, mob
decoration) but are used only when the prompt asks for them by name ("Minecraft", "gamified", "game style", "pixel").
A hackathon or a student project is not a reason to use them.

## 2. Scope table

`python scripts/cli.py new --list` prints the events; `cli.py themes --scope <scope>` filters themes.

| Scope | Events | Default theme | Other fitting themes | Tone |
|---|---|---|---|---|
| Competition | `hackathon`, `demo-day`, `datathon`, `data-story` | `midnight-navy`, `aurora-mesh`, `ultraviolet-core`, `datablue` | `deep-space`, `graphite-cyan`, `terminal-slate`, `matrix-green`, `synthwave`, `cobalt-pop` | confident, demo first, one number per claim |
| Science | `research-talk`, `thesis-defense`, `conference-paper` | `academic`, `conference-dark` | `clinical`, `quantum-teal`, `deep-ocean`, `petrol`, `graphite-cyan`, `cloud-light` | precise, claims bounded by the data, limits shown |
| Business | `investor-pitch`, `business-review`, `strategy-proposal`, `sales-pitch`, `project-status`, `grant-proposal` | `venture-dark`, `boardroom`, `consulting`, `startup-bright`, `ledger`, `forest` | `signal-yellow`, `navy-gold`, `harbor`, `cloud-light`, `editorial` | answer first, numbers with sources, one decision per deck |
| Product and planning | `product-launch`, `product-roadmap`, `okr-review`, `market-analysis`, `go-to-market` | `sunset-mesh`, `signal-yellow`, `harbor`, `coral-market`, `plum` | `startup-bright`, `venture-dark`, `navy-gold`, `ledger` | outcome first, priorities and owners, honest status |
| Design and research | `ux-research` | `lavender` | `terracotta`, `swiss`, `quantum-teal` | evidence from users, quotes, a clear recommendation |
| Education | `assignment`, `lecture`, `workshop` | `cloud-light`, `chalkboard`, `forest` | `academic`, `clinical`, `sage`, `terracotta`, `lavender` | clear structure, goals first, examples |
| Tech | `tech-talk`, `keynote`, `model-review`, `architecture-review`, `postmortem`, `sprint-review` | `terminal-slate`, `ember`, `matrix-green`, `blueprint`, `petrol`, `deep-ocean` | `midnight-navy`, `graphite-cyan`, `swiss` | technical depth, diagrams, a demo, blameless tone in reviews |
| Portfolio | `portfolio`, `case-study` | `portfolio-mono`, `portfolio-warm` | `editorial`, `swiss`, `plum` | visual, spacious, a story per project |
| Game (on request) | `gamified` | `obsidian-craft` | `classic-craft` | playful, still one message per slide |

## 3. Choosing the theme

1. Name the scope from the brief, then take the default theme of its event.
2. Check the room: dark themes for dim rooms and recorded talks, light themes for bright rooms, print and PDF handouts.
3. Check the audience: conservative (board, regulator, faculty) -> `boardroom`, `academic`, `consulting`, `ledger`;
   startup or product audience -> `startup-bright`, `venture-dark`, `signal-yellow`; consumer or brand -> `sunset-mesh`, `plum`, `coral-market`;
   creative -> `editorial`, `portfolio-*`, `swiss`; hackathon and data crowd -> `aurora-mesh`, `datablue`, `matrix-green`, `synthwave`;
   research and health -> `quantum-teal`, `clinical`, `academic`.
4. A brand colour or an organisation template overrides the table: add a custom theme (`extending.md`).
5. Run `cli.py preview --sheet` with two candidate themes (`--theme`) and look before choosing.

## 4. Choosing the components per scope

| Scope | Core components (families in `design/layouts.md`) |
|---|---|
| Competition | `cover_poster`, `hmw`, `problem`, `solution`, `architecture`, `demo`, `kpi`, `roadmap`, `links`; datathons add `schema`, `pipeline`, `insight_cards`, `chart_insight`, `model_card`, `comparison` |
| Science | `abstract`, `hypotheses`, `pipeline`, `factsheet`, `equation`, `figure`, `figures2`, `comparison`, `references` |
| Business | `exec_summary`, `scorecard`, `kpi_table`, `okr`, `matrix`, `market`, `funnel`, `pricing`, `feature_matrix`, `risk`, `gantt`, `process`, `org`, `canvas9`, `customer_case`, `ask`, `proof_wall` |
| Product and design | `statement`, `persona`, `journey`, `hmw`, `kanban`, `checklist`, `okr`, `roadmap`, `proof_wall`, `quote` |
| Education | `agenda`, `section`, `bullets`, `columns`, `equation`, `figure`, `quote`, `references` |
| Tech | `architecture`, `schema`, `tech_stack`, `pipeline`, `demo`, `model_card`, `kanban`, `checklist`, `risk`, `chart_insight`, `comparison`, `roadmap` |
| Portfolio | `profile`, `skills`, `timeline`, `case_header`, `gallery`, `before_after`, `quote`, `image_full` |
| Game | `boss`, `crafting`, `strata`, `hud`, `inventory`, `advancements`, `leaderboard`, `trade`, `chat`, `book` |

Rules: one component per message; do not repeat a component more than three times in a row; use a section divider
(`section`) only in decks of ten slides or more.

## 5. When the user asks for a game look

1. Confirm the use is personal, educational or hackathon, not commercial (`design/entities.md`).
2. Scaffold with the game theme: `cli.py new --event hackathon --theme obsidian-craft --out deck.md` (the scaffold adds
   `game: true`), or use the `gamified` event.
3. Read `design/game-components.md`; fetch characters with `cli.py entities fetch` only if the user wants them.
4. Lint warns (Medium) about a game theme without `game: true` and about game layouts in a formal theme. Heed both.

## 6. Mixing and overriding

- A formal deck may borrow one game-free accent: a `big_number`, a `quote` or a `section` slide.
- Restyle without rewriting: `cli.py build deck.md --theme boardroom`. Layouts adapt; check the previews, because dense
  slides can overflow in a serif theme.
- A scope not listed (for example law, architecture, sport) takes the nearest scope's theme and components; say so in the
  profile and add a theme only if the user supplies a brand.
