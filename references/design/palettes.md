# Palettes

Eight themes live in `assets/themes/*.yaml`. Six are the stereotyped IT looks (navy blue, purple, dark gray, with
cyan, blue or pink accents; one light variant); two are block-game style packs, one dark (`obsidian-craft`) and one
light (`classic-craft`). Hex values are our own
proposals from the IT genre, not sampled from any template. Live figures: `cli.py themes`; full table:
`design/catalog.md`.

## Contents

1. Themes at a glance
2. Contrast figures
3. Pitfalls
4. Using a custom palette
5. As-of note

---

## 1. Themes at a glance

| Theme | Mood | bg | primary | accent | Use for |
|---|---|---|---|---|---|
| `midnight-navy` | default IT, calm authority | #0B1220 | #3B82F6 | #22D3EE | tech pitches, unsure choices |
| `ultraviolet-core` | data and AI, modern | #120B2E | #8B5CF6 | #00E5FF | datathons, AI and ML stories |
| `graphite-cyan` | engineering, restrained | #14161B | #00B8D9 | #7DF9FF | research talks, architecture reviews |
| `deep-space` | loud, stage energy | #0A0F2C | #6C5CE7 | #FF4F9A | hackathon finals, demo days |
| `terminal-slate` | developer console | #0D1117 | #58A6FF | #3FB950 | dev tools, security, CLI products |
| `cloud-light` | clean, printable | #F8FAFC | #1D4ED8 | #0E7490 | assignments, handouts, bright rooms |
| `obsidian-craft` | dark obsidian, purple veins, IT cyan | #0E0818 | #8B5CF6 | #E879F9 | hackathons and tech events with a game flavour |
| `classic-craft` | light classic: sky, inventory gray, grass | #D6EBFF | #2E6A14 | #6B4A00 | education, assignments, fun events, bright rooms |

Each theme also defines surface, secondary, text, muted, success, warning, danger.

## 2. Contrast figures

WCAG 2.x ratios computed from the theme files. Body text needs 4.5 or more, large text (18 pt, or 14 pt bold) 3 or more.

| Theme | text/bg | muted/bg | muted/surface | primary/bg | primary/surface | accent/bg |
|---|---|---|---|---|---|---|
| `midnight-navy` | 17.09 | 7.30 | 6.61 | 5.09 | 4.61 | 10.36 |
| `ultraviolet-core` | 17.20 | 8.61 | 7.66 | 4.46 | 3.96 | 12.27 |
| `graphite-cyan` | 15.02 | 7.11 | 6.19 | 7.63 | 6.64 | 14.54 |
| `deep-space` | 18.79 | 9.17 | 8.05 | 3.87 | 3.40 | 6.12 |
| `terminal-slate` | 16.02 | 6.15 | 5.62 | 7.49 | 6.85 | 7.45 |
| `cloud-light` | 17.06 | 7.24 | 7.58 | 6.41 | 6.70 | 5.12 |
| `obsidian-craft` | 16.69 | 8.80 | 8.05 | 4.65 | 4.25 | 8.00 |
| `classic-craft` | 14.10 | 7.25 | 5.19 | 3.99 | 2.95 | 3.72 |

## 3. Pitfalls

- White text on the primary colour fails body-text contrast in several themes (`graphite-cyan` 2.37,
  `terminal-slate` 2.53, `midnight-navy` 3.68). The layouts use `theme.on(fill)`, which picks the
  most readable text colour; do the same in custom code instead of hard-coding white.
- Primary as text on a surface is large-text only in `deep-space` (3.40), `ultraviolet-core` (3.96), `obsidian-craft`
  (4.25) and `classic-craft` (2.95; there primary is a fill colour, its text is `on(primary)`). Use primary for shapes and chart fills, not paragraphs.
- Do not encode meaning by colour alone: pair success, warning and danger with a word or icon.
- Light theme on a dark projector washes out; dark themes lose detail on cheap bright projectors. See
  `design/accessibility.md`.

## 4. Using a custom palette

Add a theme file (`extending.md`), run `cli.py themes` to read its ratios, and fix any pair below 4.5. A brand
colour that fails as text can still be used as a fill with `on()` text. Measure a palette from a reference with
`cli.py inspire --from-image shot.png` (`design/inspiration/README.md`).

## 5. As-of note

Palette trends move; the colours here follow the dark navy, purple and gray tech genre as of 2026-10. Verify taste
against the audience and the venue, not against this table.
