# Playbook: assignment report

**Preconditions**: a handout with marking criteria; a report, code or analysis already done; 8 to 12 minutes.

## Steps

1. **Rubric first**: copy every criterion and weight into the front matter in the handout's order.
2. **Scaffold**: `python scripts/cli.py new --event assignment --out decks/report.md`, theme `cloud-light`.
3. **Agenda from the rubric**: one section per criterion, in the handout's words.
4. **One slide per marking line** with its evidence: figure, table, snippet, result, reference. Tag `rubric: Rn`.
5. **Own work visible**: your screenshots, your numbers, your decisions with reasons.
6. **Conclusion**: done, limits, next.
7. **Appendix**: references, long tables, extra figures.
8. **QA**: `cli.py trace` must exit 0; lint clean; timing within the limit; PDF as the submitted file.

## Examples

| Situation | Adjustment |
|---|---|
| group work | name who did what on the team or conclusion slide |
| word or slide limit | treat as a requirement; the build and `timing` show the count |
| citations required | references slide in the required style; cite on the slide too |

## Traps

Chapter-by-chapter summary; figures without sources; no limits; reading the slide aloud.

## Output

The deck source, `.pptx` and `.pdf`, speaker script, traceability table.
