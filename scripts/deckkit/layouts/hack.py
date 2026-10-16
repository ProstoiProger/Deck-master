"""Hackathon and datathon layouts: data schema, model card, insight cards."""
from ..core import color, textfit
from ..core.canvas import MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow


@layout("schema", "data", "Data dictionary: up to four tables as cards listing their columns, types and keys, with the relations underneath.", 80,
        accepts="groups: one `## table` per card; bullets `column | type | note` (note containing key marks the column); props: relations (one line)",
        example="# Four tables hold everything the model reads\nlayout: schema\nrelations: orders.user_id -> users.id, events.order_id -> orders.id\n## users\n- id | int | primary key\n- country | text\n- joined_at | date\n"
                "## orders\n- id | int | primary key\n- user_id | int | foreign key\n- amount | float\n## events\n- id | int | primary key\n- order_id | int | foreign key\n- kind | text")
def schema(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1] or g[0]][:4]
    n = max(len(groups), 1)
    rel = s.prop("relations")
    foot = 0.6 if rel else 0
    gap = 0.3
    cw = (w - gap * (n - 1)) / n
    top, ch = y + 0.1, h - 0.1 - foot
    for i, (head, items) in enumerate(groups):
        cx = x + i * (cw + gap)
        c.box(cx, top, cw, ch, fill="surface", shadow=False, radius=min(c.style["radius"], 0.1))
        c.rect(cx, top, cw, 0.55, "primary")
        c.fit_text(cx + 0.2, top, cw - 0.4, 0.55, head, 18, 11, c.t.on("primary"), "mono", True, valign="middle")
        rows = items[:8]
        rh = min(0.5, (ch - 0.7) / max(len(rows), 1))
        for k, it in enumerate(rows):
            col, typ, note = cells(it, 3)[:3]
            ry = top + 0.65 + k * rh
            if "key" in note.lower():
                c.rect(cx + 0.14, ry + rh / 2 - 0.07, 0.14, 0.14, "accent", kind="rect" if c.style["corner"] == "square" else "round", radius=0.03)
            c.fit_text(cx + 0.4, ry, cw * 0.5 - 0.3, rh, col, 15, 11, "text", "mono", True, valign="middle")
            c.fit_text(cx + cw * 0.5, ry, cw * 0.5 - 0.25, rh, typ, 13, 11, "muted", "mono", False, "right", "middle")
        if i < n - 1:
            c.line(cx + cw, top + 0.28, cx + cw + gap, top + 0.28, c.t.c("accent"), 2.0)
    if rel:
        c.fit_text(x, y + h - foot + 0.1, w, foot - 0.1, rel, 15, 11, "muted", "mono", False, valign="middle")


@layout("model_card", "data", "Model card: key facts about the model and data, its headline metrics as tiles, and its known limits.", 110,
        accepts="groups: `## Facts` (`Label | value` rows), `## Metrics` (`name | value | note`, up to four), `## Limits` (bullets); set `source:` for the metrics",
        example="# The model is accurate on holdout and weak on new merchants\nlayout: model_card\nsource: runs/log.jsonl#champion\n## Facts\n- Task | Fraud probability per payment\n- Model | Gradient boosting, 400 trees\n- Data | 2.1 M payments, 12 weeks\n- Split | Time-ordered holdout\n"
                "## Metrics\n- PR-AUC | 0.74 | holdout\n- Recall at 1% | 0.61 | holdout\n- Latency | 38 ms | p95\n## Limits\n- Drops on merchants with under 30 payments\n- Not tested outside the card market")
def model_card(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    by = {k.strip().lower(): v for k, v in s.groups}
    facts, metrics, limits = by.get("facts", []), by.get("metrics", []), by.get("limits", [])
    lw, gap = 4.5, 0.3
    top, ch = y + 0.1, h - 0.1
    c.box(x, top, lw, ch, fill="surface")
    c.pill(x + 0.3, top + 0.25, "WHAT IT IS", fill="bg", col="accent", size=11)
    rows = [cells(i, 2)[:2] for i in facts[:6]]
    rh = min(0.7, (ch - 0.95) / max(len(rows), 1))
    for k, (label, value) in enumerate(rows):
        ry = top + 0.85 + k * rh
        c.text(x + 0.3, ry, 1.2, rh, label.upper(), 11, "muted", "mono", True, valign="middle", chrome=True)
        c.fit_text(x + 1.55, ry, lw - 1.8, rh, value, 16, 11, "text", valign="middle")
    rx, rw = x + lw + gap, w - lw - gap
    tiles = [cells(i, 3)[:3] for i in metrics[:4]]
    nt = max(len(tiles), 1)
    tw = (rw - 0.25 * (nt - 1)) / nt
    th = 2.2
    for k, (name, value, note) in enumerate(tiles):
        tx = rx + k * (tw + 0.25)
        c.box(tx, top, tw, th, fill="surface", line="primary" if k == 0 else "border")
        c.fit_text(tx + 0.2, top + 0.15, tw - 0.4, 0.4, name, 14, 11, "muted", "body", True, "center", "middle")
        size = textfit.fit_line(c.t, value, "heading", tw - 0.4, 48 * c.style["heading_scale"], 18, True)
        c.text(tx + 0.2, top + 0.6, tw - 0.4, 1.0, value, size, "accent", "heading", True, "center", "middle", 1.0)
        c.fit_text(tx + 0.2, top + 1.65, tw - 0.4, 0.45, note, 13, 11, "muted", align="center")
    ly = top + th + 0.25
    c.box(rx, ly, rw, ch - th - 0.25, fill="surface", line="warning")
    c.pill(rx + 0.3, ly + 0.2, "KNOWN LIMITS", fill="bg", col="warning", size=11)
    flow(c, limits[:4], rx + 0.3, ly + 0.75, rw - 0.6, ch - th - 0.25 - 0.9, max_size=18, min_size=12, gap=0.12, marker_col="warning")


@layout("insight_cards", "data", "Three or four findings, each as a headline, its evidence number and the action it leads to.", 80,
        accepts="items: `Finding | evidence number | evidence caption | action` (up to four); set `source:` for the numbers",
        example="# Three findings explain most of the churn\nlayout: insight_cards\nsource: analysis/churn.ipynb\n- Late onboarding hurts | 2.4x | churn when setup takes over 3 days | Offer a guided setup\n"
                "- Weekend users stay | 61% | still active after 90 days | Send weekend prompts\n- Price is not the driver | 4% | of cancellations cite price | Keep the price")
def insight_cards(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = [cells(i, 4)[:4] for i in s.items[:4]]
    n = max(len(items), 1)
    gap = 0.3
    cw = (w - gap * (n - 1)) / n
    top, ch = y + 0.1, h - 0.1
    ah = 1.0
    for k, (finding, num, cap, action) in enumerate(items):
        cx = x + k * (cw + gap)
        c.box(cx, top, cw, ch, fill="surface", line="primary" if k == 0 else "border")
        c.text(cx + 0.25, top + 0.2, cw - 0.5, 0.3, f"FINDING {k + 1}", 11, "muted", "mono", True, chrome=True)
        c.fit_text(cx + 0.25, top + 0.55, cw - 0.5, 1.1, finding, 20, 13, "text", "heading", True)
        size = textfit.fit_line(c.t, num, "heading", cw - 0.5, 60 * c.style["heading_scale"], 18, True)
        c.text(cx + 0.25, top + 1.75, cw - 0.5, 1.0, num, size, "accent", "heading", True, "left", "middle", 1.0)
        c.fit_text(cx + 0.25, top + 2.8, cw - 0.5, ch - 2.8 - ah - 0.1, cap, 15, 11, "muted")
        c.rect(cx, top + ch - ah, cw, ah, "primary")
        on = c.t.on("primary")
        c.text(cx + 0.25, top + ch - ah + 0.08, cw - 0.5, 0.28, "DO", 11, on, "mono", True, chrome=True)
        c.fit_text(cx + 0.25, top + ch - ah + 0.36, cw - 0.5, ah - 0.42, action, 16, 11, on, "body", True)
