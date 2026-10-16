"""Portfolio components: case header, gallery, before and after, profile, skills, timeline."""
import re

from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import H, W
from ._util import cells, flow, number


_num = number


@layout("case_header", "portfolio", "Case study opener: project name, role, year, client and tools beside a large image.", 60,
        accepts="image: hero picture; props: role, year, client, tools (comma list); first paragraph: one-sentence summary; the title is the project name",
        example="# Atlas: a fraud console for analysts\nlayout: case_header\nimage: work/atlas.png\nrole: Lead designer\nyear: 2026\nclient: Northbank\ntools: Figma, React, Python\nA queue that ranks alerts by expected loss.")
def case_header(c, s):
    x0 = MARGIN
    meta = " / ".join(p for p in (s.prop("client"), s.prop("year")) if p)
    if meta:
        c.pill(x0, 0.75, meta.upper(), fill="surface", col="accent", size=12)
    scale = c.style["heading_scale"]
    c.fit_text(x0, 1.3, 5.7, 2.4, s.title, 44 * scale, 22 * scale, "text", "heading", True, line_h=c.style["heading_line_h"])
    if s.paragraphs:
        c.fit_text(x0, 3.8, 5.5, 1.3, s.paragraphs[0], 20, 14, "muted")
    if s.prop("role"):
        c.text(x0, 5.25, 2.0, 0.3, "ROLE", 11, "accent", "body", True, chrome=True)
        c.fit_text(x0, 5.55, 5.5, 0.4, s.prop("role"), 18, 12, "text", "body", True)
    tools = [t.strip() for t in s.prop("tools").split(",") if t.strip()]
    tx = x0
    for t in tools[:6]:
        tx += c.pill(tx, 6.15, t, fill="surface", col="text", size=12, h=0.38, role="body", bold=False) + 0.12
    c.box(6.8, 0.6, W - 6.8 - MARGIN, H - 1.2, fill="surface", shadow=False)
    c.image(6.9, 0.7, W - 6.8 - MARGIN - 0.2, H - 1.4, s.image, "project image")


@layout("gallery", "portfolio", "Image grid with a caption under each picture: two to six works or screens.", 40,
        accepts="items: `image path | caption` (2 to 6); the grid is 2 columns for 2 or 4 images, otherwise 3",
        example="# Four screens, one flow\nlayout: gallery\n- work/s1.png | Onboarding\n- work/s2.png | Queue\n- work/s3.png | Case view\n- work/s4.png | Report")
def gallery(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    cols = 2 if n in (2, 4) else 3
    rows = (n + cols - 1) // cols
    gap = 0.3
    cw = (w - gap * (cols - 1)) / cols
    rh = (h - 0.1 - gap * (rows - 1)) / rows
    for k, it in enumerate(items):
        path, cap = cells(it, 2)[:2]
        r, col = divmod(k, cols)
        cx, cy = x + col * (cw + gap), y + 0.1 + r * (rh + gap)
        ih = rh - (0.45 if cap else 0)
        c.box(cx, cy, cw, ih, fill="surface", shadow=False, radius=0.06)
        c.image(cx + 0.06, cy + 0.06, cw - 0.12, ih - 0.12, path, "work")
        if cap:
            c.fit_text(cx, cy + ih + 0.05, cw, 0.35, cap, 15, 11, "muted")


@layout("before_after", "portfolio", "Two images side by side with BEFORE and AFTER labels; for redesigns and improvements.", 30,
        accepts="items: `image path | label` (two); first paragraph: caption",
        example="# The redesign cut clicks in half\nlayout: before_after\n- work/old.png | Before\n- work/new.png | After\nThe same task, six clicks down to three.")
def before_after(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = (s.items + [None, None])[:2]
    cap = 0.6 if s.paragraphs else 0
    pw = (w - 0.9) / 2
    ph = h - 0.1 - cap
    for k, it in enumerate(items):
        path, label = cells(it, 2)[:2] if it else ("", "")
        px = x + k * (pw + 0.9)
        c.box(px, y + 0.1, pw, ph, fill="surface", shadow=False, radius=0.06)
        c.image(px + 0.06, y + 0.16, pw - 0.12, ph - 0.12, path, "image")
        c.rect(px + 0.2, y + 0.3, 1.5, 0.36, "accent" if k else "primary")
        c.text(px + 0.2, y + 0.3, 1.5, 0.36, (label or ("After" if k else "Before")).upper(), 12, c.t.on("accent" if k else "primary"), "body", True, "center", "middle", chrome=True)
    mx = x + pw + 0.45
    c.rect(mx - 0.02, y + 0.1, 0.04, ph, "accent")
    c.rect(mx - 0.3, y + ph / 2 - 0.3 + 0.1, 0.6, 0.6, "accent", kind="ellipse")
    c.arrow(mx - 0.17, y + ph / 2 - 0.12 + 0.1, 0.34, 0.24, c.t.on("accent"), head=0.12)
    if cap:
        c.fit_text(x, y + h - cap, w, cap, s.paragraphs[0], 18, 12, "text", valign="middle")


@layout("profile", "portfolio", "About me: portrait, a short bio, facts and contact lines.", 70,
        accepts="image: portrait; first paragraph: bio; items: `Label | value` facts (up to 5); props: email, web",
        example="# Hi, I design data products\nlayout: profile\nimage: me.jpg\nemail: aigerim@example.org\nweb: aigerim.example.org\nI turn messy data into tools people use daily.\n- Role | Product designer\n- Based in | Astana\n- Experience | 6 years")
def profile(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    c.box(x, y + 0.1, 3.7, 3.7, fill="surface", shadow=False, radius=0.06)
    c.image(x + 0.06, y + 0.16, 3.58, 3.58, s.image, "portrait")
    rx = x + 4.2
    rw = w - 4.2
    if s.paragraphs:
        c.fit_text(rx, y + 0.1, rw, 1.5, s.paragraphs[0], 24, 15, "text", "heading", True)
    items = s.items[:5]
    for k, it in enumerate(items):
        label, value = cells(it, 2)[:2]
        ry = y + 1.85 + k * 0.5
        c.rect(rx, ry, rw, 0.012, color.mix(c.t.c("bg"), c.t.c("text"), 0.2))
        c.text(rx, ry + 0.05, 2.0, 0.42, label.upper(), 12, "accent", "body", True, valign="middle", chrome=True)
        c.fit_text(rx + 2.1, ry + 0.05, rw - 2.1, 0.42, value, 18, 12, "text", valign="middle")
    contact = " / ".join(p for p in (s.prop("email"), s.prop("web")) if p)
    if contact:
        c.fit_text(x, y + h - 0.5, w, 0.45, contact, 18, 12, "accent", "body", True, valign="middle")


@layout("skills", "portfolio", "Skills as bars (with a level) or as chips under group headings.", 60,
        accepts="items: `Skill | level 1-5 or 0-100 | group` shown as bars (the level is never printed); or groups `## heading` with plain skill names as chips",
        example="# What I work with\nlayout: skills\n## Design\n- Figma\n- Prototyping\n## Code\n- Python\n- React")
def skills(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    leveled = [it for it in s.items if len(it.cells) >= 2 and _num(it.cells[1]) is not None]
    if leveled:
        items = leveled[:10]
        cols = 2 if len(items) > 5 else 1
        per = (len(items) + cols - 1) // cols
        cw = (w - 0.6) / cols
        rh = min(0.8, (h - 0.1) / per)
        for k, it in enumerate(items):
            name, level = cells(it, 2)[:2]
            lv = _num(level)
            frac = lv / 5 if lv <= 5 else lv / 100
            col, r = divmod(k, per)
            cx, cy = x + col * (cw + 0.6), y + 0.1 + r * rh
            c.fit_text(cx, cy, cw, 0.38, name, 18, 12, "text", "body", True, valign="middle")
            c.rect(cx, cy + 0.42, cw, 0.14, color.mix(c.t.c("bg"), c.t.c("text"), 0.14))
            c.rect(cx, cy + 0.42, cw * min(frac, 1), 0.14, "accent")
        return
    groups = [g for g in s.groups if g[1]] or [("", s.items)]
    gh = (h - 0.1) / max(len(groups[:4]), 1)
    for gi, (head, items) in enumerate(groups[:4]):
        gy = y + 0.1 + gi * gh
        c.text(x, gy, 2.6, 0.4, head.upper(), 13, "accent", "body", True, valign="middle", chrome=True)
        cx, cy = x + 2.8, gy
        for it in items[:12]:
            tw = textfit.width_in(c.t, it.text, "body", 17, False) + 0.5
            if cx + tw > x + w:
                cx, cy = x + 2.8, cy + 0.6
            c.rect(cx, cy, tw, 0.46, "surface", line="border", kind="round" if c.style["corner"] != "square" else "rect", radius=0.23)
            c.text(cx, cy, tw, 0.46, it.text, 17, "text", "body", False, "center", "middle")
            cx += tw + 0.18


@layout("timeline", "portfolio", "Vertical timeline for a career, a project history or a study path: when, what, detail.", 80,
        accepts="items: `When | What | detail` (up to 6)",
        example="# Six years from analyst to lead\nlayout: timeline\n- 2020 | Data analyst | Retail analytics\n- 2022 | Product designer | Fintech app\n- 2025 | Design lead | Team of five")
def timeline(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    rh = (h - 0.2) / n
    lx = x + 2.4
    c.rect(lx - 0.015, y + 0.2, 0.03, rh * (n - 1) + 0.2, color.mix(c.t.c("bg"), c.t.c("text"), 0.3))
    for k, it in enumerate(items):
        when, what, detail = cells(it, 3)[:3]
        cy = y + 0.2 + k * rh
        c.fit_text(x, cy - 0.12, 2.1, 0.5, when, 20, 12, "accent", "heading", True, "right", "middle")
        c.rect(lx - 0.13, cy, 0.26, 0.26, "accent" if k == 0 else "primary", kind="ellipse" if c.style["corner"] != "square" else "rect")
        c.fit_text(lx + 0.4, cy - 0.12, w - 2.9, 0.5, what, 21, 13, "text", "heading", True, valign="middle")
        if detail:
            c.fit_text(lx + 0.4, cy + 0.36, w - 2.9, rh - 0.6, detail, 16, 11, "muted")
