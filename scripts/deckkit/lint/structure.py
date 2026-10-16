"""Findings raised while laying out slides, and rubric coverage."""
from .common import RANK, finding


def split_tag(problem):
    """`[Medium] text` -> ('Medium', 'text'); untagged problems default to High."""
    if problem.startswith("[") and "]" in problem:
        tag = problem[1:problem.index("]")]
        if tag in RANK:
            return tag, problem[problem.index("]") + 1:].strip()
    return "High", problem


def rubric_ids(deck):
    return [str(r.get("id")) if isinstance(r, dict) else str(r).split(":")[0] for r in (deck.meta.get("rubric") or [])]


def game_findings(deck, theme):
    """Game themes and game layouts are opt-in: the user must ask for them, and the deck records that with `game: true`."""
    from ..core import layout
    layout.ensure_loaded()
    asked = str(deck.meta.get("game", "")).lower() in ("true", "yes", "1")
    out = []
    if "game" in theme.scopes and not asked:
        out.append(finding("Medium", None, f"game theme {theme.name} without `game: true` in the front matter; "
                                           "use game themes only when the user asked for a Minecraft or gamified deck"))
    if "game" not in theme.scopes:
        for s in deck.slides:
            spec = layout.LAYOUTS.get(s.layout)
            if spec is not None and spec.family == "game":
                out.append(f"[Medium] slide {s.index} ({s.layout}): game layout in the formal theme {theme.name}; "
                           "use a formal layout or switch to a game theme")
    return out


def check(deck, scenes, theme):
    out = game_findings(deck, theme)
    for sc in scenes:
        for p in sc.problems:
            sev, msg = split_tag(p)
            out.append(finding(sev, sc, msg))
    ids = rubric_ids(deck)
    if ids:
        covered = {r for s in deck.slides for r in s.rubric}
        for rid in ids:
            if rid not in covered:
                out.append(finding("Critical", None, f"rubric item {rid} is not covered by any slide (`rubric: {rid}`)"))
        for s, sc in zip(deck.slides, scenes):
            for r in s.rubric:
                if r not in ids:
                    out.append(finding("Medium", sc, f"rubric id {r} is not defined in the front matter"))
    return out
