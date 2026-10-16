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
| Competition | `hackathon`, `datathon` | `midnight-navy`, `ultraviolet-core` | `deep-space`, `graphite-cyan`, `terminal-slate` | confident, demo first, one number per claim |
| Science | `research-talk`, `thesis-defense`, `conference-paper` | `academic`, `conference-dark` | `clinical`, `graphite-cyan`, `cloud-light` | precise, claims bounded by the data, limits shown |
| Business | `investor-pitch`, `business-review`, `strategy-proposal`, `sales-pitch`, `project-status`, `grant-proposal` | `venture-dark`, `boardroom`, `consulting`, `startup-bright`, `ledger`, `forest` | `cloud-light`, `editorial` | answer first, numbers with sources, one decision per deck |
| Education | `assignment`, `lecture`, `workshop` | `cloud-light`, `chalkboard`, `forest` | `academic`, `clinical` | clear structure, goals first, examples |
| Tech | `tech-talk` | `terminal-slate` | `midnight-navy`, `graphite-cyan` | technical depth, diagrams, a demo |
| Portfolio | `portfolio`, `case-study` | `portfolio-mono`, `portfolio-warm` | `editorial` | visual, spacious, a story per project |
| Game (on request) | `gamified` | `obsidian-craft` | `classic-craft` | playful, still one message per slide |

## 3. Choosing the theme

1. Name the scope from the brief, then take the default theme of its event.
2. Check the room: dark themes for dim rooms and recorded talks, light themes for bright rooms, print and PDF handouts.
3. Check the audience: conservative (board, regulator, faculty) -> `boardroom`, `academic`, `consulting`, `ledger`;
   startup or product audience -> `startup-bright`, `venture-dark`; creative -> `editorial`, `portfolio-*`.
4. A brand colour or an organisation template overrides the table: add a custom theme (`extending.md`).
5. Run `cli.py preview --sheet` with two candidate themes (`--theme`) and look before choosing.

## 4. Choosing the components per scope

| Scope | Core components (families in `design/layouts.md`) |
|---|---|
| Competition | `problem`, `solution`, `architecture`, `demo`, `kpi`, `roadmap`; datathons add `pipeline`, `chart_insight`, `comparison` |
| Science | `abstract`, `hypotheses`, `pipeline`, `factsheet`, `equation`, `figure`, `figures2`, `comparison`, `references` |
| Business | `exec_summary`, `scorecard`, `matrix`, `market`, `funnel`, `pricing`, `feature_matrix`, `risk`, `gantt`, `process`, `org` |
| Education | `agenda`, `section`, `bullets`, `columns`, `equation`, `figure`, `quote`, `references` |
| Tech | `architecture`, `tech_stack`, `pipeline`, `demo`, `chart_insight`, `comparison`, `roadmap` |
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
