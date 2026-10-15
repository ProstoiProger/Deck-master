# Playbook: datathon findings

**Preconditions**: an analysis exists with result files or logs; judged on insight, method, value, clarity; 5 to 7
minutes.

## Steps

1. **Collect evidence**: result tables, figures, the run log, the data card. Every number in the deck must come from
   these files.
2. **Pick the findings**: 3 to 5, ranked by decision value; drop the rest to an appendix.
3. **Write each finding** as claim, number, interval or n, why it matters, action (`modes/hackathon-tracks/ds-track.md`).
4. **Scaffold**: `python scripts/cli.py new --event datathon --out decks/findings.md`, theme `ultraviolet-core`.
5. **Slides**: question, data and checks, one slide per finding with `chart_insight`, method against baseline,
   value, limits, next step.
6. **Charts**: put the chart data as a table under the slide properties and cite `source:` (`communication/charts-and-tables.md`).
7. **Limits slide**: what you can and cannot claim, written before the jury asks.
8. **QA and Q&A**: `protocol/5-qa.md`, `communication/judge-qa.md` (method and causality questions).

## Examples

| Situation | Adjustment |
|---|---|
| only correlations | title each finding as association; say what experiment would show cause |
| many segments tested | state how multiple comparisons were handled |
| no baseline | add the simplest one (last value, group mean) before presenting any model |

## Traps

Ten charts and no recommendation; intervals missing; the model first, the question last.

## Output

The deck source, `.pptx`, `.pdf`, speaker script, a finding table (claim, number, interval, action), traceability.
