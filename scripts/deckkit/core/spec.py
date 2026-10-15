"""Markdown outline -> Deck. One file holds the whole deck.

    ---                       deck front matter (YAML)
    title: Team - value proposition
    event: hackathon
    ---
    # Slide title as a takeaway
    layout: kpi               slide properties: lowercase `key: value` lines right after the title
    notes: Speaker notes.     indented lines continue the previous property
    source: runs/log.jsonl#a
    - 92% | F1 | vs 81% baseline        bullets; ` | ` splits cells
    ---                       next slide
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

PROP = re.compile(r"^([a-z_][a-z0-9_]*):[ \t]*(.*)$")
SEP = re.compile(r"^\s*---\s*$")
BULLET = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
IMAGE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")


class SpecError(ValueError):
    pass


@dataclass
class Item:
    text: str
    cells: list = field(default_factory=list)
    level: int = 0
    ordered: bool = False


@dataclass
class Slide:
    index: int
    title: str
    layout: str = "bullets"
    props: dict = field(default_factory=dict)
    items: list = field(default_factory=list)
    groups: list = field(default_factory=list)      # [(heading, [Item])] split by `## heading`
    paragraphs: list = field(default_factory=list)
    table: list = field(default_factory=list)       # rows of cells, header first
    code: str = ""
    image: str = ""
    quote: str = ""
    notes: str = ""
    source: str = ""
    time: float = None
    rubric: list = field(default_factory=list)

    def prop(self, key, default=""):
        return self.props.get(key, default)

    def text_blob(self):
        parts = [self.title, *self.paragraphs, self.quote]
        parts += [i.text for i in self.items]
        parts += [c for row in self.table for c in row]
        return "\n".join(p for p in parts if p)


@dataclass
class Deck:
    meta: dict
    slides: list
    path: Path = None

    @property
    def base_dir(self):
        return self.path.parent if self.path else Path(".")

    def resolve(self, rel):
        p = Path(rel)
        return p if p.is_absolute() else (self.base_dir / p)


def _split_chunks(lines):
    chunks, cur, fence = [], [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            fence = not fence
        if not fence and SEP.match(ln):
            chunks.append(cur)
            cur = []
        else:
            cur.append(ln)
    chunks.append(cur)
    return chunks


def _cells(text):
    return [c.strip() for c in re.split(r"\s+\|\s+", text.strip())] if " | " in text else []


def _parse_slide(index, chunk):
    lines = list(chunk)
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines or not lines[0].startswith("# "):
        first = lines[0][:60] if lines else "(empty)"
        raise SpecError(f"slide {index}: first line must be '# Title', got {first!r}")
    slide = Slide(index=index, title=lines[0][2:].strip())
    i, last = 1, None
    while i < len(lines):
        ln = lines[i]
        m = PROP.match(ln)
        if m:
            last = m.group(1)
            slide.props[last] = m.group(2).strip()
            i += 1
        elif last and ln.startswith("  ") and ln.strip():
            slide.props[last] = (slide.props[last] + "\n" + ln.strip()).strip()
            i += 1
        else:
            break
    body = lines[i:]
    heading, bucket = "", []
    in_code, code = False, []

    def flush():
        if bucket or heading:
            slide.groups.append((heading, list(bucket)))

    for ln in body:
        if ln.strip().startswith("```"):
            if in_code:
                slide.code = "\n".join(code)
                code, in_code = [], False
            else:
                in_code = True
            continue
        if in_code:
            code.append(ln)
            continue
        s = ln.strip()
        if not s:
            continue
        if s.startswith("## "):
            flush()
            heading, bucket = s[3:].strip(), []
            continue
        m = IMAGE.match(s)
        if m:
            slide.image = m.group(2)
            continue
        if s.startswith("|"):
            row = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in row if c):
                continue
            slide.table.append(row)
            continue
        if s.startswith("> "):
            slide.quote = (slide.quote + " " + s[2:]).strip()
            continue
        m = BULLET.match(ln)
        if m:
            level = len(m.group(1).replace("\t", "    ")) // 2
            text = m.group(3).strip()
            item = Item(text=text, cells=_cells(text), level=level, ordered=m.group(2)[0].isdigit())
            bucket.append(item)
            slide.items.append(item)
            continue
        slide.paragraphs.append(s)
    flush()
    p = slide.props
    slide.layout = p.get("layout", "bullets")
    slide.notes = " ".join(p.get("notes", "").split())
    slide.source = p.get("source", "")
    slide.image = p.get("image", slide.image)
    if p.get("time"):
        try:
            slide.time = float(p["time"].rstrip("s"))
        except ValueError:
            raise SpecError(f"slide {index}: time must be seconds, got {p['time']!r}")
    slide.rubric = [r.strip() for r in re.split(r"[,\s]+", p.get("rubric", "")) if r.strip()]
    return slide


def parse_text(text, path=None):
    lines = text.replace("\r\n", "\n").lstrip("﻿").split("\n")
    meta = {}
    if lines and SEP.match(lines[0]):
        try:
            end = next(k for k in range(1, len(lines)) if SEP.match(lines[k]))
        except StopIteration:
            raise SpecError("front matter opened with --- but never closed")
        try:
            meta = yaml.safe_load("\n".join(lines[1:end])) or {}
        except yaml.YAMLError as e:
            raise SpecError(f"front matter is not valid YAML: {e}")
        if not isinstance(meta, dict):
            raise SpecError("front matter must be a YAML mapping")
        lines = lines[end + 1:]
    slides = []
    for chunk in _split_chunks(lines):
        if not any(c.strip() for c in chunk):
            continue
        slides.append(_parse_slide(len(slides) + 1, chunk))
    if not slides:
        raise SpecError("deck has no slides")
    return Deck(meta=meta, slides=slides, path=Path(path) if path else None)


def load_deck(path):
    p = Path(path)
    return parse_text(p.read_text(encoding="utf-8"), p)
