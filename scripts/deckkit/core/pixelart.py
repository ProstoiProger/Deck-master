"""Small original pixel icons for the game components, drawn from character bitmaps ('.' is transparent).

The art is made for this skill in a generic block-game style: hearts, drumsticks, shield, XP orb, gems, tools, potion,
book, torch. No game textures are used, so the icons can be shared freely.
"""
PAL = {
    "k": "#1B1B1B", "w": "#F2F2F2", "g": "#A8A8A8", "G": "#5F5F5F", "s": "#7F7F7F",
    "r": "#8B1A12", "R": "#E02B20", "q": "#FF9A8F",
    "o": "#F28C28", "y": "#FCDB05", "Y": "#B8860B",
    "n": "#7A4B1F", "N": "#4F3115", "M": "#C0662E", "l": "#E39A5B", "b": "#EDE3CF",
    "B": "#3B82F6", "c": "#4EE3D6", "C": "#1DA8A0", "h": "#B8FFF8",
    "e": "#8BDB3C", "E": "#46A92B", "p": "#8B5CF6", "m": "#E879F9", "u": "#B93FD1", "x": "#CFE8FF",
}

SPRITES = {
    "heart": [".rr.rr.", "rRqRRRr", "rRRRRRr", ".rRRRr.", "..rRr..", "...r..."],
    "drumstick": ["..nNNn..", ".nMMMMn.", "nMMlMMMn", "nMMMMMMn", ".nMMMMn.", "..nNNn..", "...bb...", "..bbbb.."],
    "shield": ["kkkkkkk", "kBBwBBk", "kBBwBBk", "kwwwwwk", "kBBwBBk", ".kBwBk.", "..kwk..", "...k..."],
    "xp": ["..yyy..", ".yeeey.", "yeeEeey", "yeEEEey", "yeeEeey", ".yeeey.", "..yyy.."],
    "diamond": ["..cccc..", ".chhccC.", "chhccccC", "ccccccCC", ".cccCCC.", "..cCCC..", "...CC..."],
    "emerald": ["..eeee..", ".eqeeeE.", "eqeeeeEE", "eeeeeEEE", ".eeeEEE.", "..eEEE..", "...EE..."],
    "coin": ["..yyyy..", ".yYYYYy.", "yYyyyyYy", "yYyyyyYy", ".yYYYYy.", "..yyyy.."],
    "apple": ["...N...", ".rrNee.", "rRRrRRr", "rRqRRRr", "rRRRRRr", ".rRRRr.", "..r.r.."],
    "potion": ["..kkk..", "..kxk..", ".kkxkk.", "kmmmmmk", "kmuuumk", "kmuuumk", ".kmmmk.", "..kkk.."],
    "book": ["nnnnnnn", "nRRRRbn", "nRRRRbn", "nRRRRbn", "nRRRRbn", "nnnnnnn"],
    "torch": ["..y..", ".yoy.", ".yoy.", "..n..", "..n..", "..n..", "..N..", "..N.."],
    "sword": ["......gw", ".....gww", "....gww.", "...gww..", "..gww...", ".nnw....", "nnN.....", "nN......"],
    "pickaxe": ["..gggg..", ".gGggGg.", "gG....Gg", "g..n...g", "...n....", "...n....", "...N....", "...N...."],
    "star": ["...y...", "..yyy..", "yyyyyyy", ".yyyyy.", "..yyy..", ".yy.yy.", "yy...yy"],
    "trophy": ["yyyyyyyy", "yYyyyyYy", ".yyyyyy.", ".yyyyyy.", "..yyyy..", "...yy...", "..YYYY..", ".YYYYYY."],
    "sparkle": ["..y..", "..y..", "yyyyy", "..y..", "..y.."],
}

# icon -> (base sprite, {char: replacement char or hex}) for recolored variants
VARIANTS = {
    "heart_empty": ("heart", {"R": "#2A2A2A", "q": "#2A2A2A", "r": "#6B6B6B"}),
    "drumstick_empty": ("drumstick", {"M": "#2A2A2A", "l": "#2A2A2A", "n": "#6B6B6B", "N": "#6B6B6B", "b": "#6B6B6B"}),
    "shield_empty": ("shield", {"B": "#2A2A2A", "w": "#555555"}),
    "xp_empty": ("xp", {"e": "#2A2A2A", "E": "#2A2A2A", "y": "#6B6B6B"}),
}


def names():
    return sorted([*SPRITES, *VARIANTS])


def _grid(name):
    if name in SPRITES:
        return SPRITES[name], {}
    if name in VARIANTS:
        base, repl = VARIANTS[name]
        return SPRITES[base], repl
    raise KeyError(f"unknown icon {name!r}; choose from {names()}")


def size_of(name):
    rows, _ = _grid(name)
    return len(rows[0]), len(rows)


def runs(name, clip=1.0):
    """[(col, row, length, hex)] horizontal runs of equal color; `clip` keeps only the left fraction of the columns."""
    rows, repl = _grid(name)
    cols = len(rows[0])
    limit = max(0, min(cols, round(cols * clip)))
    out = []
    for r, line in enumerate(rows):
        c = 0
        while c < limit:
            ch = line[c]
            if ch == ".":
                c += 1
                continue
            start = c
            while c < limit and line[c] == ch:
                c += 1
            color = repl.get(ch) or PAL[ch]
            out.append((start, r, c - start, color if color.startswith("#") else PAL[color]))
    return out


for _name, _rows in SPRITES.items():  # fail at import, not at draw time, when a bitmap is ragged
    assert len({len(r) for r in _rows}) == 1, f"icon {_name} has rows of different lengths"
