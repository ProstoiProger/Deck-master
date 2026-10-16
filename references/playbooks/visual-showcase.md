# Playbook: visual showcase (futuristic tech talk, data-viz report)

**Preconditions**: the audience judges clarity and polish as much as content; the numbers exist; 8 to 10 minutes. Events:
`tech-showcase` (a product, platform or technology) and `data-viz-report` (a data story told with dashboards and flows).

## Steps

1. **Pick the one idea**: a sentence the audience can repeat. Every visual must support it; a clever diagram that does not is cut.
2. **Open with the frame**: `cover_poster` (or `cover_split`), then one `statement` with a sourced number.
3. **Choose the visual by the question**:

   | Question | Layout |
   |---|---|
   | what are the layers or parts | `iso_stack`, `orbit`, `network` |
   | how big is each part of the whole | `treemap`, `iso_bars` |
   | where does the quantity go | `sankey` |
   | how close to the goal | `gauges`, `kpi_table` |
   | what is the state of everything | `bento` (one big number first, small tiles after) |
   | when does it happen | `activity_grid` |
   | where in the world | `globe` |
   | who wins | `podium` |
   | what does the command line say | `terminal` |
   | one image for the idea | `hero_3d` (`orbs`, `ring`, `cube`, `stack`) |

4. **One idea per visual**: at most six tiles in a bento, twelve areas in a treemap, ten flows in a sankey, fourteen links in a network.
5. **Theme**: `cyber-hud` (HUD brackets, wireframe globe), `glass-dusk` (glass cards, 3D orbs), `liquid-light` (frosted glass on a bright page);
   `blueprint` or `matrix-green` for engineering crowds. Glass and bracket card styles are theme settings, not layout options.
6. **Scaffold**: `new --event tech-showcase` or `new --event data-viz-report`.
7. **QA**: every number has a `source:`; labels are readable from the back row (15 pt or more where the layout allows); the 3D object is
   decoration, never the only place a fact appears; lint, previews, a timed run.

## Traps

Decoration with no message; a 3D chart where a flat bar chart says it better (`iso_bars` is for a few bars, not for twenty);
a sankey with crossing bands nobody can follow; glass cards over a busy background; more than one hero object per deck.

## Output

Deck source, `.pptx`, `.pdf`, speaker script. The 3D object and mesh covers are pictures inside the PPTX; all other shapes stay editable.
