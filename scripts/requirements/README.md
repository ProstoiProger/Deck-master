# Requirements

Dependency groups, each file starts with `-r core.txt`. Minimums only; no upper bounds.

| Group | File | Needed for |
|---|---|---|
| core | `core.txt` | parsing decks, themes, lint, text measuring (`pyyaml`, `pillow`, `fonttools`) |
| pptx | `pptx.txt` | writing `.pptx` (`python-pptx`) |
| pdf | `pdf.txt` | writing `.pdf` (`reportlab`) |
| charts | `charts.txt` | themed charts (`matplotlib`) |
| preview | `preview.txt` | PDF to PNG thumbnails and contact sheets (`pymupdf`) |

Install: `python -m pip install -r scripts/requirements/pptx.txt -r scripts/requirements/pdf.txt -r scripts/requirements/charts.txt -r scripts/requirements/preview.txt`

Verify: `python scripts/install_check.py core pptx pdf charts preview`

Run tests: `python -m pytest scripts/tests -q`

Notes on minimums:
- `python-pptx` 1.0 dropped Python 2 shims and is the first release with typed shapes used here.
- `pymupdf` imports as `pymupdf` (the old `fitz` name is deprecated).
- No system binary is required. LibreOffice is not used: the PDF is drawn by `reportlab`, not converted from PPTX.
