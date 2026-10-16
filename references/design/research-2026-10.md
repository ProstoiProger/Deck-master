# Research notes, 2026-10: what the new palettes, layouts and events come from

Inputs gathered on 2026-10-16 to widen the skill beyond its first IT and business set: Pitch templates, Behance
presentation projects, Coolors and Color Hunt palettes, Meshy mesh gradients. These are design inputs, not rules. Read this
file when you add a theme or layout and want to know why the current ones look as they do.

## Contents

1. Method and limits
2. Pitch: structures that became layouts and events
3. Behance: looks that became themes and patterns
4. Palettes: where each new theme comes from
5. Meshy: mesh gradients
6. Figma Community: 3D, advanced visualisation, futuristic components
7. Not done, ideas

---

## 1. Method and limits

| Source | What was looked at | How |
|---|---|---|
| Pitch (pitch.com/templates) | the template library: collections Pitch deck, Startups, Product, Strategy, Report, Research, UX; the slide text of eight templates (Series A, Business Model Canvas, Go-to-Market Strategy, OKR, KPI Report, Product Roadmap, Competitor Analysis, Usability Testing Report); the names of about eighty more | browser, page text and gallery thumbnails |
| Behance | search results for "hackathon pitch deck", "datathon", "data science presentation" | browser, result thumbnails only; no project was opened |
| Coolors | trending palettes, and the dark, neon and blue lists | browser, hex values read from the page |
| Color Hunt | popular, dark, blue, neon and night lists | browser, hex values read from the page |
| Meshy (meshgradient.in) | the preset gradients and the generator | browser, four-colour presets read from the page |

Limits: a single session, thumbnail level for Behance, so treat style notes as impressions. Plain page fetches return
nothing useful from these sites (they render in the browser). Palettes are common colour combinations; the skill uses
tuned versions of them (contrast-checked, section 4), not copies of any author's artwork. No template text, artwork, logo or
photo was copied; Behance projects belong to their authors and only general patterns were taken, as with the Canva and
Dribbble inputs in `design/visual-style.md`.

## 2. Pitch: structures that became layouts and events

| Structure seen | Became | Used in event |
|---|---|---|
| Business Model Canvas: nine blocks in the standard arrangement | `canvas9` | `go-to-market`, `strategy-proposal` |
| OKR deck: objectives with key results and progress | `okr` | `okr-review`, `product-roadmap` |
| KPI report: tables with a change column, plus status | `kpi_table` | `okr-review`, `sprint-review`, `product-roadmap` |
| Series A deck: customer case with customer, problem, solution, growth | `customer_case` | `investor-pitch`, `sales-pitch` |
| Series A deck: the ask as a big amount with use of funds | `ask` | `investor-pitch` |
| Series A deck: achievements, press and partnerships pages | `proof_wall` | `product-launch`, `investor-pitch` |
| Series A deck: a big sentence with the key number highlighted | `statement` | `keynote`, `product-launch`, `data-story` |
| Business Model Canvas customer personas; usability report goals, findings and next steps | `persona`, `insight_cards`, `checklist` | `ux-research` |
| Product roadmap: teams, quarterly calendar, release timeline | `kanban`, `gantt`, `roadmap` (existing) | `product-roadmap`, `sprint-review` |
| Competitor analysis, market research: market size, competitor profiles | `market`, `feature_matrix` (existing) | `market-analysis` |
| Go-to-market strategy: summary, objectives, buyer personas, channels, timeline | the sequence in the event skeleton | `go-to-market` |

Style impressions from the Series A template: black with one yellow, a diagonal corner triangle, large quotes, phone mockups.
That became the `signal-yellow` theme and the `corner` pattern.

Needs that no template covered, added from what judges and reviewers ask for rather than from a source: the challenge as a
question (`hmw`), the user journey (`journey`), the data dictionary (`schema`), a model card (`model_card`), a "where to find
it" slide (`links`), a delivery checklist (`checklist`) and a poster-style cover (`cover_poster`). The `postmortem`,
`sprint-review`, `model-review` and `architecture-review` events come from the same reasoning, not from a template.

## 3. Behance: looks that became themes and patterns

| Impression from result thumbnails | Became |
|---|---|
| Cobalt blue poster with white type, a retro-tech hackathon cover | `cobalt-pop`, `rings` pattern |
| Black or green datathon covers; navy to electric blue with hatching and stripes | `datablue` (`hatch` pattern), `matrix-green` (`blueprint` pattern) |
| Oversized display type that fills the slide ("Presentation", "fire scrubs") | `cover_poster`, the `ember` and `cobalt-pop` display fonts (Unbounded) |
| Dark slides with TAM, SAM, SOM circles and laptop mockups; KPI cards on dark with one hot colour | `market` (existing), `signal-yellow`, `ember` |
| Coral and pink B2B decks, soft rounded cards | `coral-market` (`dots` pattern) |
| Teal liquid or mesh gradient covers, pastel scientific data-visualisation pages | `quantum-teal`, `lavender` (mesh covers) |
| Black-and-white minimal research slides with a dot grid | `swiss`, `dots` pattern |
| Red and black keynote-style product talks | `ember` (`bars` pattern) |

## 4. Palettes: where each new theme comes from

Hex values seen on the palette pages, and the theme they informed. Every theme was then tuned so that text on the page colour
reaches 7:1 or more and other text pairs 4.5:1 (`design/palettes.md`, section 3), which changed some values.

| Theme | Seen on | Observed values | Notes |
|---|---|---|---|
| `aurora-mesh` | Meshy preset | #4DFFB2 #DDF3FF #0FF5DA #507CE2 | mint, ice and cyan on a deep navy page |
| `sunset-mesh` | Meshy presets | #FF4D4D #FFF2DB #FBFF1A #FF7024 and #FF004C #FFDB9E | red, orange and peach on plum-black; the yellow was dropped for contrast |
| `quantum-teal` | Meshy preset, Behance teal covers | #00D6B3 #66D1FF | light mode, deep teal type |
| `datablue` | Color Hunt dark and neon, Coolors dark and blue | #080616 #1A1953 #162E93 #2F2FE4; #00FFDE #00CAFF #0065F8 | navy, electric blue and aqua |
| `matrix-green` | Color Hunt neon | #B6FFA1 #00FF9C; #98CD00 #A4DD00 #B6F500 | phosphor greens on near-black, monospaced headings |
| `signal-yellow` | Coolors dark and blue; Pitch Series A impression | #000814 #FFC300 #FFD60A | black with one yellow |
| `coral-market` | Color Hunt popular; Behance coral B2B | #FF95A5 #FFF6DC #76C0EC | coral darkened so that text on it passes |
| `ember` | Color Hunt dark | #E6501B #C3110C #740A03 #280905 | red and orange on black |
| `terracotta` | Color Hunt popular | #FDB773 #EB895B #DA6556 #A14646 | clay red as the primary, cream page |
| `sage` | Color Hunt popular, Coolors | #A8BBA3 #97A87A #FCF9EA; #CAD2C5 #84A98C #52796F | greens darkened to be used as text |
| `deep-ocean` | Coolors blue | #03045E #0077B6 #00B4D8 #90E0EF #CAF0F8 | blue ramp on a midnight page |
| `synthwave` | Coolors neon | #F72585 #B5179E #7209B7 #3A0CA3 #4361EE #4CC9F0 | pink to cyan; the pink is darkened for primary fills |
| `petrol` | Coolors | #001219 #005F73 #0A9396 #94D2BD #E9D8A6 #EE9B00 | teal, sand and amber |
| `harbor` | Coolors | #E63946 #F1FAEE #A8DADC #457B9D #1D3557 | navy, steel and a red accent on mint-white |
| `lavender` | Coolors | #CDB4DB #FFC8DD #BDE0FE #A2D2FF | pastels for the mesh; purple type for contrast |
| `navy-gold` | Coolors dark and blue | #000814 #001D3D #003566 #FFC300 | gold on ink navy with a serif heading |
| `plum` | Color Hunt dark and night | #2C2C2C #522546 #88304E; #211832 #412B6B #5C3E94 #F25912 | aubergine with orange |
| `cobalt-pop` | Behance cobalt poster; Color Hunt neon | #0033FF; #E4FF30 #008BFF #5B23FF | saturated cobalt page with yellow and pink |
| `blueprint`, `swiss` | none: genre conventions | | drafting-sheet blue; Swiss black, white and one red |

## 5. Meshy: mesh gradients

Meshy blends four colours into a soft mesh and gives each result an id; the preset list shows about seven combinations
(mint and cyan, red and yellow, orange and peach, aqua and blue). The skill reproduces the look with its own generator
(`deckkit/charts/mesh.py`): four colour blobs, a gentle domain warp, grain against banding, a veil of the page colour that is
strongest where text sits. It does not call Meshy and uses none of its images. Where the mesh is used and how to tune it:
`design/visual-style.md`, section 7.

## 6. Figma Community: 3D, advanced visualisation, futuristic components

Searched on 2026-10-16 in the Community library (files, sorted by popularity): "3d presentation", "futuristic ui", "data visualization charts",
"glassmorphism", "isometric", "hud sci-fi dashboard", "ai presentation template dark", "bento grid". Result titles and thumbnails only;
no file was opened or duplicated. Figma's own template pages for presentations returned 404, so Community files were the source.

| Seen in the results | Became |
|---|---|
| Glossy 3D shapes and "mix and match 3D shapes" packs, 3D icons, podium backgrounds | `hero_3d`, the `orbs3d` cover, `podium` |
| Isometric illustration packs, isometric layered and 3D journey maps | `iso_stack`, `iso_bars` |
| A pitch deck with 3D glass bar charts; chart packs with donut, radar, heatmap, bar and line components | `iso_bars`, `gauges`, chart kinds `heatmap`, `radar` (2026-10 first pass), `activity_grid` |
| Glassmorphism cards, glass icon sets, "liquid glass" | card style `glass`, themes `glass-dusk` and `liquid-light`, the `glow` deco |
| HUD and futuristic UI kits: corner brackets, ring gauges, data-matrix dots, wireframe globes, scale ticks | card style `bracket`, the `hud` pattern and deco, `globe`, `gauges`, theme `cyber-hud` |
| Bento grid layouts and bento dashboards (big number, sparkline, ring and text tiles of different sizes) | `bento` |
| Dashboard kits: sparklines, mini bars, KPI tiles, dark analytics dashboards | `bento` tiles, `kpi_table` |
| Network and flow diagrams, charting plugins (sankey, treemap) | `network`, `sankey`, `treemap` |
| Terminal and code window mockups in dev-tool landing pages | `terminal` |
| Device mockups (phones, laptops, boxes) | not built: `demo` and `solution` already frame a screenshot; a vector device set is an idea below |

Notes: Figma Community files carry their authors' licences; nothing was copied, only the kinds of components and looks. Real 3D is rendered
by our own ray marcher in the theme's colors, not taken from any 3D pack.

## 7. Not done, ideas

- Native PowerPoint charts (the charts are pictures); native gradient fills instead of a picture.
- A vector device set (laptop, phone, browser window) and a rendered 3D device; a land mask for the globe; more hero objects (capsule, pyramid, knot).
- A QR code on `links` (needs a QR library; left out to keep the dependency list short).
- More Pitch templates (Board Deck, Event Report, Market Research, Employee Onboarding) could become events.
- A per-slide mesh section divider; today the mesh is only on title, cover and closing slides.
- Behance projects were not opened; a closer reading of a few hackathon decks would refine `cover_poster` and `demo`.
