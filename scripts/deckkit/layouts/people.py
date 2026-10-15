from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ._util import cells, initials


@layout("team", "people", "Up to six team members with role and one memorable fact.", 50,
        accepts="items: `Name | Role | one fact | character` (character is optional: steve, alex, creeper, villager ...)",
        example="# Four people, one weekend\nlayout: team\n- Aigerim S. | ML engineer | ex-Kaggle grandmaster\n- Dana K. | Backend | built the stream layer")
def team(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    cols = 4 if n == 4 else min(n, 3)
    rows = (n + cols - 1) // cols
    gap = 0.3
    cw, ch = (w - gap * (cols - 1)) / cols, min(2.9, (h - 0.1 - gap * (rows - 1)) / rows)
    for i, it in enumerate(items):
        r, k = divmod(i, cols)
        cx, cy = x + k * (cw + gap), y + 0.1 + r * (ch + gap)
        name, role, fact, entity = cells(it, 4)[:4]
        c.box(cx, cy, cw, ch, fill="surface")
        if entity:  # 4th cell: a character such as steve or creeper as the team member's avatar
            c.avatar(entity, cx + 0.3, cy + 0.3, 0.9, name)
        else:
            c.badge(cx + 0.7, cy + 0.7, 0.4, initials(name), ["primary", "secondary", "accent"][i % 3], 20)
        c.fit_text(cx + 1.3, cy + 0.3, cw - 1.45, 0.55, name, 20, 12, "text", "body", True, valign="middle")
        c.fit_text(cx + 1.3, cy + 0.82, cw - 1.45, 0.4, role, 14, 10, "accent", "mono", True)
        c.fit_text(cx + 0.3, cy + 1.45, cw - 0.6, ch - 1.55, fact, 16, 11, "muted")
