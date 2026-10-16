"""Geometry helpers for 3D-looking and advanced-visual components. They draw flat vector shapes (rect, ellipse, polygon, line)
through a Canvas, so PPTX and PDF stay editable and identical. All sizes are in inches.

- isometric boxes (a slab or a column seen from above at 30 degrees), oblique boxes (a podium block),
- ring segments for gauges, wireframe globes with orthographic pins, squarified treemaps, smooth bands for flows.
"""
import math

from . import color

COS30, SIN30 = math.cos(math.radians(30)), 0.5


def shade(hex_fill, kind):
    """Face colors of a lit box: the top is lightest, the left face mid, the right face darkest."""
    return {"top": color.lighten(hex_fill, 0.22), "left": hex_fill, "right": color.darken(hex_fill, 0.28)}[kind]


def iso_box(c, ox, oy, a, b, h, fill, alpha=1.0, line=None):
    """An isometric box. (ox, oy) is the back corner of the top face; `a` runs right-down, `b` runs left-down, `h` is the height.
    Returns the points of the front corner, the right corner and the left corner of the top face, and the bounding box."""
    ex, ey = (COS30, SIN30), (-COS30, SIN30)
    back = (ox, oy)
    right = (ox + a * ex[0], oy + a * ex[1])
    left = (ox + b * ey[0], oy + b * ey[1])
    front = (right[0] + b * ey[0], right[1] + b * ey[1])
    f = c.t.c(fill)
    c.poly([left, front, (front[0], front[1] + h), (left[0], left[1] + h)], shade(f, "left"), line, 0.75, alpha)
    c.poly([front, right, (right[0], right[1] + h), (front[0], front[1] + h)], shade(f, "right"), line, 0.75, alpha)
    c.poly([back, right, front, left], shade(f, "top"), line, 0.75, alpha)
    return {"back": back, "right": right, "front": front, "left": left, "h": h,
            "bbox": (left[0], oy, right[0] - left[0], front[1] + h - oy)}


def iso_width(a, b):
    """Horizontal extent of an isometric footprint."""
    return (a + b) * COS30


def iso_depth(a, b):
    """Vertical extent of the top face."""
    return (a + b) * SIN30


def oblique_box(c, x, y, w, h, depth, fill, alpha=1.0):
    """A front-facing block with a visible top and right side (podium, 3D column). (x, y) is the top-left of the front face."""
    f = c.t.c(fill)
    dx, dy = depth * 0.7, depth * 0.45
    c.poly([(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w, y)], shade(f, "top"), None, 1.0, alpha)
    c.poly([(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)], shade(f, "right"), None, 1.0, alpha)
    c.rect(x, y, w, h, f, alpha=alpha)
    return {"top": (x + dx / 2, y - dy), "front": (x, y, w, h)}


def ring_points(cx, cy, r_out, r_in, a0, a1, n=48):
    """Polygon of a ring segment. Angles are degrees clockwise from twelve o'clock."""
    a0, a1 = math.radians(a0), math.radians(a1)
    steps = max(2, int(n * abs(a1 - a0) / (2 * math.pi)) + 2)
    pts = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        pts.append((cx + r_out * math.sin(a), cy - r_out * math.cos(a)))
    for i in range(steps, -1, -1):
        a = a0 + (a1 - a0) * i / steps
        pts.append((cx + r_in * math.sin(a), cy - r_in * math.cos(a)))
    return pts


def arc_ring(c, cx, cy, r_out, r_in, a0, a1, fill, alpha=1.0):
    return c.poly(ring_points(cx, cy, r_out, r_in, a0, a1), fill, None, 1.0, alpha)


def bezier(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def band(x0, y0_top, y0_bot, x1, y1_top, y1_bot, n=24):
    """Polygon of a smooth flow band from (x0, y0) to (x1, y1), horizontal tangents at both ends."""
    mid = (x0 + x1) / 2
    top = bezier((x0, y0_top), (mid, y0_top), (mid, y1_top), (x1, y1_top), n)
    bot = bezier((x0, y0_bot), (mid, y0_bot), (mid, y1_bot), (x1, y1_bot), n)
    return top + bot[::-1]


def project_globe(lat, lon, lat0, lon0, r):
    """Orthographic projection of a point on a globe of radius r. Returns (x, y, visible) relative to the centre."""
    la, lo, la0, lo0 = (math.radians(v) for v in (lat, lon, lat0, lon0))
    cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
    x = r * math.cos(la) * math.sin(lo - lo0)
    y = r * (math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0))
    return x, -y, cosc > 0.02


def wire_globe(c, cx, cy, r, line=None, accent=None, lat0=20.0, lon0=60.0, meridians=8, parallels=5, width=0.8):
    """A wireframe globe: an outer ring, projected parallels and meridians as polylines (only the visible half)."""
    line = line or color.mix(c.t.c("bg"), c.t.c("text"), 0.28)
    c.rect(cx - r, cy - r, 2 * r, 2 * r, None, line, width * 1.4, "ellipse")
    for k in range(1, parallels + 1):                       # parallels
        lat = -90 + 180 * k / (parallels + 1)
        _polyline(c, [project_globe(lat, lon, lat0, lon0, r) for lon in range(-180, 181, 6)], cx, cy, line, width)
    for k in range(meridians):                              # meridians
        lon = -180 + 360 * k / meridians
        _polyline(c, [project_globe(lat, lon, lat0, lon0, r) for lat in range(-90, 91, 6)], cx, cy, line, width)
    if accent:
        _polyline(c, [project_globe(0, lon, lat0, lon0, r) for lon in range(-180, 181, 4)], cx, cy, accent, width * 1.6)


def _polyline(c, pts, cx, cy, col, width):
    prev = None
    for x, y, vis in pts:
        cur = (cx + x, cy + y) if vis else None
        if prev and cur:
            c.line(prev[0], prev[1], cur[0], cur[1], col, width)
        prev = cur


def squarify(values, x, y, w, h):
    """Squarified treemap: rectangles (x, y, w, h) for `values` (sorted descending is best), filling the box."""
    total = float(sum(values)) or 1.0
    areas = [v / total * w * h for v in values]
    rects, i = [], 0
    while i < len(areas):
        short = min(w, h)
        row, best = [], float("inf")
        while i < len(areas):
            cand = row + [areas[i]]
            worst = _worst(cand, short)
            if row and worst > best:
                break
            row, best = cand, worst
            i += 1
        s = sum(row)
        if w >= h:                                          # lay the row as a column on the left
            cw = s / h
            yy = y
            for a in row:
                rects.append((x, yy, cw, a / cw))
                yy += a / cw
            x, w = x + cw, w - cw
        else:                                               # lay the row along the top
            rh = s / w
            xx = x
            for a in row:
                rects.append((xx, y, a / rh, rh))
                xx += a / rh
            y, h = y + rh, h - rh
    return rects


def _worst(row, side):
    s = sum(row)
    return max(max(side * side * a / (s * s), s * s / (side * side * a)) for a in row)


def sparkline(c, x, y, w, h, values, col, width=2.0, fill_alpha=0.18, dot=True):
    """A small line chart of `values` scaled into the box, with a faint area and an end dot."""
    if len(values) < 2:
        return
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    pts = [(x + w * i / (len(values) - 1), y + h - (v - lo) / span * h) for i, v in enumerate(values)]
    if fill_alpha:
        c.poly(pts + [(x + w, y + h), (x, y + h)], col, None, 1.0, fill_alpha)
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, c.t.c(col), width)
    if dot:
        c.rect(pts[-1][0] - 0.06, pts[-1][1] - 0.06, 0.12, 0.12, col, kind="ellipse")
