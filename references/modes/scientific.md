# Mode: scientific talk

For conference talks, seminars, thesis and project defenses, and lab meetings. Events: `research-talk`, `thesis-defense`,
`conference-paper`. Themes: `academic` (light, serif), `conference-dark`, `clinical`, `graphite-cyan`.

## What the audience judges

Novelty, soundness of the method, strength of the evidence, clarity. They read slides critically: unsupported claims,
missing baselines and hidden limits cost more than plain design.

## Story

| Part | Slide | Layout |
|---|---|---|
| Claim | title with the claim in the subtitle | `title` |
| Gap | what existing work cannot do, with one number | `problem` |
| Question | the research question and numbered hypotheses | `hypotheses` |
| Method | three to five steps, no more than the audience needs to trust the result | `pipeline` |
| Data | size, period, split, licence | `factsheet` |
| Main result | one figure and what to see in it | `figure` |
| Robustness | two panels or a comparison table | `figures2`, `comparison` |
| Limits | shown versus open | `impact` |
| References | numbered, in small type | `references` |

`abstract` suits the first content slide of a conference talk. `equation` carries one formula, typeset, with a legend of
its symbols (`math:` takes LaTeX).

## Rules

1. State hypotheses before results and mark each as `supported`, `rejected` or `open`; keep open ones open under limits.
2. Every number has a `source:` (result file, table, page). Report uncertainty: seeds, intervals, the test used.
3. A figure has a numbered caption that says what is plotted, the unit and how many runs; the slide title states the finding.
4. Time-ordered splits for time data; say how leakage was avoided.
5. One equation per slide; define every symbol. Put derivations in the appendix.
6. Comparisons name the baselines and show the best cell in bold; do not hide losses.
7. References: author, year, title, venue; keep to the ones the talk uses.
8. Aim for about one slide per minute; thesis defenses keep an appendix of backup slides for questions.

## Component choices

- Prefer `figure` over `chart_insight` when the figure is the evidence; use `chart_insight` for a one-line so-what.
- Use `factsheet` for datasets and study design instead of a dense table.
- Language: keep terms of art in the language of the audience; check glyphs for Cyrillic and Kazakh (`design/typography.md`).
