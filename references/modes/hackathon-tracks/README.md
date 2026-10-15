# Hackathon tracks

Bank and corporate events often split into an ML track, an AI track and a DS track, with a case and a jury per
track. This folder tells the deck what each track rewards. Read the mode file first (`modes/hackathon.md` or
`modes/datathon.md`), then the track file.

## Contents

1. Tracks at a glance
2. Common start
3. What corporate jurors reward
4. Files
5. Autopilot routes

---

## 1. Tracks at a glance

| | ML track | AI track | DS track |
|---|---|---|---|
| Core question | does the model predict well and safely? | does the AI system solve the task reliably? | what does the data say and what should we do? |
| Typical deliverable | scored predictions, model, short deck | working assistant or pipeline, demo, deck | findings deck with recommendations |
| Judged on | metric on a hidden test, validation, business use | usefulness, reliability, guardrails, demo | insight, rigour, value, clarity |
| Deck emphasis | validation story, metric versus baseline, decision rule | architecture, evaluation set, failure handling, demo | findings with intervals, limits, actions |
| Main mode | hackathon | hackathon | datathon |
| Typical failure | leaderboard number without a validation story | demo that works once | many charts, no recommendation |

## 2. Common start

1. Read the case and the judging rubric; write the weights into the front matter.
2. Name the stakeholder and the decision.
3. Choose the mode (hackathon for ML and AI, datathon for DS) and the theme.
4. Fix the slide cap and minutes from the rules, not from the preset.

## 3. What corporate jurors reward

- A decision, not a model: what changes on Monday morning.
- Honest validation: out-of-time split, no leakage, a simple baseline.
- Risk awareness: privacy, fairness, explainability, regulation, monitoring.
- A deployable path: latency, cost, integration, owner.
- Clear, calm communication without hype.

## 4. Files

| File | Track |
|---|---|
| `modes/hackathon-tracks/ml-track.md` | ML |
| `modes/hackathon-tracks/ai-track.md` | AI |
| `modes/hackathon-tracks/ds-track.md` | DS |

## 5. Autopilot routes

- ML: brief -> outline (hackathon, ml-track) -> build -> qa -> qa-prep (validation questions)
- AI: brief -> outline (hackathon, ai-track) -> build (demo first) -> qa -> qa-prep (failure and safety)
- DS: brief -> outline (datathon, ds-track) -> build -> qa -> qa-prep (method and causality)
