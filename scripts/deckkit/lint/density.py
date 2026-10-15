from ..core import layout as layout_registry
from ..core import textfit
from ..core.scene import Text
from .common import finding

FRAME = {"title", "closing", "agenda"}


def check(deck, scenes, theme):
    out = []
    for sc, slide in zip(scenes, deck.slides):
        spec = layout_registry.get(slide.layout)
        words = sum(textfit.word_count(it.text) for it in sc.items if isinstance(it, Text) and not it.chrome)
        if spec and words > spec.max_words:
            out.append(finding("Medium", sc, f"{words} words on the slide, layout {spec.name} is designed for up to "
                                             f"{spec.max_words}; cut text or move detail to notes or an appendix"))
        n_words = textfit.word_count(slide.title)
        if n_words > 16 or len(slide.title) > 110:
            out.append(finding("Medium", sc, f"title has {n_words} words; keep the takeaway under about 14"))
        elif n_words <= 2 and slide.layout not in FRAME and len(deck.slides) > 3:
            out.append(finding("Low", sc, f"title {slide.title!r} is a label; state the takeaway as a sentence"))
        if len(slide.items) > 7 and slide.layout in {"bullets", "problem", "solution", "impact"}:
            out.append(finding("Medium", sc, f"{len(slide.items)} bullets; show at most 7 and split or cut"))
    return out
