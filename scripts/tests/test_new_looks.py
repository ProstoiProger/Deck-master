"""The 2026-10 additions: covers and backdrop patterns, mesh gradients, new layouts, chart kinds, fonts, events."""
import pytest
from fontTools.ttLib import TTFont

from conftest import ROOT
from deckkit import lint
from deckkit.core import layout as layout_registry, timing
from deckkit.core.canvas import Canvas
from deckkit.core.layout import build_scenes
from deckkit.core.scene import Image, Line, SceneSlide, Text
from deckkit.core.spec import parse_text
from deckkit.core.theme import load_theme, theme_names
from deckkit.lint import contrast

layout_registry.ensure_loaded()
FORMAL = [n for n in theme_names() if "game" not in load_theme(n).scopes]
STRUCTURAL = ("overflow", "contrast", "unknown layout", "failed", "glyph", "leaves the slide")
NEW_LAYOUTS = ["canvas9", "okr", "kpi_table", "customer_case", "ask", "proof_wall", "statement", "cover_poster", "cover_split", "persona",
               "journey", "hmw", "kanban", "checklist", "links", "schema", "model_card", "insight_cards"]
OPENERS = ["title", "cover_poster", "cover_split", "statement", "section", "closing"]


def deck_for(theme, names):
    parts = []
    for name in names:
        body = layout_registry.LAYOUTS[name].example
        if "layout: " + name not in body:
            body = body.replace("\n", "\nlayout: " + name + "\n", 1)
        parts.append(body.replace("\nlayout: " + name, "\nlayout: " + name + "\nnotes: n", 1))
    return f"---\nevent: investor-pitch\nminutes: 20\ntheme: {theme}\n---\n" + "\n---\n".join(parts) + "\n"


def structural(findings):
    return [f for f in findings if any(k in f for k in STRUCTURAL) and "not found" not in f]


def findings_for(theme_name, names, tmp_path):
    deck = parse_text(deck_for(theme_name, names))
    deck.meta["_cache"] = str(tmp_path)
    theme = load_theme(theme_name)
    return lint.run_all(deck, build_scenes(deck, theme), theme)


@pytest.mark.parametrize("theme_name", FORMAL)
def test_covers_and_samples_render_cleanly_in_every_formal_theme(theme_name, tmp_path):
    names = OPENERS + ["okr", "kanban", "model_card", "persona", "ask"]
    assert structural(findings_for(theme_name, names, tmp_path)) == []


@pytest.mark.parametrize("theme_name", ["aurora-mesh", "lavender", "datablue", "matrix-green", "signal-yellow", "swiss", "cobalt-pop"])
def test_every_new_layout_renders_cleanly_in_representative_themes(theme_name, tmp_path):
    bad = {}
    for name in NEW_LAYOUTS:
        found = structural(findings_for(theme_name, [name], tmp_path))
        if found:
            bad[name] = found
    assert not bad, bad


def test_new_layouts_are_registered_with_metadata():
    for name in NEW_LAYOUTS:
        spec = layout_registry.LAYOUTS[name]
        assert spec.purpose and spec.accepts and spec.example and spec.max_words, name


# ---- backdrops -----------------------------------------------------------------------------------------------

def test_every_pattern_in_use_is_known():
    known = set(Canvas.PATTERNS) | {"grid", "band", "clean", "rules", "none", "blocks", "obsidian", "classic"}
    for name in theme_names():
        assert load_theme(name).style["pattern"] in known, name


def test_mesh_cover_embeds_an_image_with_a_tone_and_text_is_checked_against_it(tmp_path):
    theme = load_theme("aurora-mesh")
    deck = parse_text("---\ntheme: aurora-mesh\n---\n# T\nlayout: title\nnotes: n\n")
    deck.meta["_cache"] = str(tmp_path)
    sc = build_scenes(deck, theme)[0]
    imgs = [i for i in sc.items if isinstance(i, Image)]
    assert len(imgs) == 1 and imgs[0].tone and imgs[0].w > 13 and imgs[0].h >= 7.5
    assert not [f for f in contrast.check(deck, [sc], theme)], "cover text must pass on the mesh"


def test_contrast_lint_uses_the_backdrop_tone_not_a_skip():
    sc = SceneSlide(index=1, layout="title", title="t", bg="#000000")
    sc.items += [Image(0, 0, 13.333, 7.5, "x.jpg", tone="#FFFFFF"), Text(1, 1, 4, 1, "white on light", 24, "#FFFFFF")]
    assert contrast.check(None, [sc], None), "white text on a light backdrop must be reported"
    sc.items[0].tone = None
    assert contrast.check(None, [sc], None) == [], "a photo declares no tone and is skipped"


def test_mesh_is_cached_and_deterministic(tmp_path):
    from deckkit.charts.mesh import render_mesh
    theme = load_theme("sunset-mesh")
    deck = parse_text("# S\n")
    deck.meta["_cache"] = str(tmp_path)
    a = render_mesh(theme, deck)
    b = render_mesh(theme, deck)
    assert a == b and len(list(tmp_path.glob("mesh-*.jpg"))) == 1


def test_hatch_lines_stay_inside_their_box():
    theme = load_theme("datablue")
    deck = parse_text("# S\n")
    sl = deck.slides[0]
    c = Canvas(theme, sl, deck, 1)
    c._hatch(2.0, 1.0, 3.0, 2.0, 0.3)
    lines = [i for i in c.items if isinstance(i, Line)]
    assert lines
    for ln in lines:
        for x, y in ((ln.x1, ln.y1), (ln.x2, ln.y2)):
            assert 2.0 - 1e-6 <= x <= 5.0 + 1e-6 and 1.0 - 1e-6 <= y <= 3.0 + 1e-6


def test_deco_triangle_appears_on_content_slides_only_for_deco_themes(tmp_path):
    from deckkit.core.scene import Poly
    text = "---\ntheme: signal-yellow\n---\n# A claim\nlayout: bullets\nnotes: n\n- one\n"
    for name, expect in (("signal-yellow", True), ("midnight-navy", False)):
        theme = load_theme(name)
        deck = parse_text(text)
        deck.meta["_cache"] = str(tmp_path)
        sc = build_scenes(deck, theme)[0]
        small = [p for p in sc.items if isinstance(p, Poly) and max(q[0] for q in p.points) > 13.3 and p.bbox[2] < 1]
        assert bool(small) is expect, name


# ---- layout behaviour ----------------------------------------------------------------------------------------

def test_ask_splits_milestones_on_semicolons_so_numbers_keep_their_commas():
    theme = load_theme("boardroom")
    deck = parse_text(deck_for("boardroom", ["ask"]))
    sc = build_scenes(deck, theme)[0]
    labels = [i.text for i in sc.items if isinstance(i, Text)]
    assert "1,000 schools" in labels


def test_okr_bar_length_follows_progress():
    from deckkit.core.scene import Shape
    theme = load_theme("boardroom")
    text = ("---\ntheme: boardroom\nevent: okr-review\n---\n# O\nlayout: okr\nnotes: n\nsource: x\n## Grow\n- A | 50 | 100\n- B | 100 | 100\n")
    deck = parse_text(text)
    sc = build_scenes(deck, theme)[0]
    bars = [s for s in sc.items if isinstance(s, Shape) and abs(s.h - 0.15) < 1e-6 and s.fill == theme.c("warning")]
    full = [s for s in sc.items if isinstance(s, Shape) and abs(s.h - 0.15) < 1e-6 and s.fill == theme.c("success")]
    assert bars and full and bars[0].w < full[0].w


def test_canvas9_places_named_blocks_in_the_standard_slots():
    theme = load_theme("boardroom")
    deck = parse_text(deck_for("boardroom", ["canvas9"]))
    sc = build_scenes(deck, theme)[0]
    heads = {i.text: (i.x, i.y) for i in sc.items if isinstance(i, Text) and i.text.isupper() and i.role == "mono"}
    assert heads["VALUE PROPOSITIONS"][0] > heads["KEY ACTIVITIES"][0] > heads["KEY PARTNERS"][0]
    assert heads["COST STRUCTURE"][1] > heads["KEY PARTNERS"][1] and heads["REVENUE STREAMS"][0] > heads["COST STRUCTURE"][0]


# ---- charts --------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("kind,table", [
    ("heatmap", [["", "Mon", "Tue"], ["Morning", "12", "18"], ["Noon", "30", "44"]]),
    ("heatmap", [["", "A", "B"], ["x", "-3", "2"], ["y", "1", "-2"]]),
    ("radar", [["Skill", "A", "B"], ["Data", "8", "5"], ["Model", "6", "9"], ["Pitch", "9", "5"]]),
    ("lollipop", [["Feature", "Importance"], ["amount", "0.31"], ["hour", "0.14"], ["device", "0.06"]]),
    ("slope", [["Segment", "Before", "After"], ["New", "42", "61"], ["Free", "30", "29"]]),
])
def test_new_chart_kinds_render(kind, table, tmp_path):
    from pathlib import Path
    from deckkit.charts.themed import render_chart
    deck = parse_text("# S\n")
    deck.meta["_cache"] = str(tmp_path)
    path = render_chart(load_theme("datablue"), kind, table, 6.0, 4.0, deck=deck, index=1)
    assert Path(path).exists()


# ---- fonts ---------------------------------------------------------------------------------------------------

def test_bold_font_files_carry_their_own_names():
    """A static Bold instance that keeps the Regular name makes the PDF embed one face for both."""
    import yaml
    book = yaml.safe_load((ROOT / "assets" / "presets" / "fonts.yaml").read_text(encoding="utf-8"))
    for fam, spec in book.items():
        if spec["regular"] == spec["bold"]:
            continue
        names = {}
        for style in ("regular", "bold"):
            f = TTFont(str(ROOT / "assets" / "fonts" / spec[style]))
            names[style] = f["name"].getDebugName(6)
        assert names["regular"] != names["bold"], (fam, names)


def test_ibm_plex_mono_covers_kazakh():
    cmap = TTFont(str(ROOT / "assets" / "fonts" / "IBMPlexMono-Regular.ttf")).getBestCmap()
    assert all(ord(ch) in cmap for ch in "әғқңөүұһіӘҒҚҢӨҮҰҺІ")


# ---- events and docs -----------------------------------------------------------------------------------------

NEW_EVENTS = ["demo-day", "data-story", "product-launch", "product-roadmap", "okr-review", "market-analysis", "go-to-market", "ux-research",
              "keynote", "model-review", "architecture-review", "postmortem", "sprint-review"]


@pytest.mark.parametrize("event", NEW_EVENTS)
def test_new_event_skeleton_uses_registered_layouts_and_a_formal_theme(event):
    e = timing.load_events()[event]
    assert all(name in layout_registry.LAYOUTS for name in e["skeleton"]), event
    assert "game" not in load_theme(e["theme"]).scopes


@pytest.mark.parametrize("event", NEW_EVENTS)
def test_new_event_template_layouts_match_the_skeleton(event):
    e = timing.load_events()[event]
    text = (ROOT / "assets" / "templates" / f"deck-{event}.md").read_text(encoding="utf-8")
    used = [ln.split(":", 1)[1].strip() for ln in text.splitlines() if ln.startswith("layout:")]
    assert used == e["skeleton"], (event, used)


def test_every_playbook_is_linked_from_the_index_and_skill():
    index = (ROOT / "references" / "00-index.md").read_text(encoding="utf-8")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for p in sorted((ROOT / "references" / "playbooks").glob("*.md")):
        assert f"playbooks/{p.name}" in index, p.name
        assert p.stem in skill, p.name


def test_initials_skip_ages_and_punctuation():
    from deckkit.layouts._util import initials
    assert initials("Dana, 21") == "D"
    assert initials("Aigerim S.") == "AS"
    assert initials("21") == "?"
