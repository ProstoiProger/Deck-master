# Visual style

Patterns behind the looks of each scope and how style packs work. The skill is formal by default (`design/scopes.md`); the
IT dark look below is one of several, and the game packs are on request only. The IT observations were gathered as follows. Observations come from browsing Canva technology, startup
pitch, hackathon and data-science template grids and Dribbble tech presentation searches in 2026-10, extended on 2026-10-16 with
Pitch templates, Behance presentation projects, Coolors, Color Hunt and Meshy (`design/research-2026-10.md`); they are
general patterns, not copied artwork. Canva was viewed at grid level (plain fetches are blocked), so treat the
observations as indicative. Add your own references in `design/inspiration/`.

## Contents

1. IT look patterns
2. Motifs used here
3. Style packs
4. Looks by scope
5. The block-game themes
6. Dark versus light
7. Mesh gradients
8. Using references

---

## 1. IT look patterns

| Pattern seen | Used here as |
|---|---|
| Dark navy, black or purple backgrounds with one bright accent (cyan, electric blue, lime, pink) | the six dark themes |
| Gradient glows and blurred blobs behind a big title | translucent circles on title and closing slides |
| Circuit or grid lines in a corner | thin grid lines on the right half of title and closing slides |
| Rounded cards and pill chips | cards for content, pills for labels |
| 2 by 2 or 3 by 2 icon-and-text grids | `feature_grid` |
| Timeline with dots | `roadmap` |
| Dashboard or device frame mockups | `demo` and `solution` frames |
| Big numbers with small captions | `kpi`, `problem` stat |
| Layered diagrams with one highlighted block | `architecture` |

Typical slide types in tech templates: title, agenda, problem, solution, features, architecture, demo, metrics,
roadmap, team, contact. Business, science and portfolio decks add their own types (`design/layouts.md`).

## 2. Motifs used here

Rounded cards, pill chips, a thin accent rule under titles, translucent glow circles, a faint grid, corner-free
flat content slides. Decoration stays off content slides so text keeps its contrast.

## 3. Style packs

A theme's `style:` block tells the layouts how to draw:

| Key | Values | Effect |
|---|---|---|
| `corner` | `round`, `square`, `pixel` | card corners; `pixel` draws stepped bevelled blocks |
| `border` | `thin`, `none`, `bevel` | outline treatment |
| `shadow` | `soft`, `hard`, `none` | soft blurred-looking offset, hard pixel offset, or flat |
| `card` | `fill`, `outline`, `flat` | filled panel, hairline outline on the page colour, or flat surface with no border |
| `title_rule` | `bar`, `line`, `none` | short accent bar, full hairline plus bar, or nothing under titles |
| `footer` | `plain`, `rule` | footer text only, or a hairline above it |
| `chips` | `pill`, `text` | rounded labels, or plain uppercase text with a hairline |
| `show_source` | true, false | print the slide's `source:` as a footnote |
| `radius` | inches | corner radius of cards |
| `pattern` | `clean`, `rules`, `band`, `grid`, `none`, `mesh`, `hatch`, `corner`, `dots`, `blueprint`, `rings`, `bars`, and the game packs `blocks`, `obsidian`, `classic` | title, cover and closing backdrop |
| `mesh`, `mesh_veil` | four hex colours, 0 to 1 | colours and page-colour veil of the `mesh` backdrop (default: the first four `series` colours, veil 0.5) |
| `deco` | `none`, `tri`, `tab` | a small accent triangle in the top-right corner, or an accent tab on the left edge, of every content slide |
| `metaphor` | `none`, `game` | game variants: hotbar agenda, XP bars, "press start" closing |
| `heading_scale`, `heading_line_h` | numbers | size and leading for wide fonts |
| `min_font` | points | lint floor for heading text |

Everything is drawn with flat vector shapes, so PPTX and PDF look the same and no textures need a licence; the only
images are the ones you add, including the optional character images (`design/entities.md`).

## 4. Looks by scope

| Look | Themes | How it is drawn |
|---|---|---|
| Scientific | `academic`, `conference-dark`, `clinical` | serif headings, paper background, hairline title rule, outlined or flat cards, source footnotes |
| Corporate | `boardroom`, `consulting`, `ledger` | navy or green on white, outlined cards, tabular numbers, hairline footer, action titles |
| Startup | `startup-bright`, `venture-dark` | big rounded cards, a bold colour band on title slides, glow circles in the dark one |
| Education | `chalkboard`, `forest`, `cloud-light` | warm, soft cards, generous spacing |
| Portfolio | `portfolio-mono`, `portfolio-warm`, `editorial` | large type, thin frames, one accent, little chrome; editorial adds a thick rule and a serif display face |
| IT | `midnight-navy`, `ultraviolet-core`, `graphite-cyan`, `deep-space`, `terminal-slate` | the patterns in section 1 |
| Hackathon and data (2026-10) | `aurora-mesh`, `datablue`, `matrix-green`, `synthwave`, `cobalt-pop`, `blueprint` | mesh-gradient covers, hatched panel, monospaced headings with a drafting grid, concentric rings; see `design/research-2026-10.md` |
| Product and brand (2026-10) | `signal-yellow`, `coral-market`, `sunset-mesh`, `plum`, `ember` | one loud accent, corner triangles, dot fields, wide display headings, bar-chart silhouette |
| Calm and institutional (2026-10) | `quantum-teal`, `deep-ocean`, `petrol`, `harbor`, `navy-gold`, `sage`, `terracotta`, `lavender`, `swiss` | pale aqua or pastel mesh, concentric rings, serif display, hairline rules, outline cards |

## 5. The block-game themes (on request only)

Two themes in a blocky pixel-game style, drawn with original flat shapes (no game textures):

| Theme | Look | Title art |
|---|---|---|
| `obsidian-craft` (dark) | obsidian black-purple, bevelled slots, purple veins in the floor, IT cyan and magenta highlights | nether-portal frame with a glowing purple interior, or a character on the right |
| `classic-craft` (light) | sky blue, inventory-gray panels, grass and dirt ground, pixel clouds and a square sun | clouds and sun, or a character standing on the grass |

Both use Press Start 2P headings, bevelled "inventory slot" cards and hard pixel shadows. Game metaphors for the same
layouts: agenda as a hotbar (a character per slot with `Step | creeper`), KPIs with an XP bar when the value is a
percentage, closing as "press start" with an advancement toast. Ten game components (boss fight, crafting table, inventory, hearts
and XP, advancement path, trade list, chat, ore strata, leaderboard, open book) and automatic mob decoration are in
`design/game-components.md`; the characters come from `design/entities.md`.

Use them only when the user asks for a Minecraft or gamified deck (hackathons with a playful brief, education, games,
student projects). Avoid them for formal juries or rubrics that penalise gimmicks, and for company or commercial decks when
characters are shown. Examples:
`examples/studybuddy-obsidian/studybuddy.md` (dark) and `examples/network-lesson-classic/lesson.md` (light). The themes are inspired by the style
and are not affiliated with any game: no logos, wordmarks or textures (`ops/security.md`).

## 6. Dark versus light

Dark themes dominate tech templates and suit screens, stages and recorded talks. Use a light theme (`cloud-light`,
`academic`, `boardroom`, `consulting`) for printing, PDF handouts and bright rooms. Switch with `cli.py build deck.md --theme cloud-light` (or `classic-craft` for the game look); the content does not change.

## 7. Mesh gradients

Five themes (`aurora-mesh`, `sunset-mesh`, `quantum-teal`, `synthwave`, `lavender`) open and close with a mesh-gradient picture: four colours blended
by soft blobs with a gentle warp, rendered once by `deckkit/charts/mesh.py` into the cache folder and embedded as a JPEG of the slide size. A veil of
the page colour is strongest under the text zone (the left two thirds), so the lint can check text against the lightest or darkest pixel
there. Change the colours with `mesh: ["#...", ...]` and `mesh_veil:` in a custom theme. Content slides stay flat: a gradient behind
body text costs contrast and file size. Mesh needs numpy; without it the cover falls back to the glow pattern and lint reports a Low finding.

## 8. Using references

Add links and screenshots as described in `design/inspiration/README.md`. Extract palette, grid, density and
motifs; never reproduce a template's artwork or text.
