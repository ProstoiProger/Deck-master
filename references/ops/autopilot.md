# Autopilot

Run this when the user hands over a whole task: a brief, a rubric, a results folder, or "make me a deck for
tomorrow". It chains the stages with checkpoints and ends with a traceability table.

## Contents

1. Intake
2. Classification
3. Plan
4. Execution loop
5. Routes by task type
6. Human checkpoints
7. Task ledger
8. Finish

---

## 1. Intake

Extract into the profile (`assets/templates/profile.md`):

- requirements R1..Rn, each quoting its source line; implicit ones marked as such;
- time limit, slide cap, format, language, audience, deadline;
- rubric with weights, if any;
- the material available and where each number comes from.

Ask the user only for what blocks the work; everything else becomes an assumption with a check.

## 2. Classification

| Decision | Options | Source of truth |
|---|---|---|
| Event mode | assignment, hackathon, datathon, research-talk | brief and rules |
| Playbook | hackathon-pitch, datathon-findings, assignment-report, project-defense, tech-talk, novel | what the user has |
| Theme | eight themes or a custom one | user request, brand, event mood |
| Domain card | data-science, ai-llm, web-mobile, cybersecurity, fintech, healthtech, edtech, iot, none | topic |
| Language | deck language | brief, audience |

One line of reasoning per decision.

## 3. Plan

Write the plan once, show it, then proceed: ordered stages, per step the files to read, the commands to run, the
exit criterion and a time budget; a requirement map (R-id to slide); checkpoints.

## 4. Execution loop

1. Load only the files the step names.
2. Do the step; record evidence (command output, previews viewed).
3. Check the exit criterion; if not met, fix the largest finding first and repeat.
4. Report in one or two lines, then continue.

## 5. Routes by task type

| Task | Route |
|---|---|
| Hackathon pitch | brief -> outline (hackathon) -> design -> build -> qa -> qa-prep |
| Datathon deck | brief -> outline (datathon) -> design -> build -> qa -> qa-prep |
| Assignment | brief -> rubric map -> outline -> build -> qa |
| Research talk or defense | brief -> outline -> build -> qa -> qa-prep |
| Restyle | design -> build -> qa |
| Trim to N minutes | outline (cut) -> build -> qa |
| Translate | build (translate) -> qa (glyphs, overflow) |
| Review a deck | qa only, fixes as concrete edits |

## 6. Human checkpoints

Stop and ask only for: a blocking unknown (no time limit and none can be assumed), a hard stop from `SKILL.md`,
or a re-framing that changes the deliverable. Everything else proceeds with the decision recorded.

## 7. Task ledger

Keep these in the task folder, not in the skill:

| File | Content |
|---|---|
| `profile.md` | the profile and open questions |
| `brief-intake.md` | requirements table |
| `deck.md` | the deck source |
| `build/` | `.pptx`, `.pdf`, `log.jsonl`, previews |
| `qa-prep.md` | likely questions and answers |

## 8. Finish

Run the gates in `protocol/5-qa.md`, then close with the traceability table
(`Requirement | Text | Slides | Evidence | Status`), for example
`R1 | Show a working demo | 5 | demo-ui.png, run log row 12 | met`. Every requirement is met or listed as not met with
the reason. The final message states what was delivered, the lint and timing result, assumptions and illustrative
numbers, open risks, and the rebuild command.
