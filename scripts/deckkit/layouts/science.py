"""Scientific components: abstract, hypotheses, equation, figure, two figures, references, fact sheet."""
from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow

STATUS = {"supported": "success", "confirmed": "success", "yes": "success", "rejected": "danger", "refuted": "danger", "no": "danger",
          "open": "warning", "partial": "warning", "mixed": "warning", "untested": "muted"}


@layout("abstract", "science", "Structured abstract: background, methods, results and conclusion as labelled rows.", 110,
        accepts="items: `Label | text` (up to 4; defaults Background, Methods, Results, Conclusion); keywords: comma list",
        example="# Calibration fixes rare-event probabilities\nlayout: abstract\nkeywords: calibration, boosting, rare events\n- Background | Boosted trees misstate rare-event risk\n- Methods | Isotonic map on a later holdout\n- Results | Calibration error fell 80%\n- Conclusion | Calibrate before using probabilities")
def abstract(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    defaults = ["Background", "Methods", "Results", "Conclusion"]
    items = s.items[:4]
    n = max(len(items), 1)
    kw = 0.45 if s.prop("keywords") else 0
    rh = (h - 0.1 - kw) / n
    rule = color.mix(c.t.c("bg"), c.t.c("text"), 0.22)
    for k, it in enumerate(items):
        parts = cells(it, 2)
        label, text = (parts[0], parts[1]) if parts[1] else (defaults[k], parts[0])
        ry = y + 0.1 + k * rh
        c.rect(x, ry, w, 0.015, rule)
        c.text(x, ry + 0.1, 2.3, 0.4, label.upper(), 13, "accent", "body", True, chrome=True)
        c.fit_text(x + 2.5, ry + 0.08, w - 2.5, rh - 0.16, text, 20, 12, "text")
    if kw:
        c.rect(x, y + h - kw, w, 0.015, rule)
        c.text(x, y + h - kw + 0.05, w, 0.35, f"Keywords: {s.prop('keywords')}", 14, "muted", "body", False, valign="middle")


@layout("hypotheses", "science", "Research question and numbered hypotheses, each with a status chip.", 90,
        accepts="first paragraph: the research question; items: `H1 | statement | supported, rejected, open or partial` (up to 4)",
        example="# Two of three hypotheses hold\nlayout: hypotheses\nDoes calibration improve decisions at a 1% base rate?\n- H1 | Calibration lowers expected error | supported\n- H2 | Ranking quality is unchanged | supported\n- H3 | Gains hold under drift | open")
def hypotheses(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    top = 0
    if s.paragraphs:
        c.box(x, y + 0.1, w, 1.15, fill="surface", shadow=False)
        c.text(x + 0.3, y + 0.18, 4, 0.3, "RESEARCH QUESTION", 11, "accent", "body", True, chrome=True)
        c.fit_text(x + 0.3, y + 0.5, w - 0.6, 0.7, s.paragraphs[0], 22, 14, "text", "heading", True, valign="middle")
        top = 1.45
    items = s.items[:4]
    n = max(len(items), 1)
    rh = min(1.0, (h - 0.1 - top) / n - 0.12)
    for k, it in enumerate(items):
        tag, text, status = cells(it, 3)[:3]
        ry = y + 0.1 + top + k * (rh + 0.12)
        c.box(x, ry, w, rh, fill="surface", shadow=False)
        c.badge(x + 0.5, ry + rh / 2, min(0.3, rh / 2 - 0.1), tag, "primary", 14)
        c.fit_text(x + 1.05, ry + 0.05, w - 3.5, rh - 0.1, text, 20, 12, "text", valign="middle")
        tone = STATUS.get(status.strip().lower(), "muted")
        c.rect(x + w - 2.2, ry + rh / 2 - 0.19, 1.9, 0.38, tone, kind="round", radius=0.19)
        c.text(x + w - 2.2, ry + rh / 2 - 0.19, 1.9, 0.38, status.upper(), 12, c.t.on(tone), "body", True, "center", "middle", chrome=True)


@layout("equation", "science", "A formula shown large and typeset, with a legend of its symbols.", 60,
        accepts="props: math (LaTeX subset, e.g. `\\hat{y}=\\sigma(Wx+b)`); items: `symbol | meaning` (up to 6); first paragraph: caption",
        example="# Predictions are a sigmoid of a linear score\nlayout: equation\nmath: \\hat{y}=\\sigma(w^{T}x+b)\n- y-hat | predicted probability\n- w | weights\n- b | bias")
def equation(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    c.box(x, y + 0.1, w, 1.9, fill="surface", shadow=False)
    latex = s.prop("math")
    try:
        from ..charts.themed import render_math
        path, mw, mh = render_math(c.t, latex, 44, c.deck, s.index)
        k = min((w - 0.8) / mw, 1.55 / mh, 1.4)
        from ..core.scene import Image
        c.items.append(Image(x + (w - mw * k) / 2, y + 0.1 + (1.9 - mh * k) / 2, mw * k, mh * k, path))
    except (ImportError, ValueError) as e:
        c.text(x + 0.3, y + 0.1, w - 0.6, 1.9, latex, 26, "text", "mono", False, "center", "middle")
        c.scene.problems.append(f"[Medium] formula not typeset ({e}); install scripts/requirements/charts.txt or fix the LaTeX")
    items = s.items[:6]
    cols = 2
    cw = (w - 0.4) / cols
    for k, it in enumerate(items):
        sym, meaning = cells(it, 2)[:2]
        r, col = divmod(k, cols)
        cx, cy = x + col * (cw + 0.4), y + 2.3 + r * 0.62
        c.fit_text(cx, cy, 1.5, 0.52, sym, 20, 12, "accent", "heading", True, valign="middle")
        c.fit_text(cx + 1.6, cy, cw - 1.6, 0.52, meaning, 18, 11, "text", valign="middle")
    if s.paragraphs:
        c.fit_text(x, y + h - 0.55, w, 0.5, s.paragraphs[0], 16, 11, "muted", "body", False, valign="middle")


def _figure_no(c, s):
    n = 1 + sum(1 for x in c.deck.slides[:s.index - 1] if x.layout in ("figure", "figures2"))
    return s.prop("fig") or str(n)


@layout("figure", "science", "A large figure with a numbered caption and the key observations beside it.", 70,
        accepts="image: figure file, or `chart:` plus a table; caption: caption text; items: key observations (up to 4)",
        example="# Error falls as data grows\nlayout: figure\nimage: figures/learning-curve.png\ncaption: Test error against training size, mean of five seeds.\n- Error halves by 10 k rows\n- The gap to the baseline persists")
def figure(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    fw = 7.9
    cap = 0.7 if s.prop("caption") else 0
    if s.image:
        c.image(x, y + 0.1, fw, h - 0.1 - cap, s.image, "figure")
    elif s.table:
        try:
            from ..charts.themed import render_chart
            path = render_chart(c.t, s.prop("chart", "bar"), s.table, fw, h - 0.1 - cap, c.deck, s.index, s.prop("ylabel"))
            c.image(x, y + 0.1, fw, h - 0.1 - cap, path)
        except (ImportError, ValueError) as e:
            c.box(x, y + 0.1, fw, h - 0.1 - cap, fill="surface")
            c.scene.problems.append(f"chart not drawn: {e}")
    else:
        c.box(x, y + 0.1, fw, h - 0.1 - cap, fill="surface")
        c.scene.problems.append("[Medium] figure has no image or table")
    if cap:
        c.fit_text(x, y + h - cap + 0.05, fw, cap - 0.05, f"**Figure {_figure_no(c, s)}.** {s.prop('caption')}", 14, 11, "muted")
    px = x + fw + 0.45
    c.text(px, y + 0.15, w - fw - 0.45, 0.3, "WHAT TO SEE", 12, "accent", "body", True, chrome=True)
    items = s.items[:4]
    n = max(len(items), 1)
    rh = (h - 0.8) / n
    for k, it in enumerate(items):
        ry = y + 0.65 + k * rh
        c.badge(px + 0.22, ry + 0.3, 0.2, str(k + 1), "primary", 13)
        c.fit_text(px + 0.6, ry, w - fw - 1.1, rh - 0.1, it.text, 18, 12, "text")


@layout("figures2", "science", "Two panels side by side, (a) and (b), each with a caption and one takeaway line.", 70,
        accepts="image and image2: the two figures; caption and caption2: their captions; takeaway: the line under both",
        example="# The effect holds on both datasets\nlayout: figures2\nimage: figures/a.png\nimage2: figures/b.png\ncaption: Dataset A\ncaption2: Dataset B\ntakeaway: Same ordering of methods on both.")
def figures2(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    take = s.prop("takeaway") or (s.paragraphs[0] if s.paragraphs else "")
    tb = 0.75 if take else 0
    pw = (w - 0.4) / 2
    ph = h - 0.1 - tb - 0.7
    for k, (img, cap) in enumerate(((s.image, s.prop("caption")), (s.prop("image2"), s.prop("caption2")))):
        px = x + k * (pw + 0.4)
        c.text(px, y + 0.1, 0.5, 0.35, f"({'ab'[k]})", 16, "accent", "heading", True, valign="middle", chrome=True)
        c.image(px, y + 0.5, pw, ph, img, f"panel {'ab'[k]}")
        if cap:
            c.fit_text(px, y + 0.5 + ph + 0.05, pw, 0.6, cap, 14, 11, "muted")
    if take:
        c.rect(x, y + h - tb, w, tb, "accent")
        c.fit_text(x + 0.3, y + h - tb, w - 0.6, tb, take, 20, 13, c.t.on("accent"), "body", True, valign="middle")


@layout("references", "science", "Numbered reference list in two columns, small but readable.", 160,
        accepts="items: one reference each (up to 14), numbered automatically",
        example="# References\nlayout: references\n- Friedman J. (2001). Greedy function approximation. Annals of Statistics.\n- Niculescu-Mizil A. (2005). Predicting good probabilities with supervised learning. ICML.")
def references(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:14]
    per = (len(items) + 1) // 2
    cw = (w - 0.5) / 2
    rh = (h - 0.1) / max(per, 1)
    for k, it in enumerate(items):
        col, r = divmod(k, per)
        cx, cy = x + col * (cw + 0.5), y + 0.1 + r * rh
        c.text(cx, cy, 0.55, 0.4, f"[{k + 1}]", 13, "accent", "body", True, chrome=True)
        c.fit_text(cx + 0.6, cy, cw - 0.6, rh - 0.08, it.text, 14, 11, "text")


@layout("factsheet", "science", "Fact sheet: key and value rows for a dataset, a study design or a specification.", 80,
        accepts="items: `Key | value` (up to 9); first paragraph: caption",
        example="# The dataset in one table\nlayout: factsheet\nsource: data/card.md\n- Rows | 365 daily records\n- Period | one year\n- Target | rides per day\n- Split | time-ordered, last 4 weeks held out")
def factsheet(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    items = s.items[:9]
    cap = 0.55 if s.paragraphs else 0
    n = max(len(items), 1)
    rh = min(0.62, (h - 0.1 - cap) / n)
    for k, it in enumerate(items):
        key, value = cells(it, 2)[:2]
        ry = y + 0.1 + k * rh
        if k % 2 == 0:
            c.rect(x, ry, w, rh, "surface", alpha=0.8)
        c.fit_text(x + 0.2, ry, 3.2, rh, key.upper(), 15, 11, "accent", "body", True, valign="middle")
        c.fit_text(x + 3.6, ry, w - 3.8, rh, value, 19, 12, "text", valign="middle")
    if cap:
        c.fit_text(x, y + h - cap, w, cap, s.paragraphs[0], 15, 11, "muted", valign="middle")
