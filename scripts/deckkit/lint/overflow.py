from ..core import textfit
from ..core.scene import H, W, Image, Shape, Text
from .common import finding


def check(deck, scenes, theme):
    out = []
    for sc in scenes:
        for it in sc.items:
            if isinstance(it, Text):
                if not it.text.strip():
                    continue
                lines = textfit.wrap(theme, it.text, it.role, it.size, it.w, it.bold)
                need = textfit.height_in(len(lines), it.size, it.line_h)
                snippet = it.text.replace("\n", " ")[:40]
                if need > it.h * 1.04 + 0.03:
                    out.append(finding("High", sc, f"text overflows its box ({need:.2f} in needed, {it.h:.2f} in available): {snippet!r}"))
                elif textfit.widest_word(theme, it.text, it.role, it.size, it.bold) > it.w + 0.01:
                    out.append(finding("High", sc, f"a word is wider than its box: {snippet!r}"))
                floor = theme.style["min_font"] if it.role == "heading" else 11
                if it.size < floor - 0.01:
                    out.append(finding("Medium", sc, f"font {it.size:.0f} pt is below the {floor} pt minimum: {snippet!r}"))
            elif isinstance(it, (Shape, Image)):
                if isinstance(it, Shape) and it.alpha < 1:
                    continue  # decorative glow may bleed off the slide
                if it.x < -0.01 or it.y < -0.01 or it.x + it.w > W + 0.01 or it.y + it.h > H + 0.01:
                    out.append(finding("Medium", sc, f"element leaves the slide at ({it.x:.1f}, {it.y:.1f}, {it.w:.1f} x {it.h:.1f})"))
    return out
