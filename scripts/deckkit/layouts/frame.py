"""General frame layouts for formal decks: section divider, quote, big number, full image, columns."""
from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import H, W
from ._util import cells, flow


def faint(c, base="primary", need=3.05):
    """A tint of `base` on the slide background that still reaches `need`:1 contrast, for large decorative numerals."""
    bg, fg = c.t.c("bg"), c.t.c(base)
    for k in range(10, 100, 5):
        col = color.mix(bg, fg, k / 100)
        if color.contrast(col, bg) >= need:
            return col
    return fg


@layout("section", "frame", "Section divider: a very large number and the section title.", 25,
        accepts="props: number (default counts section slides); first paragraph: one-line subtitle",
        example="# Results\nlayout: section\nnumber: 02\nWhat the experiments show.")
def section(c, s):
    n = s.prop("number")
    if not n:
        n = f"{1 + sum(1 for x in c.deck.slides[:s.index - 1] if x.layout == 'section'):02d}"
    scale = c.style["heading_scale"]
    c.rect(MARGIN, 2.55, 1.0, 0.08, "accent")
    c.text(W - 6.9, 0.7, 6.2, 5.6, n, 230 * scale, faint(c), "heading", True, "right", "middle", 1.0, chrome=True)
    size = c.fit_text(MARGIN, 2.85, 7.6, 2.0, s.title, 50 * scale, 22 * scale, "text", "heading", True, line_h=c.style["heading_line_h"])
    if s.paragraphs:
        c.fit_text(MARGIN, 5.05, 7.2, 1.0, s.paragraphs[0], 22, 14, "muted")


@layout("quote", "frame", "One large quotation with its author; use it for a testimonial, a principle or a user voice.", 45,
        accepts="first paragraph or `> quote` line: the quote; props: author, role; the title is the small kicker above",
        example="# What users say\nlayout: quote\nauthor: A. Student\nrole: Year 2, Computer Science\n> The rest token saved my streak.")
def quote(c, s):
    text = s.quote or (s.paragraphs[0] if s.paragraphs else "")
    c.text(MARGIN, 0.6, W - 2 * MARGIN, 0.45, s.title.upper(), 14, "muted", "mono", True, chrome=True)
    c.text(MARGIN - 0.05, 1.35, 1.6, 2.0, "“", 150, "accent", "heading", True, "left", "top", 1.0, chrome=True)
    scale = c.style["heading_scale"]
    c.fit_text(MARGIN + 1.5, 2.0, W - 2 * MARGIN - 1.7, 3.0, text, 38 * scale, 18 * scale, "text", "heading", True, line_h=1.25)
    c.rect(MARGIN + 1.5, 5.35, 0.8, 0.06, "accent")
    if s.prop("author"):
        c.text(MARGIN + 1.5, 5.5, 8, 0.4, s.prop("author"), 20, "text", "body", True)
    if s.prop("role"):
        c.text(MARGIN + 1.5, 5.9, 8, 0.35, s.prop("role"), 15, "muted")


@layout("big_number", "frame", "One hero number with its meaning and a few supporting points.", 40,
        accepts="props: stat `62% | what it measures`; items: up to 3 supporting bullets",
        example="# Churn fell by more than half\nlayout: big_number\nsource: ops/q3.csv\nstat: 62% | lower churn in the pilot cohort\n- Measured over 12 weeks\n- Same price, same product")
def big_number(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    stat = [p.strip() for p in s.prop("stat").split("|")] + ["", ""]
    scale = c.style["heading_scale"]
    size = textfit.fit_line(c.t, stat[0], "heading", 6.4, 150 * scale, 40 * scale, True)
    c.text(x, y, 6.6, 2.6, stat[0], size, "accent", "heading", True, "left", "middle", 1.0)
    if stat[1]:
        c.fit_text(x, y + 2.7, 6.2, 1.2, stat[1], 24, 14, "text")
    if s.items:
        c.rect(x + 7.0, y + 0.3, 0.03, h - 0.6, color.mix(c.t.c("bg"), c.t.c("text"), 0.3))
        flow(c, s.items[:3], x + 7.4, y + 0.5, w - 7.4, h - 0.8, max_size=22, min_size=14, gap=0.35)


@layout("image_full", "frame", "A full-slide image with the title as a caption bar; for a photo, a product shot or a figure.", 25,
        accepts="image: picture; the title is the caption; credit: photo credit",
        example="# The prototype in the lab\nlayout: image_full\nimage: figures/lab.jpg\ncredit: Photo: the team")
def image_full(c, s):
    c.has_backdrop = True  # a full-bleed picture carries no footer: it would sit on the caption bar
    c.image(0, 0, W, H, s.image, "full-slide image")
    c.rect(0, H - 1.5, W, 1.5, "#000000", alpha=0.72)
    c.fit_text(MARGIN, H - 1.4, W - 2 * MARGIN, 0.95, s.title, 32, 18, "#FFFFFF", "heading", True, valign="middle")
    if s.prop("credit"):
        c.text(MARGIN, H - 0.45, W - 2 * MARGIN, 0.3, s.prop("credit"), 12, "#D1D5DB", "body", chrome=True, valign="middle")


@layout("columns", "frame", "Two or three titled columns of bullets; for options, phases or parallel arguments.", 70,
        accepts="groups: two or three `## heading` sections with bullets; or items split evenly in two columns",
        example="# Three ways to scale\nlayout: columns\n## Vertical\n- Bigger machine\n## Horizontal\n- More machines\n## Smarter\n- Cache and batch")
def columns(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1]]
    if not groups:
        half = (len(s.items) + 1) // 2
        groups = [("", s.items[:half]), ("", s.items[half:])]
    groups = groups[:3]
    n = len(groups)
    gap = 0.35
    cw = (w - gap * (n - 1)) / n
    for i, (head, items) in enumerate(groups):
        cx = x + i * (cw + gap)
        c.box(cx, y + 0.1, cw, h - 0.1, fill="surface")
        yy = y + 0.35
        if head:
            c.badge(cx + 0.45, yy + 0.22, 0.2, str(i + 1), "primary", 14)
            c.fit_text(cx + 0.8, yy, cw - 1.0, 0.45, head, 21, 13, "text", "heading", True, valign="middle")
            yy += 0.8
        flow(c, items[:6], cx + 0.35, yy, cw - 0.7, h - (yy - y) - 0.4, max_size=19, min_size=13, gap=0.2)
