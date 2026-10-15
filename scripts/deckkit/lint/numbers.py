"""Number provenance: a claim number on a slide needs a `source:` (file, log row, brief page)."""
import re

from .common import finding

EXEMPT = {"title", "agenda", "team", "closing", "roadmap"}
CLAIM = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)?\s?%|\d+[.,]\d+|\d{3,}|\d+\s?(?:x|ms|s|k|m|b|min|h)\b)", re.IGNORECASE)
YEAR = re.compile(r"(19|20)\d{2}$")


def claims(text):
    found = []
    for m in CLAIM.finditer(text):
        tok = m.group(1).strip()
        if YEAR.fullmatch(tok):
            continue
        found.append(tok)
    return found


def check(deck, scenes, theme):
    out = []
    for sc, slide in zip(scenes, deck.slides):
        if slide.layout in EXEMPT or slide.source:
            continue
        blob = "\n".join([slide.text_blob(), slide.prop("stat"), slide.prop("takeaway")])
        nums = claims(blob)
        if nums:
            out.append(finding("High", sc, f"numbers {', '.join(dict.fromkeys(nums))[:60]} have no `source:`; "
                                           f"cite the run log, file or page, or remove them"))
    return out
