"""Requirement traceability: which slide answers which brief or rubric item, with what evidence."""
import re

from ..lint.structure import rubric_ids


def requirements(deck, brief_text=None):
    """[(id, text)] from the deck front matter `rubric:` list, or from lines `R1: text` in a brief file."""
    reqs = []
    for r in deck.meta.get("rubric") or []:
        if isinstance(r, dict):
            w = f" (weight {r['weight']})" if r.get("weight") is not None else ""
            reqs.append((str(r["id"]), f"{r.get('text', '')}{w}"))
        else:
            rid, _, text = str(r).partition(":")
            reqs.append((rid.strip(), text.strip()))
    if brief_text:
        for ln in brief_text.splitlines():
            m = re.match(r"^\s*[-*]?\s*(R\d+)\s*[:.)-]\s*(.+)$", ln)
            if m and m.group(1) not in {r[0] for r in reqs}:
                reqs.append((m.group(1), m.group(2).strip()))
    return reqs


def table(deck, brief_text=None):
    """Markdown traceability table plus the list of unmet requirement ids."""
    reqs = requirements(deck, brief_text)
    lines = ["| Requirement | Text | Slides | Evidence | Status |", "|---|---|---|---|---|"]
    unmet = []
    for rid, text in reqs:
        slides = [s for s in deck.slides if rid in s.rubric]
        nums = ", ".join(str(s.index) for s in slides) or "-"
        evid = "; ".join(sorted({s.source for s in slides if s.source})) or "-"
        status = "met" if slides else "NOT MET"
        if not slides:
            unmet.append(rid)
        lines.append(f"| {rid} | {text} | {nums} | {evid} | {status} |")
    if not reqs:
        lines.append("| - | no requirements defined (add `rubric:` to the front matter or pass --brief) | - | - | - |")
    return "\n".join(lines), unmet
