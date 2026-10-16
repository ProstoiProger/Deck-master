# Stage 4: Build

Goal: a finished deck source, a clean lint, a PPTX, a PDF and a web presentation (HTML).

## Contents

1. Setup
2. Write the source
3. Lint
4. Build
5. Rules while writing
6. Checklist

---

## 1. Setup

```
python scripts/install_check.py core pptx pdf charts preview
python scripts/cli.py new --event hackathon --out decks/pitch.md
```

`new` copies the event skeleton with `<placeholders>` and refuses to overwrite an existing file. Fill the front
matter first: title, event, theme, minutes, team, rubric.

## 2. Write the source

One Markdown file. Front matter, then slides separated by `---`. Each slide: `# takeaway title`, property lines
(`layout:`, `rubric:`, `source:`, `notes:`, and layout-specific ones), then the body.

```
# Alerts arrive 40 minutes late
layout: problem
rubric: R1
stat: 40 min | median delay
source: brief.pdf p.3
notes: Say the pain in the user's words.
- 3 of 4 cases are card-not-present
```

All properties and layout inputs: `design/catalog.md`; a full example: `examples/studybuddy-obsidian/studybuddy.md`.

## 3. Lint

`python scripts/cli.py lint decks/pitch.md` prints `[Severity] slide N (layout): message` and exits 1 on Critical or
High. Placeholders left in the text are High findings, so a fresh scaffold fails until it is filled.

## 4. Build

```
python scripts/cli.py build decks/pitch.md --out build
python scripts/cli.py preview decks/pitch.md --out build/preview --sheet
```

`build` lints first and refuses on blocking findings unless `--force` (say so in the report when used). It writes
`<name>.pptx`, `<name>.pdf` and `<name>.html` plus `log.jsonl` (name a format, `--pptx`, `--pdf` or `--html`, to build only that one).
The `.html` is one self-contained file for a browser (`cli.py serve <name>.html` opens it; `design/web-presentation.md`). `--theme <name>` restyles without touching the source.

## 5. Rules while writing

- Text in the source is in the deck language; the skill's own files stay English.
- Numbers come from the user's logs or files, never from memory. Put the origin in `source:`.
- Illustrative numbers are marked `sample: true` in the front matter and named as illustrative in the report.
- Notes are what the speaker says, 1 to 3 sentences per slide; see `communication/speaker-notes.md`.
- Edit the `.md`, rebuild; do not patch the PPTX by hand.

## 6. Checklist

- [ ] Source lints with no Critical or High finding.
- [ ] `.pptx` and `.pdf` built; previews rendered.
- [ ] Every number has a source; every slide has notes.
- [ ] Front matter rubric ids all appear on slides.
