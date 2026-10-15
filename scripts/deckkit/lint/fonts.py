from ..core.scene import Text
from ..core.textfit import missing_glyphs
from .common import finding


def check(deck, scenes, theme):
    out = []
    for sc in scenes:
        seen = set()
        for it in sc.items:
            if isinstance(it, Text):
                miss = missing_glyphs(theme, it.role, it.text, it.bold)
                new = [m for m in miss if (it.role, m) not in seen]
                seen.update((it.role, m) for m in miss)
                if new:
                    fam = theme.family(it.role)
                    out.append(finding("High", sc, f"font {fam} has no glyph for {' '.join(new[:8])!r}; "
                                                   f"use a font that covers this script (see design/typography.md)"))
    return out
