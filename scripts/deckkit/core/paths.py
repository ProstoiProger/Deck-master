from pathlib import Path

# scripts/deckkit/core/paths.py -> skill root is three levels up from this file's directory
ROOT = Path(__file__).resolve().parents[3]


def assets_dir():
    return ROOT / "assets"


def themes_dir():
    return assets_dir() / "themes"


def fonts_dir():
    return assets_dir() / "fonts"


def presets_dir():
    return assets_dir() / "presets"


def templates_dir():
    return assets_dir() / "templates"


def references_dir():
    return ROOT / "references"
