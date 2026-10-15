"""Layout registry: a decorator that rejects layouts without metadata (same idea as fe/registry.py in ds-master)."""
import hashlib
import inspect
from dataclasses import dataclass

from .canvas import Canvas

LAYOUTS = {}
FALLBACK = "bullets"


@dataclass
class LayoutSpec:
    name: str
    family: str
    purpose: str
    max_words: int
    fn: object
    accepts: str = ""
    example: str = ""

    def code_hash(self):
        return hashlib.sha256(inspect.getsource(self.fn).encode("utf-8")).hexdigest()[:10]


def layout(name, family, purpose, max_words, accepts="", example=""):
    def wrap(fn):
        if not purpose.strip():
            raise ValueError(f"layout {name} needs a purpose")
        if not max_words:
            raise ValueError(f"layout {name} needs max_words")
        LAYOUTS[name] = LayoutSpec(name, family, purpose, max_words, fn, accepts, example)
        return fn
    return wrap


def ensure_loaded():
    from .. import layouts  # noqa: F401  (importing registers every layout)


def get(name):
    ensure_loaded()
    return LAYOUTS.get(name)


def render_slide(slide, theme, deck, total):
    ensure_loaded()
    spec = LAYOUTS.get(slide.layout)
    c = Canvas(theme, slide, deck, total)
    if spec is None:
        c.scene.problems.append(f"unknown layout {slide.layout!r}; rendered as {FALLBACK}")
        spec = LAYOUTS[FALLBACK]
    try:
        spec.fn(c, slide)
    except Exception as e:  # a bad slide must become a finding, not a crash of the whole build
        c.scene.problems.append(f"layout {spec.name} failed: {type(e).__name__}: {e}")
    c.footer()
    return c.scene


def build_scenes(deck, theme):
    total = len(deck.slides)
    return [render_slide(s, theme, deck, total) for s in deck.slides]
