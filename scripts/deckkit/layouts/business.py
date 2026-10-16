"""Business components: executive summary, matrix, funnel, market, pricing, gantt, org chart, scorecard, risk, feature matrix, process."""
import re

from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow, number

RAG = {"green": "success", "on track": "success", "on-track": "success", "ok": "success", "done": "success",
       "amber": "warning", "yellow": "warning", "at risk": "warning", "at-risk": "warning", "watch": "warning",
       "red": "danger", "off track": "danger", "off-track": "danger", "late": "danger", "blocked": "danger"}
LEVEL = {"low": "success", "medium": "warning", "med": "warning", "high": "danger", "critical": "danger"}


_num = number


def _shade(c, k, n):
    """k-th of n shades from light to strong primary, mixed with the background."""
    return color.mix(c.t.c("bg"), c.t.c("primary"), 0.35 + 0.65 * (k / max(n - 1, 1)))


@layout("exec_summary", "business", "Executive summary: situation, complication, resolution and the ask as labelled rows.", 80,
        accepts="items: `Label | text` (up to 4, defaults Situation, Complication, Resolution, Ask); first paragraph: the recommendation bar",
        example="# We should expand in the second city\nlayout: exec_summary\nsource: ops/q3.csv\n- Situation | Demand in city one doubled in a year\n- Complication | Capacity is full until spring\n- Resolution | Open city two with the same playbook\nApprove 1.2 M for the launch by 30 June.")
def exec_summary(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    defaults = ["Situation", "Complication", "Resolution", "Ask"]
    items = s.items[:4]
    n = max(len(items), 1)
    bar = 0.95 if s.paragraphs else 0
    gap = 0.14
    rh = (h - 0.1 - bar - (0.25 if bar else 0) - gap * (n - 1)) / n
    for k, it in enumerate(items):
        parts = cells(it, 2)
        label, text = (parts[0], parts[1]) if parts[1] else (defaults[k], parts[0])
        ry = y + 0.1 + k * (rh + gap)
        c.rect(x, ry, 2.5, rh, "primary")
        c.fit_text(x + 0.2, ry, 2.1, rh, label.upper(), 15, 11, c.t.on("primary"), "body", True, valign="middle")
        c.box(x + 2.5, ry, w - 2.5, rh, fill="surface", shadow=False, radius=0.0)
        c.fit_text(x + 2.8, ry + 0.05, w - 3.1, rh - 0.1, text, 20, 12, "text", valign="middle")
    if bar:
        by = y + h - bar
        c.rect(x, by, w, bar, "accent")
        c.text(x + 0.25, by, 2.3, bar, "RECOMMENDATION", 12, c.t.on("accent"), "body", True, valign="middle", chrome=True)
        c.fit_text(x + 2.6, by + 0.05, w - 2.9, bar - 0.1, s.paragraphs[0], 20, 12, c.t.on("accent"), "body", True, valign="middle")


@layout("matrix", "business", "Two by two matrix: SWOT or any four-way split, each cell with its own bullets.", 80,
        accepts="groups: four `## heading` sections; or items `Quadrant | text`; props: quadrants (comma list), tone swot or neutral, x and y axis captions",
        example="# Strengths outweigh the threats\nlayout: matrix\n## Strengths\n- Fast delivery\n## Weaknesses\n- Small team\n## Opportunities\n- New market\n## Threats\n- Big incumbents")
def matrix(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1] or g[0]]
    if len(groups) < 4 and s.items:
        names = [q.strip() for q in s.prop("quadrants", "Strengths, Weaknesses, Opportunities, Threats").split(",")]
        buckets = {nm: [] for nm in names}
        for it in s.items:
            q, text = (cells(it, 2)[0], cells(it, 2)[1]) if it.cells else ("", it.text)
            buckets.setdefault(q, []).append(type(it)(text=text))
        groups = [(nm, buckets.get(nm, [])) for nm in names]
    groups = (groups + [("", [])] * 4)[:4]
    tones = ["success", "warning", "info", "danger"] if s.prop("tone", "swot") == "swot" else ["primary", "secondary", "accent", "muted"]
    cap = 0.3 if (s.prop("x") or s.prop("y")) else 0
    gap = 0.22
    cw, ch = (w - gap) / 2, (h - 0.1 - cap - gap) / 2
    for k, (head, items) in enumerate(groups):
        r, col = divmod(k, 2)
        cx, cy = x + col * (cw + gap), y + 0.1 + r * (ch + gap)
        c.box(cx, cy, cw, ch, fill="surface", shadow=False)
        c.rect(cx, cy, 0.12, ch, tones[k])
        c.fit_text(cx + 0.35, cy + 0.12, cw - 0.6, 0.45, head, 19, 12, "text", "heading", True, valign="middle")
        flow(c, items[:4], cx + 0.35, cy + 0.7, cw - 0.65, ch - 0.85, max_size=17, min_size=12, gap=0.12, marker_col=tones[k])
    if cap:
        c.text(x, y + h - cap, w / 2, cap, s.prop("y"), 12, "muted", "body", True, chrome=True)
        c.text(x + w / 2, y + h - cap, w / 2, cap, s.prop("x"), 12, "muted", "body", True, "right", chrome=True)


@layout("funnel", "business", "Conversion funnel: stages narrowing from top to bottom, each with a value and a note.", 60,
        accepts="items: `Stage | value | note | conversion` (up to 6); widths follow the values",
        example="# Most prospects drop at the trial step\nlayout: funnel\nsource: crm/export.csv\n- Visitors | 48,000 | website\n- Sign-ups | 5,200 | free plan\n- Active | 1,900 | used twice\n- Paying | 410 | after the trial")
def funnel(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    vals = [_num(cells(i, 2)[1]) or 1 for i in items]
    top = max(vals)
    fw = 7.4
    rh = (h - 0.1) / n
    cx = x + fw / 2
    for k, it in enumerate(items):
        stage, value, note, conv = cells(it, 4)[:4]
        wd = max(0.28, vals[k] / top) * fw
        nxt = max(0.2, (vals[k + 1] / top) if k + 1 < n else vals[k] / top * 0.8) * fw
        yy = y + 0.1 + k * rh
        fill = _shade(c, n - 1 - k, n)
        c.poly([(cx - wd / 2, yy + 0.04), (cx + wd / 2, yy + 0.04), (cx + nxt / 2, yy + rh - 0.04), (cx - nxt / 2, yy + rh - 0.04)], fill)
        on = c.t.on(fill)
        tw = min(wd, nxt) - 0.3
        tx = cx - tw / 2
        if rh >= 0.95:
            by = yy + (rh - 0.78) / 2
            c.fit_text(tx, by, tw, 0.3, stage, 16, 10, on, "body", True, "center", "middle")
            c.fit_text(tx, by + 0.32, tw, 0.46, value, 24, 12, on, "heading", True, "center", "middle")
        else:
            c.fit_text(tx, yy + 0.04, tw, rh - 0.08, f"{stage}  {value}", 17, 10, on, "body", True, "center", "middle")
        if note or conv:
            c.fit_text(x + fw + 0.45, yy, w - fw - 0.45, rh - 0.05, f"**{conv}**  {note}" if conv else note, 17, 11, "text", valign="middle")


@layout("market", "business", "Market size as nested circles: total, serviceable and obtainable market with a value each.", 55,
        accepts="items: `Name | value | description` from the largest to the smallest (up to 3), e.g. TAM, SAM, SOM",
        example="# We can win 12 M in year three\nlayout: market\nsource: research/market.md\n- TAM | 4.2 B | all schools worldwide\n- SAM | 310 M | schools in our regions\n- SOM | 12 M | reachable in three years")
def market(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:3]
    n = max(len(items), 1)
    base = y + h - 0.1
    r0 = min(h / 2 - 0.05, 2.15)
    cx = x + r0 + 0.2
    radii = [r0 * (1 - 0.3 * k) for k in range(n)]
    for k, (it, r) in enumerate(zip(items, radii)):
        fill = _shade(c, k, n)
        c.rect(cx - r, base - 2 * r, 2 * r, 2 * r, fill, kind="ellipse")
    for k, (it, r) in enumerate(zip(items, radii)):
        name, value, desc = cells(it, 3)[:3]
        on = c.t.on(_shade(c, k, n))
        c.text(cx - 1.2, base - 2 * r + 0.18, 2.4, 0.4, name.upper(), 15, on, "body", True, "center", chrome=True)
        if k == n - 1:
            c.text(cx - 1.2, base - 2 * r + 0.55, 2.4, 0.5, value, 22, on, "heading", True, "center", "top", 1.0)
    lx = x + 2 * r0 + 0.9
    rh = (h - 0.4) / n
    for k, it in enumerate(items):
        name, value, desc = cells(it, 3)[:3]
        yy = y + 0.2 + k * rh
        c.rect(lx, yy + 0.05, 0.14, rh - 0.3, _shade(c, k, n))
        c.text(lx + 0.35, yy, 2.0, 0.4, name.upper(), 14, "muted", "body", True, chrome=True)
        c.text(lx + 0.35, yy + 0.35, 3.2, 0.7, value, 34, "text", "heading", True, "left", "top", 1.0)
        c.fit_text(lx + 0.35, yy + 1.0, w - (lx - x) - 0.5, rh - 1.15, desc, 17, 12, "muted")


@layout("pricing", "business", "Plan cards with a price and a short feature list; one plan can be highlighted.", 70,
        accepts="items: `Plan | price | feature; feature; feature` (2 to 4); highlight: plan number",
        example="# Three plans cover every team size\nlayout: pricing\nhighlight: 2\n- Starter | 0 | 1 project; Community support\n- Team | 19 | 10 projects; Priority support; Reports\n- Business | 99 | Unlimited projects; SSO; Audit log")
def pricing(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:4]
    n = max(len(items), 1)
    hi = int(s.prop("highlight", "0") or 0) - 1
    gap = 0.3
    cw = (w - gap * (n - 1)) / n
    for k, it in enumerate(items):
        plan, price, feats = cells(it, 3)[:3]
        cx = x + k * (cw + gap)
        top = y + (0.0 if k == hi else 0.3)
        hh = h - (0.0 if k == hi else 0.3) - 0.05
        fill = "primary" if k == hi else "surface"
        c.box(cx, top, cw, hh, fill=fill, shadow=(k == hi))
        on = c.t.on("primary") if k == hi else None
        c.text(cx + 0.3, top + 0.25, cw - 0.6, 0.35, plan.upper(), 14, on or "muted", "body", True, chrome=True)
        c.fit_text(cx + 0.3, top + 0.65, cw - 0.6, 0.9, price, 42, 20, on or "text", "heading", True, valign="middle")
        yy = top + 1.75
        for f in [p.strip() for p in feats.split(";") if p.strip()][:6]:
            c.tick(cx + 0.32, yy + 0.07, 0.2, on or "success", 2.5)
            c.fit_text(cx + 0.68, yy - 0.04, cw - 0.95, 0.5, f, 16, 11, on or "text", valign="middle")
            yy += 0.5


@layout("gantt", "business", "Plan on a timeline: tasks as bars across periods, with owners and milestones.", 70,
        accepts="items: `Task | start | end | owner` (up to 9); props: periods (comma list, default numbers); a task whose start equals its end is a milestone",
        example="# The launch fits in two quarters\nlayout: gantt\nperiods: Q1, Q2, Q3, Q4\n- Design | 1 | 1 | Design\n- Build | 1 | 2 | Engineering\n- Pilot | 2 | 3 | Sales\n- Launch | 4 | 4 | All")
def gantt(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:9]
    rows = [cells(i, 4) for i in items]

    def idx(v, names):
        v = str(v).strip()
        if v in names:
            return names.index(v) + 1
        n = _num(v)
        return n if n is not None else 1
    periods = [p.strip() for p in s.prop("periods").split(",") if p.strip()]
    if not periods:
        top = max([idx(r[2], []) for r in rows] + [4])
        periods = [str(i + 1) for i in range(int(top))]
    n = len(periods)
    lw = 3.3
    gw = (w - lw) / n
    hh = 0.45
    c.rect(x + lw, y + 0.1, w - lw, hh, "primary")
    for k, p in enumerate(periods):
        c.text(x + lw + k * gw, y + 0.1, gw, hh, p, 14, c.t.on("primary"), "body", True, "center", "middle", chrome=True)
    rh = min(0.55, (h - 0.2 - hh) / max(len(rows), 1))
    owners = []
    for r in rows:
        if r[3] not in owners:
            owners.append(r[3])
    for k in range(n + 1):
        c.line(x + lw + k * gw, y + 0.1 + hh, x + lw + k * gw, y + 0.1 + hh + rh * len(rows), color.mix(c.t.c("bg"), c.t.c("text"), 0.18), 0.75)
    for k, (task, a, b, owner) in enumerate(rows):
        ry = y + 0.2 + hh + k * rh
        if k % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.6)
        c.fit_text(x + 0.1, ry, lw - 0.2, rh, task, 16, 11, "text", "body", True, valign="middle")
        sa, sb = idx(a, periods), idx(b, periods)
        col = c.t.series[owners.index(owner) % len(c.t.series)] if owner else c.t.c("primary")
        if sa == sb and a == b:
            cx = x + lw + (sa - 0.5) * gw
            c.poly([(cx, ry + rh / 2 - 0.2), (cx + 0.2, ry + rh / 2), (cx, ry + rh / 2 + 0.2), (cx - 0.2, ry + rh / 2)], col)
        else:
            c.rect(x + lw + (sa - 1) * gw + 0.05, ry + 0.09, (sb - sa + 1) * gw - 0.1, rh - 0.18, col, kind="round", radius=0.06)
    if len(owners) > 1:
        lx = x + lw
        for k, o in enumerate(owners[:5]):
            c.rect(lx, y + h - 0.12, 0.16, 0.16, c.t.series[k % len(c.t.series)])
            c.text(lx + 0.22, y + h - 0.2, 1.8, 0.3, o, 12, "muted", "body", chrome=True, valign="middle")
            lx += 2.0


@layout("org", "business", "Organisation or team chart: a lead and the people who report to them, up to three levels.", 60,
        accepts="items: `Name | Role | reports to` (the first item is the root; others name their manager)",
        example="# One lead, three squads\nlayout: org\n- Dana K. | Head of product\n- Timur B. | Engineering | Dana K.\n- Mira L. | Design | Dana K.\n- Aigerim S. | Data | Dana K.")
def org(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    nodes = [cells(i, 3)[:3] for i in s.items[:12]]
    if not nodes:
        return
    names = [n[0] for n in nodes]
    kids = {n: [] for n in names}
    for name, role, boss in nodes[1:]:
        kids.setdefault(boss if boss in names else names[0], []).append(name)
    depth, order = {names[0]: 0}, []

    def walk(n):
        order.append(n)
        for ch in kids.get(n, []):
            depth[ch] = depth[n] + 1
            walk(ch)
    walk(names[0])
    leaves = [n for n in order if not kids.get(n)]
    pos = {}
    for i, lf in enumerate(leaves):
        pos[lf] = i

    def center(n):
        if n in pos and not kids.get(n):
            return pos[n]
        cs = [center(k) for k in kids[n]]
        pos[n] = (min(cs) + max(cs)) / 2
        return pos[n]
    center(names[0])
    nl = max(len(leaves), 1)
    levels = max(depth.values()) + 1
    bw = min(2.4, (w - 0.2) / nl - 0.15)
    bh = 0.95
    vstep = min(1.75, (h - bh - 0.2) / max(levels - 1, 1)) if levels > 1 else 0
    role = {n[0]: n[1] for n in nodes}

    def xy(n):
        return x + (w / nl) * (pos[n] + 0.5), y + 0.15 + depth[n] * vstep
    for n in order:
        cx, cy = xy(n)
        for ch in kids.get(n, []):
            kx, ky = xy(ch)
            my = (cy + bh + ky) / 2
            col = color.mix(c.t.c("bg"), c.t.c("text"), 0.4)
            c.line(cx, cy + bh, cx, my, col, 1.5)
            c.line(cx, my, kx, my, col, 1.5)
            c.line(kx, my, kx, ky, col, 1.5)
    for n in order:
        cx, cy = xy(n)
        root = depth[n] == 0
        c.box(cx - bw / 2, cy, bw, bh, fill="primary" if root else "surface", shadow=False)
        on = c.t.on("primary") if root else "text"
        c.fit_text(cx - bw / 2 + 0.08, cy + 0.08, bw - 0.16, bh * 0.5, n, 17, 11, on, "body", True, "center", "middle")
        c.fit_text(cx - bw / 2 + 0.08, cy + bh * 0.52, bw - 0.16, bh * 0.4, role.get(n, ""), 13, 10, on if root else "muted", "body", False, "center", "top")


@layout("scorecard", "business", "KPI scorecard: metric, actual, target and a status dot for each row.", 90,
        accepts="items: `Metric | actual | target | green, amber or red | note` (up to 7)",
        example="# Four of five KPIs are on track\nlayout: scorecard\nsource: bi/q3.xlsx\n- Revenue | 4.1 M | 4.0 M | green | ahead of plan\n- Churn | 3.2% | 3.0% | amber | one segment worse")
def scorecard(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 5)[:5] for i in s.items[:7]]
    cols = [("METRIC", 3.3), ("ACTUAL", 1.8), ("TARGET", 1.8), ("STATUS", 1.9)]
    c.rect(x, y + 0.1, w, 0.42, "primary")
    cx = x
    for label, cw in cols:
        c.text(cx + 0.15, y + 0.1, cw - 0.2, 0.42, label, 12, c.t.on("primary"), "body", True, valign="middle", chrome=True)
        cx += cw
    c.text(cx + 0.15, y + 0.1, w - (cx - x) - 0.2, 0.42, "NOTE", 12, c.t.on("primary"), "body", True, valign="middle", chrome=True)
    rh = min(0.68, (h - 0.7) / max(len(rows), 1))
    for k, (metric, actual, target, status, note) in enumerate(rows):
        ry = y + 0.55 + k * rh
        if k % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.7)
        c.fit_text(x + 0.15, ry, cols[0][1] - 0.3, rh, metric, 18, 11, "text", "body", True, valign="middle")
        c.text(x + cols[0][1] + 0.15, ry, cols[1][1] - 0.2, rh, actual, 20, "text", "heading", True, valign="middle", line_h=1.0)
        c.text(x + cols[0][1] + cols[1][1] + 0.15, ry, cols[2][1] - 0.2, rh, target, 18, "muted", "body", False, valign="middle")
        tone = RAG.get(status.strip().lower(), "muted")
        sx = x + sum(cw for _, cw in cols[:3]) + 0.15
        c.rect(sx, ry + rh / 2 - 0.12, 0.24, 0.24, tone, kind="ellipse")
        c.text(sx + 0.38, ry, cols[3][1] - 0.5, rh, status.upper(), 12, "text", "body", True, valign="middle", chrome=True)
        nx = x + sum(cw for _, cw in cols) + 0.15
        c.fit_text(nx, ry + 0.03, w - (nx - x) - 0.25, rh - 0.06, note, 15, 11, "muted", valign="middle")


@layout("risk", "business", "Risk register: each risk with likelihood and impact chips and its mitigation.", 90,
        accepts="items: `Risk | likelihood | impact | mitigation` with low, medium or high (up to 6)",
        example="# Three risks need an owner this month\nlayout: risk\n- Key supplier delay | medium | high | Second source approved\n- Regulation change | low | high | Legal review each quarter")
def risk(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 4)[:4] for i in s.items[:6]]
    c.rect(x, y + 0.1, w, 0.42, "primary")
    for label, cx, cw in (("RISK", x + 0.15, 4.0), ("LIKELIHOOD", x + 4.4, 1.6), ("IMPACT", x + 6.2, 1.4), ("MITIGATION", x + 7.8, 3.5)):
        c.text(cx, y + 0.1, cw, 0.42, label, 12, c.t.on("primary"), "body", True, valign="middle", chrome=True)
    rh = min(0.78, (h - 0.7) / max(len(rows), 1))
    for k, (name, lik, imp, mit) in enumerate(rows):
        ry = y + 0.55 + k * rh
        if k % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.7)
        c.fit_text(x + 0.15, ry, 4.0, rh, name, 18, 11, "text", "body", True, valign="middle")
        for label, cx in ((lik, x + 4.4), (imp, x + 6.2)):
            tone = LEVEL.get(label.strip().lower(), "muted")
            cw = 1.15
            c.rect(cx, ry + rh / 2 - 0.17, cw, 0.34, tone, kind="round", radius=0.17)
            c.text(cx, ry + rh / 2 - 0.17, cw, 0.34, label.upper(), 11, c.t.on(tone), "body", True, "center", "middle", chrome=True)
        c.fit_text(x + 7.8, ry + 0.03, w - 7.95, rh - 0.06, mit, 15, 11, "muted", valign="middle")


@layout("feature_matrix", "business", "Feature or competitor matrix: rows of capabilities, columns of options, with ticks and crosses.", 70,
        accepts="markdown table; cells yes, no or partial draw a tick, a cross or a dash; highlight: column number to frame",
        example="# We cover every must-have feature\nlayout: feature_matrix\nhighlight: 4\n| Feature | A | B | Us |\n|---|---|---|---|\n| Offline mode | no | yes | yes |\n| API | partial | yes | yes |")
def feature_matrix(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [r for r in s.table[:9]]
    if not rows:
        c.scene.problems.append("[Medium] feature_matrix has no table")
        return
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    first = 3.8
    cw = (w - first) / max(ncol - 1, 1)
    rh = min(0.62, (h - 0.1) / len(rows))
    hi = int(s.prop("highlight", "0") or 0)
    c.rect(x, y + 0.1, w, rh, "primary")
    for j, cell in enumerate(rows[0]):
        cx = x if j == 0 else x + first + (j - 1) * cw
        c.fit_text(cx + 0.15, y + 0.1, (first if j == 0 else cw) - 0.3, rh, cell, 16, 11, c.t.on("primary"), "body", True, "left" if j == 0 else "center", "middle")
    for i, row in enumerate(rows[1:], 1):
        ry = y + 0.1 + i * rh
        if i % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.7)
        c.fit_text(x + 0.15, ry, first - 0.3, rh, row[0], 17, 11, "text", "body", True, valign="middle")
        for j, cell in enumerate(row[1:], 1):
            cx = x + first + (j - 1) * cw + cw / 2
            t = cell.strip().lower().strip("*")
            if t in ("yes", "y", "true", "✓", "ok"):
                c.tick(cx - 0.14, ry + rh / 2 - 0.12, 0.28, "success", 3.5)
            elif t in ("no", "n", "false", "x", "✗"):
                c.cross(cx - 0.12, ry + rh / 2 - 0.12, 0.24, "danger", 3.0)
            elif t in ("partial", "p", "~", "some"):
                c.rect(cx - 0.14, ry + rh / 2 - 0.03, 0.28, 0.06, "warning")
            else:
                c.fit_text(cx - cw / 2 + 0.1, ry, cw - 0.2, rh, cell.strip("*"), 15, 11, "text", "body", cell.startswith("**"), "center", "middle")
    if 0 < hi < ncol:
        c.rect(x + first + (hi - 1) * cw, y + 0.1, cw, rh * len(rows), None, "accent", 2.5)


@layout("process", "business", "Chevron process: two to six steps in order, each with a short description.", 60,
        accepts="items: `Step | description | owner` (up to 6)",
        example="# Four steps from request to payout\nlayout: process\n- Request | the customer files a claim\n- Review | an adjuster checks it\n- Approve | a manager signs off\n- Pay | funds arrive in 3 days")
def process(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    cw = (w + 0.3 * (n - 1)) / n
    for k, it in enumerate(items):
        step, desc, owner = cells(it, 3)[:3]
        cx = x + k * (cw - 0.3)
        fill = _shade(c, k, n)
        c.chevron(cx, y + 0.5, cw, 1.2, fill, notch=0.35, first=(k == 0))
        on = c.t.on(fill)
        c.text(cx + (0.45 if k else 0.2), y + 0.5, cw - 0.9, 1.2, f"{k + 1}  {step}", 18, on, "body", True, "left", "middle")
        c.fit_text(cx + 0.1, y + 1.95, cw - 0.7, 1.6, desc, 17, 11, "text")
        if owner:
            c.text(cx + 0.1, y + 3.6, cw - 0.7, 0.35, owner.upper(), 11, "muted", "body", True, chrome=True)
