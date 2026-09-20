#!/usr/bin/env python3
"""Build the Cheat Sheet Pack — a PRINTABLE reference set.

    python build_cheatsheets.py

Deliberately NOT the house dark theme. The rest of the series is #0F0F1A full-bleed,
which is the wrong choice for something people are meant to print: it drains a cartridge
and looks terrible on a home printer. This pack uses a light, ink-frugal theme — white
page, thin rules, colour only on headings and the accent bar.

Layout is one wide column of key/value rows, one sheet per page. Two guards hard-fail the
build rather than ship a broken sheet: `verify_no_overflow()` on any row that would run
past the column, and `verify_fits_one_page()` on any sheet that would spill onto a second
page. Do not remove either — one sheet per page IS the product promise, and a silent
truncation is a refund.

Content lives in cheatsheet_data.py (single source).
"""
import os

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from cheatsheet_data import SHEETS

W, H = LETTER
MX = 0.55 * inch
CW = W - 2 * MX
OUTDIR = r'C:\Projects\UserGuide\outputs'
OUT = os.path.join(OUTDIR, 'Claude_Cheat_Sheet_Pack.pdf')

# Print-friendly palette. Ink coverage kept low on purpose.
PAPER = HexColor('#FFFFFF')
INK   = HexColor('#1A1A24')
OG    = HexColor('#C4611F')      # darker than the screen orange — reads on paper
OGD   = HexColor('#8F4514')
GREY  = HexColor('#6B6660')
RULE  = HexColor('#D8D3CC')
BAND  = HexColor('#F4F0EA')      # alternating row tint, very light

# One wide column, not two. Two columns squeezed the value field to ~34 characters, which
# would have meant gutting the content to fit the layout — the wrong way round. A single
# column also scans better on a printed page.
COLW = CW
LH = 19                          # row height
KEY_W = 0.36                     # share of the column given to the left-hand term
FS = 10.5                        # body size — this gets pinned to a wall, size it for that

KEYW = COLW * KEY_W
VALW = COLW - KEYW - 6


def verify_no_overflow():
    """Fail the build rather than ship a truncated line."""
    problems = []
    for s in SHEETS:
        for heading, rows in s['blocks']:
            if stringWidth(heading, 'Helvetica-Bold', 9.5) > COLW:
                problems.append('%s / heading too wide: %s' % (s['title'], heading))
            for left, right in rows:
                if stringWidth(left, 'Helvetica-Bold', FS) > KEYW - 6:
                    problems.append('%s / key too wide: %s' % (s['title'], left))
                if stringWidth(right, 'Helvetica', FS) > VALW:
                    problems.append('%s / value too wide: %s' % (s['title'], right))
    if problems:
        for p in problems:
            print('OVERFLOW  ' + p)
        raise SystemExit('%d line(s) would overflow — fix cheatsheet_data.py' % len(problems))


def verify_fits_one_page():
    """Every sheet must be exactly one page — that is the product promise."""
    avail = (H - 88) - 44
    bad = []
    for s in SHEETS:
        h = sum(20 + len(rows) * LH + 12 for _h, rows in s['blocks'])
        if h > avail:
            bad.append('%s needs %.0fpt, page has %.0fpt' % (s['title'], h, avail))
    if bad:
        for b in bad:
            print('TOO TALL  ' + b)
        raise SystemExit('%d sheet(s) would run onto a second page' % len(bad))


def sheet_height(blocks):
    """Total vertical space this sheet's content needs, single column."""
    h = 0
    for heading, rows in blocks:
        h += 16 + len(rows) * LH + 10
    return h


def page(c, s, index, total):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Accent bar + title block
    c.setFillColor(OG)
    c.rect(0, H - 8, W, 8, fill=1, stroke=0)

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 19)
    c.drawString(MX, H - 44, s['title'])
    c.setFillColor(GREY)
    c.setFont('Helvetica', 9.5)
    c.drawString(MX, H - 59, s['sub'])

    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(MX, H - 68, W - MX, H - 68)

    x, y = MX, H - 88
    for heading, rows in s['blocks']:
        c.setFillColor(OGD)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(x, y, heading.upper())
        y -= 6
        c.setStrokeColor(OG)
        c.setLineWidth(1)
        c.line(x, y, x + COLW, y)
        y -= 14

        for i, (left, right) in enumerate(rows):
            if i % 2 == 0:
                c.setFillColor(BAND)
                c.rect(x - 3, y - 4, COLW + 6, LH, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont('Helvetica-Bold', FS)
            c.drawString(x, y, left)
            c.setFillColor(GREY)
            c.setFont('Helvetica', FS)
            c.drawString(x + KEYW, y, right)
            y -= LH
        y -= 12

    # Footer
    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.line(MX, 34, W - MX, 34)
    c.setFillColor(GREY)
    c.setFont('Helvetica', 7.5)
    c.drawString(MX, 24, 'Claude AI Field Guide  ·  Cheat Sheet Pack')
    c.drawCentredString(W / 2, 24, 'etsy.com/shop/FranksMarketDesigns')
    c.drawRightString(W - MX, 24, 'Sheet %d of %d' % (index, total))
    c.showPage()


def cover(c, total):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(0, H - 10, W, 10, fill=1, stroke=0)

    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 40)
    c.drawString(MX, H - 130, 'Cheat Sheet Pack')
    c.setFillColor(OGD)
    c.setFont('Helvetica', 16)
    c.drawString(MX, H - 158, '%d printable one-page references for Claude AI' % total)

    c.setStrokeColor(OG)
    c.setLineWidth(2)
    c.line(MX, H - 172, W - MX, H - 172)

    c.setFillColor(GREY)
    c.setFont('Helvetica', 10.5)
    y = H - 200
    for line in [
        'Designed to be printed. Light background, low ink coverage, one sheet per page.',
        'Print the ones you need, pin them up, and stop searching the docs for the same',
        'five commands. Every sheet stands alone.',
    ]:
        c.drawString(MX, y, line)
        y -= 16

    y -= 18
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, "WHAT'S INSIDE")
    y -= 6
    c.setStrokeColor(RULE)
    c.line(MX, y, W - MX, y)
    y -= 18

    for i, s in enumerate(SHEETS, start=1):
        if i % 2 == 1:
            c.setFillColor(BAND)
            c.rect(MX - 2, y - 4, CW + 4, 18, fill=1, stroke=0)
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(MX, y, '%02d' % i)
        c.setFillColor(INK)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 24, y, s['title'])
        c.setFillColor(GREY)
        c.setFont('Helvetica', 8.5)
        c.drawRightString(W - MX, y, s['sub'])
        y -= 18

    c.setFillColor(GREY)
    c.setFont('Helvetica', 8.5)
    c.drawString(MX, 56, 'Unofficial and independent. Not affiliated with, endorsed by, '
                         'or sponsored by Anthropic.')
    c.setFillColor(OGD)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(MX, 40, 'etsy.com/shop/FranksMarketDesigns')
    c.showPage()


def main():
    verify_no_overflow()
    verify_fits_one_page()
    os.makedirs(OUTDIR, exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=LETTER)
    c.setTitle('Claude AI Cheat Sheet Pack')
    c.setAuthor('Claude AI Field Guide Series')
    c.setSubject('%d printable one-page references' % len(SHEETS))

    cover(c, len(SHEETS))
    for i, s in enumerate(SHEETS, start=1):
        page(c, s, i, len(SHEETS))
    c.save()
    print('Saved: %s  (%d sheets + cover = %d pages)'
          % (OUT, len(SHEETS), len(SHEETS) + 1))


if __name__ == '__main__':
    main()
