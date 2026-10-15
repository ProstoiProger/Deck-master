# Pitch story

A deck is a story with a decision at the end. Use this arc for hackathons, datathons and most talks.

## Arc

1. **Problem and stakes**: who suffers, how much it costs or matters (money, time, risk, users), in the audience's language.
2. **Insight**: the non-obvious thing you found or understood.
3. **Solution**: what you built or recommend, in one sentence.
4. **Evidence**: the measured result against a baseline, with its source.
5. **Impact**: what changes for the user and what it is worth.
6. **Trust**: why the evidence can be believed (validation, limits, risks handled).
7. **Demo**: the thing working, in the fewest steps.
8. **Path to use**: the next three steps and what is needed to start.

Not every deck uses all eight: a datathon spends most slides on 2, 4 and 6; a hackathon on 1, 3, 7 and 8.

## Rules

- One message per slide; the title carries it.
- Every number traces to a source: a run log row, a result file, a brief page. No source, no number.
- Say what was not done; limits stated by you build trust, limits found by the jury cost it.
- Use the audience's terms, not yours: "late alerts", not "inference latency distribution".
- Start with the problem, not with the team or the technology.
- End with a decision or an ask: pilot, feedback, access to data, vote.
- Rehearse with a timer at least twice; prepare answers (`communication/judge-qa.md`).
- No raw confidential data on slides (`ops/security.md`).

## Opening lines

| Weak | Strong |
|---|---|
| "Hello, we are team X and we built Y" | "Every 40 minutes a stolen card is used before the owner knows" |
| "Today I will talk about..." | "In five minutes: a way to cut that to two seconds, and proof it works" |

## Closing lines

State the claim again with its number, then the ask: "Scoring each swipe on arrival cuts alert delay from 40
minutes to 2 seconds. We would like a one-branch pilot."
