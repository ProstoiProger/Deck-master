from ..core import textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow


@layout("problem", "story", "State the problem in one sentence with one supporting number.", 55,
        accepts="first paragraph: the statement; props: stat `63% | of projects never ship`, mascot (character name); items: up to 3 evidence bullets",
        example="# Fraud alerts arrive 40 minutes late\nlayout: problem\nstat: 40 min | median alert delay\nsource: bank-brief.pdf p.3\nCustomers lose money before the alert fires.\n- 3 of 4 cases are card-not-present")
def problem(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lw = 6.9
    if s.paragraphs:
        c.fit_text(x, y + 0.05, lw, 1.7, s.paragraphs[0], 28, 18, "text", valign="top")
        y2 = y + 2.0
    else:
        y2 = y + 0.1
    flow(c, s.items[:3], x, y2, lw, CONTENT_BOTTOM - y2, max_size=20, min_size=14)
    rx, rw = x + lw + 0.5, w - lw - 0.5
    c.box(rx, y + 0.1, rw, h - 0.2, fill="surface")
    if s.prop("mascot"):
        c.avatar(s.prop("mascot"), rx + 0.25, y + 0.3, 0.85)
    if s.prop("stat"):
        stat = [p.strip() for p in s.prop("stat").split("|")] + ["", ""]
        scale = c.style["heading_scale"]
        size = textfit.fit_line(c.t, stat[0], "heading", rw - 0.6, 70 * scale, 16 * scale, True)
        top = 1.25 if s.prop("mascot") else 0.8  # leave room for the character in the card corner
        c.text(rx + 0.3, y + top, rw - 0.6, 1.6, stat[0], size, "accent", "heading", True, "center", "middle", 1.0)
        c.fit_text(rx + 0.4, y + top + 2.0, rw - 0.8, 1.2, stat[1], 20, 13, "muted", align="center")
    else:
        c.badge(rx + rw / 2, y + h / 2, 0.8, "!", "danger", 44)


@layout("solution", "story", "Show the solution in one line, three benefits and a product visual.", 60,
        accepts="first paragraph: the one-line solution; items: up to 3 benefits; image: product picture",
        example="# Stream scoring cuts alert delay to 2 s\nlayout: solution\nimage: assets/ui.png\nA streaming model scores each card swipe on arrival.\n- 2 s median latency\n- Explains every alert\n- Runs on one GPU")
def solution(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lw = 6.0
    if s.paragraphs:
        c.fit_text(x, y + 0.05, lw, 1.5, s.paragraphs[0], 24, 16, "text")
        y += 1.7
    items = s.items[:3]
    rh = min(1.0, (CONTENT_BOTTOM - y) / max(len(items), 1) - 0.12)
    for i, it in enumerate(items):
        yy = y + i * (rh + 0.12)
        c.box(x, yy, lw, rh, fill="surface")
        c.badge(x + 0.45, yy + rh / 2, min(0.24, rh / 2 - 0.08), str(i + 1), "primary")
        c.fit_text(x + 0.9, yy + 0.04, lw - 1.0, rh - 0.08, it.text, 19, 12, valign="middle")
    vx, vw = x + lw + 0.5, w - lw - 0.5
    vy, vh = CONTENT_TOP + 0.1, CONTENT_BOTTOM - CONTENT_TOP - 0.1
    if s.image:
        c.image(vx, vy, vw, vh, s.image)
    else:
        c.box(vx, vy, vw, vh, fill="surface")
        c.rect(vx, vy, vw, 0.42, "bg", alpha=0.5)
        for k, col in enumerate(("danger", "warning", "success")):
            c.rect(vx + 0.2 + k * 0.28, vy + 0.13, 0.16, 0.16, col, kind="ellipse" if not c.pixel else "rect")
        for k in range(5):
            c.rect(vx + 0.4, vy + 0.9 + k * 0.55, (vw - 0.8) * (1 - 0.14 * k), 0.22, "primary" if k == 0 else "border",
                   kind="round", radius=0.05)


@layout("feature_grid", "story", "Grid of two to six capabilities, each with a short name and one line.", 70,
        accepts="items: `Name | one-line description`",
        example="# Four things the app does\nlayout: feature_grid\n- Live scoring | under 2 s per swipe\n- Reason codes | top 3 drivers\n- Case queue | ranked by loss\n- Audit log | every decision")
def feature_grid(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = len(items)
    cols = 3 if n > 4 or n == 3 else 2
    rows = (n + cols - 1) // cols
    gap = 0.3
    cw, ch = (w - gap * (cols - 1)) / cols, (h - 0.1 - gap * (rows - 1)) / rows
    for i, it in enumerate(items):
        r, k = divmod(i, cols)
        cx, cy = x + k * (cw + gap), y + 0.1 + r * (ch + gap)
        c.box(cx, cy, cw, ch, fill="surface")
        c.badge(cx + 0.55, cy + 0.55, 0.3, str(i + 1), "primary")
        name, desc = cells(it, 2)[:2]
        c.fit_text(cx + 1.0, cy + 0.22, cw - 1.2, 0.7, name, 21, 14, "text", "body", True, valign="middle")
        c.fit_text(cx + 0.3, cy + 1.05, cw - 0.6, ch - 1.2, desc, 17, 12, "muted")


@layout("impact", "story", "Two columns: what was achieved and what comes next; use for impact and next steps.", 60,
        accepts="groups: `## Achieved` and `## Next` each with bullets",
        example="# What we shipped and what is next\nlayout: impact\n## Achieved\n- Prototype scored 1M events\n## Next\n- Pilot with one bank branch")
def impact(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1]] or [("", s.items)]
    if len(groups) == 1 and len(groups[0][1]) > 3:
        half = (len(groups[0][1]) + 1) // 2
        groups = [("", groups[0][1][:half]), ("", groups[0][1][half:])]
    groups = groups[:2]
    cw = (w - 0.5) / len(groups)
    for i, (head, items) in enumerate(groups):
        cx = x + i * (cw + 0.5)
        c.box(cx, y + 0.1, cw, h - 0.2, fill="surface")
        mark = "success" if i == 0 else "accent"
        yy = y + 0.35
        if head:
            c.pill(cx + 0.3, yy, head.upper(), fill="bg", col=mark, size=12)
            yy += 0.65
        flow(c, items[:5], cx + 0.35, yy, cw - 0.7, CONTENT_BOTTOM - yy - 0.3, max_size=20, min_size=13, marker_col=mark)
