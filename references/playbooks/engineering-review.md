# Playbook: engineering review (model, architecture, post-mortem, sprint)

**Preconditions**: engineers or technical leaders must decide, learn or sign off; 10 to 15 minutes; the evidence is in logs, runs or tickets.
Events: `model-review`, `architecture-review`, `postmortem`, `sprint-review`.

## Steps

1. **State the decision**: approve, approve with conditions, send back, or accept the actions (post-mortem); it is the last slide.
2. **Context**: `problem` with the scale or limit that shapes the design, or `hmw` for the question a model answers.
3. **Design or data**: `architecture` and `tech_stack` for a system; `schema` for data and keys; `model_card` for a model
   (facts, metrics on a time-ordered holdout, known limits).
4. **Alternatives**: `comparison` of two or three options against the criteria that matter, with the chosen one highlighted.
5. **Evidence**: `chart_insight` (latency, error rate, drift, velocity) with `source:`; `kpi_table` for the numbers that moved.
6. **Risks and readiness**: `risk` with mitigations; `checklist` for monitoring, rollback, on-call, security, privacy.
7. **Incident** (`postmortem`): `timeline` of what happened (time, event), `matrix` for what went wrong, why it was not caught,
   what went well, where we got lucky; actions on a `kanban` with owners and dates. Blameless: no names in causes.
8. **Sprint** (`sprint-review`): `demo` of finished work, `kanban` for done and carried over, `risk` for blockers.
9. **Scaffold**: `new --event <event>`; themes `matrix-green` (model), `blueprint` (architecture), `petrol` (post-mortem), `deep-ocean` (sprint).
10. **QA**: timestamps share one timezone; numbers have a `source:`; every action has an owner and a date; lint and previews.

## Traps

Blaming a person; a design with one option; metrics with no baseline; a post-mortem with no actions; a sprint review that is a
list of ticket numbers.

## Output

Deck source, `.pptx`, `.pdf`, speaker script, an appendix of raw logs or tables for questions.
