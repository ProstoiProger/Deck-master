"""Text measuring and wrapping with the bundled fonts, shared by layouts, the PDF backend and lint.

Inline markup: `**bold**` toggles bold; `\\n` is a hard line break. Widths come from Pillow at a large reference size
so that fractional point sizes stay accurate.
"""
import re
from functools import lru_cache

REF = 200


@lru_cache(maxsize=32)
def _font(path):
    from PIL import ImageFont
    return ImageFont.truetype(str(path), REF)


@lru_cache(maxsize=32)
def _cmap(path):
    from fontTools.ttLib import TTFont
    return frozenset(TTFont(str(path)).getBestCmap())


def missing_glyphs(theme, role, text, bold=False):
    """Characters of text that the role's font file cannot draw."""
    have = _cmap(theme.font_file(role, bold))
    return sorted({ch for ch in str(text) if not ch.isspace() and ch != "*" and ord(ch) not in have})


def width_in(theme, text, role, size, bold=False):
    if not text:
        return 0.0
    return _font(theme.font_file(role, bold)).getlength(text) * size / REF / 72


def tokenize(text, bold=False):
    """Split into (word, bold) tokens; ('\\n', False) marks a hard break."""
    out = []
    for li, line in enumerate(str(text).split("\n")):
        if li:
            out.append(("\n", False))
        state = bold
        for i, part in enumerate(re.split(r"\*\*", line)):
            if i:
                state = not state
            for word in part.split():
                out.append((word, state))
    return out


def wrap(theme, text, role, size, width, bold=False):
    """Return a list of lines, each a list of (word, bold) tokens."""
    space = {}

    def sp(b):
        if b not in space:
            space[b] = width_in(theme, " ", role, size, b)
        return space[b]

    lines, cur, cur_w = [], [], 0.0
    for word, b in tokenize(text, bold):
        if word == "\n":
            lines.append(cur)
            cur, cur_w = [], 0.0
            continue
        w = width_in(theme, word, role, size, b)
        add = w if not cur else sp(b) + w
        if cur and cur_w + add > width:
            lines.append(cur)
            cur, cur_w = [(word, b)], w
        else:
            cur.append((word, b))
            cur_w += add
    lines.append(cur)
    return lines


def line_width(theme, line, role, size):
    total = 0.0
    for i, (word, b) in enumerate(line):
        total += width_in(theme, word, role, size, b)
        if i:
            total += width_in(theme, " ", role, size, b)
    return total


def widest_word(theme, text, role, size, bold=False):
    return max((width_in(theme, w, role, size, b) for w, b in tokenize(text, bold) if w != "\n"), default=0.0)


def height_in(n_lines, size, line_h=1.2):
    return n_lines * size * line_h / 72


def fit(theme, text, role, width, height, max_size, min_size=10, bold=False, line_h=1.2, step=1.0):
    """Largest size in [min_size, max_size] where the wrapped text fits width x height.
    Returns (size, lines, fits); when nothing fits, returns min_size with fits False."""
    size = max_size
    while size >= min_size - 1e-9:
        lines = wrap(theme, text, role, size, width, bold)
        too_wide = widest_word(theme, text, role, size, bold) > width
        if not too_wide and height_in(len(lines), size, line_h) <= height + 1e-6:
            return size, lines, True
        size -= step
    return min_size, wrap(theme, text, role, min_size, width, bold), False


def fit_line(theme, text, role, width, max_size, min_size=10, bold=False):
    """Largest size at which text stays on one line within width (returns min_size if even that overflows)."""
    size = max_size
    while size > min_size and width_in(theme, text.replace("**", ""), role, size, bold) > width:
        size -= 1
    return size


def word_count(text):
    return len([w for w, _ in tokenize(text) if w != "\n"])
