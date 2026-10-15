# Environment

Discover the environment yourself before asking the user.

## Check

```
python scripts/cli.py env                  packages, fonts, skill root (add --json file.json to save)
python scripts/install_check.py core pptx pdf charts preview
```

| Missing | Effect | Fix |
|---|---|---|
| `python-pptx` | no `.pptx` | `python -m pip install -r scripts/requirements/pptx.txt` |
| `reportlab` | no `.pdf` | `python -m pip install -r scripts/requirements/pdf.txt` |
| `matplotlib` | chart slides show a finding, not a chart | `python -m pip install -r scripts/requirements/charts.txt` |
| `pymupdf` | no `preview` PNGs | `python -m pip install -r scripts/requirements/preview.txt` |

No system program is required. LibreOffice and PowerPoint are not used for building; the PDF is drawn directly.

## Fonts

The PDF embeds the bundled fonts from `assets/fonts`, so it looks the same everywhere. A PPTX stores only font
names, so the machine that opens it needs Inter (and JetBrains Mono, Press Start 2P for the game themes) installed,
otherwise PowerPoint substitutes another font and line breaks move. Install by opening each `.ttf` in
`assets/fonts` and choosing Install, or send the PDF instead. Details: `design/typography.md`.

## Viewers

- PowerPoint, Keynote and Google Slides open the PPTX; Google Slides replaces missing fonts silently.
- Check the deck once in the viewer that will be used on stage.
- Projector or screen share: 16:9 (13.333 by 7.5 inches) is used for every deck.

## Network

Nothing here needs the network at build time. Do not send material to online services without the user's approval
(`ops/security.md`).

## Where the skill can live

The CLI finds its own folder, so the skill can sit anywhere: a Claude Code skills folder, a Codex skills folder, a
vendored `.deck-master` folder in a project, or a plain clone. `python scripts/install.py` copies or links it
(see `extending.md`).
