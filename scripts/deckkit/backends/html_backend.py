"""Write the scene as one self-contained web presentation (a single .html file, no network needed).

Same geometry as the PPTX and PDF backends: shapes, polygons and lines become inline SVG in their original z-order, pictures are embedded as
data URIs, and every text line is placed exactly where the shared text fitting broke it (so the lines match the PDF and the lint), using
subset copies of the bundled fonts embedded as WOFF. The page adds keyboard, click and swipe navigation, an overview grid, speaker notes with
a timer, a synchronised presenter window, fullscreen and a print stylesheet (one slide per page). Needs fontTools (the `core` group).
"""
import base64
import html
import re
from io import BytesIO
from pathlib import Path

from ..core import color, paths, textfit
from ..lint.contrast import background_under

PX = 100.0                      # stage pixels per inch: the stage is 1333.333 x 750 px
LINK = re.compile(r"^(?:https?://)?([\w-]+\.)+[a-z]{2,}(?:/[^\s]*)?$", re.I)
MAIL = re.compile(r"^[\w.+-]+@([\w-]+\.)+[a-z]{2,}$", re.I)
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".svg": "image/svg+xml"}


def _px(v):
    return f"{v * PX:.2f}".rstrip("0").rstrip(".")


def _esc(s):
    return html.escape(str(s), quote=True)


def _family(path):
    return "dk-" + Path(path).stem


def _subset_font(path, chars):
    """Base64 WOFF of `path` holding only the glyphs for `chars` (falls back to the whole file if subsetting fails)."""
    try:
        import logging
        from fontTools import subset
        logging.getLogger("fontTools").setLevel(logging.ERROR)   # silence "table NOT subset" notices
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk"]
        opts.name_IDs = [1, 2, 6]
        opts.notdef_outline = True
        opts.hinting = False
        font = subset.load_font(str(path), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars | {" ", " "})))
        sub.subset(font)
        buf = BytesIO()
        subset.save_font(font, buf, opts)
        return base64.b64encode(buf.getvalue()).decode("ascii"), "woff"
    except Exception:
        return base64.b64encode(Path(path).read_bytes()).decode("ascii"), "truetype"


def _linkify(text):
    t = text.strip()
    if "\n" in t or " " in t:
        return None
    if MAIL.match(t):
        return "mailto:" + t
    if LINK.match(t) and ("/" in t or t.count(".") >= 1) and not re.fullmatch(r"[\d.,]+", t):
        return t if t.lower().startswith("http") else "https://" + t
    return None


def _svg_item(it):
    from ..core.scene import Line, Poly, Shape
    if isinstance(it, Shape):
        fill = f'fill="{it.fill}"' + (f' fill-opacity="{it.alpha:g}"' if it.alpha < 1 else "") if it.fill else 'fill="none"'
        stroke = f' stroke="{it.line}" stroke-width="{it.line_w / 72 * PX:.2f}"' if it.line else ""
        if it.kind == "ellipse":
            return f'<ellipse cx="{_px(it.x + it.w / 2)}" cy="{_px(it.y + it.h / 2)}" rx="{_px(it.w / 2)}" ry="{_px(it.h / 2)}" {fill}{stroke}/>'
        rx = min(it.radius, it.h / 2, it.w / 2) if it.kind == "round" else 0
        rxa = f' rx="{_px(rx)}"' if rx else ""
        return f'<rect x="{_px(it.x)}" y="{_px(it.y)}" width="{_px(it.w)}" height="{_px(it.h)}"{rxa} {fill}{stroke}/>'
    if isinstance(it, Poly):
        fill = f'fill="{it.fill}"' + (f' fill-opacity="{it.alpha:g}"' if it.alpha < 1 else "") if it.fill else 'fill="none"'
        stroke = f' stroke="{it.line}" stroke-width="{it.line_w / 72 * PX:.2f}" stroke-linejoin="round"' if it.line else ""
        pts = " ".join(f"{_px(x)},{_px(y)}" for x, y in it.points)
        return f'<polygon points="{pts}" {fill}{stroke}/>'
    if isinstance(it, Line):
        dash = ' stroke-dasharray="6 6"' if it.dash else ""
        return (f'<line x1="{_px(it.x1)}" y1="{_px(it.y1)}" x2="{_px(it.x2)}" y2="{_px(it.y2)}" stroke="{it.color}" '
                f'stroke-width="{it.width / 72 * PX:.2f}"{dash}/>')
    return ""


def _group_key(sc, text):
    """The card a text sits in: the smallest card-sized shape that contains its center, as 'y:x' in hundredths of an inch (None when free).
    The reading view uses it to keep a card's texts together instead of interleaving neighbouring cards row by row.
    Returns (key, fill of that card)."""
    from ..core.scene import Shape
    cx, cy = text.x + text.w / 2, text.y + text.h / 2
    best = None
    for s in sc.items:
        if not isinstance(s, Shape) or s.kind not in ("rect", "round") or not (s.fill or s.line):
            continue
        if s.w < 1.2 or s.h < 0.55 or (s.w >= 12.5 and s.h >= 6.5):
            continue
        if s.x <= cx <= s.x + s.w and s.y <= cy <= s.y + s.h and (best is None or s.w * s.h < best.w * best.h):
            best = s
    if best is None:
        return None, None
    fill = best.fill if (best.fill and best.alpha >= 0.85) else None
    return f"{round(best.y * PX)}:{round(best.x * PX)}", fill


def _text_item(theme, it, used, index, bg=None, group=None, gfill=None):
    """One absolutely positioned text block; the lines are the ones textfit breaks, joined by <br> so no browser re-wraps them."""
    lines = textfit.wrap(theme, it.text, it.role, it.size, it.w, it.bold)
    base_file = theme.font_file(it.role, it.bold)
    parts = []
    for line in lines:
        spans = []
        for word, bold in line:
            f = theme.font_file(it.role, bool(it.bold or bold))
            used.setdefault(str(f), set()).update(word)
            safe = _esc(word)
            if f != base_file:
                safe = f'<span style="font-family:{_family(f)}">{safe}</span>'
            spans.append(safe)
        parts.append(" ".join(spans))
    used.setdefault(str(base_file), set())
    body_html = "<br>".join(parts)
    href = _linkify(it.text) if len(lines) == 1 else None
    if href:
        body_html = f'<a href="{_esc(href)}" target="_blank" rel="noopener noreferrer">{body_html}</a>'
    size = it.size / 72 * PX
    style = (f"left:{_px(it.x)}px;top:{_px(it.y)}px;width:{_px(it.w)}px;height:{_px(it.h)}px;font-family:{_family(base_file)},sans-serif;"
             f"font-size:{size:.2f}px;line-height:{it.line_h};color:{it.color}")
    cls = f"t va-{it.valign} ta-{it.align}"
    # data-* feed the reader view for small screens: position (reading order), size, role, the color really behind the text and its raw text
    data = f' data-x="{round(it.x * PX)}" data-y="{round(it.y * PX)}" data-s="{it.size:g}" data-r="{it.role}"'
    if it.chrome:
        data += " data-chrome"
    else:                                   # body text and titles rise in one after the other; furniture does not
        cls += " rv"
        style += f";--i:{min(index, 14)}"
        data += f' data-text="{_esc(it.text)}"' + (f' data-bg="{bg}"' if bg else "") + (f' data-g="{group}"' if group else "") + (f' data-gbg="{gfill}"' if gfill else "")
    return f'<div class="{cls}" style="{style}"{data}>{body_html}</div>'


def _image_item(it, scene):
    p = Path(it.path)
    mime = MIME.get(p.suffix.lower(), "application/octet-stream")
    data = base64.b64encode(p.read_bytes()).decode("ascii")
    decorative = it.tone is not None or (it.w >= 13 and it.h >= 7)
    alt = "" if decorative else "Figure"
    full = it.w >= 13 and it.h >= 7
    return (f'<img src="data:{mime};base64,{data}" alt="{alt}" draggable="false" data-x="{round(it.x * PX)}" data-y="{round(it.y * PX)}" '
            f'data-w="{round(it.w * PX)}"{" data-full" if full else ""} style="left:{_px(it.x)}px;top:{_px(it.y)}px;width:{_px(it.w)}px;height:{_px(it.h)}px">')


def build_html(scenes, theme, deck, path):
    from ..core.scene import Image, Line, Poly, Shape, Text

    title = str(deck.meta.get("title", "")) or scenes[0].title
    lang = str(deck.meta.get("lang", "en")) or "en"
    minutes = deck.meta.get("minutes", "") or ""
    used = {}
    sections = []
    for sc in scenes:
        out, svg, rv = [], [], 0
        tones = {i.tone for i in sc.items if isinstance(i, Image) and i.tone}

        def flush():
            if svg:
                out.append('<svg class="v" viewBox="0 0 1333.333 750" aria-hidden="true" shape-rendering="geometricPrecision">' + "".join(svg) + "</svg>")
                svg.clear()
        for k, it in enumerate(sc.items):
            if isinstance(it, (Shape, Poly, Line)):
                svg.append(_svg_item(it))
            elif isinstance(it, Text):
                if not it.text.strip():
                    continue
                flush()
                behind = background_under(sc, k, it)
                if behind in tones:                      # text over a decorative backdrop picture: no chip behind it in the reading view
                    behind = None
                out.append(_text_item(theme, it, used, rv, behind if behind and behind.upper() != sc.bg.upper() else None, *_group_key(sc, it)))
                rv += 0 if it.chrome else 1
            elif isinstance(it, Image):
                flush()
                out.append(_image_item(it, sc))
        flush()
        label = f"Slide {sc.index} of {len(scenes)}: {sc.title}"
        notes = f'<aside class="notes">{_esc(sc.notes)}</aside>' if sc.notes else '<aside class="notes"></aside>'
        sections.append(f'<section class="slide" id="slide-{sc.index}" role="group" aria-roledescription="slide" aria-label="{_esc(label)}" data-title="{_esc(sc.title)}">'
                        f'<div class="stage" style="background:{sc.bg}">{"".join(out)}</div>{notes}</section>')

    faces = []
    for fpath, chars in sorted(used.items()):
        data, fmt = _subset_font(fpath, chars)
        faces.append(f'@font-face{{font-family:"{_family(fpath)}";src:url(data:font/{"woff" if fmt == "woff" else "ttf"};base64,{data}) format("{fmt}");'
                     f'font-weight:400;font-style:normal;font-display:block}}')

    t = theme
    dark = t.mode == "dark"
    page = color.mix(t.c("bg"), "#000000", 0.45) if dark else color.mix(t.c("bg"), t.c("text"), 0.14)
    css = (paths.assets_dir() / "web" / "deck.css").read_text(encoding="utf-8")
    js = (paths.assets_dir() / "web" / "deck.js").read_text(encoding="utf-8")
    root_vars = (f":root{{--page:{page};--ui-accent:{t.c('accent')};--ui-bg:{color.mix(t.c('bg'), '#000000', 0.2) if dark else 'rgba(255,255,255,.9)'};"
                 f"--ui-fg:{t.c('text')};color-scheme:{'dark' if dark else 'light'}}}")
    csp = "default-src 'none'; img-src data:; style-src 'unsafe-inline'; font-src data:; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
    bar = ('<nav id="bar" aria-label="Presentation controls">'
           '<button id="b-prev" aria-label="Previous slide" title="Previous (left arrow)">&#8249;</button><span id="count" aria-hidden="true">1 / 1</span>'
           '<button id="b-next" aria-label="Next slide" title="Next (right arrow, space)">&#8250;</button>'
           '<button id="b-ov" aria-label="Overview" title="Overview (O)">&#9638;</button>'
           '<button id="b-view" aria-label="Switch to the reading view" title="Reading view (V)">&#9776;</button>'
           '<button id="b-notes" aria-label="Speaker notes" title="Notes (N)">&#9998;</button>'
           '<button id="b-pres" aria-label="Open presenter window" title="Presenter window (P)">&#9201;</button>'
           '<button id="b-full" aria-label="Fullscreen" title="Fullscreen (F)">&#9974;</button>'
           '<button id="b-help" aria-label="Keyboard help" title="Help (?)">?</button></nav>')
    help_ = ('<div id="help" role="dialog" aria-label="Keyboard help"><div><b>Keys</b><br><kbd>&rarr;</kbd> <kbd>Space</kbd> next &nbsp; <kbd>&larr;</kbd> previous<br>'
             '<kbd>Home</kbd> <kbd>End</kbd> first, last &nbsp; <kbd>O</kbd> overview<br><kbd>N</kbd> notes &nbsp; <kbd>P</kbd> presenter window &nbsp; '
             '<kbd>R</kbd> reset timer<br><kbd>F</kbd> fullscreen &nbsp; <kbd>V</kbd> reading view &nbsp; <kbd>?</kbd> this help<br>Click the right side to go on, the left side to go back; '
             'swipe on a touch screen. Print (Ctrl+P) gives one slide per page.</div></div>')
    page_html = (f'<!doctype html>\n<html lang="{_esc(lang)}"><head><meta charset="utf-8">'
                 f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
                 f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
                 f'<meta name="generator" content="deck-master"><meta name="color-scheme" content="{"dark" if dark else "light"}">'
                 f'<title>{_esc(title)}</title><style>{"".join(faces)}{css}{root_vars}</style>'
                 f'<noscript><style>html,body{{overflow:auto}}#deck{{position:static}}.slide{{position:relative;visibility:visible;opacity:1;height:750px;width:1333px;margin:20px auto}}'
                 f'.stage{{left:0;top:0;transform:none}}#bar,#progress{{display:none}}</style></noscript></head>'
                 f'<body data-minutes="{_esc(minutes)}"><main id="deck" aria-label="{_esc(title)}">{"".join(sections)}</main>'
                 f'<div id="pv"></div><div id="reader" aria-label="{_esc(title)} (reading view)"></div><div id="progress" role="presentation"></div>{bar}'
                 f'<div id="notes" role="region" aria-label="Speaker notes"><small id="ntimer">00:00</small><span id="ntext"></span></div>{help_}'
                 f'<div id="live" class="sr" aria-live="polite"></div>'
                 f'<noscript><p style="position:fixed;top:0;left:0;color:#fff;background:#000;padding:8px">This presentation needs JavaScript to switch slides; '
                 f'print this page for a PDF with one slide per page.</p></noscript><script>{js}</script></body></html>\n')
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(page_html, encoding="utf-8", newline="\n")
    return path
