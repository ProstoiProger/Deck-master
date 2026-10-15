# Speaker notes

Notes are what the speaker says, not what the slide shows. They travel inside the PPTX and are exported by
`cli.py notes`; they also drive the time plan (`cli.py timing`).

## Writing rules

- 1 to 3 sentences per slide, about 25 to 60 words, spoken language.
- Start with the point of the slide, then the one fact that proves it; do not repeat the bullets.
- Mark the handover: "Next, Dana shows the demo."
- Put numbers in words the way they are said: "forty minutes", not "40 min" if the speaker would say it differently.
- Include the transition to the next slide in the last sentence.
- Keep detail that answers likely questions in the notes of backup slides.

## Pace

| Event | Words per minute | Source |
|---|---|---|
| Pitch and hackathon | 150 | `assets/presets/events.yaml` |
| Assignment and research talk | 140 | same |

A talk of 5 minutes has about 750 words of notes at most, including the demo narration. `cli.py lint` raises a High
finding when the notes exceed the budget by more than 10 percent.

## Several speakers

Give each speaker whole slides, not alternating sentences. Handovers on slide boundaries; write the name in the
first line of that slide's notes. Rehearse the handovers separately.

## Templates

`assets/templates/speaker-notes.md` has a per-slide table: slide, seconds, say, show, handover.

## Example

```
# The streaming model beats the batch baseline on every metric
notes: On a held-out week the model reaches 0.92 F1 against 0.81 for the batch baseline. Latency drops from forty
  minutes to two seconds. Next, Dana shows how a case is handled.
```
