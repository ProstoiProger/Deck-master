"""The web presentation backend: one self-contained .html, same geometry and text lines as the other outputs."""
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser

import pytest

from conftest import ROOT
from deckkit.backends.html_backend import _linkify, _subset_font, build_html
from deckkit.core import textfit
from deckkit.core.layout import build_scenes
from deckkit.core.scene import Text
from deckkit.core.spec import load_deck, parse_text
from deckkit.core.theme import load_theme

EXAMPLE = ROOT / "examples" / "data-story-datablue" / "northwind.md"


class Collect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections, self.ids, self.tags, self.attrs = [], set(), [], []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append(tag)
        self.attrs.append((tag, d))
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "section" and "slide" in (d.get("class") or ""):
            self.sections.append(d)


def make(tmp_path, deck_path=EXAMPLE, name="deck.html"):
    deck = load_deck(deck_path)
    theme = load_theme(deck.meta["theme"])
    deck.meta["_cache"] = str(tmp_path / ".cache")
    scenes = build_scenes(deck, theme)
    build_html(scenes, theme, deck, tmp_path / name)
    return deck, theme, scenes, (tmp_path / name).read_text(encoding="utf-8")


def test_one_section_per_slide_with_aria_labels_and_notes(tmp_path):
    deck, theme, scenes, text = make(tmp_path)
    p = Collect()
    p.feed(text)
    assert len(p.sections) == len(deck.slides)
    assert all(s.get("aria-label", "").startswith("Slide ") and s.get("role") == "group" for s in p.sections)
    assert text.count('<aside class="notes">') == len(deck.slides) and "Read it left to right" in text


def test_page_is_self_contained_and_has_a_strict_csp(tmp_path):
    _d, _t, _s, text = make(tmp_path)
    assert "Content-Security-Policy" in text and "default-src 'none'" in text
    assert "<link" not in text and "@import" not in text and "url(http" not in text
    for tag, attrs in _attrs(text):
        if tag in ("img", "script", "link", "iframe"):
            assert not (attrs.get("src") or attrs.get("href") or "").startswith("http"), (tag, attrs)
    assert text.count("@font-face") >= 2 and "data:font/woff;base64" in text and "@page" in text


def _attrs(text):
    p = Collect()
    p.feed(text)
    return p.attrs


def test_text_lines_are_the_ones_textfit_breaks(tmp_path):
    deck, theme, scenes, text = make(tmp_path)
    sc = scenes[1]                                              # the statement slide
    big = max((i for i in sc.items if isinstance(i, Text) and i.text.strip()), key=lambda i: i.size)
    lines = textfit.wrap(theme, big.text, big.role, big.size, big.w, big.bold)
    flat = "<br>".join(" ".join(w for w, _b in line) for line in lines)
    assert flat.replace("&amp;", "&") in text or flat in text


def test_every_dom_id_the_runtime_looks_up_exists(tmp_path):
    _d, _t, _s, text = make(tmp_path)
    p = Collect()
    p.feed(text)
    js = (ROOT / "assets" / "web" / "deck.js").read_text(encoding="utf-8")
    wanted = set(re.findall(r"\$\('([\w-]+)'\)", js))
    dynamic = {"pcur", "pnext", "pnotes", "pcount", "ptimer", "pp", "pn", "pr", "rcount", "rview"}   # built inside the presenter window and the reading view
    assert wanted - dynamic <= p.ids, wanted - dynamic - p.ids


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_runtime_javascript_parses(tmp_path):
    js = tmp_path / "deck.js"
    js.write_text((ROOT / "assets" / "web" / "deck.js").read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run(["node", "--check", str(js)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_fonts_are_subset_and_pictures_are_embedded(tmp_path):
    deck, theme, scenes, text = make(tmp_path)
    import base64
    blobs = re.findall(r"base64,([A-Za-z0-9+/=]{200,})\)", text)
    assert blobs
    fonts = [b for b in blobs]
    sizes = [len(base64.b64decode(b)) for b in fonts]
    full = (ROOT / "assets" / "fonts" / "Inter-Regular.ttf").stat().st_size
    assert min(sizes) < full / 2, "fonts are subset to the characters used"
    assert re.search(r'<img src="data:image/png;base64,', text)


def test_subset_keeps_only_the_requested_glyphs():
    from fontTools.ttLib import TTFont
    from io import BytesIO
    import base64
    data, fmt = _subset_font(ROOT / "assets" / "fonts" / "Inter-Regular.ttf", set("abc"))
    f = TTFont(BytesIO(base64.b64decode(data)))
    cmap = f.getBestCmap()
    assert ord("a") in cmap and ord("z") not in cmap and fmt == "woff"


def test_titles_and_notes_are_escaped(tmp_path):
    text = ('---\ntitle: "A <script>alert(1)</script> deck"\ntheme: boardroom\n---\n# T <b>x</b>\nlayout: bullets\n'
            'notes: <img src=x onerror=alert(1)> note\n- one & two\n')
    deck = parse_text(text)
    theme = load_theme("boardroom")
    scenes = build_scenes(deck, theme)
    build_html(scenes, theme, deck, tmp_path / "x.html")
    out = (tmp_path / "x.html").read_text(encoding="utf-8")
    assert "<script>alert(1)" not in out and "&lt;script&gt;" in out
    assert "<img src=x" not in out and "&lt;img src=x" in out
    assert "one &amp; two" in out


@pytest.mark.parametrize("text,href", [("github.com/team/repo", "https://github.com/team/repo"), ("orbit.example.org", "https://orbit.example.org"),
                                       ("team@example.org", "mailto:team@example.org"), ("https://a.io/x", "https://a.io/x"),
                                       ("0.61", None), ("48,213", None), ("two words.com", None), ("plain", None)])
def test_linkify_only_real_addresses(text, href):
    assert _linkify(text) == href


def test_z_order_is_kept_text_after_the_shapes_it_sits_on(tmp_path):
    _d, _t, _s, text = make(tmp_path)
    first_slide = text[text.index('id="slide-1"'):text.index('id="slide-2"')]
    assert first_slide.index("<svg") < first_slide.index('<div class="t ')


def test_deck_title_is_escaped_in_the_page_title(tmp_path):
    deck, theme, scenes, text = make(tmp_path)
    assert "<title>Why Northwind customers leave: slow setup and early tickets</title>" in text


# ---- CLI ---------------------------------------------------------------------------------------------------

def run_cli(*args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "cli.py"), *args], capture_output=True, text=True)


def test_build_without_flags_writes_pptx_pdf_and_html(tmp_path):
    r = run_cli("build", str(EXAMPLE), "--out", str(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert {p.suffix for p in tmp_path.glob("northwind.*")} == {".pptx", ".pdf", ".html"}


def test_build_with_html_flag_writes_only_html(tmp_path):
    r = run_cli("build", str(EXAMPLE), "--html", "--out", str(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert {p.suffix for p in tmp_path.glob("northwind.*")} == {".html"}


def test_pdf_flag_alone_still_means_only_pdf(tmp_path):
    r = run_cli("build", str(EXAMPLE), "--pdf", "--out", str(tmp_path))
    assert r.returncode == 0
    assert {p.suffix for p in tmp_path.glob("northwind.*")} == {".pdf"}


def test_print_stylesheet_gives_one_unscaled_page_per_slide():
    css = (ROOT / "assets" / "web" / "deck.css").read_text(encoding="utf-8")
    assert "@page { size: 1333.333px 750px; margin: 0; }" in css
    assert "body > :not(#deck) { display: none !important; }" in css
    assert ".slide:last-child { break-after: auto" in css, "no blank page after the last slide"


def test_shipped_example_pages_have_the_same_slide_count_as_their_decks():
    for folder in ("data-story-datablue", "tech-showcase-cyber"):
        deck_md = next(p for p in (ROOT / "examples" / folder).glob("*.md") if p.read_text(encoding="utf-8").startswith("---") and "event:" in p.read_text(encoding="utf-8")[:300])
        page = deck_md.with_suffix(".html").read_text(encoding="utf-8")
        assert page.count('role="group" aria-roledescription="slide"') == len(load_deck(deck_md).slides)


# ---- adaptive: the reading view and the device rules ------------------------------------------------------------------

def test_every_body_text_carries_its_raw_text_group_and_slide_title_for_the_reading_view(tmp_path):
    deck, theme, scenes, text = make(tmp_path)
    body_texts = [i for sc in scenes for i in sc.items if isinstance(i, Text) and i.text.strip() and not i.chrome]
    assert text.count("data-text=") == len(body_texts)
    assert text.count('data-title="') == len(deck.slides) and 'data-title="The model finds 58% of leavers in its top 10%"' in text
    assert re.search(r'data-g="\d+:\d+" data-gbg="#[0-9A-F]{6}"', text), "texts inside a filled card know the card"


def test_group_key_picks_the_smallest_card_containing_the_text():
    from deckkit.backends.html_backend import _group_key
    from deckkit.core.scene import SceneSlide, Shape
    sc = SceneSlide(index=1, layout="x", title="t", bg="#000000")
    sc.items += [Shape(1, 1, 8, 4, "#111111"), Shape(2, 2, 3, 1.5, "#222222", kind="round"), Shape(0, 0, 13.3, 7.5, "#000000"), Shape(2, 2, 3, 0.05, "#FFFFFF")]
    inside = Text(2.2, 2.2, 2.0, 0.5, "a", 14)
    assert _group_key(sc, inside) == ("200:200", "#222222")
    outer = Text(6, 1.2, 1.0, 0.5, "b", 14)
    assert _group_key(sc, outer) == ("100:100", "#111111")
    assert _group_key(sc, Text(10, 6.5, 1, 0.4, "c", 14)) == (None, None)


def test_text_over_a_backdrop_picture_gets_no_chip_color(tmp_path):
    deck = parse_text("---\ntheme: aurora-mesh\n---\n# T\nlayout: title\nnotes: n\n")
    theme = load_theme("aurora-mesh")
    deck.meta["_cache"] = str(tmp_path)
    build_html(build_scenes(deck, theme), theme, deck, tmp_path / "m.html")
    page = (tmp_path / "m.html").read_text(encoding="utf-8")
    tag = re.search(r'<div class="t [^"]*"[^>]*data-r="heading"[^>]*>', page).group(0)
    assert "data-bg" not in tag


def test_page_declares_device_rules():
    css = (ROOT / "assets" / "web" / "deck.css").read_text(encoding="utf-8")
    js = (ROOT / "assets" / "web" / "deck.js").read_text(encoding="utf-8")
    for needle in ("@media (pointer: coarse)", "env(safe-area-inset-bottom)", "forced-colors", "prefers-reduced-motion", "html.reader { overflow: auto", ".rhead { position: sticky"):
        assert needle in css, needle
    for needle in ("innerHeight > innerWidth * 1.1", "params.get('view')", "requestFullscreen", "IntersectionObserver", "deck-master:view"):
        assert needle in js, needle


def test_viewport_meta_covers_notched_screens(tmp_path):
    _d, _t, _s, text = make(tmp_path)
    assert 'content="width=device-width, initial-scale=1, viewport-fit=cover"' in text and 'id="reader"' in text and 'id="b-view"' in text
