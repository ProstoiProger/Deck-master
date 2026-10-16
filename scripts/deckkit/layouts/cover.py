"""Opening and statement layouts beyond `title`: a poster cover, a split cover and a big highlighted statement."""
from ..core import textfit
from ..core.canvas import MARGIN
from ..core.layout import layout
from ..core.scene import H, W
from ._util import cells

# backdrops that leave the middle of the slide free, so an oversized title can run across the full width
WIDE_OK = ("mesh", "blueprint", "dots", "grid", "rules", "clean", "none")
# backdrops with a picture or globe on the right: keep the poster title to the left two thirds
NARROW_OK = ("hud", "orbs3d")


def _meta_line(c, s):
    meta = c.deck.meta
    return [str(v) for v in (s.prop("team") or meta.get("team", ""), s.prop("date") or str(meta.get("date", ""))) if v]


@layout("cover_poster", "frame", "Poster-style opening: an oversized title across the whole slide with small meta lines; for hackathons, events and bold decks.", 30,
        accepts="props: eyebrow, subtitle, team, date; the title can be long, it is sized to fill the width",
        example="# Build it in a weekend, ship it on Monday\nlayout: cover_poster\neyebrow: Hack the Campus 2026\nsubtitle: Team Atlas, track: AI for education\nteam: Team Atlas\ndate: 2026-10-24")
def cover_poster(c, s):
    meta = c.deck.meta
    pat = c.style["pattern"]
    tw = 7.9 if pat in NARROW_OK else W - 2 * MARGIN
    if pat in WIDE_OK or pat in NARROW_OK:
        c.backdrop()
    else:  # side decorations would run into a title this wide: keep the theme's rule and color only
        c.has_backdrop = True
        c.rect(MARGIN, 0.72, 0.9, 0.07, "accent")
    eyebrow = s.prop("eyebrow") or str(meta.get("event", "")).replace("-", " ")
    if eyebrow:
        c.pill(MARGIN, 0.95, eyebrow.upper(), fill="surface", col="accent", size=12)
    scale, lh = c.style["heading_scale"], c.style["heading_line_h"]
    size, _, _ = textfit.fit(c.t, s.title, "heading", tw, 3.7, 92 * scale, 30 * scale, True, lh)
    c.text(MARGIN, 1.65, tw, 3.7, s.title, size, "text", "heading", True, "left", "top", lh)
    sub = s.prop("subtitle") or (s.paragraphs[0] if s.paragraphs else "") or meta.get("subtitle", "")
    if sub:
        c.fit_text(MARGIN, 5.35, min(9.2, tw), 0.7, sub, 22, 14, "muted")
    x = MARGIN
    for label in _meta_line(c, s):
        x += c.pill(x, 6.1, label, fill="surface", col="text", size=13) + 0.2


@layout("cover_split", "frame", "Split opening: the title on a solid color panel on the left, subtitle and meta on the right; optional picture on the right.", 35,
        accepts="props: eyebrow, subtitle, team, date, image (a picture filling the right side)",
        example="# Fraud alerts ranked by expected loss\nlayout: cover_split\neyebrow: Fintech Hack 2026\nsubtitle: A queue that puts the costliest alert first\nteam: Team Atlas\ndate: 2026-10-24")
def cover_split(c, s):
    meta = c.deck.meta
    c.has_backdrop = True
    pw = 6.1
    c.rect(0, 0, pw, H, "primary")
    on = c.t.on("primary")
    eyebrow = s.prop("eyebrow") or str(meta.get("event", "")).replace("-", " ")
    if eyebrow:
        c.text(MARGIN, 0.8, pw - 2 * MARGIN, 0.35, eyebrow.upper(), 12, on, "mono", True, chrome=True)
    scale, lh = c.style["heading_scale"], c.style["heading_line_h"]
    size, _, _ = textfit.fit(c.t, s.title, "heading", pw - 1.3, 4.2, 54 * scale, 24 * scale, True, lh)
    c.text(MARGIN, 1.6, pw - 1.3, 4.2, s.title, size, on, "heading", True, "left", "top", lh)
    c.rect(MARGIN, 6.35, 0.9, 0.07, on)
    rx = pw + 0.7
    if s.image:
        c.image(pw, 0, W - pw, H, s.image, "cover picture")
        return
    sub = s.prop("subtitle") or (s.paragraphs[0] if s.paragraphs else "") or meta.get("subtitle", "")
    if sub:
        c.fit_text(rx, 2.0, W - rx - MARGIN, 2.6, sub, 30, 16, "text", "heading", True)
    c.accent_rule(rx, 4.9, 1.0)
    y = 5.2
    for label in _meta_line(c, s):
        c.text(rx, y, W - rx - MARGIN, 0.4, label, 18, "muted", "body", False, valign="middle")
        y += 0.5


@layout("statement", "frame", "One big sentence with its key figure or phrase blown up in the accent color; for the problem, a surprising fact or a thesis.", 30,
        accepts="items: one line `lead-in | key figure or phrase | continuation`; the title is the small kicker above; set `source:` when the key is a number",
        example="# The cost of meetings\nlayout: statement\nsource: survey/2026-q2.csv\n- Teams spend | 31 hours | in unproductive meetings every month")
def statement(c, s):
    c.text(MARGIN, 0.6, W - 2 * MARGIN, 0.45, s.title.upper(), 14, "muted", "mono", True, chrome=True)
    parts = cells(s.items[0], 3) if s.items else [s.paragraphs[0] if s.paragraphs else "", "", ""]
    lead, key, tail = (p.strip() for p in parts[:3])
    scale = c.style["heading_scale"]
    c.rect(MARGIN, 1.35, 0.9, 0.07, "accent")
    c.fit_text(MARGIN, 1.65, W - 2 * MARGIN, 1.0, lead, 36, 18, "text", "body", False, valign="bottom")
    size = textfit.fit_line(c.t, key, "heading", W - 2 * MARGIN, 140 * scale, 36, True)
    c.text(MARGIN, 2.7, W - 2 * MARGIN, 2.3, key, size, "accent", "heading", True, "left", "middle", 1.0)
    c.fit_text(MARGIN, 5.1, W - 2 * MARGIN, 1.3, tail, 36, 18, "text", "body", False)
