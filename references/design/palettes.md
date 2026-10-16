# Palettes

44 themes live in `assets/themes/*.yaml`. 42 are formal and grouped by scope (technology and data, science, business,
education, portfolio and creative); two are block-game style packs that the skill uses only when the user asks for Minecraft or a
gamified deck. Hex values are our own tuned versions of common palette conventions, not sampled artwork (provenance of the
2026-10 additions: `design/research-2026-10.md`); every theme passes the contrast checks in section 3. Live figures:
`cli.py themes` (`--scope <scope>` filters); full table: `design/catalog.md`; choosing by kind of deck: `design/scopes.md`.

## Contents

1. Themes by scope
2. Fonts and style per theme
3. Contrast figures
4. Pitfalls
5. Using a custom palette
6. As-of note

---

## 1. Themes by scope

### Technology, hackathons and data

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `midnight-navy` | Default IT look | #0B1220 | #3B82F6 | #22D3EE | default IT look; tech pitches, unsure choices |
| `ultraviolet-core` | Purple-led dark theme for data and AI stories | #120B2E | #8B5CF6 | #00E5FF | datathons, AI and ML stories |
| `graphite-cyan` | Dark gray with a cyan accent | #14161B | #00B8D9 | #7DF9FF | engineering reviews, architecture, research with code |
| `deep-space` | Navy and violet with a hot pink accent | #0A0F2C | #6C5CE7 | #FF4F9A | hackathon finals, demo days, stage energy |
| `terminal-slate` | Developer-console palette (GitHub-dark inspired) | #0D1117 | #58A6FF | #3FB950 | dev tools, security, CLI products |
| `cloud-light` | Light variant for printed handouts, assignments and projectors in bright rooms | #F8FAFC | #1D4ED8 | #0E7490 | assignments, handouts, bright rooms, print |
| `aurora-mesh` | Deep navy with a mint-to-cyan mesh gradient on title and closing slides | #07121F | #4DFFB2 | #0FF5DA | hackathon demos, AI products, cover slides with a gradient |
| `datablue` | Navy to electric blue with a hatched side panel | #060B2B | #3B82FF | #00FFDE | datathons, analytics readouts, dashboards and data stories |
| `matrix-green` | Near-black green with phosphor accents, monospaced headings and a blueprint grid | #06100A | #19E58C | #B6F500 | security, dev tools, terminal-style talks, model reviews |
| `synthwave` | Indigo-black with hot pink, violet and cyan, mesh cover | #0F0524 | #C21CA8 | #4CC9F0 | demo days, creative-tech and community events |
| `cobalt-pop` | Saturated cobalt with yellow, pink and mint, concentric rings | #1A2BC8 | #FFE14D | #7CF5E0 | hackathon openings, event talks, loud youth-oriented decks |
| `blueprint` | Drafting-sheet blue with white linework and a title block | #0B2A5C | #7FD4FF | #FFD54A | architecture reviews, hardware, systems design |
| `cyber-hud` | Near-black blue with cyan, amber and red; bracketed HUD cards, monospaced headings, a wireframe globe cover | #03080D | #0FB5D6 | #4DE8FF | futuristic IT, security, systems and tech showcases |
| `glass-dusk` | Deep indigo with translucent glass cards, violet, pink and aqua blooms, and shaded 3D orbs on the cover | #0B0920 | #8B7CFF | #5EEAD4 | AI products and data stories with glass cards and 3D orbs |
| `liquid-light` | Pale periwinkle with frosted white glass cards, a pastel mesh cover and indigo, pink and teal accents | #EEF1FF | #4F46E5 | #0B7285 | bright modern product and design decks with frosted glass |

### Science and research

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `academic` | Warm paper white, deep blue and crimson | #FBFAF6 | #1F3C88 | #9B1C2E | conference talks, thesis defenses, seminars |
| `conference-dark` | Ink blue-black with soft blue and amber | #0E1621 | #6FA8DC | #F2C14E | dark conference rooms, recorded talks |
| `clinical` | Clean white with teal and orange | #FFFFFF | #0B6E79 | #B54708 | medicine, life science, teaching with data |
| `quantum-teal` | Pale aqua with a liquid teal mesh and deep teal type | #F1FBF8 | #0B7A75 | #B8430C | research, health-tech, calm technical reports |
| `deep-ocean` | Midnight blue with cyan and ice accents and concentric rings | #031126 | #00B4D8 | #90E0EF | climate, oceanography, analytics on a dark screen |
| `petrol` | Deep petrol teal with amber and sand | #001A22 | #0A9396 | #E9D8A6 | energy, engineering reports, post-mortems |

### Business, finance and strategy

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `boardroom` | Corporate navy and gold on white | #FFFFFF | #1B365D | #8A5A00 | board packs, business reviews, executive committees |
| `consulting` | White, deep green and gray, minimal | #FFFFFF | #0B5D3B | #8A5A00 | strategy proposals, status reports, action titles |
| `ledger` | Light gray, ink blue and green for gains | #F6F7F9 | #12355B | #1D6B52 | financial results, investor updates, number-heavy decks |
| `startup-bright` | White with electric violet and coral | #FFFFFF | #5B2EFF | #B4195B | investor and sales pitches, product launches |
| `venture-dark` | Near-black with violet, orange and mint | #0B0B14 | #7C5CFF | #35E0B1 | dark-room pitches, launch events |
| `signal-yellow` | Black with one loud yellow and a corner triangle | #0E0E0E | #FFC933 | #FFE45C | investor and sales decks that must be remembered, roadmaps |
| `coral-market` | Warm white with coral and violet, dot motif | #FFF8F4 | #D93A52 | #B3263E | B2B product, marketing, market analysis |
| `harbor` | Pale mint-white with navy, steel blue and a red accent, corner triangles | #F1FAEE | #1D3557 | #B3141F | public sector, institutions, OKR and finance reviews |
| `navy-gold` | Ink navy with gold and steel blue, hairline rules | #000814 | #FFC300 | #FFD60A | executive, finance and awards presentations |
| `sunset-mesh` | Warm plum-black with a red-orange-peach mesh gradient | #14090F | #FF4D4D | #FFDB9E | consumer product launches, brand talks |

### Education and impact

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `chalkboard` | Deep green board with chalk yellow, mint and pink | #1F3A2E | #F2E6B1 | #FFB4A2 | lectures, workshops, informal teaching |
| `forest` | Soft green and earth tones | #F7FAF5 | #1F5D3A | #8A4B00 | sustainability, nonprofit, grant proposals, community |
| `terracotta` | Warm cream with clay red and amber, editorial rules | #FBF3E8 | #A14646 | #9A4A0E | humanities, culture, education |
| `sage` | Soft sage greens on off-white with a left stripe | #F5F8F2 | #3F6B4F | #8F5A1C | wellbeing, sustainability, policy reports |
| `lavender` | Pastel lilac, pink and sky mesh with purple type | #FBF8FF | #6B43B5 | #8C2F7E | design critiques, UX research, friendly lectures |

### Portfolio and creative

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `editorial` | Cream paper, black ink and vermilion | #F6F1E7 | #161616 | #B03A0E | magazine-style decks, portfolios, long-form stories |
| `portfolio-mono` | Black and white with one lime accent | #0A0A0A | #F5F5F5 | #C8FF3D | designer and developer portfolios, strong contrast |
| `portfolio-warm` | Warm off-white, terracotta and sage | #FFF8F1 | #A63D1F | #2B6A58 | case studies, creative and friendly portfolios |
| `swiss` | White, black and one red | #FFFFFF | #111111 | #D10A00 | design-led and research-led decks, print handouts |
| `plum` | Aubergine with orange, violet and peach, dot motif | #1A0F24 | #F25912 | #FFB38A | design, media, consumer-brand talks, go-to-market |
| `ember` | Black with ember red and orange, wide display headings and a bar-chart silhouette | #0B0707 | #E5332A | #FFB4A2 | keynotes and product reveals |

### Game styles (only when the user asks)

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `obsidian-craft` | Dark obsidian look with purple veins and IT cyan highlights; pixel blocks, nether-portal title art | #0E0818 | #8B5CF6 | #E879F9 | dark Minecraft-style decks on request |
| `classic-craft` | Light classic block-game look: sky blue, inventory-gray panels, grass and dirt ground, pixel clouds and sun | #D6EBFF | #2E6A14 | #6B4A00 | light Minecraft-style lessons on request |

Each theme also defines surface, secondary, text, muted, success, warning, danger, info and a `series` list of chart colours.

## 2. Fonts and style per theme

The style block changes the component design, not only the colours.

| Theme | Heading font | Cards | Title rule | Footer | Pattern | Deco |
|---|---|---|---|---|---|---|
| `academic` | SourceSerif4 | flat | line | rule | rules | none |
| `aurora-mesh` | Manrope | fill | bar | plain | mesh | none |
| `blueprint` | IBMPlexMono | outline | line | rule | blueprint | none |
| `boardroom` | SourceSerif4 | outline | line | rule | band | none |
| `chalkboard` | Inter | outline | line | rule | rules | none |
| `classic-craft` | PressStart2P | fill | bar | plain | classic | none |
| `clinical` | Inter | fill | bar | plain | clean | none |
| `cloud-light` | Inter | fill | bar | plain | none | none |
| `cobalt-pop` | Unbounded | fill | bar | plain | rings | none |
| `conference-dark` | SourceSerif4 | outline | line | rule | rules | none |
| `consulting` | Inter | outline | line | rule | clean | none |
| `coral-market` | Manrope | fill | bar | plain | dots | none |
| `cyber-hud` | IBMPlexMono | bracket | line | rule | hud | hud |
| `datablue` | Manrope | fill | bar | plain | hatch | none |
| `deep-ocean` | Manrope | fill | bar | plain | rings | none |
| `deep-space` | Inter | fill | bar | plain | grid | none |
| `editorial` | PlayfairDisplay | flat | line | rule | rules | none |
| `ember` | Unbounded | fill | bar | plain | bars | none |
| `forest` | SourceSerif4 | fill | bar | plain | clean | none |
| `glass-dusk` | Manrope | glass | bar | plain | orbs3d | glow |
| `graphite-cyan` | Inter | fill | bar | plain | grid | none |
| `harbor` | Manrope | fill | bar | plain | corner | tri |
| `lavender` | Manrope | fill | bar | plain | mesh | none |
| `ledger` | Inter | flat | bar | rule | band | none |
| `liquid-light` | Manrope | glass | bar | plain | mesh | glow |
| `matrix-green` | IBMPlexMono | outline | line | plain | blueprint | none |
| `midnight-navy` | Inter | fill | bar | plain | grid | none |
| `navy-gold` | PlayfairDisplay | fill | line | rule | rules | none |
| `obsidian-craft` | PressStart2P | fill | bar | plain | obsidian | none |
| `petrol` | Manrope | fill | bar | plain | grid | none |
| `plum` | Manrope | fill | bar | plain | dots | none |
| `portfolio-mono` | Montserrat | outline | none | plain | clean | none |
| `portfolio-warm` | Montserrat | fill | bar | plain | band | none |
| `quantum-teal` | Manrope | fill | bar | plain | mesh | none |
| `sage` | Manrope | fill | bar | plain | clean | none |
| `signal-yellow` | Manrope | fill | bar | plain | corner | tri |
| `startup-bright` | Montserrat | fill | bar | plain | band | none |
| `sunset-mesh` | Manrope | fill | bar | plain | mesh | none |
| `swiss` | Montserrat | outline | line | rule | rules | none |
| `synthwave` | Manrope | fill | bar | plain | mesh | none |
| `terminal-slate` | Inter | fill | bar | plain | grid | none |
| `terracotta` | Manrope | flat | line | plain | rules | none |
| `ultraviolet-core` | Inter | fill | bar | plain | grid | none |
| `venture-dark` | Montserrat | fill | bar | plain | grid | none |

- Cards: `fill` (soft filled panel), `outline` (hairline border on the page colour), `flat` (surface colour, no border).
- Title rule: `bar` (short accent bar), `line` (hairline across the slide plus a short accent bar), `none`.
- Footer: `plain`, `rule` (hairline above the footer). Themes with `show_source` print the slide's `source:` as a footnote.
- Pattern: backdrop on the title and closing slides. Flat motifs: `clean`, `rules`, `band`, `grid`, `none`, `hatch` (hatched side panel),
  `corner` (diagonal corner triangles), `dots` (dot field), `blueprint` (drafting grid and title block), `rings` (concentric circles),
  `bars` (bar-chart silhouette). `mesh` is a four-colour mesh-gradient picture rendered once and cached (needs numpy). Game packs: `blocks`, `obsidian`, `classic`.
- Deco: `tri` puts a small accent triangle in the top-right corner of content slides, `tab` an accent tab on the left edge, `glow` two soft color blooms behind the content, `hud` a tick scale in the top-right corner, `none` nothing.
- Cards (futuristic): `glass` is a frosted pane with a light edge and a top highlight, `bracket` an opaque HUD panel with bright corner brackets. Pattern `hud` draws a wireframe globe with pins and corner brackets; `orbs3d` embeds a rendered 3D object (`hero3d: orbs, ring, cube or stack`).

## 3. Contrast figures

WCAG 2.x ratios computed from the theme files. Body text needs 4.5 or more, large text (18 pt, or 14 pt bold) 3 or more. Formal themes keep text on background at 7 or more.

| Theme | text/bg | muted/bg | muted/surface | primary/bg | accent/bg | on(primary)/primary |
|---|---|---|---|---|---|---|
| `academic` | 16.66 | 8.49 | 7.56 | 9.76 | 7.74 | 10.19 |
| `aurora-mesh` | 17.15 | 8.78 | 7.52 | 14.58 | 13.53 | 16.26 |
| `blueprint` | 13.15 | 8.62 | 6.79 | 8.51 | 9.91 | 12.76 |
| `boardroom` | 15.97 | 7.56 | 6.85 | 12.12 | 5.93 | 12.12 |
| `chalkboard` | 10.91 | 8.27 | 6.76 | 9.82 | 7.22 | 16.73 |
| `classic-craft` | 14.1 | 7.25 | 5.19 | 5.39 | 6.6 | 6.59 |
| `clinical` | 15.59 | 7.38 | 6.59 | 5.96 | 5.43 | 5.96 |
| `cloud-light` | 17.06 | 7.24 | 7.58 | 6.41 | 5.12 | 6.7 |
| `cobalt-pop` | 9.44 | 6.8 | 5.59 | 7.25 | 7.19 | 16.13 |
| `conference-dark` | 16.16 | 8.99 | 7.77 | 7.19 | 10.83 | 8.31 |
| `consulting` | 17.74 | 7.56 | 6.87 | 7.95 | 5.93 | 7.95 |
| `coral-market` | 16.14 | 7.57 | 6.76 | 4.27 | 6.12 | 4.68 |
| `cyber-hud` | 18.09 | 9.01 | 8.05 | 8.24 | 13.69 | 8.6 |
| `datablue` | 17.65 | 9.86 | 8.34 | 5.34 | 15.0 | 5.82 |
| `deep-ocean` | 17.42 | 9.39 | 7.84 | 7.66 | 12.67 | 8.52 |
| `deep-space` | 18.79 | 9.17 | 8.05 | 3.87 | 6.12 | 4.86 |
| `editorial` | 16.36 | 7.21 | 6.35 | 16.08 | 5.4 | 18.1 |
| `ember` | 18.18 | 9.44 | 8.62 | 4.62 | 11.74 | 4.84 |
| `forest` | 15.52 | 7.23 | 6.41 | 7.43 | 6.46 | 7.82 |
| `glass-dusk` | 17.14 | 9.29 | 8.02 | 5.98 | 13.22 | 6.42 |
| `graphite-cyan` | 15.02 | 7.11 | 6.19 | 7.63 | 14.54 | 8.86 |
| `harbor` | 14.85 | 6.14 | 5.33 | 11.56 | 6.47 | 12.36 |
| `lavender` | 14.37 | 7.03 | 6.12 | 6.45 | 7.08 | 6.78 |
| `ledger` | 16.12 | 7.07 | 7.58 | 11.62 | 5.98 | 12.46 |
| `liquid-light` | 15.9 | 6.89 | 7.76 | 5.59 | 4.96 | 6.29 |
| `matrix-green` | 18.42 | 8.85 | 7.86 | 11.63 | 14.78 | 12.63 |
| `midnight-navy` | 17.09 | 7.3 | 6.61 | 5.09 | 10.36 | 5.71 |
| `navy-gold` | 18.73 | 9.88 | 8.26 | 12.5 | 14.24 | 13.06 |
| `obsidian-craft` | 16.69 | 8.8 | 8.05 | 4.65 | 8.0 | 4.96 |
| `petrol` | 16.51 | 9.15 | 7.17 | 4.81 | 12.67 | 5.63 |
| `plum` | 16.37 | 8.69 | 7.59 | 5.46 | 10.61 | 6.21 |
| `portfolio-mono` | 18.16 | 7.85 | 7.17 | 18.16 | 16.81 | 19.26 |
| `portfolio-warm` | 15.73 | 7.78 | 6.93 | 6.03 | 6.04 | 6.35 |
| `quantum-teal` | 15.21 | 5.97 | 5.33 | 4.91 | 5.17 | 5.18 |
| `sage` | 13.9 | 6.72 | 5.88 | 5.72 | 5.37 | 6.13 |
| `signal-yellow` | 19.3 | 10.28 | 9.07 | 12.55 | 15.17 | 13.65 |
| `startup-bright` | 18.41 | 7.92 | 7.02 | 6.4 | 6.5 | 6.4 |
| `sunset-mesh` | 17.99 | 10.28 | 9.31 | 5.97 | 14.76 | 6.42 |
| `swiss` | 18.88 | 7.46 | 6.6 | 18.88 | 5.59 | 18.88 |
| `synthwave` | 17.9 | 9.6 | 8.77 | 3.77 | 10.23 | 5.22 |
| `terminal-slate` | 16.02 | 6.15 | 5.62 | 7.49 | 7.45 | 8.31 |
| `terracotta` | 15.0 | 6.86 | 5.92 | 5.48 | 5.68 | 6.03 |
| `ultraviolet-core` | 17.2 | 8.61 | 7.66 | 4.46 | 12.27 | 4.96 |
| `venture-dark` | 18.02 | 8.49 | 7.76 | 4.51 | 11.61 | 4.83 |

## 4. Pitfalls

- White text on the primary colour fails body-text contrast in several themes. The layouts use `theme.on(fill)`, which
  picks the most readable text colour; do the same in custom code instead of hard-coding white.
- Primary as text on the background is large-text only where its ratio is below 4.5 (`deep-space`, `ultraviolet-core`,
  `classic-craft`, `synthwave`, `coral-market`). Use primary for shapes and chart fills, not paragraphs.
- Mesh covers (`aurora-mesh`, `sunset-mesh`, `quantum-teal`, `synthwave`, `lavender`) keep a veil of the page colour under the text zone and the lint
  checks text against the lightest (dark themes) or darkest (light themes) pixel there; never put small text on the open right side of a cover.
- Do not encode meaning by colour alone: red, amber and green dots carry a word (`GREEN`, `AMBER`, `RED`) and chips carry text.
- A dark theme in a bright room washes out and a light theme on a dark stage glares: pick by the venue (`design/accessibility.md`).
- Chart series come from the theme's `series` list; with more series than colours, switch to small multiples or a table.

## 5. Using a custom palette

Add a theme file (`extending.md`), run `cli.py themes` to read its ratios, and fix any pair below 4.5. A brand colour that
fails as text can still be used as a fill with `on()` text. Measure a palette from a reference with
`cli.py inspire --from-image shot.png` (`design/inspiration/README.md`).

## 6. As-of note

Palette trends move; these colours follow common conventions of each genre as of 2026-10 (checked against Color Hunt, Coolors and Meshy on 2026-10-16). Verify taste against the audience
and the venue, not against this table.
