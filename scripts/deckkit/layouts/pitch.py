"""Pitch and business additions: business model canvas, OKRs, KPI table, customer case, the ask, proof wall."""
from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow, number
from .business import RAG

CANVAS_BLOCKS = ["Key partners", "Key activities", "Key resources", "Value propositions", "Customer relationships", "Channels",
                 "Customer segments", "Cost structure", "Revenue streams"]


def _track(c, x, y, w, h, frac, tone):
    """A flat progress bar: a faint track and a filled part."""
    track = color.mix(c.t.c("surface"), c.t.c("text"), 0.16)
    kind = "rect" if c.style["corner"] == "square" else "round"
    c.rect(x, y, w, h, track, kind=kind, radius=h / 2)
    if frac > 0:
        c.rect(x, y, max(h, w * min(frac, 1.0)), h, tone, kind=kind, radius=h / 2)


@layout("canvas9", "business", "Business model canvas: nine labelled blocks in the standard arrangement, each with a few short bullets.", 100,
        accepts="groups: up to nine `## heading` sections named like Key partners, Key activities, Key resources, Value propositions, "
                "Customer relationships, Channels, Customer segments, Cost structure, Revenue streams (matched by name, else in that order); keep bullets to three or four words",
        example="# A tutoring marketplace in one page\nlayout: canvas9\n## Key partners\n- Schools\n- Payment provider\n## Key activities\n- Vetting tutors\n- Matching\n"
                "## Key resources\n- Tutor network\n- Matching model\n## Value propositions\n- Verified tutors\n- First lesson free\n## Customer relationships\n- Self-service\n- Lesson reminders\n"
                "## Channels\n- Parent groups\n- School newsletters\n## Customer segments\n- Parents of teens\n- Exam candidates\n## Cost structure\n- Tutor payouts\n- Cloud and support\n"
                "## Revenue streams\n- 15% lesson fee\n- Monthly subscription")
def canvas9(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    names = [n.lower() for n in CANVAS_BLOCKS]
    slots = {}
    spare = []
    for head, items in s.groups:
        key = head.strip().lower()
        hit = next((i for i, n in enumerate(names) if n == key or key in n or n in key), None) if key else None
        if hit is not None and hit not in slots:
            slots[hit] = (CANVAS_BLOCKS[hit], items)
        else:
            spare.append((head, items))
    for i in range(9):
        if i not in slots and spare:
            slots[i] = spare.pop(0)
    gap = 0.12
    bh = 1.25
    th = h - 0.1 - bh - gap
    cw = (w - 4 * gap) / 5
    top = y + 0.1
    col = lambda k: x + k * (cw + gap)
    half = (th - gap) / 2
    cells_xywh = {0: (col(0), top, cw, th), 1: (col(1), top, cw, half), 2: (col(1), top + half + gap, cw, half),
                  3: (col(2), top, cw, th), 4: (col(3), top, cw, half), 5: (col(3), top + half + gap, cw, half),
                  6: (col(4), top, cw, th), 7: (x, top + th + gap, (w - gap) / 2, bh), 8: (x + (w + gap) / 2, top + th + gap, (w - gap) / 2, bh)}
    for i, (cx, cy, cwid, chei) in cells_xywh.items():
        head, items = slots.get(i, (CANVAS_BLOCKS[i], []))
        c.box(cx, cy, cwid, chei, fill="surface", shadow=False, radius=min(c.style["radius"], 0.1))
        c.rect(cx, cy, cwid, 0.06, "accent" if i == 3 else "primary")
        c.fit_text(cx + 0.12, cy + 0.1, cwid - 0.24, 0.42, head.upper(), 12, 11, "accent" if i == 3 else "muted", "mono", True, valign="middle")
        flow(c, items[:4], cx + 0.12, cy + 0.58, cwid - 0.24, chei - 0.66, max_size=15, min_size=12, gap=0.06)


@layout("okr", "business", "OKRs: up to three objectives, each with key results shown as progress bars against their targets.", 80,
        accepts="groups: one `## Objective` per card (up to three); bullets `Key result | current | target` (up to three each); set `source:` for the numbers",
        example="# Two of three objectives are on track for the quarter\nlayout: okr\nsource: bi/okr-q3.xlsx\n## Grow active learners\n- Weekly active users | 4,200 | 6,000\n- Day-7 retention | 31 | 40\n"
                "## Raise revenue quality\n- Paid conversion | 3.1 | 4\n- Refund rate | 2 | 2\n## Ship the mobile app\n- Beta users | 120 | 500\n- Crash-free sessions | 97 | 99")
def okr(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1] or g[0]][:3]
    n = max(len(groups), 1)
    gap = 0.3
    cw = (w - gap * (n - 1)) / n
    for i, (head, items) in enumerate(groups):
        cx = x + i * (cw + gap)
        c.box(cx, y + 0.1, cw, h - 0.1, fill="surface")
        c.badge(cx + 0.5, y + 0.72, 0.26, f"O{i + 1}", "primary", 13)
        c.fit_text(cx + 0.9, y + 0.3, cw - 1.15, 0.85, head, 19, 12, "text", "heading", True, valign="middle")
        rows = items[:3]
        ky = y + 1.5
        kh = (h - 0.1 - 1.5 - 0.1) / max(len(rows), 1)
        for it in rows:
            name, cur, target = cells(it, 3)[:3]
            a, b = number(cur), number(target)
            frac = (a / b) if a is not None and b else 0.0
            tone = "success" if frac >= 0.7 else "warning" if frac >= 0.4 else "danger"
            c.fit_text(cx + 0.3, ky, cw - 0.6, 0.4, name, 16, 11, "text", "body", True, valign="middle")
            _track(c, cx + 0.3, ky + 0.46, cw - 0.6, 0.15, frac, c.t.c(tone))
            c.text(cx + 0.3, ky + 0.62, cw - 0.6, 0.3, f"{cur} of {target}  ({min(frac, 9.99) * 100:.0f}%)", 12, "muted", "mono", chrome=True, valign="middle")
            ky += kh


@layout("kpi_table", "business", "KPI table with a change column: value, delta with an up or down marker, a status dot and a note per metric.", 90,
        accepts="items: `Metric | value | delta | green, amber or red | note` (up to 8); a delta starting with + points up, - points down; set `source:`",
        example="# Revenue is up and churn is flat\nlayout: kpi_table\nsource: bi/q3.xlsx\n- Revenue | 4.1 M | +8% | green | ahead of plan\n- Active users | 61,000 | +12% | green | all regions\n"
                "- Churn | 3.2% | -0.1 pt | amber | one segment worse\n- Support tickets | 1,840 | +21% | red | release 5.2")
def kpi_table(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 5)[:5] for i in s.items[:8]]
    cols = [("METRIC", 3.5), ("VALUE", 1.9), ("CHANGE", 1.8), ("STATUS", 1.6)]
    c.rect(x, y + 0.1, w, 0.42, "primary")
    cx = x
    for label, cw in cols:
        c.text(cx + 0.15, y + 0.1, cw - 0.2, 0.42, label, 12, c.t.on("primary"), "body", True, valign="middle", chrome=True)
        cx += cw
    c.text(cx + 0.15, y + 0.1, w - (cx - x) - 0.2, 0.42, "NOTE", 12, c.t.on("primary"), "body", True, valign="middle", chrome=True)
    rh = min(0.6, (h - 0.7) / max(len(rows), 1))
    for k, (metric, value, delta, status, note) in enumerate(rows):
        ry = y + 0.55 + k * rh
        if k % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.7)
        c.fit_text(x + 0.15, ry, cols[0][1] - 0.3, rh, metric, 17, 11, "text", "body", True, valign="middle")
        c.text(x + cols[0][1] + 0.15, ry, cols[1][1] - 0.2, rh, value, 19, "text", "heading", True, valign="middle", line_h=1.0)
        d = delta.strip()
        up, down = d.startswith("+"), d[:1] in ("-", "−", "–")
        tone = RAG.get(status.strip().lower()) or ("success" if up else "danger" if down else "muted")
        dx = x + cols[0][1] + cols[1][1] + 0.15
        if up or down:
            c.triangle(dx + 0.12, ry + rh / 2, 0.11, tone, up=up)
        c.text(dx + 0.34, ry, cols[2][1] - 0.5, rh, d, 17, tone if tone != "muted" else "text", "body", True, valign="middle")
        sx = x + sum(cw for _, cw in cols[:3]) + 0.15
        if status.strip():
            c.rect(sx, ry + rh / 2 - 0.11, 0.22, 0.22, RAG.get(status.strip().lower(), "muted"), kind="ellipse")
            c.text(sx + 0.34, ry, cols[3][1] - 0.5, rh, status.upper(), 11, "text", "body", True, valign="middle", chrome=True)
        nx = x + sum(cw for _, cw in cols) + 0.15
        c.fit_text(nx, ry + 0.03, w - (nx - x) - 0.25, rh - 0.06, note, 15, 11, "muted", valign="middle")


@layout("customer_case", "business", "Customer story: who the customer is, problem, solution and result, with the headline result as a big number.", 90,
        accepts="props: customer, industry, quote, stat `-42% | support tickets`; items: `Problem | text`, `Solution | text`, `Result | text`; set `source:`",
        example="# A regional bank cut ticket volume by 42 percent\nlayout: customer_case\nsource: customers/bank-case.md\ncustomer: Northern Savings Bank\nindustry: Retail banking, 900 staff\n"
                "quote: We stopped answering the same ten questions every day.\nstat: -42% | support tickets in 90 days\n- Problem | Agents repeated the same answers all day\n- Solution | A searchable help assistant inside the agent desktop\n- Result | Faster first replies and fewer escalations")
def customer_case(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lw, rw, gap = 3.7, 3.1, 0.3
    mw = w - lw - rw - 2 * gap
    top, ch = y + 0.1, h - 0.1
    c.box(x, top, lw, ch, fill="surface")
    c.pill(x + 0.3, top + 0.3, "CUSTOMER", fill="bg", col="accent", size=11)
    c.fit_text(x + 0.3, top + 0.85, lw - 0.6, 1.0, s.prop("customer"), 24, 14, "text", "heading", True)
    if s.prop("industry"):
        c.fit_text(x + 0.3, top + 1.9, lw - 0.6, 0.6, s.prop("industry"), 15, 11, "muted")
    if s.prop("quote"):
        c.text(x + 0.25, top + 2.45, 0.8, 0.8, "“", 60, "accent", "heading", True, line_h=1.0, chrome=True)
        c.fit_text(x + 0.3, top + 3.0, lw - 0.6, ch - 3.2, s.prop("quote"), 16, 12, "text")
    labels = ["PROBLEM", "SOLUTION", "RESULT"]
    rows = s.items[:3]
    rh = (ch - 0.1 * (len(rows) - 1)) / max(len(rows), 1)
    mx = x + lw + gap
    for k, it in enumerate(rows):
        label, text = (cells(it, 2)[0], cells(it, 2)[1]) if it.cells else (labels[k], it.text)
        ry = top + k * (rh + 0.1)
        c.box(mx, ry, mw, rh, fill="surface", shadow=False)
        c.rect(mx, ry, 0.1, rh, "primary" if k < 2 else "success")
        c.text(mx + 0.3, ry + 0.12, mw - 0.5, 0.3, label.upper(), 11, "muted", "mono", True, chrome=True)
        c.fit_text(mx + 0.3, ry + 0.45, mw - 0.55, rh - 0.55, text, 18, 12, "text")
    rx = mx + mw + gap
    stat = [p.strip() for p in s.prop("stat").split("|")] + ["", ""]
    c.box(rx, top, rw, ch, fill="primary", shadow=False)
    on = c.t.on("primary")
    size = textfit.fit_line(c.t, stat[0], "heading", rw - 0.4, 72 * c.style["heading_scale"], 20, True)
    c.text(rx + 0.2, top + 0.9, rw - 0.4, 1.5, stat[0], size, on, "heading", True, "center", "middle", 1.0)
    c.fit_text(rx + 0.3, top + 2.6, rw - 0.6, 1.4, stat[1], 18, 12, on, "body", False, "center")


@layout("ask", "business", "The ask: the amount, what the money is used for as a split bar, and what it unlocks.", 70,
        accepts="props: amount, detail, milestones (list separated by semicolons); items: `Use | share | note` (up to 5, shares become the bar); set `source:`",
        example="# We are raising 1.5 M to reach break-even in 18 months\nlayout: ask\nsource: finance/plan-2027.xlsx\namount: 1.5 M\ndetail: 18 months of runway\n"
                "milestones: 1,000 schools; Break-even; Second country\n- Product | 45 | four engineers and one designer\n- Sales | 35 | school partnerships team\n- Operations | 20 | support and compliance")
def ask(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lw, gap = 4.4, 0.35
    top, ch = y + 0.1, h - 0.1
    c.box(x, top, lw, ch, fill="surface", line="accent")
    c.pill(x + 0.3, top + 0.3, "THE ASK", fill="bg", col="accent", size=12)
    amount = s.prop("amount")
    size = textfit.fit_line(c.t, amount, "heading", lw - 0.6, 96 * c.style["heading_scale"], 24, True)
    c.text(x + 0.3, top + 1.0, lw - 0.6, 1.8, amount, size, "accent", "heading", True, "left", "middle", 1.0)
    if s.prop("detail"):
        c.fit_text(x + 0.3, top + 3.0, lw - 0.6, 1.0, s.prop("detail"), 20, 13, "text")
    rx, rw = x + lw + gap, w - lw - gap
    items = [cells(i, 3)[:3] for i in s.items[:5]]
    vals = [number(i[1]) or 0 for i in items]
    total = sum(vals) or 1
    c.text(rx, top, rw, 0.3, "USE OF FUNDS", 12, "muted", "mono", True, chrome=True)
    bx = rx
    palette = c.t.series
    for k, v in enumerate(vals):
        sw = rw * v / total
        c.rect(bx, top + 0.4, max(sw - 0.04, 0.05), 0.6, palette[k % len(palette)])
        bx += sw
    ry = top + 1.25
    rh = min(0.62, (ch - 1.25 - (1.25 if s.prop("milestones") else 0)) / max(len(items), 1))
    for k, (name, share, note) in enumerate(items):
        yy = ry + k * rh
        c.rect(rx, yy + rh / 2 - 0.09, 0.18, 0.18, palette[k % len(palette)], kind="round", radius=0.04)
        c.fit_text(rx + 0.35, yy, 2.2, rh, name, 18, 12, "text", "body", True, valign="middle")
        pct = share if "%" in share else (f"{vals[k] / total * 100:.0f}%")
        c.text(rx + 2.6, yy, 0.9, rh, pct, 18, "accent", "heading", True, valign="middle")
        c.fit_text(rx + 3.6, yy, rw - 3.6, rh, note, 15, 11, "muted", valign="middle")
    raw = s.prop("milestones")
    miles = [m.strip() for m in raw.split(";" if ";" in raw else ",") if m.strip()]
    if miles:
        my = top + ch - 0.95
        c.text(rx, my, rw, 0.3, "UNLOCKS", 12, "muted", "mono", True, chrome=True)
        px = rx
        for m in miles[:4]:
            px += c.pill(px, my + 0.4, m, fill="surface", col="text", size=14, h=0.46, role="body", bold=True) + 0.15


@layout("proof_wall", "business", "Wall of proof: awards, press, partners and milestones as a grid of short headlines with a caption each.", 70,
        accepts="items: `Headline | caption` (up to 8); the headline is a short claim or name, the caption its source or date; set `source:` when a number appears",
        example="# Schools, press and prizes back the product\nlayout: proof_wall\nsource: press/clippings.md\n- Top 10 | Education apps, App Store 2026\n- 40 schools | Paying pilots in two countries\n"
                "- Best Product | Regional EdTech Awards\n- Featured | National Education Weekly\n- 2x growth | Active classes since January\n- Partner | District education office")
def proof_wall(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = [cells(i, 2)[:2] for i in s.items[:8]]
    n = max(len(items), 1)
    cols = 4 if n > 6 else 3 if n > 4 else 2 if n == 4 else n
    cols = max(cols, 1)
    rows = (n + cols - 1) // cols
    gap = 0.25
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - 0.1 - gap * (rows - 1)) / rows
    for k, (head, cap) in enumerate(items):
        r, col = divmod(k, cols)
        cx, cy = x + col * (cw + gap), y + 0.1 + r * (ch + gap)
        c.box(cx, cy, cw, ch, fill="surface", line="primary" if k == 0 else "border")
        c.rect(cx + 0.3, cy + 0.3, 0.5, 0.06, "accent")
        c.fit_text(cx + 0.3, cy + 0.5, cw - 0.6, ch * 0.45, head, 26 * c.style["heading_scale"], 14, "text", "heading", True, valign="top")
        c.fit_text(cx + 0.3, cy + ch * 0.58, cw - 0.6, ch * 0.34, cap, 15, 11, "muted")
