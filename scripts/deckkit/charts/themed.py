"""Theme-colored matplotlib charts and equations rendered to transparent PNGs. Needs the `charts` requirements group."""
import hashlib
import re
import tempfile
import textwrap
from pathlib import Path

from ..core.numbers import number

KINDS = ("bar", "hbar", "line", "area", "stacked", "waterfall", "donut", "scatter", "confusion", "heatmap", "radar", "lollipop", "slope")


def _num(v):
    n = number(v)
    if n is None:
        raise ValueError(f"not a number: {v!r}")
    return n


def _cache_dir(deck):
    base = deck.meta.get("_cache") if deck is not None else None
    d = Path(base).resolve() if base else Path(tempfile.gettempdir()) / "deckkit-cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _setup(theme):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    c = theme.colors
    for bold in (False, True):
        font_manager.fontManager.addfont(str(theme.font_file("body", bold)))
    family = font_manager.FontProperties(fname=str(theme.font_file("body"))).get_name()
    plt.rcParams.update({"font.family": family, "text.color": c["text"], "axes.labelcolor": c["muted"],
                         "xtick.color": c["muted"], "ytick.color": c["muted"], "font.size": 14})
    return plt


def render_chart(theme, kind, table, w_in, h_in, deck=None, index=0, ylabel=""):
    """kinds: bar, hbar, line, area, stacked, waterfall, donut, scatter, confusion, heatmap, radar, lollipop, slope.
    Tables: header row first, label in column 1."""
    if kind not in KINDS:
        raise ValueError(f"unknown chart kind {kind!r}; choose from {KINDS}")
    if len(table) < 2:
        raise ValueError("chart table needs a header row and at least one data row")
    key = hashlib.sha1(repr((theme.name, kind, table, w_in, h_in, ylabel)).encode("utf-8")).hexdigest()[:12]
    out = _cache_dir(deck) / f"chart-{index}-{key}.png"
    if out.exists():
        return str(out)
    plt = _setup(theme)
    import numpy as np

    c = theme.colors
    grid = _mix(c["bg"], c["text"], 0.16)
    fig, ax = plt.subplots(figsize=(w_in, h_in), dpi=200)
    head, rows = table[0], table[1:]
    labels = [r[0] for r in rows]
    palette = theme.series
    pos = list(range(len(rows)))

    def wrap_labels(n_per_axis):
        width = max(8, int(40 / max(n_per_axis, 1)))
        return [textwrap.fill(str(lb), width, break_long_words=False) or str(lb) for lb in labels]

    if kind in ("bar", "hbar", "stacked"):
        nser = len(head) - 1
        vals = [[_num(r[j + 1]) for r in rows] for j in range(nser)]
        if kind == "stacked":
            bottom = np.zeros(len(rows))
            for j in range(nser):
                ax.bar(pos, vals[j], 0.62, bottom=bottom, color=palette[j % len(palette)], label=head[j + 1])
                for p, v, b in zip(pos, vals[j], bottom):
                    if v:
                        ax.text(p, b + v / 2, f"{v:g}", ha="center", va="center", color=_on(palette[j % len(palette)], c), fontsize=12)
                bottom += np.array(vals[j])
            ax.set_xticks(pos)
            ax.set_xticklabels(wrap_labels(len(rows)))
            ax.legend(frameon=False, labelcolor=c["text"])
        else:
            width = 0.7 / nser
            for j in range(nser):
                offs = [p + (j - (nser - 1) / 2) * width for p in pos]
                cols = [palette[j % len(palette)]] * len(rows)
                if nser == 1 and min(vals[0]) >= 0:  # highlight the largest bar; ambiguous for negative values
                    best = max(pos, key=lambda i: vals[0][i])
                    cols = [palette[0] if i != best else palette[1 % len(palette)] for i in pos]
                bars = (ax.bar if kind == "bar" else ax.barh)(offs, vals[j], width * 0.92, color=cols, label=head[j + 1])
                for b, v in zip(bars, vals[j]):
                    if kind == "bar":
                        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{v:g}", ha="center", va="bottom", color=c["text"], fontsize=13)
                    else:
                        ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {v:g}", ha="left", va="center", color=c["text"], fontsize=13)
            (ax.set_xticks if kind == "bar" else ax.set_yticks)(pos)
            (ax.set_xticklabels if kind == "bar" else ax.set_yticklabels)(wrap_labels(len(rows)) if kind == "bar" else labels)
            if kind == "hbar":
                ax.invert_yaxis()
            if nser > 1:
                ax.legend(frameon=False, labelcolor=c["text"])
    elif kind in ("line", "area"):
        for j in range(len(head) - 1):
            ys = [_num(r[j + 1]) for r in rows]
            col = palette[j % len(palette)]
            if kind == "area":
                ax.fill_between(range(len(ys)), ys, color=col, alpha=0.22)
            ax.plot(range(len(ys)), ys, color=col, linewidth=3, marker="o", markersize=8, label=head[j + 1])
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(wrap_labels(len(rows)))
        if len(head) > 2:
            ax.legend(frameon=False, labelcolor=c["text"])
    elif kind == "waterfall":
        # rows: label | value. A label starting with "=" is a total (absolute value); other rows are changes.
        run, bottoms, heights, cols, shown = 0.0, [], [], [], []
        for lb, r in zip(labels, rows):
            v = _num(r[1])
            if lb.startswith("="):
                bottoms.append(0.0)
                heights.append(v)
                run = v
                cols.append(palette[0])
                shown.append((lb.lstrip("= ").strip(), v, v))
            else:
                bottoms.append(run if v >= 0 else run + v)
                heights.append(abs(v))
                run += v
                cols.append(c["success"] if v >= 0 else c["danger"])
                shown.append((lb, v, run))
        ax.bar(pos, heights, 0.6, bottom=bottoms, color=cols)
        for p, (lb, v, tot), b, h in zip(pos, shown, bottoms, heights):
            ax.text(p, b + h, f"{v:+g}" if not labels[p].startswith("=") else f"{v:g}", ha="center", va="bottom", color=c["text"], fontsize=13)
        for p in range(len(pos) - 1):  # connectors
            level = shown[p][2]
            ax.plot([p + 0.3, p + 1 - 0.3], [level, level], color=grid, linewidth=1.2)
        ax.set_xticks(pos)
        ax.set_xticklabels([textwrap.fill(s[0], max(8, int(40 / len(pos))), break_long_words=False) for s in shown])
    elif kind == "donut":
        vals = [_num(r[1]) for r in rows]
        wedges, _t = ax.pie(vals, colors=[palette[i % len(palette)] for i in range(len(vals))], startangle=90, counterclock=False,
                            wedgeprops={"width": 0.38, "edgecolor": c["bg"], "linewidth": 2})
        total = sum(vals)
        ax.text(0, 0.06, f"{total:g}", ha="center", va="center", fontsize=26, fontweight="bold", color=c["text"])
        ax.text(0, -0.2, head[1] if len(head) > 1 else "", ha="center", va="center", fontsize=12, color=c["muted"])
        ax.legend(wedges, [f"{lb}  {v / total:.0%}" for lb, v in zip(labels, vals)], loc="center left", bbox_to_anchor=(1.0, 0.5),
                  frameon=False, labelcolor=c["text"], fontsize=13)
        ax.set_aspect("equal")
    elif kind == "scatter":
        xs, ys = [_num(r[0]) for r in rows], [_num(r[1]) for r in rows]
        ax.scatter(xs, ys, s=60, color=palette[0], alpha=0.85)
        ax.set_xlabel(head[0])
        ax.set_ylabel(head[1])
    elif kind == "radar":  # rows = axes (labels), columns = series; every value is scaled by the largest in the table
        fig.delaxes(ax)
        ax = fig.add_subplot(111, polar=True)
        vals = [[_num(r[j + 1]) for r in rows] for j in range(len(head) - 1)]
        top = max(max(v) for v in vals) or 1.0
        ang = [2 * np.pi * i / len(rows) for i in range(len(rows))]
        for j, ys in enumerate(vals):
            col = palette[j % len(palette)]
            ax.plot(ang + ang[:1], [v / top for v in ys] + [ys[0] / top], color=col, linewidth=3, label=head[j + 1])
            ax.fill(ang + ang[:1], [v / top for v in ys] + [ys[0] / top], color=col, alpha=0.18)
        ax.set_xticks(ang)
        ax.set_xticklabels(wrap_labels(len(rows)), color=c["text"], fontsize=13)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels([])
        ax.set_ylim(0, 1.05)
        ax.set_facecolor("none")
        ax.grid(color=grid, linewidth=0.9)
        ax.spines["polar"].set_color(grid)
        if len(head) > 2:
            ax.legend(frameon=False, labelcolor=c["text"], loc="center left", bbox_to_anchor=(1.12, 0.5))
    elif kind == "lollipop":  # one series ranked from the largest: a stem and a dot per row
        order = sorted(range(len(rows)), key=lambda i: -_num(rows[i][1]))
        vs = [_num(rows[i][1]) for i in order]
        names = [labels[i] for i in order]
        ys = list(range(len(vs)))
        ax.hlines(ys, 0, vs, color=grid, linewidth=3)
        ax.scatter(vs, ys, s=170, color=[palette[1 % len(palette)] if k == 0 else palette[0] for k in ys], zorder=3)
        for y_, v in zip(ys, vs):
            ax.text(v, y_, f"  {v:g}", ha="left", va="center", color=c["text"], fontsize=13)
        ax.set_yticks(ys)
        ax.set_yticklabels(names)
        ax.invert_yaxis()
        ax.set_xlim(0, max(vs) * 1.18)
    elif kind == "slope":  # rows: label | before | after
        a_lbl, b_lbl = (head + ["", ""])[1], (head + ["", ""])[2]
        for r in rows:
            va, vb = _num(r[1]), _num(r[2])
            col = c["success"] if vb >= va else c["danger"]
            ax.plot([0, 1], [va, vb], color=col, linewidth=3, marker="o", markersize=9)
            ax.text(-0.04, va, f"{r[0]}  {va:g}", ha="right", va="center", color=c["text"], fontsize=13)
            ax.text(1.04, vb, f"{vb:g}", ha="left", va="center", color=c["text"], fontsize=13)
        ax.set_xlim(-0.75, 1.2)
        ax.set_xticks([0, 1])
        ax.set_xticklabels([a_lbl, b_lbl])
        ax.set_yticks([])
    else:  # confusion and heatmap: header = column labels (first cell is the corner), rows = [row label, values...]
        m = np.array([[_num(v) for v in r[1:]] for r in rows])
        from matplotlib.colors import LinearSegmentedColormap
        if kind == "heatmap" and m.min() < 0:  # diverging around zero
            lim = max(abs(m.min()), abs(m.max())) or 1.0
            cmap = LinearSegmentedColormap.from_list("t", [c["danger"], c["surface"], c["success"]])
            ax.imshow(m, cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")
            shade = lambda v: (v + lim) / (2 * lim)
        else:
            cmap = LinearSegmentedColormap.from_list("t", [c["surface"], palette[0], palette[1 % len(palette)]])
            ax.imshow(m, cmap=cmap, aspect="auto" if kind == "heatmap" else "equal")
            shade = lambda v: v / (m.max() or 1)
        ax.set_xticks(range(len(head) - 1))
        ax.set_xticklabels(head[1:])
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(labels)
        for (i, j), v in np.ndenumerate(m):
            ax.text(j, i, f"{v:g}", ha="center", va="center", color=_on(cmap(shade(v)), c), fontsize=15, fontweight="bold")
        ax.tick_params(length=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if kind == "donut":
        ax.axis("off")
    elif kind == "radar":
        pass
    elif kind == "slope":
        for side in ("top", "right", "left", "bottom"):
            ax.spines[side].set_visible(False)
        ax.tick_params(length=0, labelsize=14)
    else:
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(grid)
        if kind not in ("confusion", "heatmap"):
            ax.grid(axis="y" if kind not in ("hbar", "lollipop") else "x", color=grid, linewidth=0.8, alpha=0.9)
            ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out, transparent=True, bbox_inches="tight" if kind == "donut" else None, pad_inches=0.1)
    plt.close(fig)
    return str(out)


def render_math(theme, latex, size_pt=40, deck=None, index=0):
    """Render a formula with matplotlib mathtext (a LaTeX subset) to a transparent PNG. Returns (path, width_in, height_in)."""
    key = hashlib.sha1(repr((theme.name, latex, size_pt)).encode("utf-8")).hexdigest()[:12]
    out = _cache_dir(deck) / f"math-{index}-{key}.png"
    plt = _setup(theme)
    if not out.exists():
        fig = plt.figure(figsize=(0.1, 0.1), dpi=300)
        fig.text(0, 0, f"${latex}$", fontsize=size_pt, color=theme.colors["text"], math_fontfamily="stix")
        try:
            fig.savefig(out, transparent=True, bbox_inches="tight", pad_inches=0.06)
        except ValueError as e:
            plt.close(fig)
            raise ValueError(f"cannot render formula {latex!r}: {e}")
        plt.close(fig)
    from PIL import Image as PILImage
    with PILImage.open(out) as im:
        w, h = im.size
    return str(out), w / 300, h / 300


def _mix(a, b, t):
    from ..core.color import mix
    return mix(a, b, t)


def _on(fill, c):
    """Readable text color for a bar fill (hex string or matplotlib RGBA)."""
    from ..core.color import best_on, rgb_to_hex
    if not isinstance(fill, str):
        fill = rgb_to_hex(tuple(255 * v for v in fill[:3]))
    return best_on(fill, [c["text"], c["bg"], "#FFFFFF", "#000000"])
