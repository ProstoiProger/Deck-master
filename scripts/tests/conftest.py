import sys
import warnings
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
warnings.filterwarnings("ignore")

ROOT = SCRIPTS.parent
EXAMPLES = ROOT / "examples"
FLAGSHIP = EXAMPLES / "studybuddy-obsidian" / "studybuddy.md"
LESSON = EXAMPLES / "network-lesson-classic" / "lesson.md"

GOOD = """---
title: Test deck
event: hackathon
theme: midnight-navy
minutes: 5
rubric:
  - {id: R1, text: Impact, weight: 50}
  - {id: R2, text: Demo, weight: 50}
---
# Atlas scores each swipe on arrival
layout: title
notes: Opening in one sentence.

---
# Alerts arrive 40 minutes late
layout: problem
rubric: R1
stat: 40 min | median delay
source: brief.pdf p.3
notes: The pain, in the user's words.
Customers lose money before the alert fires.
- First point
- Second point

---
# The demo takes three clicks
layout: bullets
rubric: R2
notes: Show the queue.
- Open the queue
- Open a case
- Block the card
"""


@pytest.fixture(autouse=True)
def isolated_entities(tmp_path_factory, monkeypatch):
    """Tests never depend on downloaded character images: point the entity folder at an empty temp dir."""
    monkeypatch.setenv("DECKKIT_ENTITIES_DIR", str(tmp_path_factory.mktemp("entities")))


@pytest.fixture
def good_text():
    return GOOD


@pytest.fixture
def parse():
    from deckkit.core.spec import parse_text
    return parse_text


@pytest.fixture
def theme():
    from deckkit.core.theme import load_theme
    return load_theme("midnight-navy")


@pytest.fixture
def lint_text(parse, theme):
    """Lint a deck given as text: returns the findings."""
    from deckkit import lint
    from deckkit.core.layout import build_scenes
    from deckkit.core.theme import load_theme

    def run(text, theme_name=None):
        deck = parse(text)
        th = load_theme(theme_name) if theme_name else theme
        return lint.run_all(deck, build_scenes(deck, th), th)
    return run


@pytest.fixture
def deck_file(tmp_path, good_text):
    p = tmp_path / "deck.md"
    p.write_text(good_text, encoding="utf-8")
    return p
