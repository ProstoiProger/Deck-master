"""Canvas: the drawing helper layouts use. Style-aware (round, square or pixel corners; soft, hard or no shadow)."""
import math
from pathlib import Path

from . import color, entities, pixelart, shapes3d, textfit
from .scene import H, W, Image, Line, Poly, SceneSlide, Shape, Text

MARGIN = 0.7
CONTENT_TOP = 2.0
CONTENT_BOTTOM = 6.4  # leaves room for the walkers that stand on the floor strip of the game themes


class Canvas:
    def __init__(self, theme, slide, deck, total):
        self.t = theme
        self.slide = slide
        self.deck = deck
        self.total = total
        self.scene = SceneSlide(index=slide.index, layout=slide.layout, title=slide.title, bg=theme.c("bg"),
                                notes=slide.notes, time=slide.time)
        self.items = self.scene.items
        self.style = theme.style
        self.pixel = self.style["corner"] == "pixel"
        self.game = self.style.get("metaphor") == "game"
        self.has_backdrop = False
        self.badge_mob = None
        self.walkers = []
        self._plan_decor()

    # ---- raw primitives -------------------------------------------------
    def rect(self, x, y, w, h, fill=None, line=None, line_w=1.0, kind="rect", radius=0.12, alpha=1.0):
        s = Shape(x, y, w, h, self.t.c(fill) if fill else None, self.t.c(line) if line else None, line_w, kind, radius, alpha)
        self.items.append(s)
        return s

    def line(self, x1, y1, x2, y2, col="border", width=1.0, dash=False):
        self.items.append(Line(x1, y1, x2, y2, self.t.c(col), width, dash))

    def text(self, x, y, w, h, text, size=18, col="text", role="body", bold=False, align="left", valign="top",
             line_h=1.2, chrome=False):
        if role != "body" and textfit.missing_glyphs(self.t, role, text, bold):
            role = "body"  # the themed font lacks a glyph (e.g. Kazakh letters in a mono font): use the body font
        t = Text(x, y, w, h, str(text), size, self.t.c(col), role, bold, align, valign, line_h, chrome)
        self.items.append(t)
        return t

    def fit_text(self, x, y, w, h, text, max_size=20, min_size=11, col="text", role="body", bold=False, align="left",
                 valign="top", line_h=1.2):
        size, _, ok = textfit.fit(self.t, text, role, w, h, max_size, min_size, bold, line_h)
        self.text(x, y, w, h, text, size, col, role, bold, align, valign, line_h)
        return size

    def image(self, x, y, w, h, rel, label="image"):
        """Place an image contained in the box; a labelled placeholder (and a problem) when the file is missing."""
        p = self.deck.resolve(rel) if rel else None
        if p is None or not Path(p).exists():
            self.box(x, y, w, h, fill="surface", line="border")
            self.text(x + 0.2, y, w - 0.4, h, f"[{label}]" if not rel else f"[missing: {rel}]", 14, "muted", "mono",
                      align="center", valign="middle")
            if rel:
                self.scene.problems.append(f"image not found: {rel}")
            return None
        from PIL import Image as PILImage
        with PILImage.open(p) as im:
            iw, ih = im.size
        k = min(w / iw, h / ih)
        nw, nh = iw * k, ih * k
        img = Image(x + (w - nw) / 2, y + (h - nh) / 2, nw, nh, str(Path(p).resolve()))
        self.items.append(img)
        return img

    # ---- style-aware shapes ---------------------------------------------
    def _notched(self, x, y, w, h, s, fill):
        self.rect(x + s, y, w - 2 * s, h, fill)
        self.rect(x, y + s, w, h - 2 * s, fill)

    def box(self, x, y, w, h, fill="surface", line="border", shadow=None, radius=None):
        """A card. Round, square or pixel-bevel depending on the theme style; surface cards follow the theme's `card` style
        (fill, outline or flat)."""
        radius = self.style["radius"] if radius is None else radius
        f = self.t.c(fill)
        shadow = (self.style["shadow"] != "none") if shadow is None else shadow
        card = self.style["card"]
        force_line = False
        if fill == "surface" and not self.pixel and card == "glass":
            return self._glass(x, y, w, h, radius)
        if fill == "surface" and not self.pixel and card == "bracket":
            return self._bracket(x, y, w, h)
        if fill == "surface" and not self.pixel and card in ("outline", "flat"):
            shadow = False
            if card == "outline":
                f = self.t.c("bg")
                line = color.mix(self.t.c("bg"), self.t.c("text"), 0.32)
                force_line = True
            else:
                line = None
        if self.pixel and min(w, h) > 0.35:
            s = 0.07
            if self.style["shadow"] == "hard":
                self._notched(x + s, y + s, w, h, s, color.darken(self.t.c("bg"), 0.5))
            outline = color.darken(f, 0.65)
            self._notched(x, y, w, h, s, outline)
            self._notched(x + s, y + s, w - 2 * s, h - 2 * s, s * 0.6, f)
            light, dark = color.lighten(f, 0.22), color.darken(f, 0.35)
            self.rect(x + 2 * s, y + s, w - 4 * s, s * 0.7, light)
            self.rect(x + s, y + 2 * s, s * 0.7, h - 4 * s, light)
            self.rect(x + 2 * s, y + h - 1.7 * s, w - 4 * s, s * 0.7, dark)
            self.rect(x + w - 1.7 * s, y + 2 * s, s * 0.7, h - 4 * s, dark)
            return
        kind = "rect" if self.style["corner"] == "square" else "round"
        if shadow and self.style["shadow"] == "soft":
            self.rect(x + 0.03, y + 0.05, w, h, color.darken(self.t.c("bg"), 0.45), None, kind=kind, radius=radius, alpha=0.55)
        draw_line = line if (self.style["border"] != "none" or force_line) else None
        self.rect(x, y, w, h, f, draw_line, 1.25 if force_line else 1.0, kind, min(radius, h / 2, w / 2))

    def _glass(self, x, y, w, h, radius):
        """Glassmorphism card: a frosted pane, a light edge and a highlight along the top."""
        t = self.t
        dark = t.mode == "dark"
        kind = "rect" if self.style["corner"] == "square" else "round"
        r = min(radius, h / 2, w / 2)
        if not dark:
            self.rect(x + 0.03, y + 0.06, w, h, color.mix(t.c("bg"), t.c("primary"), 0.35), None, 1.0, kind, r, 0.22)
        # the pane is the color a translucent layer would give over the page, drawn opaque so text on it keeps a known contrast
        # even where a card sits on a colored band
        pane = color.mix(t.c("bg"), t.c("text"), 0.09) if dark else color.mix(t.c("bg"), "#FFFFFF", 0.65)
        self.rect(x, y, w, h, pane, None, 1.0, kind, r)
        edge = color.mix(t.c("bg"), t.c("text"), 0.30) if dark else color.mix("#FFFFFF", t.c("primary"), 0.25)
        self.rect(x, y, w, h, None, edge, 1.0, kind, r)
        inset = r * 0.8
        self.rect(x + inset, y + 0.015, max(w - 2 * inset, 0.01), 0.02, "#FFFFFF", None, 1.0, "rect", 0, 0.38 if dark else 0.95)

    def _bracket(self, x, y, w, h):
        """HUD card: an opaque panel with a hairline edge and bright corner brackets."""
        t = self.t
        self.rect(x, y, w, h, t.c("surface"))
        self.rect(x, y, w, h, None, color.mix(t.c("surface"), t.c("accent"), 0.30), 0.75)
        ln = min(0.24, w / 4, h / 4)
        for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
            self.line(cx, cy, cx + dx * ln, cy, t.c("accent"), 1.75)
            self.line(cx, cy, cx, cy + dy * ln, t.c("accent"), 1.75)

    def badge(self, cx, cy, r, label, fill="primary", size=None):
        """Round number badge, a square block in pixel themes."""
        if self.pixel:
            self.box(cx - r, cy - r, 2 * r, 2 * r, fill=fill, shadow=False)
        elif self.style["corner"] == "square":
            self.rect(cx - r, cy - r, 2 * r, 2 * r, fill)
        else:
            self.rect(cx - r, cy - r, 2 * r, 2 * r, fill, kind="ellipse")
        self.text(cx - r, cy - r, 2 * r, 2 * r, label, size or max(12, r * 36), self.t.on(fill), "heading" if not self.pixel else "mono",
                  True, "center", "middle")

    def pill(self, x, y, label, fill="surface", col="muted", size=12, h=0.36, role="mono", bold=True, pad=0.2):
        tw = textfit.width_in(self.t, label, role, size, bold)
        if self.style["chips"] == "text" and not self.pixel:
            # formal themes: a plain label with a hairline under it instead of a chip
            self.text(x, y, tw + 0.1, h, label, size, col, role, bold, "left", "middle")
            self.rect(x, y + h - 0.03, tw, 0.015, color.mix(self.t.c("bg"), self.t.c("text"), 0.3))
            return tw + 0.3
        w = tw + 2 * pad
        if self.pixel:
            self.box(x, y, w, h, fill=fill, shadow=False)
        else:
            self.rect(x, y, w, h, fill, self.t.c("border"), 1.0, "round", h / 2)
        self.text(x, y, w, h, label, size, col, role, bold, "center", "middle")
        return w

    # ---- mob decoration (game themes) ----------------------------------------
    OBSIDIAN_POOL = ["creeper", "enderman", "skeleton", "witch", "ghast", "spider", "blaze", "warden", "phantom", "vex", "shulker",
                     "evoker", "guardian", "magma-cube", "husk", "stray", "drowned", "endermite"]
    CLASSIC_POOL = ["pig", "cow", "sheep", "chicken", "wolf", "fox", "panda", "bee", "parrot", "rabbit", "villager", "steve", "alex",
                    "cat", "horse", "turtle", "mooshroom", "iron-golem"]

    def _mob_pool(self):
        raw = self.slide.prop("mobs") or self.deck.meta.get("mobs")
        if isinstance(raw, str):
            raw = [r.strip() for r in raw.split(",") if r.strip()]
        if not raw:
            raw = self.CLASSIC_POOL if self.style["pattern"] == "classic" else self.OBSIDIAN_POOL
        return [n for n in raw if entities.known(n) and entities.find(n, "face")]

    def _plan_decor(self):
        """Every content slide of a game theme gets a mob badge beside the title and walkers on the floor strip."""
        s = self.slide
        if not self.game or s.layout in ("title", "closing") or s.prop("decor") == "none":
            return
        pool = self._mob_pool()
        if not pool:
            if s.index == 2:
                self.scene.problems.append("[Low] game decoration skipped: no character images; run: python scripts/cli.py entities fetch")
            return
        i = s.index
        self.badge_mob = pool[i % len(pool)]
        taken = {self.badge_mob}
        for k in range(1, 3 * len(pool)):
            cand = pool[(i * 3 + k) % len(pool)]
            if cand not in taken and len(self.walkers) < 3:
                self.walkers.append(cand)
                taken.add(cand)

    def _mob_image(self, name, x, y, size, kind="head"):
        path = entities.find(name, kind) or entities.find(name, "face")
        if path:
            self.items.append(Image(x, y, size, size, str(Path(path).resolve())))
        return path

    def _xp_progress(self):
        """Slide progress as an XP bar along the top edge (game themes)."""
        frac = self.slide.index / max(self.total, 1)
        self.rect(0, 0, W, 0.1, color.darken(self.t.c("bg"), 0.45))
        self.rect(0, 0, W * frac, 0.1, "success")
        self.rect(0, 0, W * frac, 0.035, color.lighten(self.t.c("success"), 0.35))
        for k in range(1, 10):
            self.rect(W * k / 10 - 0.01, 0, 0.02, 0.1, color.darken(self.t.c("bg"), 0.6), alpha=0.8)

    def _game_footer(self):
        """Floor strip with the footer text, and walkers standing on it."""
        t = self.t
        self._xp_progress()
        h = 0.34
        y = H - h
        sz = 0.34
        if self.style["pattern"] == "classic":
            a, b = t.c("secondary"), color.darken(t.c("secondary"), 0.22)
            top = "#4C9A2A"
        else:
            a, b = color.darken(t.c("surface"), 0.35), color.darken(t.c("surface"), 0.15)
            top = t.c("primary")
        for i in range(int(W / sz) + 1):
            bw = min(sz, W - i * sz)
            if bw > 0.01:
                self.rect(i * sz, y, bw, h, a if (i * 5 + 1) % 3 else b)
        self.rect(0, y - 0.05, W, 0.05, top)
        txt = t.on(a)
        foot = str(self.deck.meta.get("footer") or self.deck.meta.get("title", ""))
        if len(foot) > 70:
            foot = foot[:67] + "..."
        self.text(MARGIN, y, 9.0, h, foot, 11, txt, "mono", chrome=True, valign="middle")
        self.text(W - MARGIN - 1.6, y, 1.6, h, f"{self.slide.index:02d} / {self.total:02d}", 11, txt, "mono", align="right", chrome=True,
                  valign="middle")
        slots = [1.7, 4.2, 6.7, 9.2, 11.4]
        start = self.slide.index % len(slots)
        for k, name in enumerate(self.walkers):
            x = slots[(start + 2 * k) % len(slots)]
            self._mob_image(name, x, y - 0.05 - 0.8 + 0.12, 0.8, "head")  # stands in the floor strip

    # ---- pixel icons, inventory slots, bars --------------------------------------
    def icon(self, name, x, y, size, clip=1.0):
        """Draw a pixel icon `size` inches wide (height follows the bitmap). Returns its height."""
        cols, rows = pixelart.size_of(name)
        px = size / cols
        for c, r, ln, col in pixelart.runs(name, clip):
            self.rect(x + c * px, y + r * px, ln * px + 0.004, px + 0.004, col)
        return px * rows

    def slot(self, x, y, size, icon=None, entity=None, count=None, selected=False, face=True):
        """Inventory slot: inset bevel, an icon or a character, an item count, optional selection frame."""
        base = color.darken(self.t.c("surface"), 0.25) if self.t.mode == "dark" else "#8B8B8B"
        edge = 0.045
        self.rect(x, y, size, size, base)
        self.rect(x, y, size, edge, color.darken(base, 0.55))
        self.rect(x, y, edge, size, color.darken(base, 0.55))
        self.rect(x, y + size - edge, size, edge, color.lighten(base, 0.45))
        self.rect(x + size - edge, y, edge, size, color.lighten(base, 0.45))
        pad = size * 0.15
        if icon:
            w = size - 2 * pad
            cols, rows = pixelart.size_of(icon)
            h = w * rows / cols
            self.icon(icon, x + pad, y + (size - h) / 2, w)
        elif entity:
            self._mob_image(entity, x + pad * 0.6, y + pad * 0.6, size - 1.2 * pad, "face" if face else "head")
        if count not in (None, ""):  # count on a small dark chip so it stays readable over any icon
            cw = max(0.3, textfit.width_in(self.t, str(count), "mono", 12, True) + 0.14)
            self.rect(x + size - cw - 0.05, y + size - 0.3, cw, 0.25, "#000000", alpha=0.9)
            self.text(x + size - cw - 0.05, y + size - 0.3, cw, 0.25, str(count), 12, "#FFFFFF", "mono", True, "center", "middle", chrome=True)
        if selected:
            f = 0.06
            for rx, ry, rw, rh in ((x - f, y - f, size + 2 * f, f), (x - f, y + size, size + 2 * f, f), (x - f, y, f, size), (x + size, y, f, size)):
                self.rect(rx, ry, rw, rh, "accent")

    def bar(self, x, y, w, h, frac, fill="success", ticks=10):
        """Segmented pixel progress bar (health, XP, boss bar)."""
        frac = max(0.0, min(1.0, frac))
        self.rect(x, y, w, h, color.darken(self.t.c("bg"), 0.4))
        self.rect(x + 0.04, y + 0.04, w - 0.08, h - 0.08, color.darken(self.t.c("surface"), 0.2))
        if frac > 0:
            self.rect(x + 0.04, y + 0.04, (w - 0.08) * frac, h - 0.08, fill)
            self.rect(x + 0.04, y + 0.04, (w - 0.08) * frac, (h - 0.08) * 0.35, color.lighten(self.t.c(fill), 0.3), alpha=0.7)
        for k in range(1, ticks):
            self.rect(x + 0.04 + (w - 0.08) * k / ticks - 0.01, y + 0.04, 0.02, h - 0.08, color.darken(self.t.c("bg"), 0.5), alpha=0.8)

    def meter(self, x, y, frac, kind="heart", n=10, size=0.34, gap=0.05):
        """Row of n hearts, drumsticks, shields or XP orbs filled to frac (halves work)."""
        full, empty = {"heart": ("heart", "heart_empty"), "hunger": ("drumstick", "drumstick_empty"), "armor": ("shield", "shield_empty"),
                       "xp": ("xp", "xp_empty")}[kind]
        total = max(0.0, min(1.0, frac)) * n
        for i in range(n):
            xi = x + i * (size + gap)
            self.icon(empty, xi, y, size)
            part = max(0.0, min(1.0, total - i))
            if part > 0:
                self.icon(full, xi, y, size, clip=part)
        return n * (size + gap) - gap

    # ---- polygons and symbols ------------------------------------------------------
    def poly(self, points, fill=None, line=None, line_w=1.0, alpha=1.0):
        p = Poly([(float(x), float(y)) for x, y in points], self.t.c(fill) if fill else None, self.t.c(line) if line else None, line_w, alpha)
        self.items.append(p)
        return p

    def chevron(self, x, y, w, h, fill, notch=0.3, first=False, line=None):
        left = x if first else x + notch
        return self.poly([(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h), (x, y + h), (left, y + h / 2)] if not first else
                         [(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h), (x, y + h)], fill, line)

    def arrow(self, x, y, w, h, fill, head=0.35):
        b = h * 0.28
        return self.poly([(x, y + b), (x + w - head, y + b), (x + w - head, y), (x + w, y + h / 2), (x + w - head, y + h), (x + w - head, y + h - b),
                          (x, y + h - b)], fill)

    def triangle(self, cx, cy, r, fill, up=True):
        d = -1 if up else 1
        return self.poly([(cx, cy + d * r), (cx + r, cy - d * r), (cx - r, cy - d * r)], fill)

    def tick(self, x, y, size, col="success", width=3.0):
        self.line(x, y + size * 0.55, x + size * 0.35, y + size, col, width)
        self.line(x + size * 0.35, y + size, x + size, y, col, width)

    def cross(self, x, y, size, col="danger", width=3.0):
        self.line(x, y, x + size, y + size, col, width)
        self.line(x + size, y, x, y + size, col, width)

    # ---- scene furniture --------------------------------------------------
    def title(self, text=None, y=0.5, h=1.12, max_size=32, col="text"):
        text = text or self.slide.title
        scale = self.style["heading_scale"]
        lh = self.style["heading_line_h"]
        tw = W - 2 * MARGIN - (1.05 if self.badge_mob else 0)
        size, _, _ = textfit.fit(self.t, text, "heading", tw, h, max_size * scale, 14 * scale, True, lh)
        self.text(MARGIN, y, tw, h, text, size, col, "heading", True, "left", "top", lh)
        self._deco()
        if self.badge_mob:  # a framed mob head at the right end of the title line
            self.box(W - MARGIN - 0.85, 0.42, 0.85, 0.85, fill="surface", shadow=False)
            self._mob_image(self.badge_mob, W - MARGIN - 0.85 + 0.07, 0.42 + 0.07, 0.71, "face")
        return size

    def _deco(self):
        """Small furniture on content slides, set by the theme's `deco` key: tri (a corner triangle) or tab (a left edge tab)."""
        deco = self.style.get("deco", "none")
        if deco == "tri":
            self.poly([(W - 0.7, 0), (W, 0), (W, 0.7)], self.t.c("accent"))
        elif deco == "tab":
            self.rect(0, 0.62, 0.16, 0.95, "accent")
        elif deco == "glow":     # two soft color blooms behind the content, drawn first so they sit under everything
            for cx, cy, r, col in ((W - 1.0, 0.4, 3.6, "primary"), (1.2, H - 0.2, 3.2, "accent")):
                for k in (1.0, 0.88, 0.76, 0.64, 0.52, 0.4, 0.28, 0.16):
                    s = self.rect(cx - r * k, cy - r * k, 2 * r * k, 2 * r * k, col, kind="ellipse", alpha=0.02)
                    self.items.remove(s)
                    self.items.insert(0, s)
        elif deco == "hud":      # a short scale of ticks in the top-right corner
            for i in range(16):
                hh = 0.1 + 0.12 * ((i * 5) % 4) / 3 + (0.08 if i % 5 == 0 else 0)
                self.rect(W - MARGIN - 1.6 + i * 0.1, 0.45 - hh, 0.035, hh, "accent", alpha=0.85 if i % 5 == 0 else 0.45)

    def accent_rule(self, x=MARGIN, y=1.76, w=0.9):
        mode = self.style["title_rule"] if abs(y - 1.76) < 0.01 else "bar"  # title and closing slides always use the short bar
        if mode == "none":
            return
        if self.pixel:
            self.rect(x, y, w, 0.1, "primary")
            self.rect(x + w + 0.08, y, 0.3, 0.1, "accent")
        elif mode == "line":
            self.rect(x, y + 0.02, W - x - MARGIN, 0.015, color.mix(self.t.c("bg"), self.t.c("text"), 0.3))
            self.rect(x, y, w, 0.05, "accent")
        else:
            self.rect(x, y, w, 0.06, "accent", kind="round", radius=0.03)

    def eyebrow(self, label):
        self.text(MARGIN, 0.28, 8, 0.28, label.upper(), 11, "accent", "mono", True, chrome=True)

    def footer(self):
        if self.has_backdrop:
            return  # title and closing slides carry no footer
        if self.game:
            return self._game_footer()
        foot = str(self.deck.meta.get("footer") or self.deck.meta.get("title", ""))
        if len(foot) > 70:
            foot = foot[:67] + "..."
        if self.style["show_source"] and self.slide.source:
            self.text(MARGIN, 6.6, W - 2 * MARGIN, 0.3, f"Source: {self.slide.source}", 11, "muted", "body", chrome=True, valign="middle")
        if self.style["footer"] == "rule":
            self.rect(MARGIN, 6.98, W - 2 * MARGIN, 0.015, color.mix(self.t.c("bg"), self.t.c("text"), 0.3))
        self.text(MARGIN, 7.04, 9.0, 0.28, foot, 11, "muted", "mono", chrome=True, valign="middle")
        self.text(W - MARGIN - 1.6, 7.04, 1.6, 0.28, f"{self.slide.index:02d} / {self.total:02d}", 11, "muted", "mono",
                  align="right", chrome=True, valign="middle")

    def backdrop(self, strength=1.0, portal=True):
        """Decorative pattern for title and closing slides. Light, flat vector shapes only.
        `portal=False` keeps the right side free (a mascot stands there)."""
        t = self.t
        pat = self.style["pattern"]
        self.has_backdrop = True
        if self.game:
            self._xp_progress()
        if pat == "obsidian":
            self._obsidian(portal)
            return
        if pat == "classic":
            self._classic()
            return
        if pat == "blocks":
            sz, n = 0.5, int(W / 0.5) + 1
            cols = [t.c("primary"), color.darken(t.c("primary"), 0.25), t.c("secondary"), color.darken(t.c("secondary"), 0.25)]
            for i in range(n):
                top = (i * 7) % 4
                bw = min(sz, W - i * sz)
                if bw <= 0.01:
                    continue
                self.rect(i * sz, H - 0.5, bw, 0.5, cols[2 + (i + top) % 2])
                self.rect(i * sz, H - 0.5 - 0.14, bw, 0.14, cols[(i + top) % 2])
            return
        if pat == "none":
            return
        if pat in self.PATTERNS:
            if getattr(self, "_pat_" + pat)():
                return
            pat = "grid"  # the pattern could not be drawn (e.g. numpy missing): fall back to the default glow
        if pat == "clean":
            self.rect(0, 0, 0.28, H, "primary")
            self.rect(0.28, 0, 0.06, H, "accent")
            return
        if pat == "rules":
            rc = color.mix(t.c("bg"), t.c("text"), 0.35)
            self.rect(MARGIN, 0.72, 0.9, 0.07, "accent")
            self.rect(MARGIN, 0.82, W - 2 * MARGIN, 0.02, rc)
            self.rect(MARGIN, 6.62, W - 2 * MARGIN, 0.02, rc)
            return
        if pat == "band":
            bw = 4.7
            self.rect(W - bw, 0, bw, H, "primary")
            on = t.on("primary")
            for r, a in ((3.6, 0.06), (2.7, 0.07), (1.8, 0.09)):
                self.rect(W - bw / 2 - r + 0.3, 3.2 - r, 2 * r, 2 * r, on, kind="ellipse", alpha=a)
            for k in range(6):
                self.rect(W - bw + 0.5 + k * 0.62, 0, 0.05, H, on, alpha=0.08)
            self.rect(W - bw, 0, 0.12, H, "accent")
            return
        if pat == "grid":
            line_col = color.mix(t.c("bg"), t.c("text"), 0.06 * strength)
            x0 = W * 0.52
            step = 0.55
            for k in range(int((W - x0) / step) + 1):
                self.line(x0 + k * step, 0, x0 + k * step, H, line_col, 0.75)
            for k in range(int(H / step) + 1):
                self.line(x0, k * step, W, k * step, line_col, 0.75)
        glow = t.c("primary")
        for r, a in ((3.4, 0.05), (2.5, 0.07), (1.7, 0.10)):
            self.rect(W - 2.6 - r, 1.9 - r, 2 * r, 2 * r, glow, kind="ellipse", alpha=a * (1.0 if t.mode == "dark" else 0.7))
        acc = t.c("accent")
        for r, a in ((1.9, 0.05), (1.2, 0.08)):
            self.rect(W - 1.2 - r, H - 1.3 - r, 2 * r, 2 * r, acc, kind="ellipse", alpha=a)

    PATTERNS = ("mesh", "hatch", "corner", "dots", "blueprint", "rings", "bars", "hud", "orbs3d")

    def _hatch(self, x0, y0, w, h, step=0.3, col=None, width=0.75, alpha_col=None):
        """Diagonal lines (45 degrees, rising to the right) clipped to a rectangle."""
        col = col or color.mix(self.t.c("bg"), self.t.c("text"), 0.18)
        k = -h
        while k < w:
            xa, ya = x0 + max(k, 0), y0 + h - max(-k, 0)       # lower-left end of this line inside the box
            run = min(w - max(k, 0), h - max(-k, 0))
            if run > 0.02:
                self.line(xa, ya, xa + run, ya - run, col, width)
            k += step

    def _pat_mesh(self):
        try:
            from ..charts.mesh import render_mesh
            path, tone = render_mesh(self.t, self.deck, key="cover")
        except Exception as e:  # numpy or Pillow missing, or an unreadable cache folder
            self.scene.problems.append(f"[Low] mesh backdrop not drawn ({type(e).__name__}); install scripts/requirements/charts.txt")
            return False
        self.items.append(Image(0, 0, W, H, path, tone))
        return True

    def _pat_hatch(self):
        t = self.t
        self.rect(W - 3.1, 0, 3.1, H, "primary")
        on = t.on("primary")
        self._hatch(W - 3.1, 0, 3.1, H, 0.34, color.mix(t.c("primary"), on, 0.22), 1.0)
        self.rect(W - 3.1, 0, 0.1, H, "accent")
        self._hatch(MARGIN, 6.85, 6.0, 0.4, 0.18, color.mix(t.c("bg"), t.c("text"), 0.28), 1.5)
        return True

    def _pat_corner(self):
        t = self.t
        self.poly([(W - 5.2, 0), (W, 0), (W, 5.2)], t.c("primary"))
        self.poly([(W - 2.9, 0), (W, 0), (W, 2.9)], t.c("accent"))
        self.poly([(0, H), (1.2, H), (0, H - 1.2)], t.c("secondary"), alpha=0.9)
        return True

    def _pat_dots(self):
        t = self.t
        col = color.mix(t.c("bg"), t.c("text"), 0.16)
        for i in range(14):
            for j in range(9):
                x, y = W * 0.5 + i * 0.5, 0.35 + j * 0.78
                big = (i + j) % 7 == 0
                self.rect(x, y, 0.16 if big else 0.07, 0.16 if big else 0.07, t.c("accent") if big else col, kind="ellipse")
        self.rect(0, 0, 0.18, H, "primary")
        return True

    def _pat_blueprint(self):
        t = self.t
        faint = color.mix(t.c("bg"), t.c("text"), 0.07)
        for k in range(1, int(W / 0.5)):
            self.line(k * 0.5, 0, k * 0.5, H, faint, 0.5)
        for k in range(1, int(H / 0.5)):
            self.line(0, k * 0.5, W, k * 0.5, faint, 0.5)
        edge = color.mix(t.c("bg"), t.c("text"), 0.45)
        self.rect(0.3, 0.3, W - 0.6, H - 0.6, None, edge, 1.25)
        self.rect(W - 4.6, H - 1.15, 4.3, 0.85, t.c("bg"), edge, 1.0)
        self.line(W - 3.0, H - 1.15, W - 3.0, H - 0.3, edge, 1.0)
        self.line(W - 4.6, H - 0.72, W - 0.3, H - 0.72, edge, 1.0)
        self.rect(W - 4.45, H - 1.0, 0.45, 0.2, "accent")
        name = str(self.deck.meta.get("title", ""))
        name = (name[:30] + "...") if len(name) > 33 else name
        self.text(W - 2.9, H - 1.15, 2.5, 0.43, name.upper(), 11, "muted", "mono", True, valign="middle", chrome=True)
        self.text(W - 4.45, H - 0.72, 1.4, 0.42, "SHEET", 11, "muted", "mono", True, valign="middle", chrome=True)
        self.text(W - 2.9, H - 0.72, 2.5, 0.42, f"{self.slide.index:02d} / {self.total:02d}", 11, "muted", "mono", True, valign="middle", chrome=True)
        return True

    def _pat_rings(self):
        t = self.t
        ring = color.mix(t.c("bg"), t.c("text"), 0.14)
        cx, cy = W - 3.4, H / 2
        for r in (0.6, 1.2, 1.8, 2.4, 3.0):
            self.rect(cx - r, cy - r, 2 * r, 2 * r, None, ring, 1.0, "ellipse")
        for ang, r, col in ((0.6, 1.8, "accent"), (2.3, 1.2, "primary"), (4.0, 3.0, "secondary"), (5.2, 0.6, "accent")):
            self.rect(cx + r * math.cos(ang) - 0.11, cy + r * math.sin(ang) - 0.11, 0.22, 0.22, col, kind="ellipse")
        self.rect(MARGIN, 0.72, 0.9, 0.07, "accent")
        return True

    def _pat_hud(self):
        t = self.t
        shapes3d.wire_globe(self, W - 3.0, H / 2, 2.4, color.mix(t.c("bg"), t.c("text"), 0.22), t.c("accent"), lat0=22, lon0=66)
        for ang, lat, lon, col in ((0, 43, 77, "accent"), (1, 51, 7, "secondary"), (2, 28, 117, "accent")):
            x, y, vis = shapes3d.project_globe(lat, lon, 22, 66, 2.4)
            if vis:
                self.rect(W - 3.0 + x - 0.07, H / 2 + y - 0.07, 0.14, 0.14, col, kind="ellipse")
                self.rect(W - 3.0 + x - 0.16, H / 2 + y - 0.16, 0.32, 0.32, None, t.c(col), 1.0, "ellipse")
        edge = t.c("accent")
        for cx, cy, dx, dy in ((0.3, 0.3, 1, 1), (W - 0.3, 0.3, -1, 1), (0.3, H - 0.3, 1, -1), (W - 0.3, H - 0.3, -1, -1)):
            self.line(cx, cy, cx + dx * 0.55, cy, edge, 1.75)
            self.line(cx, cy, cx, cy + dy * 0.55, edge, 1.75)
        for i in range(24):
            self.rect(MARGIN + i * 0.07, 6.9, 0.02, 0.1 if i % 4 else 0.18, color.mix(t.c("bg"), t.c("accent"), 0.6))
        self.rect(MARGIN, 0.72, 0.9, 0.07, "accent")
        return True

    def _pat_orbs3d(self):
        try:
            from ..charts.render3d import render_hero
            path = render_hero(self.t, self.style.get("hero3d", "orbs"), self.deck)
        except Exception as e:  # numpy or Pillow missing
            self.scene.problems.append(f"[Low] 3D object not drawn ({type(e).__name__}); install scripts/requirements/charts.txt")
            return False
        self.items.append(Image(W - 6.4, 0.45, 6.1, 6.1, path))
        return True

    def _pat_bars(self):
        t = self.t
        n, bw, gap = 10, 0.3, 0.12
        x0 = W - MARGIN - n * (bw + gap)
        for i in range(n):
            hh = 0.8 + 3.2 * ((i * 37 % 11) / 10) * (0.35 + 0.65 * i / (n - 1))
            self.rect(x0 + i * (bw + gap), H - 0.9 - hh, bw, hh, "accent" if i == n - 1 else "primary", alpha=1.0 if i == n - 1 else 0.85)
        self.rect(x0 - 0.2, H - 0.9, n * (bw + gap) + 0.26, 0.03, color.mix(t.c("bg"), t.c("text"), 0.4))
        return True

    def _obsidian(self, portal):
        """Obsidian floor with purple veins and (optionally) a portal frame with a glowing purple interior."""
        t = self.t
        sz = 0.5
        base = [color.darken(t.c("surface"), 0.35), t.c("surface"), color.darken(t.c("surface"), 0.15)]
        vein = [t.c("primary"), t.c("accent"), t.c("info")]
        n = int(W / sz) + 1
        self.rect(0, H - 0.5 - 0.08, W, 0.08, "primary")
        for i in range(n):
            bw = min(sz, W - i * sz)
            if bw <= 0.01:
                continue
            self.rect(i * sz, H - 0.5, bw, 0.5, base[(i * 5 + 2) % 3])
            if (i * 7 + 3) % 5 == 0:
                self.rect(i * sz + 0.14, H - 0.5 + 0.12, 0.14, 0.14, vein[i % 3])
            if (i * 11 + 1) % 6 == 0:
                self.rect(i * sz + 0.3, H - 0.5 + 0.28, 0.1, 0.1, vein[(i + 1) % 3])
        if not portal:
            return
        px, py, cols, rows = W - 3.7, 1.0, 5, 9
        # glowing interior first, frame blocks on top
        self.rect(px + sz, py + sz, (cols - 2) * sz, (rows - 2) * sz, "primary", alpha=0.6)
        for k in range(6):
            self.rect(px + sz + 0.1 + (k % 2) * 0.35, py + sz + 0.2 + k * 0.62, 0.45, 0.2, "accent", alpha=0.28)
            self.rect(px + sz + 0.6 - (k % 2) * 0.2, py + sz + 0.5 + k * 0.62, 0.3, 0.16, "info", alpha=0.22)
        for r in range(rows):
            for c in range(cols):
                if r in (0, rows - 1) or c in (0, cols - 1):
                    self.box(px + c * sz, py + r * sz, sz, sz,
                             fill=color.lighten(t.c("surface"), 0.16 if (r + c) % 2 else 0.07), shadow=False)

    def _classic(self):
        """Sky with pixel clouds and a square sun, grass and dirt ground."""
        t = self.t
        sz = 0.5
        sun = "#FFE066"
        self.rect(W - 2.1, 0.45, 1.0, 1.0, sun)
        self.rect(W - 1.95, 0.6, 0.7, 0.7, "#FFF3B0")
        for cx, cy, scale in ((6.6, 0.7, 1.0), (9.4, 1.9, 0.8), (7.0, 4.6, 0.6)):
            for dx, dy, w, h in ((0.0, 0.3, 2.0, 0.35), (0.4, 0.0, 1.0, 0.35), (-0.3, 0.55, 2.4, 0.3)):
                self.rect(cx + dx * scale, cy + dy * scale, w * scale, h * scale, "#FFFFFF")
        n = int(W / sz) + 1
        grass, dirt = "#4C9A2A", t.c("secondary")
        dark_dirt = color.darken(dirt, 0.25)
        self.rect(0, H - 0.5 - 0.16, W, 0.16, grass)
        self.rect(0, H - 0.5 - 0.16, W, 0.05, color.lighten(grass, 0.25))
        for i in range(n):
            bw = min(sz, W - i * sz)
            if bw <= 0.01:
                continue
            self.rect(i * sz, H - 0.5, bw, 0.5, dirt if (i * 3) % 4 else dark_dirt)
            if (i * 5 + 1) % 4 == 0:
                self.rect(i * sz + 0.12, H - 0.5 + 0.18, 0.14, 0.14, color.lighten(dirt, 0.2))

    def code_block(self, x, y, w, h, code, max_size=18, min_size=11, col="text"):
        """Monospace code with its indentation kept. One text box per line, placed exactly, so PPTX and PDF agree.
        Shrinks the font until the longest line and all lines fit; returns the size used."""
        lines = [ln.expandtabs(4).rstrip() for ln in str(code).splitlines()]
        size = max_size
        while size > min_size:
            lh = size * 1.35 / 72
            widest = max((textfit.width_in(self.t, ln, "mono", size) for ln in lines), default=0.0)
            if widest <= w and len(lines) * lh <= h:
                break
            size -= 1
        lh = size * 1.35 / 72
        for i, ln in enumerate(lines):
            if ln.strip():
                indent = len(ln) - len(ln.lstrip(" "))
                off = indent * textfit.width_in(self.t, " ", "mono", size)
                self.text(x + off, y + i * lh, max(w - off, 0.5), lh, ln.strip(), size, col, "mono", False, "left", "top", 1.0, chrome=True)
        return size

    # ---- characters ---------------------------------------------------------
    def entity(self, name, x, y, size, kind="face", label=""):
        """Draw a character image. Missing image: initials badge for faces, nothing for other kinds, plus a Medium finding."""
        name = str(name).strip()
        path = None
        if not entities.known(name) and ("." in name or "/" in name):
            p = self.deck.resolve(name)  # a custom image path instead of a known entity
            path = p if p.exists() else None
            if path is None:
                self.scene.problems.append(f"image not found: {name}")
        elif not entities.known(name):
            self.scene.problems.append(f"[Medium] unknown entity {name!r}; known: {', '.join(sorted(entities.ENTITIES))}")
        else:
            path = entities.find(name, kind) or (entities.find(name, "face") if kind != "face" else None)
            if path is None:
                self.scene.problems.append(f"[Medium] entity {name!r} has no downloaded image; run: python scripts/cli.py entities fetch")
        if path is None:
            if kind == "face":
                self.badge(x + size / 2, y + size / 2, size / 2, "".join(w[0] for w in (label or name).split()[:2]).upper() or "?", "primary", 18)
            return None
        self.items.append(Image(x, y, size, size, str(Path(path).resolve())))
        return path

    def avatar(self, name, x, y, size, label=""):
        """Framed face for people-like slots (team members, hotbar slots)."""
        pad = 0.08
        self.box(x, y, size, size, fill="surface", shadow=False)
        return self.entity(name, x + pad, y + pad, size - 2 * pad, "face", label)

    def mascot(self, name, kind="head"):
        """Large character on the right side of title and closing slides."""
        size = 3.6
        x, y = W - 0.9 - size, H - 0.95 - size
        if self.style["pattern"] == "classic":
            y = H - 0.5 - 0.16 - size + 0.15  # stand on the grass
        return self.entity(name, x, y, size, kind)

    def content_box(self):
        return MARGIN, CONTENT_TOP, W - 2 * MARGIN, CONTENT_BOTTOM - CONTENT_TOP
