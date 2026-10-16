# Layouts

Choosing a layout for a message. The generated list of every layout with its inputs is `design/catalog.md`.

## Contents

1. How layouts work
2. Choosing by message
3. Frame, story, tech, data and people layouts
4. Rules of thumb

---

## 1. How layouts work

A layout turns a slide's title, properties and body into drawn shapes. It uses theme tokens, never raw colours, so
any theme works. A layout is designed for a word budget (`max_words` in the catalog); lint warns above it. Text sizes
shrink to fit their boxes, down to a floor; if the floor is reached the slide has too much text.

## 2. Choosing by message

| You want to say | Layout | Body it expects |
|---|---|---|
| "Here is who we are and what this is" | `title` | subtitle, team, date |
| "Here is the plan of this talk" | `agenda` | numbered steps |
| "This hurts, and here is by how much" | `problem` | statement, `stat:`, evidence bullets |
| "This is what we built" | `solution` | one line, three benefits, image |
| "These are its parts" | `feature_grid` | `Name | description` items |
| "This is how it is built" | `architecture` | `Layer: a, b, **key**` items |
| "This is how data flows" | `pipeline` | `Stage | caption` items |
| "Watch it work" | `demo` | screenshot, callouts |
| "These are the results" | `kpi` | `value | label | context` items |
| "This chart shows X" | `chart_insight` | table or image, takeaway |
| "We beat the baselines" | `comparison` | table, `highlight:` |
| "We use these tools" | `tech_stack` | `Layer: a, b, c` items |
| "This is the path" | `roadmap` | `Phase | milestone | detail` items |
| "Here is the team" | `team` | `Name | role | fact | character` items (character optional, game themes) |
| "Done, limits, next" | `impact` | two `##` groups |
| "Any questions?" | `closing` | contact lines |
| the problem as a boss to defeat (game theme) | `boss` | `boss:`, `stat:`, attacks |
| parts crafted into one product (game theme) | `crafting` | ingredients, `result:` |
| stats as hearts and XP (game theme) | `hud` | `value | label | heart | context` |
| a path with done and locked steps (game theme) | `advancements` | `Title | detail | icon | state` |
| the decision and why | `exec_summary` | `Situation | Complication | Resolution` items, recommendation |
| a four-way split or SWOT | `matrix` | four `##` groups, `x:` and `y:` captions |
| conversion from leads to paying | `funnel` | `Stage | value | note` items |
| market size | `market` | `TAM | value | description` items |
| plans and prices | `pricing` | `Plan | price | features; ...`, `highlight:` |
| a plan on a timeline | `gantt` | `periods:`, `Task | first | last | owner` items |
| who reports to whom | `org` | `Name | role | boss` items |
| KPIs against targets | `scorecard` | `Metric | actual | target | status | note` items |
| risks and mitigations | `risk` | `Risk | likelihood | impact | mitigation` items |
| we against alternatives by feature | `feature_matrix` | table with `yes`, `no`, `partial` cells |
| steps in order | `process` | `Step | description | owner` items |
| the study in four lines | `abstract` | `Background | Methods | Results | Conclusion` items |
| research question and hypotheses | `hypotheses` | question, `H1 | text | supported` items |
| a formula | `equation` | `math:` LaTeX, `symbol | meaning` items |
| a figure with observations | `figure` | `chart:` and table, or `image:`, `caption:` |
| two panels | `figures2` | `image:`, `image2:`, captions, `takeaway:` |
| facts about a dataset or design | `factsheet` | `Key | value` items |
| sources | `references` | one reference per item |
| a project opener | `case_header` | `image:`, `role:`, `year:`, `client:`, `tools:` |
| screens or works | `gallery` | `image | caption` items |
| a redesign | `before_after` | two `image | label` items, caption |
| who I am | `profile` | `image:`, bio, `Label | value` items |
| what I can do | `skills` | `Skill | level` items or grouped chips |
| a career or project history | `timeline` | `When | What | detail` items |
| one big number | `big_number` | `stat:`, supporting bullets |
| a quotation | `quote` | `> text`, `author:`, `role:` |
| options side by side | `columns` | two or three `##` groups |
| a divider | `section` | `number:`, one line |
| a full-slide picture | `image_full` | `image:`, `credit:` |
| anything else | `bullets` | bullets, optional image |

## 3. Families

Fifty-six layouts in nine families (the generated list with every input is `design/catalog.md`).

- **frame**: `title`, `agenda`, `closing`, `section`, `quote`, `big_number`, `image_full`, `columns`. Decorated backdrop on title and closing only.
- **story**: `problem`, `solution`, `feature_grid`, `impact`.
- **tech**: `architecture`, `pipeline`, `demo`, `tech_stack`, `roadmap`.
- **data**: `kpi`, `chart_insight`, `comparison`. Chart kinds: bar, hbar, line, area, stacked, waterfall, donut, scatter, confusion.
- **business**: `exec_summary`, `matrix`, `funnel`, `market`, `pricing`, `gantt`, `org`, `scorecard`, `risk`, `feature_matrix`, `process`.
- **science**: `abstract`, `hypotheses`, `equation`, `figure`, `figures2`, `references`, `factsheet`.
- **portfolio**: `case_header`, `gallery`, `before_after`, `profile`, `skills`, `timeline`.
- **people**: `team`.
- **game** (only on request): `inventory`, `crafting`, `hud`, `advancements`, `trade`, `chat`, `strata`, `boss`, `leaderboard`, `book` (`design/game-components.md`).
- **content**: `bullets`.

Components follow the theme's style block: outlined, flat or filled cards, a short bar or a full hairline under the title,
square or round badges, plain or pill chips (`design/palettes.md`, section 2). The same layout therefore looks different
in `boardroom`, `startup-bright` and `portfolio-mono`.

## 4. Rules of thumb

- Do not use one layout more than three times in a row; vary the rhythm.
- Prefer `kpi` over a bullet that contains a number; prefer `chart_insight` over a table of 4 numbers.
- `architecture` rows are layers from the user down to data; highlight one component with `**bold**`.
- Characters (`design/entities.md`): `mascot:` on `title`, `closing` and `problem`, a 4th cell on `team`, and
  `Step | creeper` in a game-theme `agenda`.
- Provide a real screenshot for `solution` and `demo`; without one lint warns (demo) or shows a stylised placeholder.
- When a message fits no layout, use `bullets` first; add a layout only if the pattern repeats (`extending.md`).
