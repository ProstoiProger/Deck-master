# Stage 3: Design

Goal: pick a theme, a layout per slide and a visual per message, with readability first.

## Contents

1. Theme
2. Layout per message
3. Visuals
4. Style packs and references
5. Checklist

---

## 1. Theme

Take the scope first (`design/scopes.md`), then the room. The look is formal unless the user asks for a game style.

| Situation | Theme |
|---|---|
| Default tech pitch, unsure | `midnight-navy` |
| Data, AI, ML story | `ultraviolet-core` |
| Engineering, architecture, calm | `graphite-cyan` |
| Loud stage energy | `deep-space` |
| Developer tools, CLI, security | `terminal-slate` |
| Printed handout, bright room, assignment | `cloud-light` |
| Scientific talk, defense (light, serif) | `academic` |
| Scientific talk in a dark room | `conference-dark` |
| Medicine, life science | `clinical` |
| Board pack, business review | `boardroom` |
| Strategy proposal, status report | `consulting` |
| Financial results, numbers first | `ledger` |
| Investor or sales pitch, bright / dark | `startup-bright` / `venture-dark` |
| Lecture, workshop | `chalkboard` |
| Sustainability, nonprofit, grant | `forest` |
| Portfolio, dark / light / magazine | `portfolio-mono` / `portfolio-warm` / `editorial` |
| Only if the user asks for Minecraft or gamified: dark / light | `obsidian-craft` / `classic-craft` |

Details and contrast figures: `design/palettes.md`. A brand or organiser template overrides this: ask for it, then
add a theme file (`extending.md`).

## 2. Layout per message

| The slide must show | Layout |
|---|---|
| one problem and one number | `problem` |
| the product and why it matters | `solution` |
| how it is built | `architecture` or `pipeline` |
| it working | `demo` |
| headline numbers | `kpi` |
| one chart and its meaning | `chart_insight` |
| us against baselines | `comparison` |
| 2 to 6 capabilities | `feature_grid` |
| next steps | `roadmap` or `impact` |
| the team | `team` |
| a decision and its reasons | `exec_summary` |
| KPIs against targets | `scorecard` |
| risks with owners | `risk` |
| market size, funnel, pricing, plan | `market`, `funnel`, `pricing`, `gantt` |
| hypotheses, a formula, a figure | `hypotheses`, `equation`, `figure` |
| a project in a portfolio | `case_header`, `gallery`, `before_after` |

Full list and inputs: `design/catalog.md`. When nothing fits use `bullets` and keep it short.

## 3. Visuals

- One chart per slide, labelled in plain words; see `communication/charts-and-tables.md`.
- Screenshots over diagrams of screenshots; crop to the part that matters.
- Icons and photos only with a clear licence (`design/imagery-icons.md`).
- Decoration stays on title and closing slides; content slides stay flat.

## 4. Style packs and references

A theme can carry a style pack (corner shape, card style, title rule, footer, pattern). The block-game looks are the
`obsidian-craft` and `classic-craft` themes, with optional characters (`design/entities.md`). The user's own Canva or Dribbble references live in `design/inspiration/`; use them for
patterns and measured palettes only (`design/inspiration/README.md`).

## 5. Checklist

- [ ] Theme chosen with a reason; contrast known (`design/accessibility.md`).
- [ ] Each slide has a layout that fits its message; no layout used for something it was not built for.
- [ ] Fonts cover the deck language (`design/typography.md`).
- [ ] Every image has a source and a licence.
