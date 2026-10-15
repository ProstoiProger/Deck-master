import pytest

from deckkit.core.spec import SpecError


def test_front_matter_and_slides_are_parsed(parse, good_text):
    deck = parse(good_text)
    assert deck.meta["event"] == "hackathon"
    assert [s.layout for s in deck.slides] == ["title", "problem", "bullets"]
    assert deck.slides[1].props["stat"] == "40 min | median delay"
    assert deck.slides[1].source == "brief.pdf p.3"
    assert deck.slides[1].rubric == ["R1"]


def test_bullets_split_cells_and_keep_paragraphs(parse, good_text):
    s = parse(good_text).slides[1]
    assert s.paragraphs == ["Customers lose money before the alert fires."]
    assert [i.text for i in s.items] == ["First point", "Second point"]
    s2 = parse("# T\n- 92% | F1 | vs 81%\n").slides[0]
    assert s2.items[0].cells == ["92%", "F1", "vs 81%"]


def test_indented_lines_continue_a_property(parse):
    s = parse("# T\nnotes: first part\n  second part\n- a\n").slides[0]
    assert s.notes == "first part second part"
    assert [i.text for i in s.items] == ["a"]


def test_tables_groups_images_and_time(parse):
    s = parse("# T\ntime: 30\n![shot](a.png)\n## Left\n- a\n## Right\n- b\n| H1 | H2 |\n|---|---|\n| x | y |\n").slides[0]
    assert s.time == 30.0 and s.image == "a.png"
    assert [g[0] for g in s.groups] == ["Left", "Right"]
    assert s.table == [["H1", "H2"], ["x", "y"]]


def test_separator_inside_a_code_fence_does_not_split_slides(parse):
    deck = parse("# A\n```\n---\ncode\n```\n---\n# B\n")
    assert len(deck.slides) == 2 and deck.slides[0].code == "---\ncode"


def test_missing_title_is_a_clear_error(parse):
    with pytest.raises(SpecError, match="slide 2"):
        parse("# A\n---\nno title here\n")


def test_unclosed_front_matter_and_empty_deck_are_errors(parse):
    with pytest.raises(SpecError, match="never closed"):
        parse("---\ntitle: x\n")
    with pytest.raises(SpecError, match="no slides"):
        parse("---\ntitle: x\n---\n")


def test_bad_time_value_is_an_error(parse):
    with pytest.raises(SpecError, match="time"):
        parse("# A\ntime: soon\n")
