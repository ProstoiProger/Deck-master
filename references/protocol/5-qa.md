# Stage 5: QA

Goal: prove the deck is readable, true, on time and complete before it is delivered.

## Contents

1. Gates
2. Look at the previews
3. Symptom table
4. Trace and timing
5. Rehearsal
6. Checklist

---

## 1. Gates

| Gate | Command | Pass when |
|---|---|---|
| Lint | `python scripts/cli.py lint deck.md` | no Critical or High finding |
| Previews | `python scripts/cli.py preview deck.md --sheet` | contact sheet viewed, every slide opened at least once |
| Trace | `python scripts/cli.py trace deck.md` | every requirement met, exit 0 |
| Timing | `python scripts/cli.py timing deck.md` | total within the budget, reserve about 10 percent |

## 2. Look at the previews

Open the PNGs, not only the lint output: lint cannot see "looks wrong". On each slide check:

- the title states the takeaway and fits in two lines;
- nothing touches the edges or another element; no text sits on busy decoration;
- one idea, at most seven bullets, numbers large enough to read from the back of the room;
- the chart has labelled axes and a visible highlight; the image is cropped to what matters;
- text in non-Latin scripts shows real letters, not boxes.

The PDF is drawn by this skill's renderer. PowerPoint lays out text itself, so open the PPTX once in PowerPoint or
another viewer and check the same slides; line breaks can differ slightly. Fonts must be installed there
(`design/typography.md`).

## 3. Symptom table

| Symptom | Likely cause | Fix |
|---|---|---|
| text overflow finding | too many words for the layout | cut to the point, move detail to notes |
| contrast finding | custom colour on a themed fill | use theme tokens; `cli.py themes` shows ratios |
| unsourced number finding | number typed from memory | add `source:` or remove the number |
| over time finding | notes too long or too many slides | cut slides first, then words (`ops/time-budget.md`) |
| glyph finding | font lacks the script | `design/typography.md` |
| chart not drawn | non-numeric cell or missing `matplotlib` | fix the table, install `scripts/requirements/charts.txt` |
| all slides look alike | one layout reused | choose by message (`protocol/3-design.md`) |

## 4. Trace and timing

`trace` prints `Requirement | Text | Slides | Evidence | Status` from the front matter rubric (or `--brief` with
lines `R1: text`). Any NOT MET row is Critical: add the slide or tell the user the requirement is not covered.

## 5. Rehearsal

Read the notes aloud with a timer at least twice. Prepare answers with `communication/judge-qa.md`. Have a PDF
copy and, for a demo, a recorded backup (`communication/demo.md`).

## 6. Checklist

- [ ] Lint clean, previews viewed, trace exit 0, timing within budget.
- [ ] PPTX opened once in a real viewer, fonts installed or fallback accepted.
- [ ] Web version opened once in a browser: arrow keys through every slide, notes (`N`) and overview (`O`) work, links on the last slide open.
- [ ] Final report lists assumptions, illustrative numbers and anything unverified.
