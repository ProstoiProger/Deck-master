# Mode: research talk

A talk for peers or a committee: a claim, the evidence, the limits. Also used for project defenses and seminars.

## Workflow

1. State the claim in one sentence; put it in the title slide subtitle or slide 2.
2. Motivate in one slide: the gap, with one number.
3. Method in one slide: only what is needed to read the results.
4. Main result: one table or figure, with seeds, intervals and the baseline that matters most.
5. Second result: ablation or robustness check that answers the obvious doubt.
6. Limits and open questions, honestly; reviewers reward it.
7. Closing with the claim again, the code and data links, and contact.
8. Prepare backup slides for the three likeliest questions (`communication/judge-qa.md`).

## Skeleton

Use `assets/templates/deck-research-talk.md` (8 to 14 slides, 10 to 15 minutes): title, gap, method, main result,
comparison, limits, closing; theme `academic` (`conference-dark` in dark rooms, `graphite-cyan` for engineering talks). For thesis
defenses and conference papers see `modes/scientific.md`.

## Claims checklist

- [ ] Every claim names its evidence slide.
- [ ] Baselines are fair and named; the strongest one is in the main table.
- [ ] Uncertainty shown: seeds, intervals or a paired test.
- [ ] Data and code availability stated; licences and ethics noted where relevant.
- [ ] Negative or null results stated, not hidden.

## Traps

- Ten minutes of related work.
- Equations nobody can read from the back row.
- A results slide with eight columns; keep the main table to what the claim needs.
- Over-claiming: "outperforms" when the interval overlaps.
