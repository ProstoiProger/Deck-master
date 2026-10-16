"""Scope coverage: every layout in formal themes, events and templates, formal default, numbers, charts, Poly."""
import pytest

from conftest import EXAMPLES, ROOT
from deckkit import lint
from deckkit.core import layout as layout_registry, timing
from deckkit.core.layout import build_scenes
from deckkit.core.numbers import number
from deckkit.core.scene import Poly
from deckkit.core.spec import load_deck, parse_text
from deckkit.core.theme import load_theme, theme_names

layout_registry.ensure_loaded()
FORMAL = [n for n in theme_names() if "game" not in load_theme(n).scopes]
GAME_THEMES = [n for n in theme_names() if "game" in load_theme(n).scopes]
GENERAL_LAYOUTS = sorted(s.name for s in layout_registry.LAYOUTS.values() if s.family != "game")
STRUCTURAL = ("overflow", "contrast", "unknown layout", "failed", "glyph")


def deck_from_example(name, theme):
    spec = layout_registry.LAYOUTS[name]
    body = spec.example.replace("\nlayout: " + name, "\nlayout: " + name + "\nnotes: n", 1)
    if "layout: " + name not in body:
        body = body.replace("\n", "\nlayout: " + name + "\nnotes: n\n", 1)
    return f"---\nevent: investor-pitch\nminutes: 10\ntheme: {theme}\n---\n{body}\n"


@pytest.mark.parametrize("theme_name", ["boardroom", "academic", "startup-bright", "portfolio-mono", "chalkboard"])
def test_every_general_layout_renders_cleanly_in_formal_themes(lint_text, theme_name):
    bad = {}
    for name in GENERAL_LAYOUTS:
        found = [f for f in lint_text(deck_from_example(name, theme_name), theme_name) if any(k in f for k in STRUCTURAL)]
        found = [f for f in found if "not found" not in f]
        if found:
            bad[name] = found
    assert not bad, bad


@pytest.mark.parametrize("theme_name", FORMAL)
def test_a_layout_from_each_family_renders_in_every_formal_theme(lint_text, theme_name):
    for name in ("exec_summary", "scorecard", "funnel", "hypotheses", "case_header", "pricing", "timeline", "bullets"):
        found = [f for f in lint_text(deck_from_example(name, theme_name), theme_name) if any(k in f for k in STRUCTURAL)]
        assert found == [], (theme_name, name, found)


def test_layout_count_and_families():
    assert len(layout_registry.LAYOUTS) == 87
    families = {s.family for s in layout_registry.LAYOUTS.values()}
    assert {"business", "science", "portfolio", "frame", "game", "product", "data"} <= families


def test_events_have_templates_scopes_and_formal_defaults():
    events = timing.load_events()
    assert len(events) == 33
    from deckkit.core import paths
    for name, e in events.items():
        assert (paths.templates_dir() / f"deck-{name}.md").exists(), name
        assert e.get("scope"), name
        assert e["min_slides"] <= len(e["skeleton"]) <= e["max_slides"] + 2, name
        is_game = "game" in load_theme(e["theme"]).scopes
        assert is_game == bool(e.get("game")), f"{name}: game themes only for game events"
    assert [n for n, e in events.items() if e.get("game")] == ["gamified"]


@pytest.mark.parametrize("event", sorted(timing.load_events()))
def test_new_scaffolds_every_event_and_only_placeholders_remain(tmp_path, event):
    import subprocess
    import sys
    out = tmp_path / "d.md"
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), "new", "--event", event, "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    deck = load_deck(out)
    th = load_theme(deck.meta["theme"])
    findings = lint.run_all(deck, build_scenes(deck, th), th)
    assert not [f for f in findings if f.startswith("[Critical]")], findings
    assert not [f for f in findings if "unknown layout" in f or "failed" in f and "not a number" not in f], findings


def test_game_theme_needs_game_flag_and_game_layouts_need_game_theme(lint_text, good_text):
    plain = good_text.replace("theme: midnight-navy", "theme: obsidian-craft")
    assert any("game theme" in f for f in lint_text(plain, "obsidian-craft"))
    flagged = plain.replace("event: hackathon", "event: hackathon\ngame: true")
    assert not any("game theme" in f for f in lint_text(flagged, "obsidian-craft"))
    boss = good_text.replace("layout: bullets", "layout: crafting\nresult: A | sword | n")
    assert any("game layout" in f for f in lint_text(boss, "midnight-navy"))


def test_new_with_a_game_theme_records_the_request(tmp_path):
    import subprocess
    import sys
    out = tmp_path / "g.md"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), "new", "--event", "hackathon", "--theme", "obsidian-craft",
                    "--out", str(out)], check=True, capture_output=True)
    assert "game: true" in out.read_text(encoding="utf-8")


def test_themes_scope_filter():
    import json
    import subprocess
    import sys
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), "themes", "--scope", "business", "--json"],
                       capture_output=True, text=True, check=True)
    names = {t["name"] for t in json.loads(r.stdout)}
    assert {"boardroom", "consulting", "ledger", "startup-bright", "venture-dark"} <= names
    assert not names & set(GAME_THEMES)


@pytest.mark.parametrize("text,expected", [("48,000", 48000.0), ("5,200", 5200.0), ("1 200 000", 1200000.0), ("0,5", 0.5),
                                          ("3,25", 3.25), ("12.5%", 12.5), ("4.2 B", 4.2), ("-9", -9.0), ("1,234.5", 1234.5),
                                          ("2020", 2020.0)])
def test_number_parser_handles_thousands_and_decimals(text, expected):
    assert number(text) == expected


def test_number_parser_returns_none_without_digits():
    assert number("none") is None


def test_funnel_widths_follow_values_with_thousands_separators(lint_text):
    from deckkit.core.layout import build_scenes
    deck = parse_text("---\nevent: investor-pitch\nminutes: 10\ntheme: boardroom\n---\n# F\nlayout: funnel\nnotes: n\nsource: x\n"
                      "- A | 48,000 | a\n- B | 5,200 | b\n- C | 410 | c\n")
    polys = [s for s in build_scenes(deck, load_theme("boardroom"))[0].items if isinstance(s, Poly)]
    widths = [max(p[0] for p in s.points) - min(p[0] for p in s.points) for s in polys]
    assert widths[0] > widths[1] > widths[2] - 1e-6


def test_poly_bbox():
    p = Poly([(1, 2), (4, 2), (3, 5)], fill="primary")
    assert p.bbox == (1, 2, 3, 3)  # x, y, width, height


@pytest.mark.parametrize("kind", ["bar", "hbar", "line", "area", "stacked", "waterfall", "donut", "scatter", "confusion"])
def test_every_chart_kind_renders(tmp_path, kind):
    from deckkit.charts.themed import render_chart
    tables = {
        "scatter": [["x", "y"], ["1", "2"], ["2", "3"], ["3", "5"]],
        "confusion": [["", "pos", "neg"], ["pos", "40", "10"], ["neg", "5", "45"]],
        "waterfall": [["Step", "Value"], ["=Start", "100"], ["Up", "20"], ["Down", "-10"], ["=End", "110"]],
        "donut": [["Part", "Share"], ["A", "60"], ["B", "40"]],
    }
    table = tables.get(kind, [["Item", "A", "B"], ["x", "1", "2"], ["y", "2", "3"], ["z", "3", "5"]])
    deck = parse_text("# S"+chr(10))
    deck.meta["_cache"] = str(tmp_path)
    path = render_chart(load_theme("boardroom"), kind, table, 6.0, 4.0, deck=deck, index=1)
    assert str(path).endswith(".png") and __import__("pathlib").Path(path).exists()


def test_math_renders(tmp_path):
    from deckkit.charts.themed import render_math
    deck = parse_text("# S"+chr(10))
    deck.meta["_cache"] = str(tmp_path)
    path, w, h = render_math(load_theme("academic"), r"\hat{y}=\sigma(w^{T}x+b)", deck=deck, index=1)
    assert w > 0 and h > 0


def formal_example_decks():
    out = []
    for p in sorted(EXAMPLES.glob("*/*.md")):
        head = p.read_text(encoding="utf-8")[:400]
        if head.startswith("---") and "event:" in head:
            out.append(p)
    return out


@pytest.mark.parametrize("path", formal_example_decks(), ids=lambda p: p.parent.name)
def test_every_example_deck_is_clean_and_game_decks_are_flagged(path, tmp_path):
    deck = load_deck(path)
    th = load_theme(deck.meta["theme"])
    deck.meta["_cache"] = str(tmp_path)
    findings = lint.run_all(deck, build_scenes(deck, th), th)
    assert lint.blocking(findings) == [], findings
    assert not any("game theme" in f or "game layout" in f for f in findings), findings
    assert ("game" in th.scopes) == bool(deck.meta.get("game")), path


@pytest.mark.parametrize("name", ["investor-pitch-venture", "quarterly-review-boardroom", "portfolio-case-mono", "demo-day-aurora",
                                  "data-story-datablue", "product-roadmap-signal", "ux-research-lavender", "tech-showcase-cyber", "data-viz-glass"])
def test_formal_examples_ship_with_built_files(name):
    folder = EXAMPLES / name
    assert list(folder.glob("*.pptx")) and list(folder.glob("*.pdf")) and list(folder.glob("*.html")) and (folder / "preview.png").exists()
    assert (folder / "prompt.md").exists() and (folder / "report.md").exists()
