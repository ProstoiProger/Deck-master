# Charts and tables

Charts and tables are generated from data, never typed from memory. In a deck the data is the table under the chart
slide's properties; the build draws it in the theme colours.

## Choosing a chart

| Message | Chart (`chart:`) | Data shape |
|---|---|---|
| ranking or comparison of a few items | `bar` or `hbar` | label, value (more value columns make grouped bars) |
| change over time | `line` | label (time), one or more value columns |
| relation of two numbers | `scatter` | x, y per row |
| classification outcome | `confusion` | header of class names, row label then counts |
| exact values matter | table (`comparison`) | header row first |

`hbar` suits long labels. The largest bar is highlighted in the accent colour when all values are positive.

## Writing a chart slide

```
# Commute hours drive demand more than rain
layout: chart_insight
chart: hbar
source: runs/importance.csv
takeaway: Hour of day explains three times more variance than rainfall.
| Driver | Importance |
|---|---|
| Hour of day | 0.46 |
| Rainfall | 0.15 |
```

A ready picture can be used instead with `image: figures/chart.png`.

## Content rules

- Title states the finding; the chart shows it; the takeaway panel says why it matters.
- Show uncertainty when the number is an estimate (interval in the bullet or the note).
- Units and direction in the header ("Time ms, lower is better").
- Mark the best result only when the difference is supported.
- Sort bars by value unless the order is meaningful.
- Start bar axes at zero.
- Never use a chart where one number would do; use `kpi`.

## Tables

- At most 6 rows and 5 columns on a slide; wider tables go to an appendix.
- Bold (`**value**`) marks the best cell; `highlight: N` outlines column N for "our method".
- Round consistently; keep the same decimals in a column.

## Provenance

Every chart and table slide has a `source:` naming the file or log row. Lint flags numbers without one.
