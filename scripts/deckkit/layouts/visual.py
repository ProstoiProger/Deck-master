"""Advanced visual layouts: isometric stack and bars, podium, globe, orbit, gauges, bento grid, treemap, sankey, network,
activity grid, terminal and a shaded 3D hero object. Everything is drawn with flat vector shapes (except `hero_3d`, which
embeds a rendered picture), so PPTX and PDF match and the shapes stay editable."""
import math

from ..core import color, shapes3d, textfit
from ..core.layout import layout
from ._util import cells, flow, number


def _track(c, k=0.14):
    return color.mix(c.t.c("bg"), c.t.c("text"), k)


# ---- isometric -----------------------------------------------------------------------------------------------

@layout("iso_stack", "visual", "Isometric layer stack: up to five floating slabs, one per layer, each with a short description; for architectures and stacks.", 50,
        accepts="items: `Layer | description` from the top layer down (up to five); highlight: the number of one layer to color in the accent",
        example="# Four layers separate what users see from what we store\nlayout: iso_stack\nhighlight: 2\n- Interface | web and mobile clients\n- Service | ranking and rules\n- Model | the scoring model\n- Data | events and features")
def iso_stack(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 2)[:2] for i in s.items[:5]]
    n = max(len(rows), 1)
    hl = int(number(s.prop("highlight")) or 0)
    thick = 0.22
    size = min(2.0, (h - 0.3 - thick) / (1 + 0.75 * (n - 1)))     # the gap between slabs is 0.75 of a slab's depth
    gap = 0.75 * size
    cx = x + 0.2 + shapes3d.iso_width(size, size) / 2
    palette = c.t.series
    pts = []
    for i in range(n - 1, -1, -1):            # draw from the bottom slab up so each slab covers the one below
        oy = y + 0.15 + i * gap
        col = "accent" if hl == i + 1 else palette[i % len(palette)]
        box = shapes3d.iso_box(c, cx, oy, size, size, thick, col)
        pts.append((i, box["right"]))
    lx = x + 6.0
    for i, (ax, ay) in sorted(pts):
        name, desc = rows[i] if i < len(rows) else ("", "")
        my = ay + thick / 2
        c.line(ax + 0.08, my, lx - 0.15, my, color.mix(c.t.c("bg"), c.t.c("text"), 0.35), 1.0)
        c.rect(lx - 0.2, my - 0.05, 0.1, 0.1, "accent" if hl == i + 1 else "muted", kind="ellipse")
        c.text(lx, my - 0.36, 0.55, 0.4, f"{i + 1:02d}", 13, "accent" if hl == i + 1 else "muted", "mono", True, valign="middle", chrome=True)
        c.fit_text(lx + 0.6, my - 0.36, w - 6.6, 0.4, name, 19, 12, "text", "heading", True, valign="middle")
        c.fit_text(lx + 0.6, my + 0.02, w - 6.6, 0.36, desc, 14, 11, "muted", valign="top")


@layout("iso_bars", "visual", "Isometric column chart: up to six 3D columns with values on top, the largest in the accent, and a so-what panel.", 50,
        accepts="items: `Label | value` (up to six); props: takeaway (text of the side panel); set `source:`",
        example="# Gradient boosting leads on every holdout month\nlayout: iso_bars\nsource: runs/log.jsonl\ntakeaway: The gap to the baseline is largest on the newest months.\n- Baseline | 0.41\n- Linear | 0.48\n- Forest | 0.55\n- Boosting | 0.61")
def iso_bars(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 2)[:2] for i in s.items[:6]]
    n = max(len(rows), 1)
    vals = [number(r[1]) or 0 for r in rows]
    top_v = max(vals) or 1.0
    pw = 3.5
    cw = w - pw - 0.4
    slot = cw / n
    a = min(0.62, slot * 0.42)
    depth = shapes3d.iso_depth(a, a)
    base_y = y + h - 0.85
    max_h = h - 1.9 - depth
    c.rect(x, base_y + 0.02, cw, 0.03, color.mix(c.t.c("bg"), c.t.c("text"), 0.3))
    for i, (label, value) in enumerate(rows):
        bh = max(0.12, vals[i] / top_v * max_h)
        cx = x + slot * (i + 0.5)
        oy = base_y - depth - bh
        c.rect(cx - a * 0.9, base_y - depth * 0.55, a * 1.8, depth * 0.7, "#000000", kind="ellipse", alpha=0.18)
        shapes3d.iso_box(c, cx, oy, a, a, bh, "accent" if vals[i] == top_v else "primary")
        c.text(cx - slot / 2, oy - 0.5, slot, 0.4, value, 20, "text", "heading", True, "center", "middle", 1.0)
        c.fit_text(cx - slot / 2 + 0.05, base_y + 0.12, slot - 0.1, 0.6, label, 14, 11, "muted", align="center")
    px = x + cw + 0.4
    c.box(px, y + 0.1, pw, h - 0.1, fill="surface", line="accent")
    c.pill(px + 0.3, y + 0.35, "SO WHAT", fill="bg", col="accent", size=12)
    take = s.prop("takeaway") or (s.paragraphs[0] if s.paragraphs else "")
    c.fit_text(px + 0.3, y + 1.0, pw - 0.6, h - 1.4, take, 22, 14, "text", "body", True)


@layout("podium", "visual", "Podium: two or three ranked options or winners on stepped 3D blocks, the first in the middle.", 40,
        accepts="items: `Name | value | note` first place first (two or three); set `source:` when a number appears",
        example="# Boosting wins, the forest is close behind\nlayout: podium\nsource: runs/log.jsonl\n- Boosting | 0.61 | PR-AUC on the holdout\n- Forest | 0.55 | PR-AUC on the holdout\n- Linear | 0.48 | PR-AUC on the holdout")
def podium(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 3)[:3] for i in s.items[:3]]
    order = {1: [0], 2: [1, 0], 3: [1, 0, 2]}.get(len(rows), [0])   # slot order left to right: 2nd, 1st, 3rd
    heights = {0: 2.3, 1: 1.7, 2: 1.2}
    cols = {0: "accent", 1: "primary", 2: "secondary"}
    bw, gap, depth = 2.7, 0.25, 0.45
    total = len(order) * bw + (len(order) - 1) * gap
    x0 = x + (w - total) / 2 - depth * 0.35
    base = y + h - 0.35
    c.rect(x0 - 0.3, base, total + 0.9, 0.04, color.mix(c.t.c("bg"), c.t.c("text"), 0.3))
    for slot, rank in enumerate(order):
        name, value, note = rows[rank]
        bh = heights[rank]
        bx = x0 + slot * (bw + gap)
        by = base - bh
        shapes3d.oblique_box(c, bx, by, bw, bh, depth, cols[rank])
        on = c.t.on(cols[rank])
        c.text(bx, by + 0.12, bw, 0.9, str(rank + 1), 52 * c.style["heading_scale"], on, "heading", True, "center", "middle", 1.0)
        c.fit_text(bx + 0.15, by - depth * 0.45 - 1.5, bw + depth * 0.7 - 0.3, 0.5, name, 22, 13, "text", "heading", True, "center", "middle")
        c.fit_text(bx + 0.15, by - depth * 0.45 - 1.0, bw + depth * 0.7 - 0.3, 0.55, value, 30, 14, "accent", "heading", True, "center", "middle")
        c.fit_text(bx + 0.15, by - depth * 0.45 - 0.45, bw + depth * 0.7 - 0.3, 0.4, note, 13, 11, "muted", align="center", valign="middle")


# ---- globe, orbit, gauges ---------------------------------------------------------------------------------------

def _slerp(p, q, t):
    la1, lo1, la2, lo2 = (math.radians(v) for v in (*p, *q))
    a = (math.cos(la1) * math.cos(lo1), math.cos(la1) * math.sin(lo1), math.sin(la1))
    b = (math.cos(la2) * math.cos(lo2), math.cos(la2) * math.sin(lo2), math.sin(la2))
    dot = max(-1.0, min(1.0, sum(i * j for i, j in zip(a, b))))
    om = math.acos(dot)
    if om < 1e-6:
        return p
    k1, k2 = math.sin((1 - t) * om) / math.sin(om), math.sin(t * om) / math.sin(om)
    v = [k1 * i + k2 * j for i, j in zip(a, b)]
    return math.degrees(math.asin(max(-1, min(1, v[2])))), math.degrees(math.atan2(v[1], v[0]))


@layout("globe", "visual", "Wireframe globe with pins and callouts for places, optionally joined by arcs; for reach, regions and routes.", 60,
        accepts="items: `Place | note | latitude | longitude` (up to five); props: lat0 and lon0 (the view centre, default 25 and 60), arcs: yes joins the pins in order",
        example="# Three regions already run the pilot\nlayout: globe\nlat0: 30\nlon0: 60\narcs: yes\n- Almaty | pilot since March | 43.2 | 76.9\n- Frankfurt | data centre | 50.1 | 8.7\n- Singapore | second pilot | 1.35 | 103.8")
def globe(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lat0, lon0 = number(s.prop("lat0")) or 25.0, number(s.prop("lon0")) or 60.0
    r = min(2.05, (h - 0.2) / 2)
    gx, gy = x + r + 0.3, y + 0.1 + (h - 0.1) / 2
    shapes3d.wire_globe(c, gx, gy, r, accent=c.t.c("accent"), lat0=lat0, lon0=lon0)
    rows = []
    for it in s.items[:5]:
        place, note, la, lo = cells(it, 4)[:4]
        la, lo = number(la), number(lo)
        rows.append((place, note, la, lo))
    pins = []
    for place, note, la, lo in rows:
        if la is None or lo is None:
            pins.append(None)
            continue
        px, py, vis = shapes3d.project_globe(la, lo, lat0, lon0, r)
        pins.append((gx + px, gy + py) if vis else None)
    if s.prop("arcs", "").lower() in ("yes", "true", "on"):
        for (a, b) in zip(rows, rows[1:]):
            if None in (a[2], a[3], b[2], b[3]):
                continue
            prev = None
            for k in range(0, 21):
                la, lo = _slerp((a[2], a[3]), (b[2], b[3]), k / 20)
                px, py, vis = shapes3d.project_globe(la, lo, lat0, lon0, r * (1 + 0.14 * math.sin(math.pi * k / 20)))
                cur = (gx + px, gy + py) if vis else None
                if prev and cur:
                    c.line(prev[0], prev[1], cur[0], cur[1], c.t.c("accent"), 2.0)
                prev = cur
    lx = x + 2 * r + 1.4
    rh = min(0.95, (h - 0.2) / max(len(rows), 1))
    for k, ((place, note, _la, _lo), pin) in enumerate(zip(rows, pins)):
        ry = y + 0.25 + k * rh
        if pin:
            c.line(pin[0], pin[1], lx - 0.2, ry + 0.3, color.mix(c.t.c("bg"), c.t.c("accent"), 0.55), 1.0)
            c.rect(pin[0] - 0.07, pin[1] - 0.07, 0.14, 0.14, "accent", kind="ellipse")
            c.rect(pin[0] - 0.16, pin[1] - 0.16, 0.32, 0.32, None, c.t.c("accent"), 1.0, "ellipse")
        c.box(lx, ry, w - (lx - x), rh - 0.14, fill="surface", shadow=False, radius=0.08)
        c.fit_text(lx + 0.25, ry + 0.04, w - (lx - x) - 0.5, (rh - 0.14) * 0.5, place, 19, 12, "text", "heading", True, valign="middle")
        c.fit_text(lx + 0.25, ry + (rh - 0.14) * 0.5, w - (lx - x) - 0.5, (rh - 0.14) * 0.42, note + ("" if pin else "  (far side)"), 14, 11, "muted", valign="top")


@layout("orbit", "visual", "Orbit diagram: one concept in the middle and up to eight related parts on tilted rings, listed beside it.", 60,
        accepts="items: `Part | note` (up to eight); props: center (the middle label)",
        example="# One platform, six parts around it\nlayout: orbit\ncenter: Platform\n- Ingest | streams in\n- Store | keeps history\n- Score | models\n- Serve | APIs\n- Watch | monitoring\n- Learn | retraining")
def orbit(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 2)[:2] for i in s.items[:8]]
    n = max(len(rows), 1)
    cx, cy = x + 3.7, y + 0.1 + (h - 0.1) / 2
    ring = color.mix(c.t.c("bg"), c.t.c("text"), 0.22)
    radii = [(1.95, 1.12), (3.3, 1.78)] if n > 3 else [(2.4, 1.3)]
    for rx, ry in radii:
        c.rect(cx - rx, cy - ry, 2 * rx, 2 * ry, None, ring, 1.0, "ellipse")
    c.rect(cx - 0.68, cy - 0.68, 1.36, 1.36, "primary", kind="ellipse")
    c.rect(cx - 0.8, cy - 0.8, 1.6, 1.6, None, c.t.c("primary"), 1.0, "ellipse")
    c.fit_text(cx - 0.55, cy - 0.4, 1.1, 0.8, s.prop("center") or s.title, 16, 10, c.t.on("primary"), "heading", True, "center", "middle")
    inner = [i for i in range(n) if i % 2 == 0] if len(radii) == 2 else list(range(n))
    outer = [i for i in range(n) if i % 2 == 1] if len(radii) == 2 else []
    palette = c.t.series
    for ring_idx, members in ((0, inner), (1, outer)):
        if not members:
            continue
        rx, ry = radii[ring_idx]
        for j, i in enumerate(members):
            ang = 2 * math.pi * j / len(members) + (0.5 if ring_idx else -0.6)
            px, py = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
            col = palette[i % len(palette)]
            c.rect(px - 0.3, py - 0.3, 0.6, 0.6, col, kind="ellipse")
            c.text(px - 0.3, py - 0.3, 0.6, 0.6, str(i + 1), 16, c.t.on(col), "heading", True, "center", "middle", 1.0)
    lx = x + 7.9
    rh = min(0.62, (h - 0.2) / max(n, 1))
    for i, (name, note) in enumerate(rows):
        ry = y + 0.2 + i * rh
        col = palette[i % len(palette)]
        c.rect(lx, ry + rh / 2 - 0.13, 0.26, 0.26, col, kind="ellipse")
        c.fit_text(lx + 0.45, ry, 1.5, rh, name, 16, 11, "text", "body", True, valign="middle")
        c.fit_text(lx + 2.0, ry, w - (lx - x) - 2.0, rh, note, 14, 11, "muted", valign="middle")


@layout("gauges", "visual", "Radial gauges: up to four rings that fill to a value out of a maximum, with the number in the middle.", 50,
        accepts="items: `Label | value | maximum | note` (up to four); the ring fills to value over maximum; set `source:`",
        example="# Three of four service goals are nearly met\nlayout: gauges\nsource: ops/sla.csv\n- Uptime | 99.6 | 100 | goal 99.9\n- Alert delay | 80 | 100 | share under 2 s\n- Coverage | 62 | 100 | merchants scored\n- Satisfaction | 4.4 | 5 | analyst survey")
def gauges(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 4)[:4] for i in s.items[:4]]
    n = max(len(rows), 1)
    cw = w / n
    r_out = min(1.25, cw / 2 - 0.2)
    thick = 0.26
    cy = y + 0.2 + r_out + 0.25
    for i, (label, value, mx, note) in enumerate(rows):
        cx = x + cw * (i + 0.5)
        v, m = number(value), number(mx)
        frac = max(0.0, min(1.0, (v / m) if v is not None and m else 0.0))
        shapes3d.arc_ring(c, cx, cy, r_out, r_out - thick, -135, 135, _track(c))
        if frac > 0.005:
            tone = "success" if frac >= 0.9 else "accent" if frac >= 0.6 else "warning"
            shapes3d.arc_ring(c, cx, cy, r_out, r_out - thick, -135, -135 + 270 * frac, tone)
        size = textfit.fit_line(c.t, value, "heading", 2 * (r_out - thick) - 0.2, 40 * c.style["heading_scale"], 16, True)
        c.text(cx - r_out + thick, cy - 0.35, 2 * (r_out - thick), 0.7, value, size, "text", "heading", True, "center", "middle", 1.0)
        c.fit_text(cx - cw / 2 + 0.15, cy + r_out + 0.15, cw - 0.3, 0.45, label, 18, 12, "text", "body", True, "center", "middle")
        c.fit_text(cx - cw / 2 + 0.15, cy + r_out + 0.62, cw - 0.3, 0.6, note, 14, 11, "muted", align="center")


# ---- bento ------------------------------------------------------------------------------------------------------

def _nums(text):
    out = []
    for part in text.split(","):
        n = number(part)
        if n is not None:
            out.append(n)
    return out


def _bento_slots(n, x, y, w, h, gap):
    cw, ch = (w - 3 * gap) / 4, (h - gap) / 2
    cell = lambda col, row, cs=1, rs=1: (x + col * (cw + gap), y + row * (ch + gap), cw * cs + gap * (cs - 1), ch * rs + gap * (rs - 1))
    if n <= 3:
        return [cell(0, 0, 2, 2), cell(2, 0, 2, 1), cell(2, 1, 2, 1)][:n]
    if n == 4:
        return [cell(0, 0, 2, 2), cell(2, 0), cell(3, 0), cell(2, 1, 2, 1)]
    if n == 5:
        return [cell(0, 0, 2, 2), cell(2, 0), cell(3, 0), cell(2, 1), cell(3, 1)]
    return [cell(0, 0, 2, 1), cell(2, 0), cell(3, 0), cell(0, 1), cell(1, 1), cell(2, 1, 2, 1)][:6]


@layout("bento", "visual", "Bento dashboard: three to six tiles of different sizes mixing big numbers, sparklines, mini bars, rings and a text note.", 60,
        accepts="items start with the tile kind: `stat | value | label | note`, `spark | label | 3,5,4,8 | value`, `bars | label | 4,7,3,9 | note`, `ring | 72 | label | note`, `text | headline | body`; the first tile is the biggest",
        example="# Adoption grew in every channel this quarter\nlayout: bento\nsource: bi/q3.xlsx\n- stat | 62% | weekly active users | up from 48%\n- spark | Sign-ups | 3,5,4,8,9,12 | 12 k\n- ring | 72 | trial to paid | target 70\n- bars | Tickets by week | 9,7,8,4,3 | falling\n- text | What changed | The guided start cut early drop-off.")
def bento(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    tiles = [cells(i, 4)[:4] for i in s.items[:6]]
    slots = _bento_slots(len(tiles), x, y + 0.1, w, h - 0.1, 0.22)
    for k, (cell, (tx, ty, tw, th)) in enumerate(zip(tiles, slots)):
        kind = cell[0].strip().lower()
        a, b, d = cell[1], cell[2], cell[3]
        big = tw > 4 and th > 3
        c.box(tx, ty, tw, th, fill="surface", line="primary" if k == 0 else "border")
        px, pw = tx + 0.25, tw - 0.5
        if kind == "stat":
            size = textfit.fit_line(c.t, a, "heading", pw, (84 if big else 44) * c.style["heading_scale"], 18, True)
            c.text(px, ty + 0.2, pw, th * 0.5, a, size, "accent", "heading", True, "left", "middle", 1.0)
            c.fit_text(px, ty + th * 0.55, pw, th * 0.22, b, 18 if big else 15, 11, "text", "body", True)
            c.fit_text(px, ty + th * 0.55 + th * 0.24, pw, th * 0.2, d, 14, 11, "muted")
        elif kind == "spark":
            c.text(px, ty + 0.15, pw, 0.3, a.upper(), 11, "muted", "mono", True, chrome=True)
            c.text(px, ty + 0.45, pw, 0.6, d or "", 28 if not big else 40, "text", "heading", True, "left", "middle", 1.0)
            vals = _nums(b)
            shapes3d.sparkline(c, px, ty + th * 0.5, pw, th * 0.38, vals, c.t.c("accent"), 2.5)
        elif kind == "bars":
            c.text(px, ty + 0.15, pw, 0.3, a.upper(), 11, "muted", "mono", True, chrome=True)
            vals = _nums(b)
            top = max(vals) if vals else 1
            n = max(len(vals), 1)
            bh = th - 1.15
            bw = pw / n
            for i, v in enumerate(vals):
                hh = max(0.06, v / top * bh)
                c.rect(px + i * bw + bw * 0.12, ty + 0.55 + bh - hh, bw * 0.76, hh, "accent" if i == len(vals) - 1 else "primary", kind="round", radius=0.04)
            c.fit_text(px, ty + th - 0.5, pw, 0.35, d, 13, 11, "muted", valign="middle")
        elif kind == "ring":
            frac = max(0.0, min(1.0, (number(a) or 0) / 100.0))
            narrow = tw < 3.8                                    # a small tile: ring on top, label under it
            r = min(th * 0.27, tw * 0.3) if narrow else min(th / 2 - 0.35, tw * 0.24)
            rx, ry = (tx + tw / 2, ty + 0.2 + r) if narrow else (tx + 0.3 + r, ty + th / 2)
            shapes3d.arc_ring(c, rx, ry, r, r * 0.74, 0, 359.9, _track(c))
            if frac > 0.005:
                shapes3d.arc_ring(c, rx, ry, r, r * 0.74, 0, 360 * min(frac, 0.999), "accent")
            c.text(rx - r * 0.74, ry - 0.3, 2 * r * 0.74, 0.6, a + ("%" if "%" not in a else ""), 24, "text", "heading", True, "center", "middle", 1.0)
            if narrow:
                c.fit_text(px, ry + r + 0.1, pw, ty + th - (ry + r + 0.1) - 0.12, b + ("\n" + d if d else ""), 14, 11, "text", align="center", valign="top")
            else:
                c.fit_text(rx + r + 0.2, ty + 0.3, tx + tw - (rx + r + 0.2) - 0.2, th - 0.6, b + ("\n" + d if d else ""), 15, 11, "text", valign="middle")
        else:  # text
            c.fit_text(px, ty + 0.2, pw, 0.9, a, 22 if big else 18, 12, "text", "heading", True)
            c.fit_text(px, ty + 1.1, pw, th - 1.3, b, 16, 11, "muted")


# ---- treemap, sankey, network, activity -------------------------------------------------------------------------------

@layout("treemap", "visual", "Treemap: up to twelve areas sized by value, labelled with a name and the number; for composition and shares.", 60,
        accepts="items: `Name | value | note` (up to twelve, areas follow the values); set `source:`",
        example="# Two thirds of the loss sits in three categories\nlayout: treemap\nsource: finance/loss.csv\n- Card not present | 420\n- Account takeover | 260\n- Refund abuse | 180\n- Chargebacks | 120\n- Other | 90")
def treemap(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = sorted([cells(i, 3)[:3] for i in s.items[:12]], key=lambda r: -(number(r[1]) or 0))
    vals = [max(number(r[1]) or 0, 0.0001) for r in rows]
    foot = 0.55 if s.paragraphs else 0
    rects = shapes3d.squarify(vals, x, y + 0.1, w, h - 0.1 - foot)
    palette = c.t.series
    gap = 0.05
    for i, ((name, value, note), (rx, ry, rw, rh)) in enumerate(zip(rows, rects)):
        col = palette[i % len(palette)] if i else "accent"
        kind = "rect" if c.style["corner"] == "square" else "round"
        c.rect(rx + gap, ry + gap, rw - 2 * gap, rh - 2 * gap, col, None, 1.0, kind, 0.08)
        on = c.t.on(col)
        if rw > 1.0 and rh > 0.7:
            c.fit_text(rx + 0.18, ry + 0.14, rw - 0.36, min(0.5, rh * 0.4), name, 18, 11, on, "body", True, valign="top")
            c.fit_text(rx + 0.18, ry + 0.14 + min(0.5, rh * 0.4), rw - 0.36, min(0.7, rh * 0.4), value, 28 if rw > 2.2 else 20, 12, on, "heading", True, valign="top", line_h=1.0)
            if note and rh > 1.5:
                c.fit_text(rx + 0.18, ry + rh - 0.7, rw - 0.36, 0.55, note, 13, 11, on, valign="bottom")
    if foot:
        c.fit_text(x, y + h - foot, w, foot, s.paragraphs[0], 18, 12, "muted", valign="middle")


@layout("sankey", "visual", "Sankey flow: bands of different width carry a quantity from sources through steps to outcomes.", 60,
        accepts="items: `Source | Target | value` (up to ten flows); steps are found from the links, left to right; set `source:`",
        example="# Most trial users never reach a paid plan\nlayout: sankey\nsource: crm/export.csv\n- Visitors | Trial | 4200\n- Visitors | Left | 5800\n- Trial | Paid | 1100\n- Trial | Free | 1400\n- Trial | Left | 1700")
def sankey(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    links = []
    for it in s.items[:10]:
        a, b, v = cells(it, 3)[:3]
        if a and b and (number(v) or 0) > 0:
            links.append((a.strip(), b.strip(), number(v)))
    if not links:
        c.scene.problems.append("[Medium] sankey has no flows: use items `Source | Target | number`")
        return
    nodes, level = [], {}
    for a, b, _v in links:
        for nm in (a, b):
            if nm not in nodes:
                nodes.append(nm)
    for _ in range(len(nodes)):                  # longest path from a source
        for a, b, _v in links:
            level[a] = level.get(a, 0)
            level[b] = max(level.get(b, 0), level[a] + 1)
    ncol = max(level.values(), default=0) + 1
    outs = {n_: sum(v for a, _b, v in links if a == n_) for n_ in nodes}
    ins = {n_: sum(v for _a, b, v in links if b == n_) for n_ in nodes}
    tot = {n_: max(outs[n_], ins[n_]) for n_ in nodes}
    cols = [[n_ for n_ in nodes if level[n_] == k] for k in range(ncol)]
    avail = h - 0.4
    gap = 0.22
    scale = min((avail - gap * (len(col) - 1)) / max(sum(tot[n_] for n_ in col), 1e-9) for col in cols if col)
    min_h = 0.5                                     # a node's label slot never gets thinner than two lines of text
    for _ in range(40):
        if all(sum(max(tot[n_] * scale, min_h) for n_ in col) + gap * (len(col) - 1) <= avail for col in cols):
            break
        scale *= 0.93
    nw = 0.24
    lab = 2.0 if ncol > 1 else 0
    x0, x1 = x + lab, x + w - lab - nw
    pos = {}
    for k, col in enumerate(cols):
        slots = [max(tot[n_] * scale, min_h) for n_ in col]
        yy = y + 0.1 + (avail - (sum(slots) + gap * (len(col) - 1))) / 2
        cx_ = x0 + (x1 - x0) * (k / max(ncol - 1, 1))
        for n_, sh in zip(col, slots):
            nh = tot[n_] * scale
            pos[n_] = (cx_, yy + (sh - nh) / 2, nh, yy, sh)        # x, node top, node height, label slot top, slot height
            yy += sh + gap
    palette = c.t.series
    color_of = {n_: palette[i % len(palette)] for i, n_ in enumerate(nodes)}
    by_src = {n_: sorted([l_ for l_ in links if l_[0] == n_], key=lambda l_: pos[l_[1]][1]) for n_ in nodes}
    by_dst = {n_: sorted([l_ for l_ in links if l_[1] == n_], key=lambda l_: pos[l_[0]][1]) for n_ in nodes}
    for a, b, v in links:
        bh = v * scale
        sy = pos[a][1] + sum(l_[2] for l_ in by_src[a][:by_src[a].index((a, b, v))]) * scale
        ty = pos[b][1] + sum(l_[2] for l_ in by_dst[b][:by_dst[b].index((a, b, v))]) * scale
        c.poly(shapes3d.band(pos[a][0] + nw, sy, sy + bh, pos[b][0], ty, ty + bh), color_of[a], None, 1.0, 0.38)
    for n_ in nodes:
        nx, ny, nh, sy_, sh = pos[n_]
        c.rect(nx, ny, nw, max(nh, 0.04), color_of[n_])
        first, last = level[n_] == 0, level[n_] == ncol - 1
        label = f"{n_}"
        val = f"{tot[n_]:,.0f}".replace(",", " ") if tot[n_] >= 1000 else f"{tot[n_]:g}"
        if first:
            c.fit_text(x, sy_, lab - 0.15, sh, f"{label}\n{val}", 15, 11, "text", "body", True, "right", "middle")
        elif last:
            c.fit_text(nx + nw + 0.15, sy_, lab - 0.15, sh, f"{label}\n{val}", 15, 11, "text", "body", True, "left", "middle")
        else:   # a middle column: the label sits on an opaque chip so the bands behind it cannot lower its contrast
            text = f"{label}  {val}"
            cw_ = textfit.width_in(c.t, text, "body", 14, True) + 0.3
            c.rect(nx + nw / 2 - cw_ / 2, ny - 0.52, cw_, 0.4, c.t.c("bg"), None, 1.0, "rect" if c.style["corner"] == "square" else "round", 0.1)
            c.fit_text(nx + nw / 2 - cw_ / 2, ny - 0.52, cw_, 0.4, text, 14, 11, "text", "body", True, "center", "middle")


@layout("network", "visual", "Network graph: nodes joined by links, the best-connected node in the middle; for dependencies, teams and data flows.", 50,
        accepts="items: `A -> B` or `A -> B | label` (up to fourteen links); props: takeaway (side panel text)",
        example="# Everything depends on the feature store\nlayout: network\ntakeaway: One shared store feeds every model; protect it first.\n- Events -> Feature store\n- Features API -> Feature store\n- Feature store -> Fraud model\n- Feature store -> Churn model\n- Fraud model -> Alerts\n- Churn model -> Campaigns")
def network(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    edges = []
    for it in s.items[:14]:
        text = it.text.split("|")[0]
        sep = "->" if "->" in text else ">" if ">" in text else None
        if not sep:
            continue
        a, b = (p.strip() for p in text.split(sep, 1))
        if a and b:
            edges.append((a, b))
    nodes = []
    for a, b in edges:
        for nm in (a, b):
            if nm not in nodes:
                nodes.append(nm)
    deg = {n_: sum(1 for a, b in edges if n_ in (a, b)) for n_ in nodes}
    order = sorted(nodes, key=lambda n_: (-deg[n_], nodes.index(n_)))
    pw = 3.4 if s.prop("takeaway") else 0
    dw = w - pw - (0.3 if pw else 0)
    cx, cy = x + dw / 2, y + 0.1 + (h - 0.1) / 2
    pos, ang = {}, {}
    if order:
        pos[order[0]] = (cx, cy)
        rest = order[1:]
        inner, outer = rest[:7], rest[7:]
        for ringset, rx, ry, off in ((inner, dw * 0.30, (h - 1.2) * 0.42, 0.45), (outer, dw * 0.43, (h - 1.0) * 0.5, 0.9)):
            for j, nm in enumerate(ringset):
                a_ = 2 * math.pi * j / max(len(ringset), 1) + off
                ang[nm] = a_
                pos[nm] = (cx + rx * math.cos(a_), cy + ry * math.sin(a_))
    edge_col = color.mix(c.t.c("bg"), c.t.c("text"), 0.38)
    for a_, b_ in edges:
        c.line(pos[a_][0], pos[a_][1], pos[b_][0], pos[b_][1], edge_col, 1.5)
    palette = c.t.series
    for i, nm in enumerate(nodes):
        px, py = pos[nm]
        r = min(0.5, 0.2 + 0.07 * deg[nm])
        hub = nm == order[0]
        col = "accent" if hub else palette[i % len(palette)]
        c.rect(px - r - 0.06, py - r - 0.06, 2 * r + 0.12, 2 * r + 0.12, col, kind="ellipse", alpha=0.22)
        c.rect(px - r, py - r, 2 * r, 2 * r, col, kind="ellipse")
        tw = 1.9
        dx, dy = (math.cos(ang[nm]), math.sin(ang[nm])) if nm in ang else (0.0, 1.0)
        if abs(dx) < 0.4:                                    # above or below the node
            ly = py + r + 0.08 if dy > 0 else py - r - 0.48
            c.fit_text(px - tw / 2, ly, tw, 0.4, nm, 15, 11, "text", "body", True, "center", "middle")
        elif dx > 0:
            c.fit_text(px + r + 0.1, py - 0.2, tw, 0.4, nm, 15, 11, "text", "body", True, "left", "middle")
        else:
            c.fit_text(px - r - 0.1 - tw, py - 0.2, tw, 0.4, nm, 15, 11, "text", "body", True, "right", "middle")
    if pw:
        px = x + dw + 0.3
        c.box(px, y + 0.1, pw, h - 0.1, fill="surface", line="accent")
        c.pill(px + 0.3, y + 0.35, "WHAT IT SHOWS", fill="bg", col="accent", size=11)
        c.fit_text(px + 0.3, y + 1.0, pw - 0.6, 2.3, s.prop("takeaway"), 21, 13, "text", "body", True)
        if order:
            c.text(px + 0.3, y + h - 1.15, pw - 0.6, 0.3, "HUB", 11, "muted", "mono", True, chrome=True)
            c.fit_text(px + 0.3, y + h - 0.85, pw - 0.6, 0.6, f"{order[0]}: {deg[order[0]]} links", 18, 12, "accent", "heading", True)


@layout("activity_grid", "visual", "Activity grid: one small square per day in weeks, shaded by value, with a few headline numbers beside it.", 40,
        accepts="props: values (a comma list, seven per week, up to 26 weeks), caption; items: `value | label` (up to three side cards); set `source:`",
        example="# Commits kept climbing through the last weekend\nlayout: activity_grid\nsource: git/log.csv\nvalues: 0,2,1,3,2,0,0,1,4,3,5,2,1,0,2,3,6,5,7,4,2,1,3,8,9,12,10,6,2,1,0,4,7,9,11,3,5,6,8,10,12,14,4,2,3,9,13,15,16,5,1,0,6,11,14,17,19,8,2,1,7,12,15,18,21,9,3,2,9,14,18,20,24,12,4,1,5,13,17,22,26,15\ncaption: Commits per day, twelve weeks\n- 62 | commits in the last 4 days\n- 4 | people committing daily")
def activity_grid(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    vals = [number(v) or 0 for v in s.prop("values").split(",") if v.strip()][:182]
    vals += [0] * (-len(vals) % 7)
    weeks = max(len(vals) // 7, 1)
    side = 3.4 if s.items else 0
    gw = w - side - (0.4 if side else 0)
    cw = min(0.62, (gw - 0.7) / weeks - 0.05)
    cell = min(0.46, (h - 1.5) / 7 - 0.05)
    top = max(vals) or 1
    gx, gy = x + 0.7, y + 0.5
    for d, name in ((0, "Mon"), (2, "Wed"), (4, "Fri")):
        c.text(x, gy + d * (cell + 0.05), 0.65, cell, name, 11, "muted", "mono", False, "right", "middle", chrome=True)
    base = _track(c, 0.1)
    for wk in range(weeks):
        for d in range(7):
            v = vals[wk * 7 + d]
            k = 0 if v <= 0 else min(4, 1 + int(3.999 * v / top))
            fill = base if k == 0 else color.mix(c.t.c("bg"), c.t.c("accent"), (0.25, 0.45, 0.7, 1.0)[k - 1])
            c.rect(gx + wk * (cw + 0.05), gy + d * (cell + 0.05), cw, cell, fill, kind="rect" if c.style["corner"] == "square" else "round", radius=0.05)
    ly = gy + 7 * (cell + 0.05) + 0.12
    c.text(gx, ly, 0.6, 0.3, "Less", 11, "muted", "mono", chrome=True, valign="middle")
    for k in range(5):
        fill = base if k == 0 else color.mix(c.t.c("bg"), c.t.c("accent"), (0.25, 0.45, 0.7, 1.0)[k - 1])
        c.rect(gx + 0.6 + k * 0.3, ly + 0.03, 0.24, 0.24, fill, kind="round", radius=0.04)
    c.text(gx + 2.2, ly, 0.6, 0.3, "More", 11, "muted", "mono", chrome=True, valign="middle")
    if s.prop("caption"):
        c.fit_text(gx + 3.2, ly, gw - 3.4, 0.3, s.prop("caption"), 13, 11, "muted", valign="middle")
    if side:
        sx = x + gw + 0.4
        rows = [cells(i, 2)[:2] for i in s.items[:3]]
        rh = (h - 0.1 - 0.2 * (len(rows) - 1)) / max(len(rows), 1)
        for k, (num, label) in enumerate(rows):
            yy = y + 0.1 + k * (rh + 0.2)
            c.box(sx, yy, side, rh, fill="surface", line="primary" if k == 0 else "border")
            size = textfit.fit_line(c.t, num, "heading", side - 0.5, 56 * c.style["heading_scale"], 18, True)
            c.text(sx + 0.25, yy + 0.15, side - 0.5, rh * 0.5, num, size, "accent", "heading", True, "left", "middle", 1.0)
            c.fit_text(sx + 0.25, yy + rh * 0.62, side - 0.5, rh * 0.32, label, 15, 11, "text")


# ---- terminal and 3D hero -----------------------------------------------------------------------------------------

@layout("terminal", "visual", "Terminal window: a command line session with colored prompts, results and errors; for demos, builds and tool talks.", 70,
        accepts="a fenced code block (or items) with one line per row: `$ command`, `# comment`, lines with OK, PASS, WARN or ERROR are colored; props: window (the title bar text), takeaway",
        example="# One command builds, lints and ships the deck\nlayout: terminal\nwindow: deck-master\ntakeaway: Lint blocks the build until the findings are fixed.\n```\n$ python scripts/cli.py lint deck.md\n[High] slide 4: text overflows its box\nERROR 1 blocking finding\n$ python scripts/cli.py build deck.md --pptx --pdf\nOK wrote deck.pptx and deck.pdf\n```")
def terminal(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lines = [ln for ln in (s.code.split("\n") if s.code else [i.text for i in s.items]) if ln.strip() != ""][:14]
    foot = 0.7 if s.prop("takeaway") else 0
    top, ch = y + 0.1, h - 0.1 - foot
    term_bg = color.mix(c.t.c("bg"), "#000000", 0.45) if c.t.mode == "dark" else color.mix(c.t.c("surface"), c.t.c("text"), 0.05)
    c.rect(x, top, w, ch, term_bg, None, 1.0, "rect" if c.style["corner"] == "square" else "round", 0.12)
    bar = color.mix(term_bg, c.t.c("text"), 0.12)
    c.rect(x, top, w, 0.45, bar, None, 1.0, "rect")
    for i, tone in enumerate(("danger", "warning", "success")):
        c.rect(x + 0.2 + i * 0.28, top + 0.14, 0.17, 0.17, tone, kind="ellipse")
    c.text(x + 1.2, top, w - 2.4, 0.45, s.prop("window") or "terminal", 12, c.t.on(bar), "mono", True, "center", "middle", chrome=True)
    on_term = c.t.on(term_bg)
    size = 20
    while size > 11:
        wide = max((textfit.width_in(c.t, ln, "mono", size) for ln in lines), default=0)
        if wide <= w - 0.9 and len(lines) * size * 1.45 / 72 <= ch - 0.9:
            break
        size -= 1
    lh = size * 1.45 / 72
    ty = top + 0.65
    for ln in lines:
        stripped = ln.strip()
        up = stripped.upper()
        if stripped.startswith(("$", ">")):
            c.text(x + 0.3, ty, 0.4, lh, stripped[0], size, "accent", "mono", True, valign="middle")
            c.text(x + 0.3 + textfit.width_in(c.t, "$ ", "mono", size), ty, w - 1.0, lh, stripped[1:].strip(), size, on_term, "mono", False, valign="middle")
        else:
            col = "muted" if stripped.startswith("#") else "danger" if ("ERROR" in up or "FAIL" in up) else "warning" if "WARN" in up or stripped.startswith("[High") \
                else "success" if ("OK" in up.split() or "PASS" in up or "DONE" in up) else on_term
            c.text(x + 0.3, ty, w - 0.6, lh, stripped, size, col, "mono", False, valign="middle")
        ty += lh
    c.rect(x + 0.3, ty + lh * 0.2, size / 72 * 0.55, lh * 0.65, "accent", alpha=0.9)
    if foot:
        c.fit_text(x, y + h - foot + 0.1, w, foot - 0.1, s.prop("takeaway"), 18, 12, "muted", valign="middle")


@layout("hero_3d", "visual", "A shaded 3D object (orbs, ring, cube or slab stack) in the theme colors beside a short message and up to four points.", 45,
        accepts="props: object (orbs, ring, cube or stack), eyebrow; first paragraph: the lede; items: up to four points; needs the charts requirements group",
        example="# Layers you can see, not just describe\nlayout: hero_3d\nobject: stack\nA stack of independent layers, each replaceable.\n- Interface\n- Service\n- Model\n- Data")
def hero_3d(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    kind = s.prop("object", "orbs")
    iw = min(h, 4.7)
    ix = x + w - iw + 0.1
    try:
        from ..charts.render3d import render_hero
        from ..core.scene import Image
        c.items.append(Image(ix, y + 0.05, iw, iw, render_hero(c.t, kind, c.deck)))
    except Exception as e:
        c.scene.problems.append(f"[Low] 3D object not drawn ({type(e).__name__}: {e}); install scripts/requirements/charts.txt")
    tw = w - iw - 0.4
    yy = y + 0.1
    if s.paragraphs:
        c.fit_text(x, yy, tw, 1.3, s.paragraphs[0], 24, 14, "text", "heading", True)
        yy += 1.5
    flow(c, s.items[:4], x, yy, tw, y + h - yy, max_size=22, min_size=14, gap=0.3)
