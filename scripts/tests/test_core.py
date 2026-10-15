import json

from deckkit.core import textfit, timing, trace
from deckkit.core.notes import speaker_script
from deckkit.core.runlog import log_run, read_runs


def test_wrap_respects_width_and_bold_markup(theme):
    lines = textfit.wrap(theme, "alpha beta gamma delta epsilon zeta eta theta", "body", 20, 1.5)
    assert len(lines) > 2
    assert all(textfit.line_width(theme, ln, "body", 20) <= 1.5 + 1e-6 for ln in lines)
    tokens = textfit.tokenize("plain **bold word** plain")
    assert [t for t in tokens if t[1]] == [("bold", True), ("word", True)]


def test_fit_shrinks_to_fit_and_reports_failure(theme):
    size, lines, ok = textfit.fit(theme, "A fairly long title that needs more than one line", "heading", 3.0, 0.6, 40, 12, True)
    assert ok and size < 40 and textfit.height_in(len(lines), size) <= 0.6 + 1e-6
    _, _, ok2 = textfit.fit(theme, "x " * 400, "body", 2.0, 0.3, 20, 12)
    assert not ok2


def test_fit_line_never_wraps(theme):
    size = textfit.fit_line(theme, "31 of 40", "heading", 1.5, 60, 10, True)
    assert textfit.width_in(theme, "31 of 40", "heading", size, True) <= 1.5 + 1e-6


def test_glyph_coverage_for_kazakh_and_a_missing_script(theme):
    assert textfit.missing_glyphs(theme, "body", "ә ғ қ ң ө ү ұ һ і Привет") == []
    assert textfit.missing_glyphs(theme, "body", "漢") == ["漢"]


def test_timing_plan_uses_notes_then_even_split(parse):
    deck = parse("---\nminutes: 2\nwpm: 60\n---\n# A\nnotes: " + "w " * 30 + "\n---\n# B\n")
    rows = timing.plan(deck)
    assert rows[0][3] == 30 and rows[0][4] == "notes"
    assert rows[1][4] == "even split" and abs(rows[1][3] - 90) < 1e-6
    assert "Total 2.0 min of 2 min" in timing.format_plan(deck)


def test_trace_table_marks_met_and_unmet(parse):
    deck = parse("---\nrubric:\n  - {id: R1, text: A, weight: 5}\n  - {id: R2, text: B}\n---\n# S\nrubric: R1\nsource: f.csv\n- x\n")
    text, unmet = trace.table(deck)
    assert unmet == ["R2"] and "| R1 | A (weight 5) | 1 | f.csv | met |" in text
    text2, unmet2 = trace.table(deck, "R3: from the brief\n")
    assert unmet2 == ["R2", "R3"]


def test_speaker_script_lists_notes_and_sources(parse):
    deck = parse("---\ntitle: T\nminutes: 1\n---\n# One\nsource: a.csv\nnotes: Say this.\n")
    text = speaker_script(deck)
    assert "## 1. One" in text and "Say this." in text and "Source: a.csv" in text


def test_run_log_is_append_only_jsonl(tmp_path):
    p = tmp_path / "runs" / "log.jsonl"
    log_run(p, deck="a", slides=3)
    log_run(p, deck="b", slides=4)
    assert [r["deck"] for r in read_runs(p)] == ["a", "b"]
    assert json.loads(p.read_text(encoding="utf-8").splitlines()[0])["slides"] == 3
