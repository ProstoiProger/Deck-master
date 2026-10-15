from deckkit.core.scene import SceneSlide, Shape, Text
from deckkit.lint import blocking, contrast, overflow, severity_of


def has(findings, sev, needle):
    return any(severity_of(f) == sev and needle in f for f in findings)


def test_clean_deck_has_no_blocking_findings(lint_text, good_text):
    assert blocking(lint_text(good_text)) == []


def test_unsourced_number_is_high_and_a_source_clears_it(lint_text):
    bad = "# Claim\nlayout: bullets\nnotes: n\n- Accuracy rose to 92%\n"
    assert has(lint_text(bad), "High", "no `source:`")
    ok = bad.replace("notes: n\n", "notes: n\nsource: runs/log.jsonl\n")
    assert not any("source" in f for f in lint_text(ok))


def test_years_and_small_integers_are_not_claims(lint_text):
    text = "# Plan for 2026\nlayout: bullets\nnotes: n\n- Three steps in 2 phases\n"
    assert not any("source" in f for f in lint_text(text))


def test_missing_notes_is_medium(lint_text):
    assert has(lint_text("# A takeaway sentence for the slide\nlayout: bullets\n- a\n"), "Medium", "no speaker notes")


def test_unknown_layout_is_high_but_still_renders(lint_text):
    f = lint_text("# Some title with enough words\nlayout: nonsense\nnotes: n\n- a\n")
    assert has(f, "High", "unknown layout")


def test_unfilled_placeholder_is_high(lint_text):
    assert has(lint_text("# <Problem as a takeaway>\nlayout: bullets\nnotes: n\n- a\n"), "High", "placeholder")


def test_generics_in_code_text_are_not_placeholders(lint_text):
    f = lint_text("# We use Map<String, Int> for lookups here\nlayout: bullets\nnotes: n\n- List<Item> stays\n")
    assert not any("placeholder" in x for x in f)


def test_chart_with_non_numeric_data_is_a_finding_not_a_crash(lint_text):
    f = lint_text("# A takeaway about the chart data\nlayout: chart_insight\nchart: bar\nnotes: n\n| A | B |\n|---|---|\n| x | n/a |\n")
    assert has(f, "High", "failed") or has(f, "High", "chart")


def test_rubric_item_without_a_slide_is_critical(lint_text):
    text = "---\nrubric:\n  - {id: R1, text: a}\n  - {id: R9, text: b}\n---\n# Covers one item only here\nlayout: bullets\nrubric: R1\nnotes: n\n- a\n"
    f = lint_text(text)
    assert has(f, "Critical", "R9") and not has(f, "Critical", "R1 ")


def test_slide_cap_and_time_budget_are_enforced(lint_text):
    slides = "\n---\n".join(f"# Slide number {i} says something\nlayout: bullets\nnotes: {'word ' * 60}\n- a" for i in range(9))
    f = lint_text("---\nevent: hackathon\nminutes: 3\n---\n" + slides)
    assert has(f, "High", "slide cap") or has(f, "High", "-slide cap")
    assert has(f, "High", "over time")


def test_missing_glyph_is_high(lint_text):
    assert has(lint_text("# Chinese 漢字 in the title here\nlayout: bullets\nnotes: n\n- a\n"), "High", "glyph")


def test_overflowing_text_is_high(theme):
    sc = SceneSlide(1, "x", "t", "#000000", [Text(1, 1, 1.0, 0.2, "A long sentence that cannot fit inside a tiny box at all", 18, "#FFFFFF")])
    assert has(overflow.check(None, [sc], theme), "High", "overflows")


def test_low_contrast_text_is_high_and_uses_the_shape_behind_it(theme):
    sc = SceneSlide(1, "x", "t", "#000000", [Shape(0, 0, 5, 5, fill="#FFFFFF"), Text(1, 1, 2, 1, "Hidden", 20, "#FFFFFF")])
    assert has(contrast.check(None, [sc], theme), "High", "contrast")
    sc.items[1].color = "#000000"
    assert contrast.check(None, [sc], theme) == []


def test_small_font_is_medium(theme):
    sc = SceneSlide(1, "x", "t", "#000000", [Text(1, 1, 5, 1, "tiny", 8, "#FFFFFF")])
    assert has(overflow.check(None, [sc], theme), "Medium", "minimum")
