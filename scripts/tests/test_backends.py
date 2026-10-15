import pytest

from conftest import FLAGSHIP, LESSON
from deckkit.core.layout import build_scenes
from deckkit.core.spec import load_deck
from deckkit.core.theme import load_theme


@pytest.fixture
def scenes_and_deck(tmp_path):
    deck = load_deck(FLAGSHIP)
    theme = load_theme(deck.meta["theme"])
    deck.meta["_cache"] = str(tmp_path)
    return build_scenes(deck, theme), deck, theme


def test_pptx_has_all_slides_notes_theme_font_and_pictures(scenes_and_deck, tmp_path):
    pptx = pytest.importorskip("pptx")
    from deckkit.backends.pptx_backend import build_pptx
    scenes, deck, theme = scenes_and_deck
    prs = pptx.Presentation(str(build_pptx(scenes, theme, deck, tmp_path / "d.pptx")))
    assert len(prs.slides) == len(deck.slides) == 8
    assert prs.slides[1].notes_slide.notes_text_frame.text == deck.slides[1].notes
    fonts = {r.font.name for s in prs.slides for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs for r in p.runs}
    assert {"Inter", "Press Start 2P"} <= fonts
    assert any(sh.shape_type == 13 for sh in prs.slides[3].shapes)  # the demo screenshot is a picture
    assert prs.core_properties.title == deck.meta["title"]


def test_pptx_text_is_real_editable_text(scenes_and_deck, tmp_path):
    pptx = pytest.importorskip("pptx")
    from deckkit.backends.pptx_backend import build_pptx
    scenes, deck, theme = scenes_and_deck
    prs = pptx.Presentation(str(build_pptx(scenes, theme, deck, tmp_path / "d.pptx")))
    text = " ".join(sh.text_frame.text for sh in prs.slides[1].shapes if sh.has_text_frame)
    assert "Boss fight" in text and "14 days" in text


def test_pdf_has_one_page_per_slide_with_extractable_text(scenes_and_deck, tmp_path):
    pytest.importorskip("reportlab")
    pymupdf = pytest.importorskip("pymupdf")
    from deckkit.backends.pdf_backend import build_pdf
    scenes, deck, theme = scenes_and_deck
    doc = pymupdf.open(str(build_pdf(scenes, theme, deck, tmp_path / "d.pdf")))
    assert doc.page_count == 8
    assert "StudyBuddy" in doc[0].get_text() and "14 days" in doc[1].get_text()
    assert abs(doc[0].rect.width / doc[0].rect.height - 13.333 / 7.5) < 0.01


def test_pdf_renders_cyrillic_and_kazakh_text(tmp_path, parse, theme):
    pytest.importorskip("reportlab")
    pymupdf = pytest.importorskip("pymupdf")
    from deckkit.backends.pdf_backend import build_pdf
    deck = parse("# Қазақша мәтін: ә ғ қ ң\nnotes: n\n- Русский текст\n")
    doc = pymupdf.open(str(build_pdf(build_scenes(deck, theme), theme, deck, tmp_path / "k.pdf")))
    text = doc[0].get_text()
    assert "Қазақша" in text and "Русский" in text


@pytest.mark.parametrize("path,theme_name", [(FLAGSHIP, "obsidian-craft"), (LESSON, "classic-craft")])
def test_game_decks_build_both_formats(tmp_path, path, theme_name):
    pytest.importorskip("pptx")
    pytest.importorskip("reportlab")
    from deckkit.backends.pdf_backend import build_pdf
    from deckkit.backends.pptx_backend import build_pptx
    deck = load_deck(path)
    theme = load_theme(theme_name)
    deck.meta["_cache"] = str(tmp_path)
    scenes = build_scenes(deck, theme)
    assert build_pptx(scenes, theme, deck, tmp_path / "b.pptx").exists()
    assert build_pdf(scenes, theme, deck, tmp_path / "b.pdf").exists()
