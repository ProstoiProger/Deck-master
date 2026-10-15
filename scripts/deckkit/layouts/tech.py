from ..core import textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow, layer_items


def _arrow_down(c, cx, y, col="muted"):
    c.line(cx - 0.12, y, cx, y + 0.12, col, 1.5)
    c.line(cx + 0.12, y, cx, y + 0.12, col, 1.5)
    c.line(cx, y - 0.1, cx, y + 0.12, col, 1.5)


@layout("architecture", "tech", "Layered system diagram; the key component is highlighted in the accent color.", 60,
        accepts="items: `Layer: component, component`; wrap the key component in **bold**",
        example="# Events flow through three layers\nlayout: architecture\n- Client: Mobile app, Web\n- API: Gateway, **Scoring service**\n- Data: Kafka, Feature store")
def architecture(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = layer_items(s.items[:5])
    n = max(len(rows), 1)
    gap = 0.34
    rh = min(1.0, (h - 0.1 - gap * (n - 1)) / n)
    lw = 2.2
    for i, (layer, comps) in enumerate(rows):
        yy = y + 0.1 + i * (rh + gap)
        c.box(x, yy, lw, rh, fill="surface")
        c.fit_text(x + 0.15, yy, lw - 0.3, rh, layer, 17, 11, "muted", "mono", True, valign="middle")
        k = max(len(comps), 1)
        cg = 0.25
        cw = (w - lw - 0.3 - cg * (k - 1)) / k
        for j, comp in enumerate(comps):
            key = comp.startswith("**") and comp.endswith("**")
            name = comp.strip("*")
            cx = x + lw + 0.3 + j * (cw + cg)
            c.box(cx, yy, cw, rh, fill="primary" if key else "surface", line="accent" if key else "border")
            c.fit_text(cx + 0.12, yy, cw - 0.24, rh, name, 19, 11, c.t.on("primary") if key else "text", "body", key,
                       "center", "middle")
        if i < len(rows) - 1:
            _arrow_down(c, x + lw / 2, yy + rh + 0.07)


@layout("pipeline", "tech", "Left-to-right pipeline of two to six numbered stages, each with a short caption.", 55,
        accepts="items: `Stage | caption`; first paragraph: one-line takeaway under the flow",
        example="# From raw logs to a ranked case list\nlayout: pipeline\n- Ingest | Kafka, 5k events/s\n- Features | 42 rolling windows\n- Score | LightGBM\n- Review | ranked queue")
def pipeline(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    gap = 0.45
    bw = (w - gap * (n - 1)) / n
    y += 0.35
    by, bh = y + 0.9, 1.4
    for i, it in enumerate(items):
        bx = x + i * (bw + gap)
        name, cap = cells(it, 2)[:2]
        c.badge(bx + 0.3, y + 0.45, 0.25, str(i + 1), "primary")
        c.box(bx, by, bw, bh, fill="surface", line="primary")
        c.fit_text(bx + 0.12, by, bw - 0.24, bh, name, 20, 12, "text", "body", True, "center", "middle")
        c.fit_text(bx, by + bh + 0.2, bw, 1.2, cap, 16, 11, "muted", align="center")
        if i < n - 1:
            ax = bx + bw + 0.06
            c.line(ax, by + bh / 2, ax + gap - 0.12, by + bh / 2, "accent", 2)
            c.line(ax + gap - 0.24, by + bh / 2 - 0.1, ax + gap - 0.12, by + bh / 2, "accent", 2)
            c.line(ax + gap - 0.24, by + bh / 2 + 0.1, ax + gap - 0.12, by + bh / 2, "accent", 2)
    if s.paragraphs:
        c.box(x, CONTENT_BOTTOM - 1.0, w, 0.9, fill="surface", line="accent")
        c.fit_text(x + 0.3, CONTENT_BOTTOM - 1.0, w - 0.6, 0.9, s.paragraphs[0], 20, 13, "text", valign="middle")


@layout("demo", "tech", "Screenshot in a browser frame with numbered callouts that walk through the demo.", 45,
        accepts="image: screenshot path (or `![](path)`); items: up to 4 callouts",
        example="# Demo: an alert becomes a decision in 3 clicks\nlayout: demo\nimage: assets/demo.png\n- Alert appears with top reasons\n- Analyst opens the case\n- Decision is logged")
def demo(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    fw = 7.5
    fy, fh = y + 0.1, h - 0.1
    c.box(x, fy, fw, fh, fill="surface")
    c.rect(x + 0.02, fy + 0.02, fw - 0.04, 0.4, "bg", alpha=0.6)
    for k, col in enumerate(("danger", "warning", "success")):
        c.rect(x + 0.22 + k * 0.28, fy + 0.13, 0.15, 0.15, col, kind="rect" if c.pixel else "ellipse")
    if s.image:
        c.image(x + 0.12, fy + 0.5, fw - 0.24, fh - 0.62, s.image)
    else:
        c.rect(x + 0.12, fy + 0.5, fw - 0.24, fh - 0.62, "bg", alpha=0.4)
        c.text(x + 0.12, fy + 0.5, fw - 0.24, fh - 0.62, "[demo screenshot]", 16, "muted", "mono", align="center", valign="middle")
        c.scene.problems.append("[Medium] demo layout has no image: add `image:` with a screenshot")
    cx, cw = x + fw + 0.5, w - fw - 0.5
    yy = fy + 0.1
    items = s.items[:4]
    rh = min(1.05, (fh - 0.1) / max(len(items), 1) - 0.12)
    for i, it in enumerate(items):
        c.badge(cx + 0.3, yy + rh / 2, 0.26, str(i + 1), "accent")
        c.fit_text(cx + 0.8, yy, cw - 0.8, rh, it.text, 19, 12, valign="middle")
        yy += rh + 0.12


@layout("tech_stack", "tech", "Technology tiles grouped by layer: language, framework, data, cloud.", 45,
        accepts="items: `Layer: Tech, Tech, Tech`",
        example="# Boring technology, on purpose\nlayout: tech_stack\n- Language: Python, SQL\n- ML: LightGBM, scikit-learn\n- Data: DuckDB, Parquet")
def tech_stack(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = layer_items(s.items[:5])
    n = max(len(rows), 1)
    gap = 0.2
    rh = min(0.9, (h - 0.1 - gap * (n - 1)) / n)
    for i, (layer, techs) in enumerate(rows):
        yy = y + 0.1 + i * (rh + gap)
        c.text(x, yy, 2.3, rh, layer.upper(), 14, "accent", "mono", True, valign="middle")
        cx = x + 2.5
        for tech in techs:
            tw = textfit.width_in(c.t, tech, "body", 18, True) + 0.6
            if cx + tw > x + w:
                break
            c.box(cx, yy + 0.08, tw, rh - 0.16, fill="surface")
            c.text(cx, yy + 0.08, tw, rh - 0.16, tech, 18, "text", "body", True, "center", "middle")
            cx += tw + 0.2


@layout("roadmap", "tech", "Horizontal timeline of two to six phases: now, next, later.", 55,
        accepts="items: `Phase | milestone | detail`; the first phase is highlighted as current",
        example="# Three steps to a pilot\nlayout: roadmap\n- Now | Prototype | scored 1M events\n- Q1 | Pilot | one branch\n- Q3 | Rollout | all branches")
def roadmap(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    ly = y + 1.3
    c.rect(x, ly - 0.03, w, 0.06, "border")
    step = w / n
    for i, it in enumerate(items):
        phase, name, detail = cells(it, 3)[:3]
        cx = x + step * i + step / 2
        c.badge(cx, ly, 0.2, "", "success" if i == 0 else "primary")
        c.text(cx - step / 2, ly - 0.95, step, 0.5, phase, 16, "accent", "mono", True, "center", "middle")
        bw = step - 0.25
        c.box(cx - bw / 2, ly + 0.5, bw, 2.1, fill="surface", line="primary" if i == 0 else "border")
        c.fit_text(cx - bw / 2 + 0.15, ly + 0.7, bw - 0.3, 0.8, name, 22, 13, "text", "body", True, "center", "top")
        c.fit_text(cx - bw / 2 + 0.2, ly + 1.45, bw - 0.4, 1.0, detail, 16, 11, "muted", align="center")
