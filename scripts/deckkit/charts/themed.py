"""Theme-colored matplotlib charts rendered to transparent PNGs. Needs the `charts` requirements group."""
import hashlib
import re
import tempfile
import textwrap
from pathlib import Path

KINDS = ("bar", "hbar", "line", "scatter", "confusion")


def _num(v):
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(v).replace(" ", ""))
    if not m:
        raise ValueError(f"not a number: {v!r}")
    return float(m.group(0).replace(",", "."))


def _cache_dir(deck):
    base = deck.meta.get("_cache") if deck is not None else None
    d = Path(base).resolve() if base else Path(tempfile.gettempdir()) / "deckkit-cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def render_chart(theme, kind, table, w_in, h_in, deck=None, index=0, ylabel=""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    if kind not in KINDS:
        raise ValueError(f"unknown chart kind {kind!r}; choose from {KINDS}")
    if len(table) < 2:
        raise ValueError("chart table needs a header row and at least one data row")
    key = hashlib.sha1(repr((theme.name, kind, table, w_in, h_in, ylabel)).encode("utf-8")).hexdigest()[:12]
    out = _cache_dir(deck) / f"chart-{index}-{key}.png"
    if out.exists():
        return str(out)

    c = theme.colors
    for bold in (False, True):
        font_manager.fontManager.addfont(str(theme.font_file("body", bold)))
    family = font_manager.FontProperties(fname=str(theme.font_file("body"))).get_name()
    plt.rcParams.update({"font.family": family, "text.color": c["text"], "axes.labelcolor": c["muted"],
                         "xtick.color": c["muted"], "ytick.color": c["muted"], "font.size": 14})
    fig, ax = plt.subplots(figsize=(w_in, h_in), dpi=200)
    head, rows = table[0], table[1:]
    labels = [r[0] for r in rows]
    palette = [c["primary"], c["accent"], c["secondary"], c["warning"], c["success"]]

    if kind in ("bar", "hbar"):
        nser = len(head) - 1
        vals = [[_num(r[j + 1]) for r in rows] for j in range(nser)]
        width = 0.7 / nser
        pos = range(len(rows))
        for j in range(nser):
            offs = [p + (j - (nser - 1) / 2) * width for p in pos]
            cols = [palette[j]] * len(rows)
            if nser == 1 and min(vals[0]) >= 0:  # highlight the largest bar; ambiguous for negative values
                best = max(range(len(rows)), key=lambda i: vals[0][i])
                cols = [c["primary"] if i != best else c["accent"] for i in pos]
            bars = (ax.bar if kind == "bar" else ax.barh)(offs, vals[j], width * 0.92, color=cols, label=head[j + 1])
            for b, v in zip(bars, vals[j]):
                if kind == "bar":
                    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{v:g}", ha="center", va="bottom", color=c["text"], fontsize=13)
                else:
                    ax.text(b.get_width(), b.get_y() + b.get_height() / 2, f" {v:g}", ha="left", va="center", color=c["text"], fontsize=13)
        shown = labels
        if kind == "bar":  # wrap long category labels so neighbours do not overlap
            width = max(8, int(40 / max(len(rows), 1)))
            shown = [textwrap.fill(str(lb), width) or str(lb) for lb in labels]
        (ax.set_xticks if kind == "bar" else ax.set_yticks)(list(pos))
        (ax.set_xticklabels if kind == "bar" else ax.set_yticklabels)(shown)
        if kind == "hbar":
            ax.invert_yaxis()
        if nser > 1:
            ax.legend(frameon=False, labelcolor=c["text"])
    elif kind == "line":
        for j in range(len(head) - 1):
            ys = [_num(r[j + 1]) for r in rows]
            ax.plot(labels, ys, color=palette[j], linewidth=3, marker="o", markersize=8, label=head[j + 1])
        if len(head) > 2:
            ax.legend(frameon=False, labelcolor=c["text"])
    elif kind == "scatter":
        xs, ys = [_num(r[0]) for r in rows], [_num(r[1]) for r in rows]
        ax.scatter(xs, ys, s=60, color=c["primary"], alpha=0.85)
        ax.set_xlabel(head[0])
        ax.set_ylabel(head[1])
    else:  # confusion: header = column labels (first cell is the corner), rows = [row label, values...]
        import numpy as np
        m = np.array([[_num(v) for v in r[1:]] for r in rows])
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap.from_list("t", [c["surface"], c["primary"], c["accent"]])
        ax.imshow(m, cmap=cmap)
        ax.set_xticks(range(len(head) - 1))
        ax.set_xticklabels(head[1:])
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(labels)
        for (i, j), v in np.ndenumerate(m):
            ax.text(j, i, f"{v:g}", ha="center", va="center", color=c["text"], fontsize=15, fontweight="bold")
        ax.tick_params(length=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(c["border"])
    if kind != "confusion":
        ax.grid(axis="y" if kind != "hbar" else "x", color=c["border"], linewidth=0.8, alpha=0.7)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out, transparent=True)
    plt.close(fig)
    return str(out)
