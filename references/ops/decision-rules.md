# Decision rules

Each rule is a default. It applies when its precondition holds; deviate when the override condition holds, and
record why.

## Story

| Rule | Precondition | Override when |
|---|---|---|
| One message per slide | always | never |
| Title is a takeaway sentence | content slides | title and closing slides, agenda |
| Problem before solution | every pitch | the audience already agrees on the problem and time is under 3 minutes |
| Evidence before roadmap | every deck with results | no results exist yet: say so on the slide |

## Density

| Rule | Precondition | Override when |
|---|---|---|
| At most 7 bullets, about 6 words each | bullets layouts | an appendix slide read offline |
| One chart per slide | chart slides | a deliberate two-panel comparison, labelled |
| Dense tables go to an appendix | tables over 6 rows | the table is the result and the audience asked for it |
| Detail goes to the notes | any slide over its word budget | the audience receives only the PDF, no speaker |

## Numbers

| Rule | Precondition | Override when |
|---|---|---|
| Every number has a source | any claim | decorative counts such as "3 steps" |
| Give a baseline with every metric | metric slides | the metric is the baseline |
| Give uncertainty for estimates | sampled or modelled numbers | the figure is an exact count |
| Round only for display, and say so | large or noisy numbers | never round a number that decides a ranking |

## Event

| Rule | Precondition | Override when |
|---|---|---|
| A working demo outranks a nicer slide | hackathon judged on the product | the demo is explicitly not scored |
| Insight outranks model detail | datathon | the rubric weights method above insight |
| Rubric lines are the agenda | assignment | the handout forbids an agenda slide |
| Limits are shown, not hidden | research, datathon | the rules forbid negative results (rare; ask) |

## Design

| Rule | Precondition | Override when |
|---|---|---|
| Theme tokens, not raw colours | all slides | a brand colour is mandated: add it to a theme file |
| Contrast 4.5 or more for body text | all text | large decorative type at 3 or more |
| Formal theme of the scope; no game styling | all decks | the user asks for Minecraft or a gamified look (then `game: true`) |
| Decoration only on title and closing | all themes | none |

## Cut order under time pressure

Polish, secondary charts, team detail, second example, background; never validation, evidence, the demo or the
limits.
