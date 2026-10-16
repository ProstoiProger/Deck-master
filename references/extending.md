# Extending deck-master

How to grow the skill without breaking it. After any change run `python -m pytest scripts/tests -q`.

## Contents

1. Add a theme
2. Add a style pack
3. Add a layout
4. Add an event mode
5. Add a domain card
6. Add a language
7. Add a backend
8. Install for other agents
9. Ideas for next steps
10. Sample prompts

---

## 1. Add a theme

1. Copy `assets/themes/midnight-navy.yaml` to `assets/themes/<name>.yaml`.
2. Set `scopes` (for `cli.py themes --scope`), `colors` (all of bg, surface, primary, secondary, accent, text, muted, success, warning, danger, info), `series` (chart colours), `fonts` and `style` (card, title_rule, footer, chips, pattern; see `design/visual-style.md`).
3. Run `python scripts/cli.py themes`; every pair must pass (text on bg 7 or more, muted 4.5 or more).
4. Build an example with it: `python scripts/cli.py preview examples/studybuddy-obsidian/studybuddy.md --theme <name> --sheet`, then view the PNGs.
5. Run `python scripts/build_catalog.py` so `design/catalog.md` lists it; the tests check the catalog is current. Add the theme to
   `design/palettes.md` and to the scope table in `design/scopes.md`.

From a reference screenshot: `cli.py inspire --from-image assets/inspiration/x.png` gives measured colours
(`design/inspiration/README.md`).

## 2. Add a style pack

A style pack is a `style:` block in a theme (`design/visual-style.md`). To add a new look such as retro terminal, 8-bit
arcade, blueprint or cyberpunk: choose `corner`, `border`, `shadow`, `pattern`, a font that covers your languages, and
optionally `metaphor: game`. New corner or pattern kinds are drawn in `scripts/deckkit/core/canvas.py`
(`Canvas.box`, `Canvas.backdrop`) with flat shapes only, so both backends render them.

To add a backdrop pattern: add its name to `Canvas.PATTERNS`, write `_pat_<name>(self)` that draws with `self.rect`, `self.line` and `self.poly` and
returns True (return False to fall back to the default glow), keep it clear of the title zone (x from 0.7 to 8.3 in) or of the bottom meta row,
and check `cli.py lint` for "leaves the slide" and contrast findings. The `mesh` pattern is the one exception: it embeds a generated picture and
supplies a `tone` so the contrast lint still checks text over it (`scripts/deckkit/charts/mesh.py`). Content-slide furniture is the `deco` style key (`Canvas._deco`); card looks are the `card` key (`Canvas.box`, `_glass`, `_bracket`).
Geometry for 3D-looking components (isometric boxes, ring segments, globe projection, treemap, flow bands) is in `scripts/deckkit/core/shapes3d.py`; the shaded 3D
objects are ray-marched in `scripts/deckkit/charts/render3d.py` (add a kind by adding a scene in `_scene`).
New chart kinds go in `scripts/deckkit/charts/themed.py` (`KINDS` and a branch in `render_chart`) with a test in `tests/test_scopes.py`.

## 3. Add a layout

Create a function in a module under `scripts/deckkit/layouts/` and register it:

```python
from ..core.layout import layout

@layout("quote", "content", "One large quotation with its source.", 30,
        accepts="first paragraph: the quote; props: author",
        example="# Users say it best\nlayout: quote\nauthor: A. Student\nWe stopped missing deadlines.")
def quote(c, s):
    c.title()
    c.fit_text(0.7, 2.2, 11.9, 3.0, s.paragraphs[0], 40, 20, "text", "heading", True)
```

Registration fails without a purpose and a word budget. Use theme tokens (`"text"`, `"accent"`), `c.box`, `c.fit_text`,
`c.badge`, never raw colours. Then add a test case (every layout must render in every theme), run
`python scripts/build_catalog.py`, and view a preview.

## 4. Add an event mode

1. Add an entry to `assets/presets/events.yaml` (scope, slide cap, minutes, wpm, default theme, skeleton, judged_on). The default theme must be formal; only `game: true` events may use a game theme.
2. Add `assets/templates/deck-<event>.md` (a valid skeleton with `{{title_yaml}}`, `{{theme}}`, `{{minutes}}`, `{{date}}`).
3. Add the event to a mode file in `references/modes/` (or a new one), a row in the routing tables of `SKILL.md` and `references/00-index.md`, and a line in `design/scopes.md`.
4. Test: `python scripts/cli.py new --event <event> --out build/x.md` then `lint` (it must report only placeholders and unresolved images; every rubric item must sit on a slide).

## 5. Add a domain card

Copy the structure in `references/domains/_template.md` into `references/domains/cards/<name>.md`, add it to
`references/00-index.md` and the Domain row of the routing table in `SKILL.md`.

## 5b. Add a character

Characters live in `ENTITIES` in `scripts/deckkit/core/entities.py`: name, the Mojang MHF skin account, a label and a
suggested role. Add a row, run `python scripts/cli.py entities fetch --names <name>`, and use it as `mascot: <name>`
or in a team cell. Your own pictures work without code: use a file path instead of a name (`design/entities.md`).

## 6. Add a language

Check glyph coverage (`design/typography.md`); add a font to `assets/fonts` and `assets/presets/fonts.yaml` if needed
and point a theme at it; add a sample deck and a glyph test.

## 7. Add a backend

A backend consumes the list of `SceneSlide` objects (`scripts/deckkit/core/scene.py`) and draws `Shape`, `Text`,
`Image` and `Line`. Copy `scripts/deckkit/backends/pdf_backend.py` as a starting point (for SVG or Marp
output), wire a flag into `cmd_build` in `scripts/cli.py`, and add a test next to `scripts/tests/test_backends.py`.
`scripts/deckkit/backends/html_backend.py` is the worked example of a third backend: SVG for vector items in z-order, text blocks with the shared line breaks,
embedded font subsets and pictures, and a runtime in `assets/web/` (`deck.css`, `deck.js`). Change the look or keys of the web version there; a test
(`test_every_dom_id_the_runtime_looks_up_exists`) keeps the runtime and the generated page in step.

## 8. Install for other agents

`SKILL.md` is the single source; `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and `adapters/` are generated by
`python scripts/build_adapters.py` (run it after editing the `SKILL.md` frontmatter or the pointer text).

| Agent | Command |
|---|---|
| Claude Code | `python scripts/install.py --agent claude --scope user` (copies to `~/.claude/skills/deck-master`) |
| Codex | `python scripts/install.py --agent codex --scope user` (copies to `~/.agents/skills/deck-master`) |
| Cursor | `python scripts/install.py --agent cursor --scope project --project <repo> [--vendor]` |
| Copilot | `python scripts/install.py --agent copilot --scope project --project <repo>` |
| Gemini CLI | `python scripts/install.py --agent gemini --scope user` or project |
| Windsurf | `python scripts/install.py --agent windsurf --scope project --project <repo>` |
| Any AGENTS.md reader | `python scripts/install.py --agent agents --scope project --project <repo>` |

Add `--check` to see drift without changing anything, `--dry-run` to preview, `--mode link` to symlink skill folders.
Existing files are extended through a marked block, never overwritten. Conventions as of 2026-10; confirm against
each tool's documentation (Codex skills in `.agents/skills`, Cursor rules `.cursor/rules/*.mdc`, Copilot
`.github/copilot-instructions.md`, Gemini `GEMINI.md` with `@file` imports).

## 8b. Test your change

`python -m pytest scripts/tests -q` runs everything. For a new behaviour, add a finished example: a folder in `examples/`
with the prompt, the inputs, the deck source and its built PPTX and PDF (`examples/README.md`).

## 9. Ideas for next steps

- Native PPTX charts (editable in PowerPoint) alongside the picture charts.
- Marp or Slidev export from the same outline.
- Brand kit import: logo, colours and fonts from a folder into a theme.
- Speaker-view PDF with notes on each page; handout PDF with 4 slides per page.
- QR code on the closing slide from the repo link.
- A `translate` helper that keeps the structure and flags text that grew past its box.
- Locale presets (Russian, Kazakh) with typography and number formats.
- A `deck diff` that shows what changed between two builds from `log.jsonl`.

## 10. Sample prompts

- "Use deck-master: build a 5-minute hackathon pitch from `brief.md` and the results in `runs/`; theme midnight-navy."
- "Restyle `decks/pitch.md` with the classic-craft theme, put Steve and Alex on the team slide and show me the preview sheet."
- "Trim `decks/findings.md` to 5 minutes and tell me what you cut."
- "Translate `decks/report.md` to Russian and check that every glyph and box still fits."
- "Here are my Canva screenshots in `assets/inspiration/`; create a theme from them and rebuild the hackathon example."
- "Review `decks/final.md` against the rubric in `brief.md`: trace, lint, previews, and list what is weak."
