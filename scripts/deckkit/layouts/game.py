"""Minecraft-style game components: inventory, crafting, hud, advancements, trade, chat, strata, boss, leaderboard, book.

They are meant for the game themes (obsidian-craft, classic-craft) and render in any theme. Items may name a pixel icon
(heart, diamond, sword...; see core/pixelart.py) or a character (steve, creeper...; see core/entities.py).
"""
import re

from ..core import color, entities, pixelart, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import H, W
from ._util import cells, layer_items

GUI_W = W - 2 * MARGIN
ICONS = set(pixelart.names())


def _num(text):
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(text).replace(" ", ""))
    return float(m.group(0).replace(",", ".")) if m else None


def _ratio(text):
    """'72%' -> .72, '31 of 40' or '4.4 / 5' -> .775 / .88; anything else -> None."""
    t = str(text).strip()
    m = re.match(r"^(\d+(?:[.,]\d+)?)\s*%$", t)
    if m:
        return min(float(m.group(1).replace(",", ".")) / 100, 1.0)
    m = re.match(r"^(\d+(?:[.,]\d+)?)\s*(?:of|/)\s*(\d+(?:[.,]\d+)?)$", t)
    if m and float(m.group(2).replace(",", ".")):
        return min(float(m.group(1).replace(",", ".")) / float(m.group(2).replace(",", ".")), 1.0)
    return None


def _draw_spec(c, spec, x, y, size, selected=False, count=None, slot=True):
    """A slot (or bare icon) showing a pixel icon or a character; unknown specs leave an empty slot."""
    spec = (spec or "").strip()
    if spec and spec not in ICONS and not entities.known(spec):
        c.scene.problems.append(f"[Medium] unknown icon or character {spec!r}; icons: {', '.join(sorted(ICONS))}; characters: see `cli.py entities list`")
    if slot:
        if spec in ICONS:
            c.slot(x, y, size, icon=spec, count=count, selected=selected)
        elif entities.known(spec):
            c.slot(x, y, size, entity=spec, count=count, selected=selected)
        else:
            c.slot(x, y, size, count=count, selected=selected)
    elif spec in ICONS:
        cols, rows = pixelart.size_of(spec)
        c.icon(spec, x, y + (size - size * rows / cols) / 2, size)
    elif entities.known(spec):
        c._mob_image(spec, x, y, size, "face")


def _panel(c, x, y, w, h, label=None, fill="surface"):
    c.box(x, y, w, h, fill=fill)
    if label:
        c.text(x + 0.3, y + 0.14, w - 0.6, 0.3, label.upper(), 11, "accent", "mono", True, chrome=True)


@layout("inventory", "game", "Inventory grid: items as slots with counts, and a legend that names each one.", 70,
        accepts="items: `Name | detail | icon or character | count` (up to 12); select: slot number to highlight; first paragraph: caption",
        example="# What is in the backpack\nlayout: inventory\nselect: 2\n- Quests | tasks in 25 minute steps | sword | 4\n- Streaks | daily chain with a rest token | torch | 7\n- XP bar | progress you can see | xp | 1")
def inventory(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:12]
    sel = int(s.prop("select", "1") or 1) - 1
    gw = 6.1
    _panel(c, x, y, gw, h, "inventory")
    size, gap = 0.8, 0.1
    gx, gy = x + 0.3, y + 0.62
    for k in range(18):
        r, col = divmod(k, 6)
        sx, sy = gx + col * (size + gap), gy + r * (size + gap)
        if k < len(items):
            name, detail, spec, count = cells(items[k], 4)[:4]
            _draw_spec(c, spec or "diamond", sx, sy, size, selected=(k == sel), count=count)
        else:
            c.slot(sx, sy, size)
    if s.paragraphs:
        c.fit_text(x + 0.3, gy + 3 * (size + gap) + 0.05, gw - 0.6, h - (gy - y) - 3 * (size + gap) - 0.15, s.paragraphs[0], 16, 11, "muted")
    lx, lw = x + gw + 0.35, w - gw - 0.35
    _panel(c, lx, y, lw, h, "item list")
    n = max(len(items), 1)
    rh = min(0.62, (h - 0.7) / n)
    for k, it in enumerate(items):
        name, detail, spec, count = cells(it, 4)[:4]
        ry = y + 0.62 + k * rh
        if k == sel:
            c.rect(lx + 0.18, ry - 0.03, lw - 0.36, rh, "bg", line="accent", line_w=2.0)
        _draw_spec(c, spec or "diamond", lx + 0.3, ry + 0.04, rh - 0.12, slot=False)
        c.fit_text(lx + 0.35 + rh, ry, lw - rh - 0.7, rh - 0.04, f"**{name}**  {detail}" if detail else f"**{name}**", 17, 11,
                   "text", valign="middle")


@layout("crafting", "game", "Crafting table: up to nine ingredients combine into one result.", 60,
        accepts="items: ingredients `Name | icon or character`; result: `Name | icon or character | note`; first paragraph: caption",
        example="# Task + timer + reward = a quest\nlayout: crafting\nresult: Quest | sword | the unit of work\n- Task | book\n- 25 minute timer | torch\n- XP reward | xp")
def crafting(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:9]
    lw = 4.3
    for k, it in enumerate(items):
        name, spec = cells(it, 2)[:2]
        ry = y + 0.1 + k * 0.5
        c.text(x, ry, 0.35, 0.4, str(k + 1), 14, "accent", "mono", True, valign="middle", chrome=True)
        _draw_spec(c, spec, x + 0.4, ry + 0.02, 0.36, slot=False)
        c.fit_text(x + 0.9, ry, lw - 0.9, 0.42, name, 16, 11, "text", valign="middle")
    px, pw = x + lw + 0.3, w - lw - 0.3
    _panel(c, px, y, pw, h, "crafting")
    size, gap = 0.92, 0.08
    gx, gy = px + 0.45, y + 0.8
    for k in range(9):
        r, col = divmod(k, 3)
        sx, sy = gx + col * (size + gap), gy + r * (size + gap)
        if k < len(items):
            _draw_spec(c, cells(items[k], 2)[1], sx, sy, size, count=str(k + 1))
        else:
            c.slot(sx, sy, size)
    ax = gx + 3 * size + 2 * gap + 0.35
    ay = gy + 1.5 * size + gap - 0.12
    for k in range(5):  # pixel arrow
        c.rect(ax + k * 0.14, ay + 0.1, 0.14, 0.14, "accent")
    c.rect(ax + 0.56, ay - 0.04, 0.14, 0.42, "accent")
    c.rect(ax + 0.7, ay + 0.06, 0.14, 0.22, "accent")
    parts = [p.strip() for p in s.prop("result").split("|")] + ["", "", ""] if s.prop("result") else ["Result", "", "", ""]
    rname, rspec, rnote = parts[:3]
    rs = 1.35
    rx, ry = ax + 1.2, gy + 1.5 * size + gap - rs / 2
    c.slot(rx, ry, rs, selected=True)
    _draw_spec(c, rspec or "star", rx + 0.12, ry + 0.12, rs - 0.24, slot=False)
    c.fit_text(rx - 0.6, ry + rs + 0.1, rs + 1.2, 0.4, rname, 20, 12, "accent", "body", True, "center", "top")
    if rnote:
        c.fit_text(rx - 0.6, ry + rs + 0.5, rs + 1.2, 0.5, rnote, 14, 10, "muted", align="center")
    if s.paragraphs:
        c.fit_text(px + 0.4, y + h - 0.75, pw - 0.8, 0.6, s.paragraphs[0], 16, 11, "text", valign="middle")


@layout("hud", "game", "Status bars: hearts, hunger, armor and XP as a stats screen for the key numbers.", 50,
        accepts="items: `value | label | heart, hunger, armor, xp or boss | context | fill%` (up to 4); % or `a of b` values fill the bar, or give the fill as a 5th cell",
        example="# The pilot passed on every stat\nlayout: hud\nsource: pilot/results.csv\n- 72% | tasks completed | heart | vs 51% with a plain list\n- 31 of 40 | kept a 7 day streak | hunger | pilot group\n- 4.4 / 5 | would use again | xp | exit survey")
def hud(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:4]
    n = max(len(items), 1)
    gap = 0.18
    rh = min(1.05, (h - 0.1 - gap * (n - 1)) / n)
    scale = c.style["heading_scale"]
    for k, it in enumerate(items):
        value, label, kind, ctx, fill = cells(it, 5)[:5]
        ry = y + 0.1 + k * (rh + gap)
        c.box(x, ry, w, rh, fill="surface")
        size = textfit.fit_line(c.t, value, "heading", 2.9, 40 * scale, 14 * scale, True)
        c.text(x + 0.3, ry, 2.9, rh, value, size, "accent", "heading", True, "left", "middle", 1.0)
        c.fit_text(x + 3.45, ry + 0.08, 3.95, rh * 0.55, label, 20, 12, "text", "body", True, valign="middle")
        c.fit_text(x + 3.45, ry + rh * 0.55, 3.95, rh * 0.38, ctx, 14, 10, "muted")
        frac = _ratio(value)
        if fill and _num(fill) is not None:  # 5th cell: bar fill in percent, graphic only, never printed
            frac = min(_num(fill) / 100, 1.0)
        frac = 1.0 if frac is None else frac
        bx = x + 7.6
        kind = (kind or "heart").strip().lower()
        if kind == "boss":
            c.bar(bx, ry + rh / 2 - 0.2, w - 7.9, 0.4, frac, "danger", ticks=20)
        elif kind == "xp":
            c.bar(bx, ry + rh / 2 - 0.16, w - 7.9, 0.32, frac, "success", ticks=10)
            c.text(bx, ry + rh / 2 - 0.5, 1.5, 0.3, "LEVEL", 11, "muted", "mono", True, chrome=True)
        else:
            c.meter(bx, ry + rh / 2 - 0.17, frac, kind if kind in ("heart", "hunger", "armor") else "heart", 10, 0.36, 0.05)


@layout("advancements", "game", "Advancement tree: milestones as framed icons joined by a path, done, current or locked.", 60,
        accepts="items: `Title | detail | icon or character | done, current or locked` (up to 6)",
        example="# Three advancements to a pilot\nlayout: advancements\n- Prototype | quests and streaks | sword | done\n- Campus pilot | 200 students | diamond | current\n- Study | grades against a control group | trophy | locked")
def advancements(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    step = w / n
    fs = 1.3 if n <= 4 else 0.95
    pts = []
    for k, it in enumerate(items):
        cx = x + step * k + step / 2
        cy = y + 0.9 + (0.0 if k % 2 == 0 else 1.0)
        pts.append((cx, cy))
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mid = (ax + bx) / 2
        for seg in ((ax, ay, mid, ay), (mid, ay, mid, by), (mid, by, bx, by)):
            c.line(*seg, col="muted", width=5.0)
    for k, (it, (cx, cy)) in enumerate(zip(items, pts)):
        title, detail, spec, state = cells(it, 4)[:4]
        state = (state or ("current" if k == 0 else "locked")).strip().lower()
        fill = {"done": "surface", "current": "primary", "locked": "bg"}.get(state, "surface")
        line = {"done": "accent", "current": "accent", "locked": "border"}.get(state, "border")
        c.box(cx - fs / 2, cy - fs / 2, fs, fs, fill=fill, line=line)
        _draw_spec(c, spec or "star", cx - fs / 2 + 0.17, cy - fs / 2 + 0.17, fs - 0.34, slot=False)
        if state == "locked":
            c.rect(cx - fs / 2 + 0.04, cy - fs / 2 + 0.04, fs - 0.08, fs - 0.08, "bg", alpha=0.55)
        tag = {"done": "DONE", "current": "NOW", "locked": "LOCKED"}.get(state, state.upper())
        ty = cy + fs / 2 + 0.12 if k % 2 == 0 else cy - fs / 2 - 0.12 - 1.35
        c.text(cx - step / 2 + 0.1, ty, step - 0.2, 0.25, tag, 11, "accent" if state != "locked" else "muted", "mono", True, "center", chrome=True)
        c.fit_text(cx - step / 2 + 0.1, ty + 0.28, step - 0.2, 0.5, title, 20, 12, "text", "body", True, "center", "top")
        c.fit_text(cx - step / 2 + 0.1, ty + 0.85, step - 0.2, 0.6, detail, 16, 10, "muted", align="center")


@layout("trade", "game", "Villager trade list: before on the left, after on the right, with a trader.", 60,
        accepts="items: `Before | After | note` (up to 4); trader: character name (default villager)",
        example="# Four trades that cut the delay\nlayout: trade\n- 40 minute delay | 2 second alert | streaming scoring\n- 11% false alarms | 3% false alarms | alert grouping")
def trade(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:4]
    n = max(len(items), 1)
    trader = s.prop("trader", "villager")
    c.box(x, y + 0.1, 2.2, h - 0.1, fill="surface")
    c.text(x + 0.2, y + 0.2, 1.8, 0.3, "TRADES", 11, "accent", "mono", True, "center", chrome=True)
    c._mob_image(trader, x + 0.1, y + 0.85, 2.0, "head")
    c.fit_text(x + 0.15, y + 3.05, 1.9, 0.5, (entities.ENTITIES.get(entities.canonical(trader), ("", trader))[1]), 16, 11, "text", "body", True, align="center")
    gx = x + 2.55
    gw = w - 2.55
    gap = 0.18
    rh = min(1.05, (h - 0.1 - gap * (n - 1)) / n)
    half = (gw - 1.3) / 2
    for k, it in enumerate(items):
        before, after, note = cells(it, 3)[:3]
        ry = y + 0.1 + k * (rh + gap)
        c.box(gx, ry, half, rh, fill="surface")
        c.icon("coin", gx + 0.2, ry + rh / 2 - 0.18, 0.36)
        c.fit_text(gx + 0.7, ry + 0.05, half - 0.85, rh - 0.1, before, 18, 11, "text", valign="middle")
        ax = gx + half + 0.2
        for j in range(4):
            c.rect(ax + j * 0.14, ry + rh / 2 - 0.07, 0.14, 0.14, "accent")
        c.rect(ax + 0.56, ry + rh / 2 - 0.2, 0.14, 0.4, "accent")
        c.rect(ax + 0.7, ry + rh / 2 - 0.1, 0.14, 0.2, "accent")
        rx = gx + half + 1.3
        c.box(rx, ry, half, rh, fill="surface", line="success")
        c.icon("emerald", rx + 0.2, ry + rh / 2 - 0.18, 0.36)
        c.fit_text(rx + 0.7, ry + 0.05, half - 0.85, rh * 0.62, after, 18, 11, "success", "body", True, valign="middle")
        if note:
            c.fit_text(rx + 0.7, ry + rh * 0.6, half - 0.85, rh * 0.36, note, 13, 10, "muted")


@layout("chat", "game", "Chat window: quotes, feedback or steps as messages from named characters.", 70,
        accepts="items: `Speaker | message | character` (up to 7); first paragraph: a [Server] line on top",
        example="# What students said\nlayout: chat\nA week into the pilot the chat looked like this.\n- Dana | the quests made me start | steve\n- Mira | the rest token saved my streak | pig")
def chat(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:7]
    c.rect(x, y + 0.1, w, h - 0.1, "bg", alpha=0.92)
    c.rect(x, y + 0.1, w, 0.04, "border")
    cy = y + 0.3
    rowh = (h - 0.4) / (len(items) + (1 if s.paragraphs else 0) or 1)
    rowh = min(rowh, 1.0)
    if s.paragraphs:
        c.fit_text(x + 0.3, cy, w - 0.6, rowh * 0.8, f"[Server] {s.paragraphs[0]}", 17, 11, "warning", "mono", True, valign="middle")
        cy += rowh
    colors = ["accent", "info", "success", "secondary", "warning"]
    for k, it in enumerate(items):
        who, msg, ent = cells(it, 3)[:3]
        av = min(0.7, rowh - 0.14)
        if ent:
            c._mob_image(ent, x + 0.3, cy + (rowh - av) / 2, av, "face")
        name = f"<{who}>"
        nw = textfit.width_in(c.t, name, "mono", 16, True) + 0.25
        c.text(x + 0.3 + av + 0.2, cy, nw, rowh, name, 16, colors[k % len(colors)], "mono", True, valign="middle")
        c.fit_text(x + 0.3 + av + 0.2 + nw, cy, w - (av + nw + 0.9), rowh, msg, 19, 12, "text", valign="middle")
        cy += rowh


_LAYER_COL = {"sky": "#8EC9F5", "grass": "#4C9A2A", "dirt": "#7A4B1F", "stone": "#7F7F7F", "deepslate": "#3A3A44", "bedrock": "#1B1B1B"}
_LAYER_ORDER = ["sky", "grass", "dirt", "stone", "deepslate", "bedrock"]
_ORES = [("coal", "#1B1B1B"), ("iron", "#E3C9A3"), ("gold", "#FCDB05"), ("redstone", "#E02B20"), ("lapis", "#3B5BDB"), ("diamond", "#4EE3D6")]


@layout("strata", "game", "Architecture as world layers: sky, grass, dirt, stone, deepslate; components are ores.", 60,
        accepts="items: `Layer: component, component` (up to 5 layers); wrap the key component in **bold** to make it a diamond",
        example="# Four layers keep the alert path short\nlayout: strata\n- Client: Web app, Phone view\n- API: Auth, **Quest engine**\n- Data: Postgres, Event log")
def strata(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = layer_items(s.items[:5])
    n = max(len(rows), 1)
    rh = (h - 0.1) / n
    pool = c._mob_pool()
    for k, (layer, comps) in enumerate(rows):
        ry = y + 0.1 + k * rh
        base = _LAYER_COL[_LAYER_ORDER[round(k * 5 / (n - 1)) if n > 1 else 1]]
        c.rect(x, ry, w, rh, base)
        for q in range(int(w / 0.4) + 1):  # deterministic speckle texture
            if (q * 7 + k * 3) % 4 == 0:
                c.rect(x + q * 0.4 + 0.1, ry + ((q * 5 + k) % 3) * rh / 3 + 0.08, 0.16, 0.16, color.darken(base, 0.18), alpha=0.9)
            if (q * 5 + k) % 5 == 0:
                c.rect(x + q * 0.4 + 0.22, ry + ((q * 3 + k) % 3) * rh / 3 + 0.2, 0.12, 0.12, color.lighten(base, 0.16), alpha=0.9)
        c.box(x + 0.15, ry + rh / 2 - 0.3, 2.1, 0.6, fill="surface", shadow=False)
        c.fit_text(x + 0.25, ry + rh / 2 - 0.3, 1.9, 0.6, layer, 17, 11, "text", "mono", True, "center", "middle")
        cx = x + 2.5
        for j, comp in enumerate(comps):
            key = comp.startswith("**") and comp.endswith("**")
            name = comp.strip("*")
            bw = textfit.width_in(c.t, name, "body", 17, True) + 1.0
            if cx + bw > x + w - 0.9:
                break
            c.box(cx, ry + rh / 2 - 0.3, bw, 0.6, fill="primary" if key else "surface", shadow=False)
            ore, col = _ORES[5] if key else _ORES[(k + j) % 5]
            c.rect(cx + 0.14, ry + rh / 2 - 0.16, 0.32, 0.32, "#6B6B6B")
            for dx, dy in ((0.04, 0.04), (0.18, 0.06), (0.08, 0.18), (0.2, 0.2)):
                c.rect(cx + 0.14 + dx, ry + rh / 2 - 0.16 + dy, 0.08, 0.08, col)
            c.text(cx + 0.55, ry + rh / 2 - 0.3, bw - 0.6, 0.6, name, 17, c.t.on("primary") if key else "text", "body", True, valign="middle")
            cx += bw + 0.2
        if pool and rh > 0.7:
            c._mob_image(pool[(k * 2 + s.index) % len(pool)], x + w - 0.85, ry + rh / 2 - 0.35, 0.7, "head")


@layout("boss", "game", "Boss fight: the problem as a boss with a health bar, a portrait and attack patterns.", 55,
        accepts="props: boss (character name), stat `14 days | what it measures`, hp (0-100); first paragraph: the lore; items: up to 3 attacks",
        example="# Planners are abandoned within two weeks\nlayout: boss\nboss: zombie\nstat: 14 days | median time until students quit a planner\nPlans feel like homework about homework.\n- No feedback during the week\n- Plans are too big to start")
def boss(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    name = s.prop("boss", "zombie")
    label = entities.ENTITIES.get(entities.canonical(name), ("", name))[1]
    stat = [p.strip() for p in s.prop("stat").split("|")] + ["", ""]
    hp = (_num(s.prop("hp", "100")) or 100) / 100
    c.text(x, y + 0.02, 6, 0.3, f"{label.upper()}  -  BOSS", 12, "danger", "mono", True, chrome=True)
    c.bar(x, y + 0.34, w, 0.5, hp, "danger", ticks=20)
    if stat[0]:
        sw = min(w - 0.4, textfit.width_in(c.t, stat[0], "mono", 18, True) + 0.7)
        c.rect(x + w / 2 - sw / 2, y + 0.42, sw, 0.34, "bg", alpha=0.92)
        c.text(x + w / 2 - sw / 2, y + 0.42, sw, 0.34, stat[0], 18, "text", "mono", True, "center", "middle", 1.0)
    py = y + 1.15
    c.box(x + 0.35, py + 2.5, 3.1, 0.25, fill="surface", shadow=False)
    c._mob_image(name, x + 0.35, py - 0.1, 3.1, "head")
    if stat[1]:
        c.fit_text(x + 0.1, py + 2.85, 3.6, 0.45, stat[1], 13, 10, "muted", align="center")
    rx = x + 4.1
    rw = w - 4.1
    if s.paragraphs:
        c.fit_text(rx, py, rw, 0.9, s.paragraphs[0], 24, 15, "text", "body", True)
    c.text(rx, py + 1.0, rw, 0.3, "ATTACK PATTERNS", 11, "accent", "mono", True, chrome=True)
    ay = py + 1.35
    for k, it in enumerate(s.items[:3]):
        c.box(rx, ay + k * 0.62, rw, 0.52, fill="surface", shadow=False)
        c.icon("sword", rx + 0.15, ay + k * 0.62 + 0.08, 0.36)
        c.fit_text(rx + 0.65, ay + k * 0.62, rw - 0.8, 0.52, it.text, 17, 11, "text", valign="middle")


@layout("leaderboard", "game", "Leaderboard: horizontal bars with a character per row; the best one gets the gold.", 50,
        accepts="items: `Name | value | character | note` (up to 6); better: lower or higher (default higher)",
        example="# The cache tops the latency board\nlayout: leaderboard\nbetter: lower\n- No cache | 840 ms | zombie\n- Plain cache | 410 ms | villager\n- Cache + coalescing | 190 ms | steve")
def leaderboard(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:6]
    n = max(len(items), 1)
    vals = [_num(cells(i, 2)[1]) or 0 for i in items]
    lower = s.prop("better", "higher") == "lower"
    best = (min(vals) if lower else max(vals)) if vals else 0
    top = max(vals) or 1
    gap = 0.14
    rh = min(0.8, (h - 0.1 - gap * (n - 1)) / n)
    for k, it in enumerate(items):
        name, value, ent, note = cells(it, 4)[:4]
        ry = y + 0.1 + k * (rh + gap)
        c.box(x, ry, w, rh, fill="surface", shadow=False)
        av = rh - 0.12
        if ent:
            c._mob_image(ent, x + 0.1, ry + 0.06, av, "face")
        c.text(x + av + 0.25, ry, 0.5, rh, str(k + 1), 18, "accent", "mono", True, valign="middle", chrome=True)
        c.fit_text(x + av + 0.8, ry, 3.2, rh, name, 18, 11, "text", "body", True, valign="middle")
        bx, bw = x + av + 4.1, w - av - 6.2
        frac = max(vals[k] / top, 0.04)
        gold = vals[k] == best
        c.rect(bx, ry + rh / 2 - 0.15, bw, 0.3, color.darken(c.t.c("bg"), 0.3))
        c.rect(bx, ry + rh / 2 - 0.15, bw * frac, 0.3, "warning" if gold else "primary")
        if gold and frac < 0.93:
            c.icon("trophy", bx + bw * frac + 0.1, ry + rh / 2 - 0.2, 0.34)
        c.text(x + w - 2.0, ry, 1.85, rh, value, 20, "warning" if gold else "text", "heading" if not c.pixel else "mono", True, "right", "middle", 1.0)


@layout("book", "game", "Open book: two parchment pages for what was done and what remains, or any two lists.", 70,
        accepts="groups: two `## heading` sections with bullets; or items on the left page and the first paragraph on the right",
        example="# What we did and what we will do\nlayout: book\n## Done\n- Prototype with quests and streaks\n## Next\n- Campus pilot with 200 students")
def book(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1]] or [("", s.items)]
    if len(groups) == 1:
        groups = [groups[0], ("", [])]
    groups = groups[:2]
    cover, paper, ink = "#4F3115", "#E9DDB8", "#3B2A14"
    c.rect(x - 0.1, y + 0.05, w + 0.2, h - 0.05, cover)
    pw = (w - 0.45) / 2
    for i, (head, items) in enumerate(groups):
        px = x + 0.12 + i * (pw + 0.2)
        c.rect(px, y + 0.2, pw, h - 0.35, paper)
        c.rect(px + (pw - 0.04 if i == 0 else 0), y + 0.2, 0.04, h - 0.35, "#CDBB8A")
        if head:
            c.text(px + 0.4, y + 0.4, pw - 0.8, 0.45, head, 20 if not c.pixel else 14, "#7A1F14", "heading", True, valign="middle")
        by = y + 1.0
        for k, it in enumerate(items[:5]):
            c.rect(px + 0.4, by + k * 0.74 + 0.16, 0.14, 0.14, "#7A4B1F")
            c.fit_text(px + 0.7, by + k * 0.74, pw - 1.1, 0.7, it.text, 20, 12, ink, valign="top")
        if i == 1 and not items and s.paragraphs:
            c.fit_text(px + 0.4, y + 1.0, pw - 0.8, h - 1.6, s.paragraphs[0], 20, 12, ink)
        if i == 0 or items:
            c.icon("book" if i == 0 else "torch", px + pw - 0.75, y + h - 0.85, 0.4)
