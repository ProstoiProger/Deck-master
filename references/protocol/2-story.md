# Stage 2: Story

Goal: one message, one slide list, one time budget. Words come after this stage, not before.

## Contents

1. The one message
2. Slide list
3. Titles as takeaways
4. Time per slide
5. Cut order
6. Checklist

---

## 1. The one message

Write one sentence that the audience should repeat after leaving: who gets what change, shown by what evidence.
Example: "Scoring each card swipe on arrival cuts alert delay from 40 minutes to 2 seconds."
If you cannot write it, the work, not the deck, is the problem: say so and ask for the missing result.

## 2. Slide list

Start from the skeleton in `communication/slides.md` for the event, then adapt:

1. List the slides as titles only.
2. Map each rubric item to at least one slide (`communication/rubric-mapping.md`).
3. Remove any slide that does not serve the message or a rubric item; move it to an appendix.
4. Order by the arc in `communication/pitch-story.md`: problem, insight, solution, evidence, impact, trust, path.

## 3. Titles as takeaways

| Weak (label) | Strong (takeaway) |
|---|---|
| Results | The streaming model beats the batch baseline on every metric |
| Architecture | Three layers keep scoring under two seconds |
| Problem | Fraud alerts arrive 40 minutes late |

Rule: a title is a sentence a judge could disagree with. Keep it under about 14 words.

## 4. Time per slide

Budget from `ops/time-budget.md`: about 1 minute per content slide, title and closing 10 to 20 seconds, the demo
slide gets the largest share in a hackathon, the key finding in a datathon. Put seconds in `time:` or let
`cli.py timing` derive them from the notes.

## 5. Cut order

When over time, cut in this order: extra background, second example, secondary charts, team slide detail, polish.
Never cut: the problem, the evidence, the demo (hackathon), the limits (datathon, research).

## 6. Checklist

- [ ] One-sentence message written.
- [ ] Slide titles are takeaways and read as a story in order.
- [ ] Every rubric item has a slide; every slide serves the message or a rubric item.
- [ ] Time per slide sums to the budget with a reserve of about 10 percent.
- [ ] Appendix slides marked so they are skipped in the talk.
