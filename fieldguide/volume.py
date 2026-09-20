"""Volume scaffolding: cover, contents, running footers, page numbering.

Written at VOLUME scale on purpose. The Claude series was built as 23 six-page guides and
then repackaged into volumes when it turned out the individual guides were not saleable —
a month of work that produced inputs rather than SKUs. Here a chapter is a run of pages
inside one document; there is no standalone-chapter product and no per-chapter cover.

    v = Volume(path, COPILOT, title=..., subtitle=..., badge=..., tagline=...)
    v.cover(stats=[...], inside=[...])
    v.contents(entries)
    p, y = v.open('Chapter 1  ·  What Copilot Is')
    ...draw...
    v.close()
    v.save()
"""
from __future__ import annotations

import os

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from .draw import CW, H, MX, W, Painter, wrap

BAR_H = 40         # cover tagline bar
VALUE_GAP = 14
VALUE_H = 44
PANEL_GAP = 16
CONTENT_TOP = H - 30


class Volume:
    def __init__(self, path, theme, *, title, subtitle, badge, tagline,
                 edition='2026 EDITION'):
        self.path = path
        self.t = theme
        self.title = title
        self.subtitle = subtitle
        self.badge = badge
        self.tagline = tagline
        self.edition = edition
        self.c = canvas.Canvas(path, pagesize=LETTER)
        self.c.setTitle(title)
        self.c.setAuthor(theme.series.title())
        self.c.setSubject(subtitle)
        self.p = Painter(self.c, theme)
        self.page_no = 0
        self._label = ''

    # ------------------------------------------------------------------- pages
    def open(self, label):
        """Start a content page. Returns (painter, starting y)."""
        self.page_no += 1
        self._label = label
        self.p.page_bg()
        self.p.header()
        return self.p, CONTENT_TOP

    def close(self):
        self.p.footer('%s  ·  %s' % (self.t.series.title(), self._label), self.page_no)
        self.c.showPage()

    def save(self):
        self.c.save()
        return self.path

    # ------------------------------------------------------------------- cover
    def cover(self, stats, inside):
        """stats: [(big, small)] · inside: [(n, title, blurb)]

        The panel STRETCHES to fill down to the value strip rather than being sized to
        its content. Content-sized panels left ~300pt of bare background at the bottom of
        the short Claude volumes — a third of the cover, and the first thing a thumbnail
        shows.
        """
        c, t, p = self.c, self.t, self.p
        self.page_no += 1
        p.page_bg()

        c.setFillColor(t.c('accent'))
        c.rect(0, H - 150, W, 150, fill=1, stroke=0)
        c.setFillColor(t.c('accent_dark'))
        c.circle(W - 70, H - 46, 54, fill=1, stroke=0)
        c.circle(W - 138, H - 122, 32, fill=1, stroke=0)
        c.setFillColor(t.c('accent_darker'))
        c.circle(64, H - 128, 24, fill=1, stroke=0)

        p.badge(MX, H - 66, self.badge)
        c.setFillColor(t.c('white'))
        c.setFont('Helvetica-Bold', 8)
        c.drawString(MX, H - 92, t.series)
        c.setFont('Helvetica', 8)
        c.drawString(MX, H - 108, self.edition)

        y = H - 210
        c.setFillColor(t.c('cream'))
        size = 30 if len(self.title) < 26 else 26
        c.setFont('Helvetica-Bold', size)
        for line in wrap(self.title, size, CW, 'Helvetica-Bold'):
            c.drawString(MX, y, line)
            y -= size + 6

        c.setFillColor(t.c('accent_light'))
        c.setFont('Helvetica', 14)
        y -= 6
        for line in wrap(self.subtitle, 14, CW):
            c.drawString(MX, y, line)
            y -= 19

        # Stat strip
        y -= 18
        c.setFillColor(t.c('panel'))
        c.roundRect(MX, y - 52, CW, 52, radius=5, fill=1, stroke=0)
        colw = CW / len(stats)
        for i, (big, small) in enumerate(stats):
            cx = MX + colw * i + colw / 2
            c.setFillColor(t.c('accent'))
            c.setFont('Helvetica-Bold', 19)
            c.drawCentredString(cx, y - 27, big)
            c.setFillColor(t.c('mid_grey'))
            c.setFont('Helvetica-Bold', 7)
            c.drawCentredString(cx, y - 42, small)
        y -= 52

        panel_top = y - 20
        panel_bottom = BAR_H + VALUE_GAP + VALUE_H + PANEL_GAP
        ph = panel_top - panel_bottom
        c.setFillColor(t.c('panel'))
        c.roundRect(MX, panel_bottom, CW, ph, radius=5, fill=1, stroke=0)
        c.setFillColor(t.c('accent'))
        c.rect(MX, panel_bottom, 4, ph, fill=1, stroke=0)
        c.setFillColor(t.c('accent_light'))
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 14, panel_top - 22, "WHAT'S INSIDE")

        area_top = panel_top - 40
        area_bottom = panel_bottom + 14
        n = len(inside)
        step = (area_top - area_bottom) / n
        card_h = step - 8
        cx0, cw3 = MX + 14, CW - 28
        for i, (num, ttl, blurb) in enumerate(inside):
            top = area_top - i * step
            bot = top - card_h
            c.setFillColor(t.c('panel2'))
            c.roundRect(cx0, bot, cw3, card_h, radius=4, fill=1, stroke=0)
            mid = bot + card_h / 2
            c.setFillColor(t.c('green'))
            c.setFont('Helvetica-Bold', 10)
            c.drawString(cx0 + 12, mid + 2, 'v')
            c.setFillColor(t.c('accent'))
            c.setFont('Helvetica-Bold', 12)
            c.drawString(cx0 + 27, mid + 2, '%02d' % num)
            c.setFillColor(t.c('cream'))
            c.setFont('Helvetica-Bold', 11)
            c.drawString(cx0 + 52, mid + 2, ttl)
            if blurb:
                c.setFillColor(t.c('mid_grey'))
                c.setFont('Helvetica', 8.5)
                c.drawString(cx0 + 52, mid - 12, blurb)

        vy = BAR_H + VALUE_GAP
        c.setFillColor(t.c('panel2'))
        c.roundRect(MX, vy, CW, VALUE_H, radius=5, fill=1, stroke=0)
        props = ['Instant PDF download', 'Printable cheat sheet',
                 'Plain English, no jargon']
        pw = CW / len(props)
        for i, prop in enumerate(props):
            px = MX + pw * i + 16
            c.setFillColor(t.c('green'))
            c.setFont('Helvetica-Bold', 10)
            c.drawString(px, vy + VALUE_H / 2 - 4, 'v')
            c.setFillColor(t.c('light_grey'))
            c.setFont('Helvetica', 9)
            c.drawString(px + 13, vy + VALUE_H / 2 - 4, prop)

        c.setFillColor(t.c('accent'))
        c.rect(0, 0, W, BAR_H, fill=1, stroke=0)
        c.setFillColor(t.c('white'))
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(W / 2, 16, self.tagline)
        c.showPage()

    # ---------------------------------------------------------------- contents
    def contents(self, entries):
        """entries: [(n, title, blurb, start_page)]"""
        c, t, p = self.c, self.t, self.p
        self.page_no += 1
        p.page_bg()
        p.header()

        y = H - 52
        c.setFillColor(t.c('accent'))
        c.setFont('Helvetica-Bold', 22)
        c.drawString(MX, y, 'Contents')
        y -= 22
        c.setFillColor(t.c('mid_grey'))
        c.setFont('Helvetica', 9.5)
        c.drawString(MX, y, self.title)
        y -= 30

        rh = 34
        for num, ttl, blurb, start in entries:
            c.setFillColor(t.c('panel2') if num % 2 == 0 else t.c('panel'))
            c.roundRect(MX, y - rh + 4, CW, rh - 3, radius=3, fill=1, stroke=0)
            c.setFillColor(t.c('accent'))
            c.setFont('Helvetica-Bold', 11)
            c.drawString(MX + 12, y - rh + 19, '%02d' % num)
            c.setFillColor(t.c('cream'))
            c.setFont('Helvetica-Bold', 11)
            c.drawString(MX + 38, y - rh + 19, ttl)
            c.setFillColor(t.c('mid_grey'))
            c.setFont('Helvetica', 8.5)
            c.drawString(MX + 38, y - rh + 8, blurb)
            c.setFillColor(t.c('accent_light'))
            c.setFont('Helvetica-Bold', 9)
            c.drawRightString(W - MX - 10, y - rh + 19, 'p.%d' % start)
            y -= rh + 4

        y -= 10
        lines = ['Chapters run easiest to hardest, so reading front to back builds on',
                 'itself — but each one stands alone if you already know the basics.',
                 'The last two pages are a printable reference and a fix-it table.']
        p.info_panel(MX, y, 'HOW TO USE THIS VOLUME', lines)

        self._label = 'Contents'
        self.close()
