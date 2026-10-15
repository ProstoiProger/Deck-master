import json
import subprocess
import sys

from conftest import ROOT

CLI = str(ROOT / "scripts" / "cli.py")


def run(*args, cwd=None):
    return subprocess.run([sys.executable, CLI, *map(str, args)], capture_output=True, text=True, encoding="utf-8", cwd=cwd)


def test_lint_passes_a_good_deck_and_fails_a_bad_one(deck_file, tmp_path):
    ok = run("lint", deck_file)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad = tmp_path / "bad.md"
    bad.write_text("# A takeaway sentence for the slide\nlayout: bullets\n- Rose to 92%\n", encoding="utf-8")
    r = run("lint", bad)
    assert r.returncode == 1 and "INVALID" in r.stdout and "[High]" in r.stdout


def test_lint_json_is_machine_readable(deck_file):
    r = run("lint", deck_file, "--json")
    data = json.loads(r.stdout)
    assert data["blocking"] == 0 and data["theme"] == "midnight-navy"


def test_build_writes_both_formats_and_a_run_log(deck_file, tmp_path):
    out = tmp_path / "out"
    r = run("build", deck_file, "--out", out)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (out / "deck.pptx").stat().st_size > 10_000 and (out / "deck.pdf").stat().st_size > 5_000
    log = [json.loads(x) for x in (out / "log.jsonl").read_text(encoding="utf-8").splitlines()]
    assert log[-1]["slides"] == 3 and log[-1]["blocking"] == 0


def test_build_refuses_a_blocked_deck_unless_forced(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("# A takeaway sentence for the slide\nlayout: bullets\n- Rose to 92%\n", encoding="utf-8")
    out = tmp_path / "out"
    r = run("build", bad, "--out", out, "--pdf")
    assert r.returncode == 1 and "INVALID" in r.stdout and not (out / "bad.pdf").exists()
    forced = run("build", bad, "--out", out, "--pdf", "--force")
    assert forced.returncode == 0 and (out / "bad.pdf").exists()


def test_theme_override_changes_the_output_name(deck_file, tmp_path):
    out = tmp_path / "out"
    assert run("build", deck_file, "--out", out, "--pdf", "--theme", "obsidian-craft").returncode == 0
    assert (out / "deck-obsidian-craft.pdf").exists()


def test_new_scaffolds_and_refuses_to_overwrite(tmp_path):
    target = tmp_path / "x" / "pitch.md"
    r = run("new", "--event", "hackathon", "--title", 'Name: "quoted" idea', "--out", target)
    assert r.returncode == 0 and target.exists()
    again = run("new", "--event", "hackathon", "--out", target)
    assert again.returncode == 1 and "--force" in again.stderr
    assert run("new", "--event", "hackathon", "--out", target, "--force").returncode == 0
    lint = run("lint", target)  # scaffolds are meant to fail until placeholders are filled
    assert lint.returncode == 1 and "placeholder" in lint.stdout


def test_bad_input_exits_2(tmp_path):
    assert run("lint", tmp_path / "missing.md").returncode == 2
    broken = tmp_path / "b.md"
    broken.write_text("no title\n", encoding="utf-8")
    r = run("lint", broken)
    assert r.returncode == 2 and "must be '# Title'" in r.stderr
    assert run("new", "--event", "wedding", "--out", tmp_path / "w.md").returncode == 2


def test_trace_reports_unmet_requirements(deck_file, tmp_path):
    assert run("trace", deck_file).returncode == 0
    text = deck_file.read_text(encoding="utf-8").replace("  - {id: R2, text: Demo, weight: 50}", "  - {id: R2, text: Demo, weight: 50}\n  - {id: R3, text: Extra}")
    other = tmp_path / "t.md"
    other.write_text(text, encoding="utf-8")
    r = run("trace", other)
    assert r.returncode == 1 and "NOT MET: R3" in r.stdout


def test_timing_notes_themes_layouts_run(deck_file):
    assert "Total" in run("timing", deck_file).stdout
    assert "Speaker script" in run("notes", deck_file).stdout
    themes = json.loads(run("themes", "--json").stdout)
    assert len(themes) == 8
    layouts = json.loads(run("layouts", "--json").stdout)
    assert len(layouts) == 27


def test_preview_writes_pngs_and_a_sheet(deck_file, tmp_path):
    import pytest
    pytest.importorskip("pymupdf")
    out = tmp_path / "pv"
    r = run("preview", deck_file, "--out", out, "--sheet")
    assert r.returncode == 0, r.stderr
    assert len(list(out.glob("slide-*.png"))) == 3 and (out / "sheet.png").exists()


def test_inspire_measures_a_palette(tmp_path):
    from PIL import Image
    im = Image.new("RGB", (40, 40), "#102040")
    p = tmp_path / "ref.png"
    im.save(p)
    r = run("inspire", "--from-image", p, "--colors", "2")
    assert r.returncode == 0 and "#102040" in r.stdout.upper()


def test_env_card_lists_packages_and_writes_json(tmp_path):
    out = tmp_path / "env.json"
    r = run("env", "--json", out)
    assert r.returncode == 0 and "python-pptx" in r.stdout
    assert json.loads(out.read_text(encoding="utf-8"))["deckkit"]
