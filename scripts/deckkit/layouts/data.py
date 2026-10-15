import re

from ..core import textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow


@layout("kpi", "data", "Two to four headline numbers, each with a label and its context or baseline.", 50,
        accepts="items: `92% | F1 score | vs 81% baseline`; first paragraph: takeaway; set `source:` for the numbers",
        example="# The model beats the baseline by 11 points\nlayout: kpi\nsource: runs/log.jsonl#champion\n- 92% | F1 | vs 81% baseline\n- 2 s | latency | p95")
def kpi(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:4]
    n = max(len(items), 1)
    gap = 0.35
    cw = (w - gap * (n - 1)) / n
    ch = 3.4 if s.paragraphs else 4.0
    scale = c.style["heading_scale"]
    for i, it in enumerate(items):
        cx = x + i * (cw + gap)
        num, label, ctx = cells(it, 3)[:3]
        c.box(cx, y + 0.1, cw, ch, fill="surface", line="primary" if i == 0 else "border")
        size = textfit.fit_line(c.t, num, "heading", cw - 0.4, 64 * scale, 14 * scale, True)
        c.text(cx + 0.2, y + 0.35, cw - 0.4, 1.25, num, size, "accent", "heading", True, "center", "middle", 1.0)
        c.fit_text(cx + 0.2, y + 2.05, cw - 0.4, 0.75, label, 20, 13, "text", "body", True, "center", "top")
        c.fit_text(cx + 0.2, y + 2.85, cw - 0.4, 0.5 if ch < 3.8 else 0.7, ctx, 15, 11, "muted", align="center")
        m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*%", num.strip())
        if c.style["metaphor"] == "game" and m and float(m.group(1)) <= 100:
            bx, bw = cx + 0.3, cw - 0.6
            c.box(bx, y + 1.62, bw, 0.3, fill="bg", shadow=False)
            c.rect(bx + 0.08, y + 1.7, (bw - 0.16) * float(m.group(1)) / 100, 0.14, "success")
    if s.paragraphs:
        c.box(x, y + ch + 0.3, w, 1.0, fill="surface", line="accent")
        c.fit_text(x + 0.3, y + ch + 0.3, w - 0.6, 1.0, s.paragraphs[0], 20, 13, "text", valign="middle")


@layout("chart_insight", "data", "One chart on the left and the so-what on the right.", 50,
        accepts="chart: bar | hbar | line | scatter | confusion; table rows `| label | value |` as data, or image: ready chart; takeaway: prop or bullets",
        example="# Recall rises with every added feature family\nlayout: chart_insight\nchart: bar\nsource: runs/ablation.csv\ntakeaway: Time-window features add 6 points of recall.\n| Family | Recall |\n|---|---|\n| Base | 0.71 |\n| + windows | 0.77 |")
def chart_insight(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    cw = 7.6
    img = None
    if s.image:
        img = c.image(x, y + 0.1, cw, h - 0.1, s.image)
    elif s.table and s.prop("chart", "bar"):
        try:
            from ..charts.themed import render_chart
            path = render_chart(c.t, s.prop("chart", "bar"), s.table, cw, h - 0.1, c.deck, s.index, s.prop("ylabel"))
            img = c.image(x, y + 0.1, cw, h - 0.1, path)
        except ImportError as e:
            c.box(x, y + 0.1, cw, h - 0.1, fill="surface")
            c.scene.problems.append(f"chart not drawn: {e}; install scripts/requirements/charts.txt")
    else:
        c.box(x, y + 0.1, cw, h - 0.1, fill="surface")
        c.scene.problems.append("[Medium] chart_insight has no data: add a table or `image:`")
    px, pw = x + cw + 0.45, w - cw - 0.45
    c.box(px, y + 0.1, pw, h - 0.1, fill="surface", line="accent")
    c.pill(px + 0.3, y + 0.35, "SO WHAT", fill="bg", col="accent", size=12)
    take = s.prop("takeaway")
    yy = y + 1.0
    if take:
        c.fit_text(px + 0.3, yy, pw - 0.6, 2.0, take, 22, 14, "text", "body", True)
        yy += 2.3
    if s.items:
        flow(c, s.items[:3], px + 0.3, yy, pw - 0.6, CONTENT_BOTTOM - yy - 0.3, max_size=17, min_size=12)


@layout("comparison", "data", "Table or side-by-side cards comparing our approach with baselines; the winner is highlighted.", 60,
        accepts="markdown table (header first); `highlight: 2` outlines the 2nd column; use **bold** for the best cell",
        example="# Ours wins on every metric\nlayout: comparison\nhighlight: 3\nsource: runs/log.jsonl\n| Metric | Baseline | Ours |\n|---|---|---|\n| F1 | 0.81 | **0.92** |\n| Latency | 9 s | **2 s** |")
def comparison(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = s.table or [cells(i) for i in s.items]
    if not rows:
        c.scene.problems.append("[Medium] comparison has no table")
        return
    rows = [r for r in rows[:8]]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    n = len(rows)
    rh = min(0.9, (h - 0.1) / n)
    first = 3.3 if ncol > 3 else 3.8
    cws = [first] + [(w - first) / (ncol - 1)] * (ncol - 1) if ncol > 1 else [w]
    hi = int(s.prop("highlight", "0") or 0)
    yy = y + 0.1
    for ri, row in enumerate(rows):
        xx = x
        for ci, cell in enumerate(row):
            fill = "primary" if ri == 0 else ("surface" if ri % 2 else "bg")
            if c.pixel:
                c.rect(xx, yy, cws[ci], rh, fill)
            else:
                c.rect(xx, yy, cws[ci], rh, fill, "border", 0.75)
            bold_cell = ri == 0 or ci == 0 or cell.startswith("**")
            txt = cell.strip("*") if cell.startswith("**") and cell.endswith("**") else cell
            col = c.t.on("primary") if ri == 0 else ("accent" if cell.startswith("**") else "text")
            c.fit_text(xx + 0.15, yy, cws[ci] - 0.3, rh, txt, 18, 11, col, "body", bold_cell, "left" if ci == 0 else "center", "middle")
            xx += cws[ci]
        yy += rh
    if 0 < hi <= ncol:
        hx = x + sum(cws[:hi - 1])
        c.rect(hx, y + 0.1, cws[hi - 1], rh * n, None, "accent", 2.5)

