# Typography

Fonts are bundled in `assets/fonts` (SIL OFL) and declared in `assets/presets/fonts.yaml`. Three roles: `heading`,
`body`, `mono` (labels, numbers in footers, code).

## Script coverage

Measured with fontTools on 2026-10:

| Font | Latin | Cyrillic | Kazakh letters (ә ғ қ ң ө ү ұ һ і) | Used for |
|---|---|---|---|---|
| Inter | yes | yes | yes | heading and body in every IT theme |
| JetBrains Mono | yes | yes | mostly no | footers, pills, code |
| Press Start 2P | yes | yes | yes | headings in `obsidian-craft` and `classic-craft` |

Candidates rejected on coverage: Space Grotesk (no Cyrillic), Manrope (Cyrillic yes, Kazakh letters partly missing),
Pixelify Sans (poor Cyrillic and Kazakh), Silkscreen and VT323 (no Cyrillic).

Text with a glyph that a role's font lacks falls back to the body font automatically (for example Kazakh text in a
mono label). If the body font lacks it too, `cli.py lint` reports a High finding with the characters.

## Sizes

| Element | Size |
|---|---|
| Slide title | 28 to 34 pt, up to 52 pt on the title slide; the layout shrinks to fit two lines |
| Body and bullets | 18 to 24 pt; never below 14 pt for text the audience must read |
| Captions and context | 14 to 16 pt |
| Footer and labels | 11 to 12 pt (minimum anywhere: 11 pt) |
| Pixel font headings | scaled to about 0.55 of normal because the font is wide; minimum 12 pt |

## Installing fonts for PPTX

A PPTX stores only font names. Without Inter installed, PowerPoint swaps in another font and wrapping changes.

- Windows: open each `.ttf` in `assets/fonts` and press Install.
- macOS: open each `.ttf` in Font Book and Install.
- Google Slides and Keynote: use the PDF, or upload the fonts where supported.
- The PDF embeds the fonts and always looks as previewed.

Fallbacks written in `fonts.yaml`: Segoe UI for Inter, Consolas for the mono and pixel fonts.

## Adding a language

1. Check coverage: `textfit.missing_glyphs(theme, "body", "sample text")` from `scripts/deckkit/core/textfit.py`, or
   build a one-slide deck in that language and run `cli.py lint`.
2. If a script is missing, add a font that covers it to `assets/fonts` and `fonts.yaml` and point the theme at it.
3. Add a sample deck in that language and a glyph test in `scripts/tests`.

CJK, Arabic and Indic scripts need shaping and larger fonts than the bundled set; add and verify before promising them.
