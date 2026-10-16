"""Futuristic and advanced visuals: 3D geometry, shaded objects, glass and HUD cards, bento, sankey, globe and friends."""
from pathlib import Path

import pytest

from conftest import ROOT
from deckkit import lint
from deckkit.core import layout as layout_registry, shapes3d, timing
from deckkit.core.canvas import Canvas
from deckkit.core.layout import build_scenes
from deckkit.core.scene import Image, Line, Poly, SceneSlide, Shape, Text
from deckkit.core.spec import parse_text
from deckkit.core.theme import load_theme
from deckkit.lint import contrast

layout_registry.ensure_loaded()
VISUAL = sorted(n for n, s in layout_registry.LAYOUTS.items() if s.family == "visual")
STRUCTURAL = ("overflow", "contrast", "unknown layout", "failed", "glyph", "leaves the slide")


def deck_for(theme, names):
    parts = []
    for name in names:
        body = layout_registry.LAYOUTS[name].example
        parts.append(body.replace("\nlayout: " + name, "\nlayout: " + name + "\nnotes: n", 1))
    return f"---\nevent: investor-pitch\nminutes: 20\ntheme: {theme}\n---\n" + "\n---\n".join(parts) + "\n"


def canvas(theme="boardroom"):
    deck = parse_text("# S\n")
    return Canvas(load_theme(theme), deck.slides[0], deck, 1)


def test_visual_family_is_registered():
    assert len(VISUAL) == 13 and "bento" in VISUAL and "sankey" in VISUAL and "hero_3d" in VISUAL


@pytest.mark.parametrize("theme_name", ["cyber-hud", "glass-dusk", "liquid-light", "boardroom", "matrix-green", "swiss", "signal-yellow", "chalkboard"])
def test_every_visual_layout_renders_cleanly(theme_name, tmp_path):
    theme = load_theme(theme_name)
    bad = {}
    for name in VISUAL:
        deck = parse_text(deck_for(theme_name, [name]))
        deck.meta["_cache"] = str(tmp_path)
        found = [f for f in lint.run_all(deck, build_scenes(deck, theme), theme) if any(k in f for k in STRUCTURAL) and "not found" not in f]
        if found:
            bad[name] = found
    assert not bad, bad


# ---- geometry ------------------------------------------------------------------------------------------------

def test_iso_box_draws_three_faces_lit_from_above():
    c = canvas()
    info = shapes3d.iso_box(c, 5.0, 2.0, 1.0, 1.0, 0.5, "#3366CC")
    polys = [i for i in c.items if isinstance(i, Poly)]
    assert len(polys) == 3
    left, right, top = polys
    from deckkit.core import color
    lum = color.luminance
    assert lum(top.fill) > lum(left.fill) > lum(right.fill)
    assert info["front"][1] > info["right"][1] > info["back"][1]


def test_ring_segment_points_stay_between_the_radii():
    import math
    pts = shapes3d.ring_points(3.0, 3.0, 1.0, 0.7, -135, 135)
    radii = [math.hypot(x - 3.0, y - 3.0) for x, y in pts]
    assert all(0.69 <= r <= 1.01 for r in radii) and min(radii) < 0.71 and max(radii) > 0.99


def test_squarify_fills_the_box_and_areas_follow_values():
    vals = [6, 3, 2, 1]
    rects = shapes3d.squarify(vals, 0, 0, 12, 4)
    assert sum(w * h for _x, _y, w, h in rects) == pytest.approx(48, rel=1e-6)
    areas = [w * h for _x, _y, w, h in rects]
    assert areas[0] / areas[3] == pytest.approx(6, rel=1e-6)
    assert all(0 <= x and x + w <= 12 + 1e-6 and 0 <= y and y + h <= 4 + 1e-6 for x, y, w, h in rects)


def test_globe_projection_hides_the_far_side_and_centres_the_view():
    x, y, vis = shapes3d.project_globe(20, 60, 20, 60, 2.0)
    assert vis and abs(x) < 1e-9 and abs(y) < 1e-9
    assert shapes3d.project_globe(-20, 240, 20, 60, 2.0)[2] is False


def test_flow_band_joins_both_ends_with_horizontal_tangents():
    pts = shapes3d.band(1, 1.0, 1.5, 5, 3.0, 3.8)
    assert pts[0] == (1, 1.0) and pts[24] == (5, 3.0) and pts[25] == (5, 3.8)


# ---- layouts -------------------------------------------------------------------------------------------------

def test_sankey_draws_one_band_per_flow_and_node_heights_follow_totals(tmp_path):
    theme = load_theme("boardroom")
    deck = parse_text(deck_for("boardroom", ["sankey"]))
    sc = build_scenes(deck, theme)[0]
    bands = [p for p in sc.items if isinstance(p, Poly) and p.alpha < 0.5]
    assert len(bands) == 5
    nodes = [s for s in sc.items if isinstance(s, Shape) and abs(s.w - 0.24) < 1e-6]
    heights = sorted(round(n.h, 3) for n in nodes)
    assert heights[-1] > heights[0] * 4          # visitors (10 000) against paid (1 100)


def test_sankey_without_numbers_reports_a_problem_instead_of_failing():
    deck = parse_text("---\ntheme: boardroom\n---\n# S\nlayout: sankey\nnotes: n\n- A | B | <n>\n")
    sc = build_scenes(deck, load_theme("boardroom"))[0]
    assert any("sankey has no flows" in p for p in sc.problems) and not any("failed" in p for p in sc.problems)


def test_gauge_arc_grows_with_the_value():
    theme = load_theme("boardroom")
    text = "---\ntheme: boardroom\n---\n# G\nlayout: gauges\nnotes: n\nsource: x\n- A | 25 | 100 | n\n- B | 100 | 100 | n\n"
    sc = build_scenes(parse_text(text), theme)[0]
    arcs = [p for p in sc.items if isinstance(p, Poly) and p.fill in (theme.c("accent"), theme.c("success"), theme.c("warning"))]
    assert len(arcs) == 2 and len(arcs[1].points) > len(arcs[0].points)


def test_bento_picks_a_slot_plan_for_each_tile_count():
    for n in (3, 4, 5, 6):
        from deckkit.layouts.visual import _bento_slots
        slots = _bento_slots(n, 0, 0, 12, 4.4, 0.2)
        assert len(slots) == n
        areas = [w * h for _x, _y, w, h in slots]
        assert areas[0] == max(areas)                         # the first tile is (one of) the biggest


def test_terminal_colors_prompts_errors_and_success_lines():
    theme = load_theme("cyber-hud")
    deck = parse_text(deck_for("cyber-hud", ["terminal"]))
    sc = build_scenes(deck, theme)[0]
    cols = {t.text: t.color for t in sc.items if isinstance(t, Text)}
    assert cols["ERROR 1 blocking finding"] == theme.c("danger")
    assert cols["OK wrote deck.pptx and deck.pdf"] == theme.c("success")
    assert any(t.text == "$" and t.color == theme.c("accent") for t in sc.items if isinstance(t, Text))


def test_globe_hides_pins_on_the_far_side_and_marks_them():
    text = ("---\ntheme: cyber-hud\n---\n# G\nlayout: globe\nnotes: n\nsource: x\nlat0: 20\nlon0: 60\n"
            "- Near | here | 20 | 60\n- Far | other side | -20 | 240\n")
    sc = build_scenes(parse_text(text), load_theme("cyber-hud"))[0]
    texts = [t.text for t in sc.items if isinstance(t, Text)]
    assert any("(far side)" in t for t in texts)


# ---- 3D objects ----------------------------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["orbs", "ring", "cube", "stack"])
def test_hero_objects_render_transparent_png_and_are_cached(kind, tmp_path):
    from PIL import Image as PILImage
    from deckkit.charts.render3d import render_hero
    theme = load_theme("glass-dusk")
    deck = parse_text("# S\n")
    deck.meta["_cache"] = str(tmp_path)
    path = render_hero(theme, kind, deck, size=240)
    again = render_hero(theme, kind, deck, size=240)
    assert path == again and len(list(tmp_path.glob("hero3d-*.png"))) == 1
    im = PILImage.open(path)
    assert im.mode == "RGBA" and im.size == (240, 240)
    alpha = im.getchannel("A")
    solid = sum(1 for v in alpha.getdata() if v > 250)
    assert 2000 < solid < 240 * 240 * 0.7, "the object fills part of the frame, the rest is transparent"


def test_unknown_hero_object_is_rejected(tmp_path):
    from deckkit.charts.render3d import render_hero
    with pytest.raises(ValueError, match="orbs"):
        render_hero(load_theme("glass-dusk"), "pyramid", None)


def test_orbs3d_cover_embeds_the_picture_and_hud_cover_draws_a_globe(tmp_path):
    deck = parse_text("---\ntheme: glass-dusk\n---\n# T\nlayout: title\nnotes: n\n")
    deck.meta["_cache"] = str(tmp_path)
    sc = build_scenes(deck, load_theme("glass-dusk"))[0]
    assert [i for i in sc.items if isinstance(i, Image) and i.path.endswith(".png")]
    deck = parse_text("---\ntheme: cyber-hud\n---\n# T\nlayout: title\nnotes: n\n")
    sc = build_scenes(deck, load_theme("cyber-hud"))[0]
    assert sum(isinstance(i, Line) for i in sc.items) > 100


# ---- card styles and lint ------------------------------------------------------------------------------------

def test_glass_card_is_a_frosted_pane_with_an_edge_and_a_highlight():
    c = canvas("glass-dusk")
    c.box(1, 1, 3, 2, fill="surface")
    shapes = [i for i in c.items if isinstance(i, Shape)]
    assert len(shapes) == 3 and shapes[0].fill != load_theme("glass-dusk").c("bg") and shapes[1].fill is None and shapes[1].line
    assert shapes[2].alpha < 0.5, "the highlight along the top is translucent"
    light = canvas("liquid-light")
    light.box(1, 1, 3, 2, fill="surface")
    pane = [i for i in light.items if isinstance(i, Shape)][1]
    from deckkit.core import color
    assert color.luminance(pane.fill) > color.luminance(load_theme("liquid-light").c("bg"))


def test_bracket_card_draws_eight_corner_lines():
    c = canvas("cyber-hud")
    c.box(1, 1, 3, 2, fill="surface")
    assert sum(isinstance(i, Line) for i in c.items) == 8


def test_contrast_lint_ignores_a_ring_when_text_sits_in_its_hole():
    sc = SceneSlide(index=1, layout="x", title="t", bg="#000000")
    sc.items.append(Poly(shapes3d.ring_points(5, 5, 1.0, 0.7, 0, 359.9), fill="#FFFFFF"))
    sc.items.append(Text(4.5, 4.7, 1.0, 0.6, "72%", 24, "#FFFFFF"))
    assert contrast.check(None, [sc], None) == []
    sc.items.append(Text(5.65, 4.7, 0.2, 0.3, "x", 24, "#FFFFFF"))      # on the ring itself: white on white
    assert contrast.check(None, [sc], None)


def test_glow_deco_sits_behind_the_content():
    theme = load_theme("glass-dusk")
    deck = parse_text("---\ntheme: glass-dusk\n---\n# A claim\nlayout: bullets\nnotes: n\n- one\n")
    sc = build_scenes(deck, theme)[0]
    first = [i for i in sc.items[:8]]
    assert all(isinstance(i, Shape) and i.kind == "ellipse" and i.alpha < 0.1 for i in first)


def test_flow_shrinks_a_long_word_to_fit_the_width():
    from deckkit.layouts._util import flow
    c = canvas("lavender")
    size, _ = flow(c, ["A plain-language-summary-of-everything"], 1, 1, 1.4, 3.0, max_size=24, min_size=10)
    assert size < 24


# ---- events and docs -----------------------------------------------------------------------------------------

@pytest.mark.parametrize("event", ["tech-showcase", "data-viz-report"])
def test_visual_events_match_their_templates(event):
    e = timing.load_events()[event]
    text = (ROOT / "assets" / "templates" / f"deck-{event}.md").read_text(encoding="utf-8")
    used = [ln.split(":", 1)[1].strip() for ln in text.splitlines() if ln.startswith("layout:")]
    assert used == e["skeleton"] and all(n in layout_registry.LAYOUTS for n in used)
    assert "game" not in load_theme(e["theme"]).scopes


def test_new_scaffolds_have_no_failed_layouts(tmp_path):
    import subprocess
    import sys
    for event in ("tech-showcase", "data-viz-report"):
        out = tmp_path / f"{event}.md"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), "new", "--event", event, "--out", str(out)], check=True, capture_output=True)
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), "lint", str(out)], capture_output=True, text=True)
        failed = [ln for ln in r.stdout.splitlines() if ("failed" in ln and "not a number" not in ln) or "unknown layout" in ln]
        assert not failed, failed
        assert "[Critical]" not in r.stdout
