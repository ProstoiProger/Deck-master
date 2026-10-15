from ..core import entities, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import H, W
from ._util import cells, flow


@layout("title", "frame", "Opening slide: project name, one-line value proposition, event and team.", 40,
        accepts="props: eyebrow, subtitle, team, date, mascot (character name, game themes); first paragraph is the subtitle",
        example="# Team Atlas: fraud alerts in 2 seconds\nlayout: title\nsubtitle: Streaming anomaly detection for card payments\nteam: Atlas | Hackathon 2026")
def title_slide(c, s):
    mascot = s.prop("mascot")
    c.backdrop(portal=not mascot)
    meta = c.deck.meta
    eyebrow = s.prop("eyebrow") or str(meta.get("event", "")).replace("-", " ")
    if eyebrow:
        c.pill(MARGIN, 1.55, eyebrow.upper(), fill="surface", col="accent", size=12)
    scale = c.style["heading_scale"]
    lh = c.style["heading_line_h"]
    size, _, _ = textfit.fit(c.t, s.title, "heading", 7.6, 2.4, 52 * scale, 24 * scale, True, lh)
    c.text(MARGIN, 2.2, 7.6, 2.4, s.title, size, "text", "heading", True, "left", "top", lh)
    c.accent_rule(MARGIN, 4.75, 1.2)
    sub = s.prop("subtitle") or (s.paragraphs[0] if s.paragraphs else "") or meta.get("subtitle", "")
    if sub:
        c.fit_text(MARGIN, 4.95, 7.4, 1.0, sub, 22, 14, "muted")
    x = MARGIN
    for label in (s.prop("team") or meta.get("team", ""), s.prop("date") or str(meta.get("date", ""))):
        if label:
            x += c.pill(x, 6.2, str(label), fill="surface", col="text", size=13) + 0.2
    if mascot:
        c.mascot(mascot)


@layout("agenda", "frame", "Three to seven numbered steps: what the talk covers or how the work was structured.", 45,
        accepts="items: one per step, optional `Step | detail`; in game themes `Step | creeper` shows that character in the hotbar slot",
        example="# What we will cover\nlayout: agenda\n- Problem | who loses and how much\n- Solution\n- Demo")
def agenda(c, s):
    c.title()
    c.accent_rule()
    items = s.items[:9]
    n = len(items)
    if c.style["metaphor"] == "game":
        gap = 0.18
        slot = min(1.3, (W - 2 * MARGIN - gap * (n - 1)) / max(n, 1))
        y = 2.7
        for i, it in enumerate(items):
            x = MARGIN + i * (slot + gap)
            parts = cells(it, 2)
            if parts[1] and entities.known(parts[1]):  # `Problem | creeper` puts the character in the slot
                c.avatar(parts[1], x, y, slot)
            else:
                c.box(x, y, slot, slot, fill="primary" if i == 0 else "surface")
                c.text(x, y, slot, slot, str(i + 1), 28, c.t.on("primary") if i == 0 else "text", "heading", True, "center", "middle")
            label = parts[0]
            c.fit_text(x - gap / 2, y + slot + 0.2, slot + gap, 1.3, label, 15, 11, "text", align="center")
        return
    two = n > 4
    cols = 2 if two else 1
    per = (n + cols - 1) // cols
    cw = (W - 2 * MARGIN - 0.4) / cols
    rh = min(0.95, (CONTENT_BOTTOM - CONTENT_TOP) / max(per, 1) - 0.14)
    for i, it in enumerate(items):
        col, row = divmod(i, per)
        x, y = MARGIN + col * (cw + 0.4), CONTENT_TOP + 0.1 + row * (rh + 0.14)
        c.box(x, y, cw, rh, fill="surface")
        c.badge(x + 0.5, y + rh / 2, min(0.26, rh / 2 - 0.08), str(i + 1), "primary")
        name, detail = cells(it, 2)[:2]
        if detail:
            c.fit_text(x + 0.95, y + 0.08, cw - 1.1, rh * 0.5, name, 20, 12, "text", "body", True, valign="middle")
            c.fit_text(x + 0.95, y + rh * 0.5, cw - 1.1, rh * 0.42, detail, 15, 11, "muted", valign="top")
        else:
            c.fit_text(x + 0.95, y + 0.04, cw - 1.1, rh - 0.08, name, 20, 12, "text", "body", True, valign="middle")


@layout("bullets", "content", "Plain titled bullet list with an optional image; the safe fallback layout.", 70,
        accepts="items: bullets; first paragraph becomes a lede; image: picture on the right; or a fenced code block shown in mono on the right",
        example="# One idea, three supports\n- First point\n- Second point\n- Third point")
def bullets(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    has_side = bool(s.image or s.code)
    tw = w * (0.5 if s.code and s.items else 0.56) if has_side else w
    if not s.items and s.code:
        tw = 0
    top, full_h = y, h
    if s.paragraphs:
        c.fit_text(x, y, tw or w, 0.9, s.paragraphs[0], 22, 14, "muted")
        y += 1.0
        h -= 1.0
    if s.items:
        flow(c, s.items[:7], x, y + 0.1, tw or w, h - 0.1, max_size=24, min_size=14)
    if s.code:
        cx = x + tw + (0.4 if tw else 0)
        cw = w - tw - (0.4 if tw else 0)
        c.box(cx, top + 0.1, cw, full_h - 0.1, fill="surface")
        c.code_block(cx + 0.3, top + 0.35, cw - 0.6, full_h - 0.6, s.code)
    elif s.image:
        c.image(x + tw + 0.4, top + 0.1, w - tw - 0.4, full_h - 0.1, s.image)


@layout("closing", "frame", "Closing slide: thanks or questions, where to find the code and the team.", 25,
        accepts="items or paragraphs: contact lines, repo link; props mascot (character name) and achievement (toast text), game themes",
        example="# Questions?\nlayout: closing\n- github.com/team/project\n- team@example.org")
def closing(c, s):
    mascot = s.prop("mascot")
    c.backdrop(portal=not mascot)
    scale = c.style["heading_scale"]
    lh = c.style["heading_line_h"]
    size, _, _ = textfit.fit(c.t, s.title, "heading", 7.8, 1.8, 60 * scale, 28 * scale, True, lh)
    c.text(MARGIN, 2.3, 7.8, 1.8, s.title, size, "text", "heading", True, "left", "top", lh)
    c.accent_rule(MARGIN, 4.3, 1.2)
    lines = [i.text for i in s.items] + s.paragraphs
    y = 4.65
    for ln in lines[:4]:
        w = c.pill(MARGIN, y, ln, fill="surface", col="text", size=14, h=0.42, role="body", bold=False)
        y += 0.56
    if mascot:
        c.mascot(mascot)
    if c.game and s.prop("achievement"):  # advancement toast: trophy, banner, text
        c.box(MARGIN, 0.7, 6.6, 0.95, fill="surface")
        c.icon("trophy", MARGIN + 0.25, 0.9, 0.5)
        c.text(MARGIN + 1.05, 0.78, 5.4, 0.3, "ADVANCEMENT MADE!", 11, "accent", "mono", True, chrome=True)
        c.fit_text(MARGIN + 1.05, 1.08, 5.4, 0.5, s.prop("achievement"), 18, 11, "text", "body", True, valign="middle")
    if c.style["metaphor"] == "game":
        c.text(MARGIN, 6.35, 8, 0.3, "> PRESS START TO CONTINUE_", 12, "accent", "mono", True, chrome=True)
