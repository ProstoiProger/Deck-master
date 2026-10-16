# Palettes

Twenty-one themes live in `assets/themes/*.yaml`. Nineteen are formal and grouped by scope (technology, science, business,
education, portfolio); two are block-game style packs that the skill uses only when the user asks for Minecraft or a
gamified deck. Hex values are our own proposals, not sampled from any template; every theme passes the contrast checks in
section 3. Live figures: `cli.py themes` (`--scope <scope>` filters); full table: `design/catalog.md`; choosing by kind of
deck: `design/scopes.md`.

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

### Science and research

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `academic` | Warm paper white, deep blue and crimson | #FBFAF6 | #1F3C88 | #9B1C2E | conference talks, thesis defenses, seminars |
| `conference-dark` | Ink blue-black with soft blue and amber | #0E1621 | #6FA8DC | #F2C14E | dark conference rooms, recorded talks |
| `clinical` | Clean white with teal and orange | #FFFFFF | #0B6E79 | #B54708 | medicine, life science, teaching with data |

### Business, finance and strategy

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `boardroom` | Corporate navy and gold on white | #FFFFFF | #1B365D | #8A5A00 | board packs, business reviews, executive committees |
| `consulting` | White, deep green and gray, minimal | #FFFFFF | #0B5D3B | #8A5A00 | strategy proposals, status reports, action titles |
| `ledger` | Light gray, ink blue and green for gains | #F6F7F9 | #12355B | #1D6B52 | financial results, investor updates, number-heavy decks |
| `startup-bright` | White with electric violet and coral | #FFFFFF | #5B2EFF | #B4195B | investor and sales pitches, product launches |
| `venture-dark` | Near-black with violet, orange and mint | #0B0B14 | #7C5CFF | #35E0B1 | dark-room pitches, launch events |

### Education and impact

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `chalkboard` | Deep green board with chalk yellow, mint and pink | #1F3A2E | #F2E6B1 | #FFB4A2 | lectures, workshops, informal teaching |
| `forest` | Soft green and earth tones | #F7FAF5 | #1F5D3A | #8A4B00 | sustainability, nonprofit, grant proposals, community |

### Portfolio and creative

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `editorial` | Cream paper, black ink and vermilion | #F6F1E7 | #161616 | #B03A0E | magazine-style decks, portfolios, long-form stories |
| `portfolio-mono` | Black and white with one lime accent | #0A0A0A | #F5F5F5 | #C8FF3D | designer and developer portfolios, strong contrast |
| `portfolio-warm` | Warm off-white, terracotta and sage | #FFF8F1 | #A63D1F | #2B6A58 | case studies, creative and friendly portfolios |

### Game styles (only when the user asks)

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `obsidian-craft` | Dark obsidian look with purple veins and IT cyan highlights; pixel blocks, nether-portal title art | #0E0818 | #8B5CF6 | #E879F9 | dark Minecraft-style decks on request |
| `classic-craft` | Light classic block-game look: sky blue, inventory-gray panels, grass and dirt ground, pixel clouds and sun | #D6EBFF | #2E6A14 | #6B4A00 | light Minecraft-style lessons on request |

Each theme also defines surface, secondary, text, muted, success, warning, danger, info and a `series` list of chart colours.

## 2. Fonts and style per theme

The style block changes the component design, not only the colours.

| Theme | Heading font | Cards | Title rule | Footer | Pattern |
|---|---|---|---|---|---|
| `midnight-navy` | Inter | fill | bar | plain | grid |
| `ultraviolet-core` | Inter | fill | bar | plain | grid |
| `graphite-cyan` | Inter | fill | bar | plain | grid |
| `deep-space` | Inter | fill | bar | plain | grid |
| `terminal-slate` | Inter | fill | bar | plain | grid |
| `cloud-light` | Inter | fill | bar | plain | none |
| `academic` | SourceSerif4 | flat | line | rule | rules |
| `conference-dark` | SourceSerif4 | outline | line | rule | rules |
| `clinical` | Inter | fill | bar | plain | clean |
| `boardroom` | SourceSerif4 | outline | line | rule | band |
| `consulting` | Inter | outline | line | rule | clean |
| `ledger` | Inter | flat | bar | rule | band |
| `startup-bright` | Montserrat | fill | bar | plain | band |
| `venture-dark` | Montserrat | fill | bar | plain | grid |
| `chalkboard` | Inter | outline | line | rule | rules |
| `forest` | SourceSerif4 | fill | bar | plain | clean |
| `editorial` | PlayfairDisplay | flat | line | rule | rules |
| `portfolio-mono` | Montserrat | outline | none | plain | clean |
| `portfolio-warm` | Montserrat | fill | bar | plain | band |
| `obsidian-craft` | PressStart2P | fill | bar | plain | obsidian |
| `classic-craft` | PressStart2P | fill | bar | plain | classic |

- Cards: `fill` (soft filled panel), `outline` (hairline border on the page colour), `flat` (surface colour, no border).
- Title rule: `bar` (short accent bar), `line` (hairline across the slide plus a short accent bar), `none`.
- Footer: `plain`, `rule` (hairline above the footer). Themes with `show_source` print the slide's `source:` as a footnote.
- Pattern: backdrop motif on the title and closing slides (`clean`, `rules`, `band`, `grid`, `blocks`, `obsidian`, `classic`, `none`).

## 3. Contrast figures

WCAG 2.x ratios computed from the theme files. Body text needs 4.5 or more, large text (18 pt, or 14 pt bold) 3 or more. Formal themes keep text on background at 7 or more.

| Theme | text/bg | muted/bg | muted/surface | primary/bg | accent/bg | on(primary)/primary |
|---|---|---|---|---|---|---|
| `midnight-navy` | 17.09 | 7.3 | 6.61 | 5.09 | 10.36 | 5.71 |
| `ultraviolet-core` | 17.2 | 8.61 | 7.66 | 4.46 | 12.27 | 4.96 |
| `graphite-cyan` | 15.02 | 7.11 | 6.19 | 7.63 | 14.54 | 8.86 |
| `deep-space` | 18.79 | 9.17 | 8.05 | 3.87 | 6.12 | 4.86 |
| `terminal-slate` | 16.02 | 6.15 | 5.62 | 7.49 | 7.45 | 8.31 |
| `cloud-light` | 17.06 | 7.24 | 7.58 | 6.41 | 5.12 | 6.7 |
| `academic` | 16.66 | 8.49 | 7.56 | 9.76 | 7.74 | 10.19 |
| `conference-dark` | 16.16 | 8.99 | 7.77 | 7.19 | 10.83 | 8.31 |
| `clinical` | 15.59 | 7.38 | 6.59 | 5.96 | 5.43 | 5.96 |
| `boardroom` | 15.97 | 7.56 | 6.85 | 12.12 | 5.93 | 12.12 |
| `consulting` | 17.74 | 7.56 | 6.87 | 7.95 | 5.93 | 7.95 |
| `ledger` | 16.12 | 7.07 | 7.58 | 11.62 | 5.98 | 12.46 |
| `startup-bright` | 18.41 | 7.92 | 7.02 | 6.4 | 6.5 | 6.4 |
| `venture-dark` | 18.02 | 8.49 | 7.76 | 4.51 | 11.61 | 4.83 |
| `chalkboard` | 10.91 | 8.27 | 6.76 | 9.82 | 7.22 | 16.73 |
| `forest` | 15.52 | 7.23 | 6.41 | 7.43 | 6.46 | 7.82 |
| `editorial` | 16.36 | 7.21 | 6.35 | 16.08 | 5.4 | 18.1 |
| `portfolio-mono` | 18.16 | 7.85 | 7.17 | 18.16 | 16.81 | 19.26 |
| `portfolio-warm` | 15.73 | 7.78 | 6.93 | 6.03 | 6.04 | 6.35 |
| `obsidian-craft` | 16.69 | 8.8 | 8.05 | 4.65 | 8.0 | 4.96 |
| `classic-craft` | 14.1 | 7.25 | 5.19 | 5.39 | 6.6 | 6.59 |

## 4. Pitfalls

- White text on the primary colour fails body-text contrast in several themes. The layouts use `theme.on(fill)`, which
  picks the most readable text colour; do the same in custom code instead of hard-coding white.
- Primary as text on the background is large-text only where its ratio is below 4.5 (`deep-space`, `ultraviolet-core`,
  `classic-craft`). Use primary for shapes and chart fills, not paragraphs.
- Do not encode meaning by colour alone: red, amber and green dots carry a word (`GREEN`, `AMBER`, `RED`) and chips carry text.
- A dark theme in a bright room washes out and a light theme on a dark stage glares: pick by the venue (`design/accessibility.md`).
- Chart series come from the theme's `series` list; with more series than colours, switch to small multiples or a table.

## 5. Using a custom palette

Add a theme file (`extending.md`), run `cli.py themes` to read its ratios, and fix any pair below 4.5. A brand colour that
fails as text can still be used as a fill with `on()` text. Measure a palette from a reference with
`cli.py inspire --from-image shot.png` (`design/inspiration/README.md`).

## 6. As-of note

Palette trends move; these colours follow common conventions of each genre as of 2026-10. Verify taste against the audience
and the venue, not against this table.
