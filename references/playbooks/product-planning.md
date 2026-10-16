# Playbook: product planning (roadmap, OKR review, go-to-market, market analysis)

**Preconditions**: the audience must agree on priorities, status or a plan; 10 to 15 minutes; the numbers have owners.
Events: `product-roadmap`, `okr-review`, `go-to-market`, `market-analysis`.

## Steps

1. **Decide the decision**: what must the room agree on today? It is the last slide and the first sentence of the summary.
2. **Summary**: `exec_summary` with situation, complication, resolution and the recommendation.
3. **Goals and status**: `okr` for objectives with key results as progress bars; `kpi_table` for metrics with change and status.
   Mark a status honestly: green means on target, amber needs an action, red needs a decision.
4. **Plan**: `roadmap` for the bets, `gantt` for dates and owners, `kanban` for work in flight.
5. **Market and customer** (`go-to-market`, `market-analysis`): `market` with a bottom-up serviceable market, `persona`, `feature_matrix`
   against two or three competitors, `matrix` for strengths and threats, `funnel` and `pricing` for the sales motion, `canvas9` for a
   one-page business model.
6. **Risks**: `risk` with owner and date; `checklist` for commitments.
7. **Scaffold**: `new --event <event>`; themes `signal-yellow` (roadmap), `harbor` (OKR), `coral-market` (market analysis), `plum` (go-to-market).
8. **QA**: every number has a `source:`; targets and actuals use the same period and unit; each risk has an owner; lint, previews, timed run.

## Traps

An OKR with a task as its key result; status colours with no definition; a market size from a top-down report only; a roadmap
with no dates; hiding a red.

## Output

Deck source, `.pptx`, `.pdf`, speaker script, a one-page decision log (decision, owner, date).
