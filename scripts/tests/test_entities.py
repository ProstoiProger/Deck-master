import io
import json

import pytest
from PIL import Image

from conftest import ROOT
from deckkit.core import entities
from deckkit.core.layout import build_scenes
from deckkit.core.scene import Image as SceneImage
from deckkit.core.theme import load_theme
from deckkit.lint import run_all, severity_of
from test_cli import run


def png_bytes(color, size=8):
    buf = io.BytesIO()
    Image.new("RGBA", (size, size), color).save(buf, "PNG")
    return buf.getvalue()


def fake_service(default_for=()):
    """Opener returning a distinct PNG per URL; accounts in default_for (and the probe account) get the default image."""
    default = png_bytes("#808080")

    def opener(url):
        if any(acc in url for acc in default_for) or "NoSuchAccount" in url:
            return default
        return png_bytes("#" + format(sum(map(ord, url)) % 0xFFFFFF, "06x"))
    return opener


def test_names_aliases_and_catalog():
    assert entities.canonical("Iron Golem") == "iron-golem" and entities.canonical("golem") == "iron-golem"
    assert entities.known("Steve") and not entities.known("herobrine")
    assert {"steve", "alex", "creeper", "villager", "zombie", "enderman", "pig"} <= set(entities.ENTITIES)


def test_fetch_writes_all_kinds_skips_existing_and_records_a_notice(tmp_path):
    written, _, failed, unavailable = entities.fetch(["steve", "creeper"], dest=tmp_path, opener=fake_service())
    assert sorted(written) == ["creeper-head.png", "creeper.png", "steve-body.png", "steve-head.png", "steve.png"]  # only players get a body
    assert failed == [] and unavailable == []
    manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert "Personal, non-commercial" in manifest["notice"] and "creeper.png" in manifest["files"]
    written2, skipped2, _, _ = entities.fetch(["steve"], dest=tmp_path, opener=fake_service())
    assert written2 == [] and len(skipped2) == 3


def test_default_skin_responses_are_reported_not_stored(tmp_path):
    written, _, failed, unavailable = entities.fetch(["steve", "slime"], kinds=("head",), dest=tmp_path,
                                                     opener=fake_service(default_for=("MHF_Slime",)))
    assert "slime-head.png" not in written and any("slime-head.png" in u for u in unavailable) and failed == []
    assert not (tmp_path / "slime-head.png").exists()


def test_network_errors_are_failures_and_unknown_names_raise(tmp_path):
    def broken(url):
        raise OSError("offline")
    _, _, failed, _ = entities.fetch(["pig"], kinds=("face",), dest=tmp_path, opener=broken)
    assert failed and "offline" in failed[0]
    with pytest.raises(ValueError, match="unknown entities"):
        entities.fetch(["notamob"], dest=tmp_path, opener=fake_service())


TEAM_DECK = """---
event: hackathon
theme: obsidian-craft
---
# Four people built it over one weekend
layout: team
decor: none
notes: n
- Dana K. | Pipeline | built the stream | steve
- Mira L. | Chaos tests | breaks things | creeper

---
# Questions?
layout: closing
mascot: creeper
notes: n
- example.org
"""


def test_missing_images_fall_back_to_initials_and_raise_medium_findings(parse):
    deck, theme = parse(TEAM_DECK), load_theme("obsidian-craft")
    findings = run_all(deck, build_scenes(deck, theme), theme)
    assert any(severity_of(f) == "Medium" and "has no downloaded image" in f and "entities fetch" in f for f in findings)
    assert not [f for f in findings if severity_of(f) in ("Critical", "High")]


def test_downloaded_images_are_placed_as_pictures(parse, tmp_path, monkeypatch):
    folder = tmp_path / "ent"
    entities.fetch(["steve", "creeper"], dest=folder, opener=fake_service())
    monkeypatch.setenv("DECKKIT_ENTITIES_DIR", str(folder))
    deck, theme = parse(TEAM_DECK), load_theme("obsidian-craft")
    scenes = build_scenes(deck, theme)
    pics = [[i for i in sc.items if isinstance(i, SceneImage)] for sc in scenes]
    assert len(pics[0]) == 2 and len(pics[1]) == 1
    assert pics[1][0].path.endswith("creeper-head.png") and pics[1][0].w == pytest.approx(3.6)
    assert not [f for f in run_all(deck, scenes, theme) if "entity" in f]


def test_a_missing_head_render_falls_back_to_the_face(parse, tmp_path, monkeypatch):
    folder = tmp_path / "ent"
    entities.fetch(["enderman"], kinds=("face",), dest=folder, opener=fake_service())
    monkeypatch.setenv("DECKKIT_ENTITIES_DIR", str(folder))
    deck = parse("# Questions?\nlayout: closing\nmascot: enderman\nnotes: n\n- example.org\n")
    scenes = build_scenes(deck, load_theme("classic-craft"))
    pics = [i for i in scenes[0].items if isinstance(i, SceneImage)]
    assert len(pics) == 1 and pics[0].path.endswith("enderman.png")


def test_unknown_entity_lists_the_known_names(parse):
    deck = parse("# A takeaway about the team members\nlayout: team\nnotes: n\n- A | B | C | herobrine\n")
    theme = load_theme("obsidian-craft")
    findings = run_all(deck, build_scenes(deck, theme), theme)
    assert any("unknown entity 'herobrine'" in f and "creeper" in f for f in findings)


def test_hotbar_agenda_puts_characters_in_slots(parse, tmp_path, monkeypatch):
    folder = tmp_path / "ent"
    entities.fetch(["villager", "witch"], kinds=("face",), dest=folder, opener=fake_service())
    monkeypatch.setenv("DECKKIT_ENTITIES_DIR", str(folder))
    deck = parse("# Our route in two steps\nlayout: agenda\ndecor: none\nnotes: n\n- Idea | villager\n- Model | witch\n- Plain step\n")
    scenes = build_scenes(deck, load_theme("classic-craft"))
    assert len([i for i in scenes[0].items if isinstance(i, SceneImage)]) == 2


def test_entities_cli_lists_and_rejects_unknown_names():
    listing = json.loads(run("entities", "list", "--json").stdout)
    assert len(listing) == len(entities.ENTITIES) and not any(r["have"]["face"] for r in listing)  # isolated empty folder
    assert run("entities", "fetch", "--names", "notamob").returncode == 2


def test_downloaded_game_images_are_git_ignored_and_not_shipped():
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "assets/entities/*" in text and "!assets/entities/.gitkeep" in text
