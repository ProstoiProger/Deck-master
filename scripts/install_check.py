"""Verify dependency groups and bundled fonts.

    python scripts/install_check.py core pptx pdf charts preview

Groups come from scripts/requirements/<group>.txt, so this check cannot drift from the requirement files.
"""
import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQ = HERE / "requirements"
IMPORT_NAME = {"pyyaml": "yaml", "pillow": "PIL", "python-pptx": "pptx", "pymupdf": "pymupdf", "fonttools": "fontTools"}
SKIP = {"pytest"}


def groups():
    return sorted(p.stem for p in REQ.glob("*.txt"))


def packages(group, seen=None):
    seen = seen or set()
    path = REQ / f"{group}.txt"
    pk = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("-r"):
            sub = line[2:].strip().removesuffix(".txt")
            if sub not in seen:
                seen.add(sub)
                pk += packages(sub, seen)
            continue
        name = re.split(r"[<>=!~\[ ]", line, maxsplit=1)[0].lower()
        if name not in SKIP:
            pk.append(name)
    return pk


def check(group_names):
    result = {}
    for g in group_names:
        rows = []
        for name in dict.fromkeys(packages(g)):
            mod = IMPORT_NAME.get(name, name.replace("-", "_"))
            try:
                m = importlib.import_module(mod)
                rows.append((name, getattr(m, "__version__", None) or getattr(m, "Version", None) or "installed"))
            except Exception:
                rows.append((name, None))
        result[g] = rows
    return result


def check_fonts():
    sys.path.insert(0, str(HERE))
    import yaml
    from deckkit.core.paths import fonts_dir, presets_dir
    book = yaml.safe_load((presets_dir() / "fonts.yaml").read_text(encoding="utf-8"))
    missing = []
    for fam, spec in book.items():
        for key in ("regular", "bold"):
            if not (fonts_dir() / spec[key]).exists():
                missing.append(spec[key])
    return missing


def main(argv):
    wanted = argv[1:] or ["core"]
    unknown = [g for g in wanted if g not in groups()]
    if unknown:
        raise SystemExit(f"unknown groups {unknown}; choose from {groups()}")
    missing = []
    for g, rows in check(wanted).items():
        print(f"[{g}]")
        for name, ver in rows:
            print(f"  {name:14} {ver or 'MISSING'}")
            if ver is None:
                missing.append(name)
    fonts = check_fonts()
    print("[fonts]")
    print("  all bundled font files present" if not fonts else f"  MISSING font files: {fonts}")
    try:
        sys.path.insert(0, str(HERE))
        import deckkit
        print(f"deckkit {deckkit.__version__} importable")
    except Exception as e:
        missing.append(f"deckkit ({e})")
    if missing or fonts:
        raise SystemExit(f"problems: {missing + fonts}")


if __name__ == "__main__":
    main(sys.argv)
