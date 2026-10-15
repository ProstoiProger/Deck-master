"""Backend-neutral drawing primitives. Layouts emit these, the PPTX and PDF backends draw them, lint inspects them.

All geometry is in inches on a 13.333 x 7.5 canvas, origin top-left. Colors are resolved hex strings.
"""
from dataclasses import dataclass, field

W, H = 13.333, 7.5


@dataclass
class Shape:
    x: float
    y: float
    w: float
    h: float
    fill: str = None
    line: str = None
    line_w: float = 1.0
    kind: str = "rect"       # rect | round | ellipse
    radius: float = 0.12     # inches, kind == round
    alpha: float = 1.0


@dataclass
class Text:
    x: float
    y: float
    w: float
    h: float
    text: str
    size: float = 18
    color: str = "#FFFFFF"
    role: str = "body"       # heading | body | mono
    bold: bool = False
    align: str = "left"      # left | center | right
    valign: str = "top"      # top | middle | bottom
    line_h: float = 1.2
    chrome: bool = False     # footer and other furniture, exempt from density rules


@dataclass
class Image:
    x: float
    y: float
    w: float
    h: float
    path: str


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    color: str = "#FFFFFF"
    width: float = 1.0
    dash: bool = False


@dataclass
class SceneSlide:
    index: int
    layout: str
    title: str
    bg: str
    items: list = field(default_factory=list)
    notes: str = ""
    time: float = None
    problems: list = field(default_factory=list)   # layout-time findings, surfaced by lint
