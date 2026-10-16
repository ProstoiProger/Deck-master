import pytest

from conftest import FLAGSHIP, LESSON
from deckkit import lint
from deckkit.core import color, layout as layout_registry
from deckkit.core.layout import build_scenes
from deckkit.core.spec import load_deck
from deckkit.core.theme import ThemeError, contrast_table, load_theme, theme_names

EXAMPLE_FILES = [FLAGSHIP, LESSON]
NO_LOW_LEVEL = ("overflow", "contrast", "unknown layout", "failed", "glyph", "not found")


def test_all_themes_ship_and_have_readable_text():
    names = theme_names()
    assert len(names) == 44 and {"obsidian-craft", "classic-craft", "midnight-navy"} <= set(names)
    for n in names:
        t = load_theme(n)
        ratios = dict(contrast_table(t))
        assert ratios["text on bg"] >= 7 and ratios["text on surface"] >= 4.5, n
        assert ratios["muted on bg"] >= 4.5 and ratios["muted on surface"] >= 4.5, n
        assert ratios["on(primary) on primary"] >= 4.5, n


def test_unknown_theme_lists_the_choices():
    with pytest.raises(ThemeError, match="midnight-navy"):
        load_theme("nope")


def test_on_picks_the_readable_color_for_a_fill(theme):
    for token in ("primary", "accent", "surface"):
        fill = theme.c(token)
        assert color.contrast(theme.on(fill), fill) >= 4.5


def test_all_layouts_have_metadata_and_are_listed():
    layout_registry.ensure_loaded()
    assert len(layout_registry.LAYOUTS) == 87
    for spec in layout_registry.LAYOUTS.values():
        assert spec.purpose and spec.max_words and spec.accepts and spec.example, spec.name


def test_registering_a_layout_without_purpose_fails():
    with pytest.raises(ValueError, match="purpose"):
        layout_registry.layout("x", "f", " ", 10)(lambda c, s: None)


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.parent.name)
def test_every_example_has_no_blocking_findings(path, tmp_path):
    deck = load_deck(path)
    theme = load_theme(deck.meta["theme"])
    deck.meta["_cache"] = str(tmp_path)
    findings = lint.run_all(deck, build_scenes(deck, theme), theme)
    assert lint.blocking(findings) == [], findings


def test_kazakh_and_russian_text_have_glyphs_in_every_theme(parse):
    text = "# Қазақша: ә ғ қ ң ө ү ұ һ і\nnotes: Текст на русском\n- Қыран | командасы\n"
    for name in theme_names():
        theme = load_theme(name)
        deck = parse(text)
        bad = [f for f in lint.run_all(deck, build_scenes(deck, theme), theme) if "glyph" in f]
        assert bad == [], (name, bad)
