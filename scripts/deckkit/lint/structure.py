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


def check(deck, scenes, theme):
    out = []
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
