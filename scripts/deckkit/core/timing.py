import yaml

from . import textfit
from .paths import presets_dir

DEFAULT_EVENT = "hackathon"


def load_events():
    return yaml.safe_load((presets_dir() / "events.yaml").read_text(encoding="utf-8"))


def preset_for(deck):
    events = load_events()
    event = str(deck.meta.get("event", DEFAULT_EVENT))
    return event, events.get(event, events[DEFAULT_EVENT])


def budget(deck):
    """(minutes, wpm, max_slides, min_slides): the deck front matter overrides the event preset."""
    _, p = preset_for(deck)
    return (float(deck.meta.get("minutes", p["minutes"])), float(deck.meta.get("wpm", p["wpm"])),
            int(deck.meta.get("max_slides", p["max_slides"])), int(p.get("min_slides", 0)))


def plan(deck):
    """Per-slide seconds: explicit `time:`, else spoken words from notes at wpm, else an even split."""
    minutes, wpm, _, _ = budget(deck)
    rows = []
    for s in deck.slides:
        words = textfit.word_count(s.notes)
        if s.time is not None:
            secs, basis = s.time, "time"
        elif words:
            secs, basis = words / wpm * 60, "notes"
        else:
            secs, basis = None, "none"
        rows.append([s.index, s.layout, words, secs, basis])
    missing = [r for r in rows if r[3] is None]
    if missing:
        known = sum(r[3] for r in rows if r[3] is not None)
        share = max(minutes * 60 - known, 0) / len(missing)
        for r in missing:
            r[3], r[4] = share, "even split"
    return rows


def format_plan(deck):
    minutes, wpm, max_slides, _ = budget(deck)
    rows = plan(deck)
    total = sum(r[3] for r in rows)
    lines = ["| # | Layout | Notes words | Seconds | Basis |", "|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]:.0f} | {r[4]} |" for r in rows]
    lines.append(f"\nTotal {total / 60:.1f} min of {minutes:g} min at {wpm:g} wpm; {len(rows)} of {max_slides} slides.")
    return "\n".join(lines)
