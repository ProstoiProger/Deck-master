from dataclasses import dataclass, field

import yaml

from . import color
from .paths import fonts_dir, presets_dir, themes_dir

REQUIRED_COLORS = ["bg", "surface", "primary", "secondary", "accent", "text", "muted", "success", "warning", "danger"]
STYLE_DEFAULTS = {"corner": "round", "border": "thin", "shadow": "soft", "pattern": "grid", "metaphor": "none",
                  "heading_scale": 1.0, "heading_line_h": 1.18, "min_font": 12}


class ThemeError(ValueError):
    pass


def load_fontbook():
    return yaml.safe_load((presets_dir() / "fonts.yaml").read_text(encoding="utf-8"))


@dataclass
class Theme:
    name: str
    mode: str
    colors: dict
    fonts: dict
    style: dict
    description: str = ""
    fontbook: dict = field(default_factory=dict)

    def c(self, token):
        """Resolve a color token (bg, primary, ...) or pass a hex value through."""
        if isinstance(token, str) and token.startswith("#"):
            return token.upper()
        return self.colors[token]

    def on(self, bg):
        """Readable text color for a given background: the best of theme text, theme bg, white, black."""
        bg = self.c(bg)
        return color.best_on(bg, [self.colors["text"], self.colors["bg"], "#FFFFFF", "#000000"])

    def family(self, role):
        return self.fonts[role]

    def font_file(self, role, bold=False):
        fam = self.fontbook[self.family(role)]
        return fonts_dir() / fam["bold" if bold else "regular"]

    def pptx_font(self, role):
        return self.fontbook[self.family(role)]["pptx"]

    def fallback_font(self, role):
        return self.fontbook[self.family(role)].get("fallback", "Arial")


def theme_names():
    return sorted(p.stem for p in themes_dir().glob("*.yaml") if not p.stem.startswith("_"))


def load_theme(name):
    path = themes_dir() / f"{name}.yaml"
    if not path.exists():
        raise ThemeError(f"unknown theme {name!r}; choose from {theme_names()}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ThemeError(f"theme file {path.name} is not valid YAML: {e}")
    colors = {k: str(v).upper() for k, v in raw["colors"].items()}
    missing = [k for k in REQUIRED_COLORS if k not in colors]
    if missing:
        raise ThemeError(f"theme {name} lacks colors {missing}")
    colors.setdefault("border", color.mix(colors["surface"], colors["text"], 0.18))
    colors.setdefault("info", colors["primary"])
    fontbook = load_fontbook()
    fonts = {"heading": "Inter", "body": "Inter", "mono": "JetBrainsMono", **raw.get("fonts", {})}
    for role, fam in fonts.items():
        if fam not in fontbook:
            raise ThemeError(f"theme {name}: font family {fam!r} for {role} is not in assets/presets/fonts.yaml")
    style = {**STYLE_DEFAULTS, **raw.get("style", {})}
    return Theme(name=raw.get("name", name), mode=raw.get("mode", "dark"), colors=colors, fonts=fonts, style=style,
                 description=raw.get("description", ""), fontbook=fontbook)


def contrast_table(theme):
    """(label, ratio) pairs that matter for readability, used by the catalog and the accessibility checks."""
    c = theme.colors
    pairs = [("text on bg", c["text"], c["bg"]), ("text on surface", c["text"], c["surface"]),
             ("muted on bg", c["muted"], c["bg"]), ("muted on surface", c["muted"], c["surface"]),
             ("primary on bg", c["primary"], c["bg"]), ("primary on surface", c["primary"], c["surface"]),
             ("accent on bg", c["accent"], c["bg"]), ("on(primary) on primary", theme.on(c["primary"]), c["primary"])]
    return [(label, round(color.contrast(a, b), 2)) for label, a, b in pairs]
