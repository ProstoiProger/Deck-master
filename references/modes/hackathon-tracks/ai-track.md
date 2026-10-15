# AI track deck

Judged on usefulness to the task, reliability, guardrails and the demo. Model names and benchmarks change quickly;
named tools in a deck should be checked against current releases (as of 2026-10).

## Slides (6 to 8, 3 to 5 minutes)

| # | Slide | Layout | Content |
|---|---|---|---|
| 1 | Title | `title` | case, team |
| 2 | The task | `problem` | who uses it, what they do today, the cost |
| 3 | The assistant | `solution` | one line, three benefits, product screenshot |
| 4 | Architecture | `architecture` | retrieval or tools, model, guardrails; key component highlighted |
| 5 | Demo | `demo` | the happy path and one failure handled gracefully |
| 6 | Evaluation | `kpi` or `comparison` | a fixed set of cases, pass rate against a simple baseline |
| 7 | Safety and limits | `impact` | what it refuses, how it is monitored, what it cannot do |
| 8 | Closing | `closing` | repo, contact |

## Evidence

A 20 to 100 case evaluation set with the pass rate, the baseline (a prompt or keyword search), and the failure
categories. Say how answers were judged. Latency and cost per request if they matter.

## Constraints to show

| Constraint | What to show |
|---|---|
| Privacy | no customer data leaves the environment; what is logged |
| Hallucination | grounding on sources, citations, refusal when unsure |
| Cost and latency | per-request cost, p95 latency |
| Human in the loop | who reviews, when the system hands over |

## Traps

A demo that works only on the scripted prompt; no evaluation set; claims of accuracy with no cases; hiding failures.
