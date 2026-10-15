"""Leftover template placeholders such as `<one line: what it does>` or `<n>`."""
import re

from .common import finding

PLACEHOLDER = re.compile(r"(?<![\w])<[A-Za-z][^<>\n]*>(?![\w])")


def check(deck, scenes, theme):
    out = []
    for sc, slide in zip(scenes, deck.slides):
        fields = [("title", slide.title), ("notes", slide.notes), *[("text", p) for p in slide.paragraphs]]
        fields += [("bullet", i.text) for i in slide.items] + [("cell", c) for row in slide.table for c in row]
        fields += [(k, v) for k, v in slide.props.items() if k != "notes"]
        hits = [m.group(0) for _, v in fields for m in PLACEHOLDER.finditer(str(v))]
        if hits:
            out.append(finding("High", sc, f"unfilled placeholder {hits[0]!r}" + (f" and {len(hits) - 1} more" if len(hits) > 1 else "")))
    meta_hits = [m.group(0) for v in deck.meta.values() if isinstance(v, (str, int, float)) for m in PLACEHOLDER.finditer(str(v))]
    if meta_hits:
        out.append(finding("High", None, f"unfilled placeholder in the front matter: {meta_hits[0]!r}"))
    return out
