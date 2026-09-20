"""Drawing primitives, themed.

Same geometry as the Claude series design system — the formulas are copied verbatim so
output is visually identical apart from colour:

    step card     card_h = 48 + len(lines) * 15
    info panel    ph     = len(lines) * 16 + pad*2 + 22     (pad=12)
    tip / warn    bh     = len(lines) * 15 + pad*2 + 20     (pad=10)
    code block    bh     = len(lines) * 13 + pad*2          (pad=10, lh=13)
    table row     rh     = 22

Every method returns the new `y` so callers can chain down the page. Origin is bottom-left
(reportlab default) — y decreases as you move down.

Two rules the Claude scripts learned the hard way and this module enforces:
  * NEVER offset a baseline inside a wrap loop that also moves `y` (the guide-01 bug).
  * NEVER hardcode a badge width while drawing centred text on it — derive it from
    stringWidth, or long labels spill out both sides (the guide-20 bug).
"""
from __future__ import annotations

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX

FOOTER_H = 22
HEADER_H = 6


def wrap(text: str, size: float, width: float, font: str = 'Helvetica') -> list[str]:
    return simpleSplit(text, font, size, width)


class Painter:
    """Wraps a canvas plus a theme so nothing has to thread colours around."""

    def __init__(self, c, theme):
        self.c = c
        self.t = theme

    # ------------------------------------------------------------ page furniture
    def page_bg(self):
        self.c.setFillColor(self.t.c('bg'))
        self.c.rect(0, 0, W, H, fill=1, stroke=0)

    def header(self):
        self.c.setFillColor(self.t.c('accent'))
        self.c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)

    def footer(self, label: str, page_no):
        c = self.c
        c.setFillColor(self.t.c('panel'))
        c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
        c.setFillColor(self.t.c('accent_light'))
        c.setFont('Helvetica', 8)
        c.drawString(MX, 7, label)
        c.setFillColor(self.t.c('mid_grey'))
        c.drawRightString(W - MX, 7, 'Page %s' % page_no)

    def badge(self, x, y, text, size=10, pad=24):
        """Rounded badge sized to its text. Returns its width.

        The width is DERIVED, never hardcoded — a fixed width with centred text is what
        made guide 20's badge start 28pt left of the page margin.
        """
        c = self.c
        bw = c.stringWidth(text, 'Helvetica-Bold', size) + pad
        c.setFillColor(self.t.c('accent_darker'))
        c.roundRect(x, y, bw, 22, radius=4, fill=1, stroke=0)
        c.setFillColor(self.t.c('white'))
        c.setFont('Helvetica-Bold', size)
        c.drawCentredString(x + bw / 2, y + 7, text)
        return bw

    # ------------------------------------------------------------------ content
    def heading(self, x, y, text, size=15):
        self.c.setFillColor(self.t.c('accent'))
        self.c.setFont('Helvetica-Bold', size)
        self.c.drawString(x, y, text)
        return y - size - 5

    def subheading(self, x, y, text, size=12):
        self.c.setFillColor(self.t.c('accent_light'))
        self.c.setFont('Helvetica-Bold', size)
        self.c.drawString(x, y, text)
        return y - size - 4

    def body(self, x, y, text, width=CW, size=10, leading=15):
        """Wrapped body text. Draws at `y` and moves `y` — never both."""
        self.c.setFillColor(self.t.c('light_grey'))
        self.c.setFont('Helvetica', size)
        for line in wrap(text, size, width):
            self.c.drawString(x, y, line)
            y -= leading
        return y

    def step_card(self, x, y, num, title, lines, w=CW):
        c, t = self.c, self.t
        pad, badge = 10, 26
        card_h = 48 + len(lines) * 15
        c.setFillColor(t.c('panel'))
        c.roundRect(x, y - card_h, w, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(t.c('accent'))
        c.roundRect(x + pad, y - pad - badge, badge, badge, radius=3, fill=1, stroke=0)
        c.setFillColor(t.c('white'))
        c.setFont('Helvetica-Bold', 12)
        c.drawCentredString(x + pad + badge / 2, y - pad - badge + 7, str(num))
        tx = x + pad + badge + 8
        c.setFillColor(t.c('cream'))
        c.setFont('Helvetica-Bold', 11)
        c.drawString(tx, y - pad - 12, title)
        c.setFillColor(t.c('light_grey'))
        c.setFont('Helvetica', 10)
        by = y - pad - 28
        for line in lines:
            c.drawString(tx, by, line)
            by -= 15
        return y - card_h

    def _boxed(self, x, y, heading, lines, w, bg_key, rule_key, prefix):
        c, t = self.c, self.t
        pad = 10
        bh = len(lines) * 15 + pad * 2 + 20
        c.setFillColor(t.c(bg_key))
        c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
        c.setFillColor(t.c(rule_key))
        c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
        c.setFillColor(t.c(rule_key))
        c.setFont('Helvetica-Bold', 10)
        c.drawString(x + 14, y - pad - 10, '%s  %s' % (prefix, heading))
        c.setFillColor(t.c('light_grey'))
        c.setFont('Helvetica', 10)
        ty = y - pad - 26
        for line in lines:
            c.drawString(x + 14, ty, line)
            ty -= 15
        return y - bh

    def tip_box(self, x, y, heading, lines, w=CW):
        return self._boxed(x, y, heading, lines, w, 'dark_green_bg', 'green', 'TIP')

    def warn_box(self, x, y, heading, lines, w=CW):
        return self._boxed(x, y, heading, lines, w, 'dark_amber_bg', 'amber', 'NOTE')

    def info_panel(self, x, y, heading, lines, w=CW):
        c, t = self.c, self.t
        pad = 12
        ph = len(lines) * 16 + pad * 2 + 22
        c.setFillColor(t.c('panel'))
        c.roundRect(x, y - ph, w, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(t.c('accent_light'))
        c.setFont('Helvetica-Bold', 11)
        c.drawString(x + pad, y - pad - 12, heading)
        c.setFillColor(t.c('light_grey'))
        c.setFont('Helvetica', 10)
        ty = y - pad - 30
        for line in lines:
            c.drawString(x + pad, ty, line)
            ty -= 16
        return y - ph

    def code_block(self, x, y, lines, w=CW):
        c, t = self.c, self.t
        pad, lh = 10, 13
        bh = len(lines) * lh + pad * 2
        c.setFillColor(t.c('code_bg'))
        c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
        c.setStrokeColor(t.c('accent'))
        c.setLineWidth(0.5)
        c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
        ty = y - pad - 10
        for line in lines:
            comment = line.strip().startswith('#') or line.strip().startswith('//')
            c.setFillColor(t.c('mid_grey') if comment else t.c('green'))
            c.setFont('Courier', 9)
            c.drawString(x + pad, ty, line)
            ty -= lh
        return y - bh

    def table(self, x, y, headers, rows, col_w):
        c, t = self.c, self.t
        rh, pad = 22, 7
        tw = sum(col_w)
        c.setFillColor(t.c('accent'))
        c.rect(x, y - rh, tw, rh, fill=1, stroke=0)
        c.setFillColor(t.c('white'))
        c.setFont('Helvetica-Bold', 9)
        cx = x
        for i, h in enumerate(headers):
            c.drawString(cx + pad, y - rh + 7, h)
            cx += col_w[i]
        for ri, row in enumerate(rows):
            ry = y - rh * (ri + 2)
            c.setFillColor(t.c('panel2') if ri % 2 == 0 else t.c('panel'))
            c.rect(x, ry, tw, rh, fill=1, stroke=0)
            cx = x
            for ci, cell in enumerate(row):
                c.setFillColor(t.c('accent_light') if ci == 0 else t.c('light_grey'))
                c.setFont('Helvetica-Bold' if ci == 0 else 'Helvetica', 9)
                c.drawString(cx + pad, ry + 7, str(cell))
                cx += col_w[ci]
        return y - rh * (len(rows) + 1)

    def bullets(self, x, y, items, step=27, size=10):
        c, t = self.c, self.t
        for b in items:
            c.setFillColor(t.c('green'))
            c.setFont('Helvetica-Bold', 11)
            c.drawString(x, y, 'v')
            c.setFillColor(t.c('light_grey'))
            c.setFont('Helvetica', size)
            c.drawString(x + 16, y, b)
            y -= step
        return y
