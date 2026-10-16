"""Draw scenes into a PDF with reportlab, using the same geometry as the PPTX backend. Needs reportlab."""
from pathlib import Path

from ..core import textfit


def _register(theme):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    names = {}
    for role in ("heading", "body", "mono"):
        for bold in (False, True):
            f = theme.font_file(role, bold)
            name = f"dk-{f.stem}"
            if name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, str(f)))
            names[(role, bold)] = name
    return names


def build_pdf(scenes, theme, deck, path):
    from reportlab.pdfgen import canvas as rl

    from ..core.scene import H, W, Image, Line, Poly, Shape, Text

    fonts = _register(theme)
    PW, PH = W * 72, H * 72
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    pdf = rl.Canvas(str(path), pagesize=(PW, PH))
    pdf.setTitle(str(deck.meta.get("title", "")) or scenes[0].title)
    pdf.setAuthor(str(deck.meta.get("team", "")))

    def hexcolor(h):
        from reportlab.lib.colors import HexColor
        return HexColor(h)

    for sc in scenes:
        pdf.setFillColor(hexcolor(sc.bg))
        pdf.rect(0, 0, PW, PH, stroke=0, fill=1)
        for it in sc.items:
            if isinstance(it, Shape):
                x, y, w, h = it.x * 72, PH - (it.y + it.h) * 72, it.w * 72, it.h * 72
                pdf.saveState()
                if it.fill:
                    pdf.setFillColor(hexcolor(it.fill))
                pdf.setFillAlpha(it.alpha)  # after setFillColor: a Color object resets alpha to 1
                if it.line:
                    pdf.setStrokeColor(hexcolor(it.line))
                    pdf.setLineWidth(it.line_w)
                fill, stroke = int(bool(it.fill)), int(bool(it.line))
                if it.kind == "ellipse":
                    pdf.ellipse(x, y, x + w, y + h, stroke=stroke, fill=fill)
                elif it.kind == "round":
                    pdf.roundRect(x, y, w, h, min(it.radius * 72, h / 2, w / 2), stroke=stroke, fill=fill)
                else:
                    pdf.rect(x, y, w, h, stroke=stroke, fill=fill)
                pdf.restoreState()
            elif isinstance(it, Poly):
                pdf.saveState()
                if it.fill:
                    pdf.setFillColor(hexcolor(it.fill))
                pdf.setFillAlpha(it.alpha)
                if it.line:
                    pdf.setStrokeColor(hexcolor(it.line))
                    pdf.setLineWidth(it.line_w)
                outline = pdf.beginPath()
                outline.moveTo(it.points[0][0] * 72, PH - it.points[0][1] * 72)
                for px, py in it.points[1:]:
                    outline.lineTo(px * 72, PH - py * 72)
                outline.close()
                pdf.drawPath(outline, stroke=int(bool(it.line)), fill=int(bool(it.fill)))
                pdf.restoreState()
            elif isinstance(it, Line):
                pdf.setStrokeColor(hexcolor(it.color))
                pdf.setLineWidth(it.width)
                pdf.line(it.x1 * 72, PH - it.y1 * 72, it.x2 * 72, PH - it.y2 * 72)
            elif isinstance(it, Image):
                pdf.drawImage(it.path, it.x * 72, PH - (it.y + it.h) * 72, it.w * 72, it.h * 72, mask="auto")
            elif isinstance(it, Text):
                _draw_text(pdf, theme, fonts, it, PH, hexcolor)
        pdf.showPage()
    pdf.save()
    return path


def _draw_text(pdf, theme, fonts, it, PH, hexcolor):
    lines = textfit.wrap(theme, it.text, it.role, it.size, it.w, it.bold)
    lh = it.size * it.line_h
    total = lh * len(lines) / 72
    top = it.y + {"top": 0.0, "middle": (it.h - total) / 2, "bottom": it.h - total}[it.valign]
    pdf.setFillColor(hexcolor(it.color))
    for i, line in enumerate(lines):
        width = textfit.line_width(theme, line, it.role, it.size)
        x0 = it.x + {"left": 0.0, "center": (it.w - width) / 2, "right": it.w - width}[it.align]
        # baseline: half the leading below the line top, then about 0.8 em of ascent
        by = PH - (top * 72 + i * lh + (lh - it.size) / 2 + it.size * 0.8)
        x = x0 * 72
        for j, (word, bold) in enumerate(line):
            font = fonts[(it.role, it.bold or bold)]
            if j:
                x += textfit.width_in(theme, " ", it.role, it.size, it.bold or bold) * 72
            pdf.setFont(font, it.size)
            pdf.drawString(x, by, word)
            x += textfit.width_in(theme, word, it.role, it.size, it.bold or bold) * 72
