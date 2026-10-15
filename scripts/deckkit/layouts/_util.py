"""Helpers shared by layouts."""
from ..core import textfit


def cells(item, n=0):
    """Item cells split on ` | `, padded with empty strings to at least n entries."""
    parts = list(item.cells) if item.cells else [item.text]
    return parts + [""] * (n - len(parts))


def layer_items(items):
    """`Layer: A, B, C` -> [(layer, [A, B, C])]; items without a colon become single-component rows."""
    out = []
    for it in items:
        if ":" in it.text:
            head, rest = it.text.split(":", 1)
            out.append((head.strip(), [p.strip() for p in rest.split(",") if p.strip()]))
        else:
            out.append((it.text.strip(), []))
    return out


def initials(name):
    parts = [p for p in name.replace("**", "").split() if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"


def flow(c, items, x, y, w, h, max_size=22, min_size=13, gap=0.2, marker="square", marker_col="accent", col="text",
         line_h=1.25):
    """Stack text items top to bottom with a marker each, shrinking the font until everything fits h.
    Returns (size, bottom_y)."""
    indent = 0.34
    t = c.t
    size = max_size
    while True:
        total, wrapped = 0.0, []
        for it in items:
            text = it if isinstance(it, str) else it.text
            lines = textfit.wrap(t, text, "body", size, w - indent)
            hh = textfit.height_in(len(lines), size, line_h)
            wrapped.append((text, hh))
            total += hh
        total += gap * max(0, len(items) - 1)
        if total <= h or size <= min_size:
            break
        size -= 1
    cy = y
    for i, (text, hh) in enumerate(wrapped):
        mk = 0.12
        first = size * line_h / 72
        my = cy + first / 2 - mk / 2
        if marker == "number":
            c.text(x, cy, indent, first, f"{i + 1}", size, marker_col, "mono", True, "left", "top", line_h)
        elif c.pixel:
            c.rect(x, my, mk, mk, marker_col)
        else:
            c.rect(x, my, mk, mk, marker_col, kind="round", radius=0.03)
        c.text(x + indent, cy, w - indent, hh, text, size, col, "body", False, "left", "top", line_h)
        cy += hh + gap
    return size, cy - gap
