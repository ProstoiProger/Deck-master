from ..core import color
from ..core.scene import Image, Poly, Shape, Text
from .common import finding


def background_under(sc, index, text):
    """Fill color behind a text box: the last opaque shape that contains its center, else the slide background, with
    translucent shapes above that base blended in. Returns None when the text sits on an image."""
    cx, cy = text.x + text.w / 2, text.y + text.h / 2
    overlays = []
    base = sc.bg
    for it in reversed(sc.items[:index]):
        if isinstance(it, Image) and it.x <= cx <= it.x + it.w and it.y <= cy <= it.y + it.h:
            return None
        if isinstance(it, Shape) and it.fill and it.x <= cx <= it.x + it.w and it.y <= cy <= it.y + it.h:
            if it.alpha >= 0.85:
                base = it.fill
                break
            if it.alpha >= 0.3:
                overlays.append((it.fill, it.alpha))
        elif isinstance(it, Poly) and it.fill and it.alpha >= 0.85:
            bx, by, bw, bh = it.bbox
            if bx <= cx <= bx + bw and by <= cy <= by + bh:
                base = it.fill
                break
    for fill, alpha in reversed(overlays):
        base = color.mix(base, fill, alpha)
    return base


def check(deck, scenes, theme):
    out = []
    for sc in scenes:
        for i, it in enumerate(sc.items):
            if not isinstance(it, Text) or not it.text.strip():
                continue
            bg = background_under(sc, i, it)
            if bg is None:
                continue
            ratio = color.contrast(it.color, bg)
            large = it.size >= 18 or (it.bold and it.size >= 14)
            need = 3.0 if large else 4.5
            if ratio < need:
                out.append(finding("High", sc, f"contrast {ratio:.2f}:1 is below {need}:1 for {it.size:.0f} pt text "
                                               f"{it.color} on {bg}: {it.text[:30]!r}"))
    return out
