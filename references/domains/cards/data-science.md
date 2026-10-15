# Domain card: data science and ML

- **Typical decks**: datathons, ML hackathon tracks, thesis defenses, internal model reviews.
- **Audience asks first**: is the validation honest, is there leakage, does it beat a simple baseline.
- **Evidence expected**: out-of-time or group split, metric with interval across folds or seeds, baseline, calibration
  when probabilities are used, error analysis by segment.
- **Vocabulary**: say "held-out weeks", "baseline", "decision threshold"; avoid unexplained acronyms for business juries.
- **Slides that matter**: `pipeline` (data and checks), `comparison` (against baseline), `chart_insight` (importance,
  lift, error by segment), `kpi` (metric and value), `impact` (limits).
- **Risks**: leakage, drift, fairness across groups, privacy of training data; state what was and was not checked.
- **Visuals**: bar and line charts, lift or gain curves, confusion matrix (`chart: confusion`).
- **Sources**: the run log and result files; cite them in `source:`.
