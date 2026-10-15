# Slides

Skeletons per event and writing rules for slides. Defaults come from `assets/presets/events.yaml`; the brief overrides
them.

## Hackathon: 6 to 8 slides, 3 to 5 minutes

| # | Slide | Layout | Content |
|---|---|---|---|
| 1 | Title and hook | `title` | name, one-line promise, team |
| 2 | Problem | `problem` | who suffers, one number, one source |
| 3 | Solution | `solution` | one line, three benefits, product picture |
| 4 | How it works | `architecture` | three layers, key component highlighted |
| 5 | Demo | `demo` | screenshot with three callouts, or the live demo |
| 6 | Evidence | `kpi` | measured result against a baseline |
| 7 | Impact and adoption | `roadmap` | now, next, later, what a pilot needs |
| 8 | Closing | `closing` | repo, contact, thanks |

## Datathon: about 10 slides, 5 to 7 minutes

| # | Slide | Layout | Content |
|---|---|---|---|
| 1 | Title | `title` | question and headline answer |
| 2 | Problem and stakes | `problem` | decision, cost, one number |
| 3 | Data and checks | `pipeline` | cleaning, split, leakage and quality checks |
| 4 | Key insight | `chart_insight` | the headline finding |
| 5 | Second insight | `chart_insight` | a finding that qualifies or extends it |
| 6 | Approach and result | `comparison` | method against baseline |
| 7 | Business impact | `kpi` | size of effect, assumptions |
| 8 | Explainability and fairness | `bullets` | drivers, segments, risks (when relevant) |
| 9 | Limits and next steps | `impact` | what we cannot claim, what to do |
| 10 | Closing | `closing` | repo, contact |

## Assignment: 8 to 15 slides, 8 to 12 minutes

Title, agenda (the rubric lines), one section per criterion (requirements, method, result, evaluation), conclusion
and limits, closing, then appendix with references and long tables.

## Research talk: 8 to 14 slides, 10 to 15 minutes

Title with the claim, gap, method, main result, comparison or ablation, limits, closing, backup slides.

## Design rules for slides

- High contrast, large fonts: body at least 18 pt, never below 11 pt anywhere.
- Title is a takeaway sentence (`communication/pitch-story.md`).
- One chart per slide with a highlighted bar or line; labels in words.
- Consistent colours: one accent for the thing that matters, one for the baseline.
- Dense tables go to the appendix; the main slide shows only the columns the claim needs.
- Numbers large, context small: "0.92" big, "F1, vs 0.81 baseline" small.
- A speaker does not read the slide: the slide shows, the notes tell.
- Last slide is the contact and the repo, not "Thank you" alone; the closing layout keeps it short.
