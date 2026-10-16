# Playbook: data story (datathon final, analytics readout)

**Preconditions**: an analysis exists (notebook, model, tables); the audience decides something with it; 6 to 10 minutes.
Event: `data-story` (use `datathon` when the jury has a published rubric with weights).

## Steps

1. **The decision**: one `statement` slide with the number that frames it ("Teams spend / 31 hours / ..."), with `source:`.
2. **Data and checks**: `schema` for the tables and keys, one line on cleaning, joins and the leakage check; say what you excluded.
3. **Findings**: `insight_cards` with up to three findings, each with its evidence number and the action it leads to.
4. **One chart per finding**: `chart_insight` with the right kind (`bar` to compare, `line` over time, `lollipop` for rankings,
   `heatmap` for two dimensions, `slope` for before and after, `radar` only for four to six comparable axes).
5. **Method**: `model_card` when a model is part of the answer: facts, headline metrics on a time-ordered holdout, known limits.
6. **Limits and next steps**: `impact` with two groups: what we can claim, what we cannot.
7. **Reproduce**: `links` to the notebook and the data card.
8. **Scaffold**: `new --event data-story` (theme `datablue`; `ultraviolet-core` is the classic datathon look).
9. **QA**: every number has a `source:` that points to a cell or a file; a baseline sits next to every metric; the holdout is
   described; lint, previews, timed run.

## Traps

Showing the model before the question; ten charts with no ranking; a metric with no baseline; random splits on time-ordered
data; a recommendation that does not follow from the findings.

## Output

Deck source, `.pptx`, `.pdf`, speaker script, a backup appendix (cohort tables, error analysis) for questions.
