import pytest

from deckkit import lint
from deckkit.core import entities, layout as layout_registry, pixelart
from deckkit.core.canvas import Canvas
from deckkit.core.layout import build_scenes
from deckkit.core.scene import Image, Shape, Text
from deckkit.core.theme import load_theme, theme_names
from deckkit.layouts.game import _ratio
from test_entities import fake_service

GAME = ["inventory", "crafting", "hud", "advancements", "trade", "chat", "strata", "boss", "leaderboard", "book"]

TOUR = """---
event: hackathon
minutes: 5
mobs: [creeper, pig, steve]
---
# Inventory: the stack on one screen
layout: inventory
select: 2
notes: n
Everything we carry.
- Quests | tasks in steps | sword | 4
- Streaks | daily chain | torch | 7
- Party | friends | steve
---
# A task and a timer craft a quest
layout: crafting
result: Quest | sword | one step
notes: n
- Task | book
- Timer | torch
- Reward | xp
---
# Stats screen
layout: hud
source: s.md
notes: n
- 72% | done | heart | vs 51%
- 31 of 40 | streaks | hunger | pilot
- 4.4 / 5 | liked | xp | survey
---
# Advancements to a pilot
layout: advancements
notes: n
- Prototype | built | sword | done
- Pilot | next | diamond | current
- Study | later | trophy | locked
---
# Trades that cut delay
layout: trade
notes: n
- slow | fast | note
---
# Chat feedback
layout: chat
notes: n
- Dana | it helped | steve
---
# Layers of the system
layout: strata
notes: n
- Client: Web, Phone
- API: **Engine**, Auth
- Data: DB
---
# The boss
layout: boss
boss: creeper
stat: 14 days | what it measures
notes: n
Lore sentence here.
- attack one
---
# Leaderboard
layout: leaderboard
better: lower
source: s.md
notes: n
- A | 840 ms | zombie
- B | 190 ms | steve
---
# Book of notes
layout: book
notes: n
## Done
- one
## Next
- two
"""


def structural(findings):
    return [f for f in findings if any(k in f for k in ("overflow", "contrast", "glyph", "failed", "unknown layout"))]


def test_ten_game_layouts_are_registered_with_metadata():
    layout_registry.ensure_loaded()
    game = sorted(n for n, s in layout_registry.LAYOUTS.items() if s.family == "game")
    assert game == sorted(GAME)
    for n in GAME:
        spec = layout_registry.LAYOUTS[n]
        assert spec.accepts and spec.example and spec.max_words


@pytest.mark.parametrize("theme_name", theme_names())
def test_every_game_component_renders_cleanly_in_every_theme(parse, theme_name):
    deck = parse(TOUR)
    theme = load_theme(theme_name)
    findings = structural(lint.run_all(deck, build_scenes(deck, theme), theme))
    assert findings == [], findings


def test_components_survive_extremes(parse, theme):
    many = "\n".join(f"- Item {i} | detail text number {i} | star | {i}" for i in range(14))
    deck = parse(f"# Many items\nlayout: inventory\nnotes: n\n{many}\n---\n# One layer\nlayout: strata\nnotes: n\n- Only: one\n---\n"
                 "# Nine ingredients\nlayout: crafting\nnotes: n\n" + "\n".join(f"- Ingredient {i} | book" for i in range(9)) + "\n")
    assert [f for f in lint.run_all(deck, build_scenes(deck, theme), theme) if "failed" in f] == []


def test_ratio_parsing_for_status_bars():
    assert _ratio("72%") == pytest.approx(0.72) and _ratio("31 of 40") == pytest.approx(0.775) and _ratio("4.4 / 5") == pytest.approx(0.88)
    assert _ratio("120%") == 1.0 and _ratio("many") is None


def test_pixel_icons_are_rectangular_and_draw_runs():
    assert len(pixelart.names()) >= 20
    for n in pixelart.names():
        cols, rows = pixelart.size_of(n)
        assert cols >= 5 and rows >= 5 and pixelart.runs(n)
    half = pixelart.runs("heart", clip=0.5)
    assert max(c + ln for c, _, ln, _ in half) <= 4


def test_unknown_icon_or_character_is_a_medium_finding(parse, theme):
    deck = parse("# Inventory with a typo in the icon\nlayout: inventory\nnotes: n\n- Item | detail | compass | 1\n")
    findings = lint.run_all(deck, build_scenes(deck, theme), theme)
    assert any("unknown icon or character 'compass'" in f for f in findings)


# ---- mob decoration -------------------------------------------------------------------

@pytest.fixture
def mobs(tmp_path, monkeypatch):
    folder = tmp_path / "ent"
    entities.fetch(["creeper", "enderman", "skeleton", "pig", "cow", "sheep", "steve"], dest=folder, opener=fake_service())
    monkeypatch.setenv("DECKKIT_ENTITIES_DIR", str(folder))


DECOR = """---
event: hackathon
mobs: [creeper, enderman, skeleton, pig]
---
# Title slide
layout: title
notes: n
---
# A content slide with decoration
layout: bullets
notes: n
- a
---
# Another content slide
layout: bullets
notes: n
- a
---
# A slide without decoration
layout: bullets
decor: none
notes: n
- a
---
# Closing
layout: closing
notes: n
- x
"""


def pictures(scene):
    return [i for i in scene.items if isinstance(i, Image)]


def test_content_slides_of_game_themes_get_a_title_badge_and_walkers(parse, mobs):
    deck = parse(DECOR)
    scenes = build_scenes(deck, load_theme("obsidian-craft"))
    title, c1, c2, plain, closing = scenes
    assert len(pictures(c1)) == 4 and len(pictures(c2)) == 4         # badge + 3 walkers
    assert [p.path for p in pictures(c1)] != [p.path for p in pictures(c2)]  # different mobs per slide
    assert len(pictures(plain)) == 0 and len(pictures(title)) == 0 and len(pictures(closing)) == 0
    assert all(p.w >= 0.6 for p in pictures(c1))


def test_it_themes_have_no_mob_decoration(parse, mobs):
    deck = parse(DECOR)
    assert all(not pictures(sc) for sc in build_scenes(deck, load_theme("midnight-navy")))


def test_every_game_slide_has_an_xp_progress_bar_and_a_floor_footer(parse, mobs):
    deck = parse(DECOR)
    theme = load_theme("classic-craft")
    for sc in build_scenes(deck, theme):
        top = [i for i in sc.items if isinstance(i, Shape) and i.y == 0 and i.h == pytest.approx(0.1) and i.fill == theme.c("success")]
        assert top, sc.index
    content = build_scenes(deck, theme)[1]
    footer = [i for i in content.items if isinstance(i, Text) and i.chrome and "/" in i.text]
    assert footer and footer[0].y > 7.0


def test_missing_images_skip_decoration_quietly_with_one_low_note(parse):
    deck = parse(DECOR)
    theme = load_theme("obsidian-craft")
    scenes = build_scenes(deck, theme)
    assert all(not pictures(s) for s in scenes)
    notes = [p for s in scenes for p in s.problems]
    assert len(notes) == 1 and notes[0].startswith("[Low]") and "entities fetch" in notes[0]


def test_default_pools_are_dark_mobs_for_obsidian_and_friendly_for_classic(parse):
    deck = parse("# A slide\nlayout: bullets\nnotes: n\n- a\n")
    assert "creeper" in Canvas.OBSIDIAN_POOL and "pig" in Canvas.CLASSIC_POOL
    assert entities.group_of("creeper") == "hostile" and entities.group_of("pig") == "friendly" and entities.group_of("tnt") == "block"
    assert len(entities.ENTITIES) >= 60
