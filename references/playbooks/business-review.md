# Playbook: business review and strategy proposal

**Preconditions**: a committee must decide or be informed; 10 to 25 minutes; the data pack exists.

## Steps

1. **Decision**: what you need from the room, how much and by when. It becomes the first content slide (`exec_summary`).
2. **Scorecard**: five to eight KPIs with actual, target and a status word; explain only red and amber rows.
3. **Trend**: one chart for the metric that explains the decision; the so-what in one sentence.
4. **Drivers**: two or three numbers that show why (`kpi`, `big_number`).
5. **Options** (strategy proposals): a `feature_matrix` of options against criteria; weights stated; recommend one.
6. **Risks**: three to five risks with likelihood, impact, mitigation and an owner.
7. **Plan**: `gantt` or `roadmap` with owners and the first milestone date.
8. **Scaffold**: `new --event business-review` (theme `boardroom`), `strategy-proposal` (`consulting`), `project-status`
   (`ledger`), `grant-proposal` (`forest`).
9. **QA**: totals agree across slides (chart sums, scorecard, summary); sources on every number; lint, previews, timed run.

## Traps

Burying the decision on the last slide; a scorecard with no targets; risks without owners; a plan with no dates; numbers
that differ between slides.

## Output

Deck source, `.pptx`, `.pdf`, one-page pre-read if the committee asks (`cli.py notes`), backup slides.
