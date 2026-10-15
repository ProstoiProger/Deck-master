from ..core import textfit, timing
from .common import finding


def check(deck, scenes, theme):
    out = []
    minutes, wpm, max_slides, min_slides = timing.budget(deck)
    for sc, slide in zip(scenes, deck.slides):
        words = textfit.word_count(slide.notes)
        if not words and slide.layout != "closing":
            out.append(finding("Medium", sc, "no speaker notes; add `notes:` with what to say (1 to 3 sentences)"))
        elif words > 120:
            out.append(finding("Low", sc, f"notes run {words} words (about {words / wpm * 60:.0f} s); trim to the spoken point"))
    n = len(deck.slides)
    event, _ = timing.preset_for(deck)
    if n > max_slides:
        out.append(finding("High", None, f"{n} slides exceeds the {max_slides}-slide cap for {event}; cut {n - max_slides}"))
    elif n < min_slides:
        out.append(finding("Low", None, f"{n} slides is under the usual {min_slides} for {event}"))
    spoken = sum(textfit.word_count(s.notes) for s in deck.slides)
    if spoken > minutes * wpm * 1.1:
        out.append(finding("High", None, f"over time: {spoken} spoken words need {spoken / wpm:.1f} min at {wpm:g} wpm, "
                                         f"budget is {minutes:g} min"))
    covered = sum(r[3] for r in timing.plan(deck) if r[4] != "even split")
    if len(deck.slides) > 2 and 0 < covered < minutes * 60 * 0.6:
        out.append(finding("Low", None, f"notes and `time:` values cover only {covered / 60:.1f} of {minutes:g} minutes; "
                                        f"write fuller notes or set `time:` for parts that are not spoken (a live demo)"))
    explicit = sum(s.time for s in deck.slides if s.time is not None)
    if explicit > minutes * 60 * 1.05:
        out.append(finding("High", None, f"over time: `time:` values sum to {explicit / 60:.1f} min, budget is {minutes:g} min"))
    return out
