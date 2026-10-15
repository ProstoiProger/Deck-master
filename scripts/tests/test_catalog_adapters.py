import re
import subprocess
import sys

import pytest
import yaml

from conftest import ROOT

SCRIPTS = ROOT / "scripts"
CLAUDE_ONLY = ["AskUserQuestion", "ToolSearch", "ExitPlanMode", "EnterPlanMode", "TodoWrite", "mcp__", "SendMessage"]


def py(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", cwd=cwd)


def test_layout_catalog_is_current_and_lists_every_layout_and_theme():
    r = py(SCRIPTS / "build_catalog.py", "--check")
    assert r.returncode == 0, r.stderr
    text = (ROOT / "references" / "design" / "catalog.md").read_text(encoding="utf-8")
    from deckkit.core.layout import LAYOUTS, ensure_loaded
    from deckkit.core.theme import theme_names
    ensure_loaded()
    assert all(f"`{n}`" in text for n in list(LAYOUTS) + theme_names())


def test_adapters_are_current_and_point_at_skill_md():
    r = py(SCRIPTS / "build_adapters.py", "--check")
    assert r.returncode == 0, r.stderr
    for rel in ["AGENTS.md", "adapters/cursor/deck-master.mdc", "adapters/copilot/copilot-instructions.md", "adapters/windsurf/deck-master.md"]:
        assert "SKILL.md" in (ROOT / rel).read_text(encoding="utf-8"), rel
    assert "@AGENTS.md" in (ROOT / "CLAUDE.md").read_text(encoding="utf-8")


def test_skill_frontmatter_and_cursor_rule_frontmatter_are_valid():
    head = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    meta = yaml.safe_load(head)
    assert meta["name"] == "deck-master" and len(meta["description"]) > 100
    mdc = (ROOT / "adapters/cursor/deck-master.mdc").read_text(encoding="utf-8").split("---", 2)[1]
    rule = yaml.safe_load(mdc)
    assert set(rule) == {"description", "globs", "alwaysApply"} and rule["alwaysApply"] is False


def test_docs_do_not_depend_on_agent_specific_tools():
    files = [ROOT / "SKILL.md", ROOT / "AGENTS.md", *(ROOT / "references").rglob("*.md"), *(ROOT / "assets" / "templates").glob("*.md")]
    for f in files:
        text = f.read_text(encoding="utf-8")
        for name in CLAUDE_ONLY:
            assert name not in text, f"{f.relative_to(ROOT)} mentions {name}"


def test_docs_use_only_ascii_dashes_and_arrows():
    for f in [ROOT / "SKILL.md", *(ROOT / "references").rglob("*.md")]:
        text = f.read_text(encoding="utf-8")
        assert not re.search("[–—→±]", text), f"{f.relative_to(ROOT)} has a non-ASCII dash, arrow or plus-minus"


def test_every_backticked_reference_path_exists():
    """Cross-links are backticked paths under references/, assets/ or scripts/; they must resolve."""
    pat = re.compile(r"`((?:references/|assets/|scripts/|examples/)?[\w./-]+\.(?:md|yaml|py|txt|mdc))`")
    skip = {"deck.md", "links.md", "brief.md", "notes.md"}  # names of the user's own files in examples
    missing = []
    for f in [ROOT / "SKILL.md", *(ROOT / "references").rglob("*.md")]:
        base = f.parent
        for m in pat.finditer(f.read_text(encoding="utf-8")):
            rel = m.group(1)
            if rel.split("/")[-1] in skip or "<" in rel or rel.startswith(("build/", "runs/", "decks/", ".")):
                continue
            candidates = [ROOT / rel, ROOT / "references" / rel, ROOT / "assets" / "templates" / rel, ROOT / "scripts" / rel, base / rel,
                          ROOT / "examples" / rel, ROOT / "assets" / "themes" / rel, ROOT / "assets" / "presets" / rel]
            if not any(c.exists() for c in candidates):
                missing.append(f"{f.relative_to(ROOT)} -> {rel}")
    assert not missing, "; ".join(sorted(set(missing)))


# ---- install.py -----------------------------------------------------------

def install(*args):
    return py(SCRIPTS / "install.py", *args)


def test_project_install_for_instruction_file_agents_is_idempotent(tmp_path):
    for agent in ["cursor", "copilot", "windsurf", "gemini", "agents"]:
        assert install("--agent", agent, "--project", tmp_path).returncode == 0
    assert (tmp_path / ".cursor/rules/deck-master.mdc").exists()
    assert "SKILL.md" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    for agent in ["cursor", "copilot", "windsurf", "gemini", "agents"]:
        assert install("--agent", agent, "--project", tmp_path, "--check").returncode == 0, agent
    assert install("--agent", "all", "--project", tmp_path, "--check").returncode == 1  # skill folders were not installed
    before = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    install("--agent", "agents", "--project", tmp_path)
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == before


def test_existing_instruction_files_are_extended_not_overwritten(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# My project rules\nKeep tests green.\n", encoding="utf-8")
    assert install("--agent", "agents", "--project", tmp_path).returncode == 0
    text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "Keep tests green." in text and "deck-master:begin" in text


def test_skill_folder_install_copies_and_refuses_foreign_directories(tmp_path):
    assert install("--agent", "claude", "--project", tmp_path).returncode == 0
    dest = tmp_path / ".claude/skills/deck-master"
    assert (dest / "SKILL.md").exists() and (dest / "scripts/cli.py").exists() and not (dest / "build").exists()
    assert install("--agent", "claude", "--project", tmp_path, "--check").returncode == 0
    foreign = tmp_path / ".agents/skills/deck-master"
    foreign.mkdir(parents=True)
    (foreign / "mine.txt").write_text("do not delete", encoding="utf-8")
    r = install("--agent", "codex", "--project", tmp_path)
    assert r.returncode == 1 and "refusing" in r.stdout and (foreign / "mine.txt").exists()


def test_installs_never_copy_downloaded_characters_or_private_screenshots(tmp_path):
    sys.path.insert(0, str(SCRIPTS))
    import install as inst
    (tmp_path / "assets" / "entities").mkdir(parents=True)
    names = ["steve.png", "manifest.json", ".gitkeep"]
    assert set(inst.IGNORE(str(tmp_path / "assets" / "entities"), names)) == {"steve.png", "manifest.json"}
    assert set(inst.IGNORE(str(tmp_path / "assets" / "inspiration"), ["r1.png", ".gitkeep"])) == {"r1.png"}
    assert "build" in inst.IGNORE(str(tmp_path), ["build", "scripts"]) and "scripts" not in inst.IGNORE(str(tmp_path), ["scripts"])


def test_installed_copy_runs_the_same_cli(tmp_path, deck_file):
    install("--agent", "claude", "--project", tmp_path)
    cli = tmp_path / ".claude/skills/deck-master/scripts/cli.py"
    r = py(cli, "lint", deck_file)
    assert r.returncode == 0, r.stdout + r.stderr


def test_vendor_mode_points_the_rule_at_a_project_relative_copy(tmp_path):
    assert install("--agent", "cursor", "--project", tmp_path, "--vendor").returncode == 0
    rule = (tmp_path / ".cursor/rules/deck-master.mdc").read_text(encoding="utf-8")
    assert "`.deck-master/SKILL.md`" in rule  # paths are relative to the project root and (tmp_path / ".deck-master/SKILL.md").exists()


def test_install_check_script_reports_all_groups_ok():
    r = py(SCRIPTS / "install_check.py", "core", "pptx", "pdf", "charts", "preview")
    assert r.returncode == 0, r.stdout + r.stderr
