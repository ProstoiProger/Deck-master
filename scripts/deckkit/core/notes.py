from . import timing


def speaker_script(deck):
    """Markdown speaker script: slide title, seconds, and the notes to say."""
    rows = {r[0]: r for r in timing.plan(deck)}
    out = [f"# Speaker script: {deck.meta.get('title', '')}".rstrip(": "), ""]
    for s in deck.slides:
        secs = rows[s.index][3]
        out.append(f"## {s.index}. {s.title} ({secs:.0f} s)")
        out.append(s.notes or "(no notes)")
        if s.source:
            out.append(f"Source: {s.source}")
        out.append("")
    return "\n".join(out)
