# Mode: portfolio and case study

For designer, developer, analyst and student portfolios, project showcases and case-study talks. Events: `portfolio`,
`case-study`. Themes: `portfolio-mono` (dark, one accent), `portfolio-warm` (light, friendly), `editorial` (magazine), or
the user's brand.

## What the audience judges

Craft, range, clarity of process and results. They look at the work first and read second: images carry the deck and
text stays short.

## Story

| Part | Slide | Layout |
|---|---|---|
| Who | portrait, role, base, experience, contact | `profile` |
| Tools | skills with levels or grouped chips | `skills` |
| Path | career or study timeline | `timeline` |
| Project | name, role, year, client, tools, hero image | `case_header` |
| Problem | who struggled with what, one number | `problem` |
| Process | steps, with your part marked | `process` |
| Work | screens or pieces | `gallery`, `image_full` |
| Change | before and after | `before_after` |
| Result | measured effect | `kpi` |
| Proof | a client or user quote | `quote` |
| Contact | how to reach you | `closing` |

For a single case study use the `case-study` event; for a whole portfolio use `portfolio` and repeat the case block per
project (two to three projects in ten minutes).

## Rules

1. One project per section; each starts with `case_header` and ends with a result.
2. Say what you did, not what the team did; name the role on the case header.
3. Results carry a number and a `source:` (analytics, usability test, survey); if there is none, say what was observed.
4. Only show work you may show: check client confidentiality and licences; blur or mock sensitive data (`ops/security.md`).
5. Images: at least 1600 px wide for full-width use, one idea per image, consistent crop. Placeholder images are labelled
   `illustrative`; real ones keep a credit line (`credit:` on `image_full`).
6. Quotes name the person and role, with permission.
7. Skills show levels as bars only if the levels are honest; otherwise use grouped chips (the level is never printed).
8. Keep text short: the lint word budgets for `gallery` (40) and `before_after` (30) are deliberate.

## Component choices

- `gallery` takes two to six images in a 2 or 3 column grid; `before_after` takes exactly two.
- `profile` facts are `Label | value` rows; `email:` and `web:` print on the last line.
- Use `image_full` for a hero shot with the title as a caption bar.
