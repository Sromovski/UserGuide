#!/usr/bin/env python3
"""Compile the individual Claude AI Field Guides into multi-guide VOLUME PDFs.

Each source guide (build_guideXX.py) exposes cover() + page2()..page6() that draw
onto a canvas and call showPage(). This script imports those modules, swaps their
module-level ftr() for a volume-aware footer with continuous page numbering, and
renders them all onto one canvas behind a new volume cover + table of contents.

Nothing in the source guides is modified. Run:  python build_volumes.py
"""
import importlib
import os
import sys

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

ROOT = r'C:\Projects\UserGuide'
OUTDIR = os.path.join(ROOT, 'outputs')
sys.path.insert(0, ROOT)

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX

BG     = HexColor('#0F0F1A')
OG     = HexColor('#E07A38')
OGL    = HexColor('#F5A66B')
CREAM  = HexColor('#F5F0E8')
LGR    = HexColor('#D4CFC7')
MGR    = HexColor('#9B9690')
PNL    = HexColor('#1C1C2E')
PNL2   = HexColor('#161625')
GRN    = HexColor('#5CB85C')
WHT    = HexColor('#FFFFFF')
DOG    = HexColor('#C86820')
DDOG   = HexColor('#B85C18')

# One-line "what it covers" blurbs used on the volume contents page.
BLURB = {
    1:  'Account setup, the claude.ai interface, and plan comparison',
    2:  'iOS and Android install, voice mode, camera input',
    3:  'Mac and Windows desktop app, Projects, local files',
    4:  'Chrome extension, browsing agent, page summarisation',
    5:  'Slack, Excel, PowerPoint and Cowork integrations',
    6:  'Node.js LTS install on Mac, Windows and Linux',
    7:  'Git and GitHub from zero — no terminal experience needed',
    8:  'Containers explained, plus a working compose file',
    9:  'VS Code install, five key extensions, settings.json',
    10: 'Install Claude Code, auth, diffs and slash commands',
    11: 'Write CLAUDE.md build plans Claude actually follows',
    12: 'Parallel subagents and the eight hook events',
    13: 'The agentic loop, stopping conditions, context growth',
    14: 'What MCP is and how the protocol is structured',
    15: 'Install Filesystem, GitHub and Brave Search servers',
    16: 'Plugins vs MCP, connectors, plan availability matrix',
    17: 'Build your own skills with SKILL.md frontmatter',
    18: 'Console setup, curl and Python SDK, pricing, errors',
    19: 'Routines, triggers, and end-to-end automation pipelines',
    20: 'Prompt anatomy, XML structuring, 30 copy-paste templates',
    21: 'Subagents, agent teams and workflow orchestration',
    22: 'Gold sets, LLM judges, and CI thresholds for agents',
    23: 'Token billing, prompt caching, batching, budget controls',
}

VOLUMES = [
    dict(key='V1', badge='VOLUME ONE', file='Claude_Field_Guide_Volume_1_Getting_Started.pdf',
         title='Getting Into Claude',
         sub='Every way to use Claude AI without writing a line of code',
         guides=[1, 2, 3, 4, 5],
         tagline='WEB  ·  MOBILE  ·  DESKTOP  ·  CHROME  ·  INTEGRATIONS'),
    dict(key='V2', badge='VOLUME TWO', file='Claude_Field_Guide_Volume_2_Developer_Setup.pdf',
         title='Developer Setup',
         sub='The four tools you need before Claude can touch your code',
         guides=[6, 7, 8, 9],
         tagline='NODE.JS  ·  GIT & GITHUB  ·  DOCKER  ·  VS CODE'),
    dict(key='V3', badge='VOLUME THREE', file='Claude_Field_Guide_Volume_3_Claude_Code.pdf',
         title='Claude Code Mastery',
         sub='From first install to agentic workflows that run themselves',
         guides=[10, 11, 12, 13],
         tagline='CLAUDE CODE  ·  CLAUDE.MD  ·  HOOKS  ·  AGENTIC LOOPS'),
    dict(key='V4', badge='VOLUME FOUR', file='Claude_Field_Guide_Volume_4_Automation_Kit.pdf',
         title='MCP, Plugins & Skills',
         sub='Connect Claude to everything else you use',
         guides=[14, 15, 16, 17],
         tagline='MCP SERVERS  ·  PLUGINS  ·  CONNECTORS  ·  SKILLS'),
    dict(key='V5', badge='VOLUME FIVE', file='Claude_Field_Guide_Volume_5_API_Automation.pdf',
         title='API & Automation',
         sub='Build things that call Claude while you sleep',
         guides=[18, 19, 20],
         tagline='THE API  ·  AUTOMATIONS  ·  PROMPTING MASTERCLASS'),
    dict(key='V6', badge='VOLUME SIX', file='Claude_Field_Guide_Volume_6_Advanced.pdf',
         title='Advanced Add-Ons',
         sub='Orchestration, evaluation and cost control for power users',
         guides=[21, 22, 23],
         tagline='ORCHESTRATION  ·  EVALUATION  ·  COST MANAGEMENT'),
    dict(key='LIB', badge='THE COMPLETE LIBRARY', file='Claude_Field_Guide_COMPLETE_LIBRARY.pdf',
         title='Claude AI Field Guide',
         sub='All 23 guides. Complete beginner to automation builder.',
         guides=list(range(1, 24)),
         tagline='23 GUIDES  ·  6 VOLUMES  ·  ONE COMPLETE LIBRARY'),
]

# Cover layout budget, bottom of the page upward. The "What's Inside" panel absorbs
# whatever is left over, so a 3-guide volume and a 23-guide one both reach the bottom.
BAR_H = 40        # orange tagline bar
VALUE_GAP = 14    # bar -> value strip
VALUE_H = 44      # value strip
PANEL_GAP = 16    # value strip -> What's Inside panel

_state = {'p': 1, 'label': ''}


def wrap(text, size, width, font='Helvetica'):
    return simpleSplit(text, font, size, width)


def pg_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def hdr(c):
    c.setFillColor(OG)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)


def vol_ftr(c):
    """Volume footer — running page number from _state, guide title from _state."""
    c.setFillColor(PNL)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica', 8)
    c.drawString(MX, 7, _state['label'])
    c.setFillColor(MGR)
    c.drawRightString(W - MX, 7, 'Page %d' % _state['p'])


def make_ftr():
    """Replacement for a guide module's ftr(c, n) — ignores the hardcoded n."""
    def _ftr(c, n=None):
        vol_ftr(c)
    return _ftr


def volume_cover(c, vol, titles, total_pages):
    pg_bg(c)

    # Orange top block with decorative circles
    c.setFillColor(OG)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    c.setFillColor(DOG)
    c.circle(W - 70, H - 46, 54, fill=1, stroke=0)
    c.circle(W - 138, H - 122, 32, fill=1, stroke=0)
    c.setFillColor(DDOG)
    c.circle(64, H - 128, 24, fill=1, stroke=0)

    # Volume badge
    c.setFillColor(DDOG)
    bw = 12 + len(vol['badge']) * 6.2
    c.roundRect(MX, H - 66, bw, 24, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 10, H - 59, vol['badge'])

    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 92, 'CLAUDE AI FIELD GUIDE SERIES')
    c.setFont('Helvetica', 8)
    c.drawString(MX, H - 108, '2026 EDITION')

    # Title
    y = H - 210
    c.setFillColor(CREAM)
    size = 30 if len(vol['title']) < 26 else 26
    c.setFont('Helvetica-Bold', size)
    for line in wrap(vol['title'], size, CW, 'Helvetica-Bold'):
        c.drawString(MX, y, line)
        y -= size + 6

    c.setFillColor(OGL)
    c.setFont('Helvetica', 14)
    y -= 6
    for line in wrap(vol['sub'], 14, CW):
        c.drawString(MX, y, line)
        y -= 19

    # Stat strip — the numbers buyers scan for
    y -= 18
    c.setFillColor(PNL)
    c.roundRect(MX, y - 52, CW, 52, radius=5, fill=1, stroke=0)
    stats = [('%d' % len(vol['guides']), 'GUIDES'),
             ('%d' % total_pages, 'PAGES'),
             ('%d' % len(vol['guides']), 'CHEAT SHEETS'),
             ('2026', 'EDITION')]
    colw = CW / len(stats)
    for i, (big, small) in enumerate(stats):
        cx = MX + colw * i + colw / 2
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 19)
        c.drawCentredString(cx, y - 27, big)
        c.setFillColor(MGR)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cx, y - 42, small)
    y -= 52

    # What's inside — stretched to fill the space down to the value strip, rather than
    # sized to its content. A 3-guide volume used to leave ~300pt of bare background
    # above the bottom bar, which is a third of the cover and the first thing an Etsy
    # thumbnail shows. The guide list now carries its one-line blurbs too, so the extra
    # room is filled with real information instead of padding.
    panel_top = y - 20
    panel_bottom = BAR_H + VALUE_GAP + VALUE_H + PANEL_GAP
    ph = panel_top - panel_bottom

    c.setFillColor(PNL)
    c.roundRect(MX, panel_bottom, CW, ph, radius=5, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(MX, panel_bottom, 4, ph, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 14, panel_top - 22, "WHAT'S INSIDE")

    compact = len(titles) > 8
    area_top = panel_top - 44
    area_bottom = panel_bottom + 14
    area_h = area_top - area_bottom

    if compact:
        rows = (len(titles) + 1) // 2
        step = min(max(area_h / rows, 14), 22)
        top = area_top - max(0, (area_h - rows * step)) / 2
        cw2 = (CW - 34) / 2
        for i, (num, t) in enumerate(titles):
            col, row = divmod(i, rows)
            tx = MX + 14 + col * cw2
            ty = top - row * step
            c.setFillColor(GRN)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(tx, ty, 'v')
            c.setFillColor(LGR)
            c.setFont('Helvetica', 8.5)
            label = '%02d  %s' % (num, t)
            while c.stringWidth(label, 'Helvetica', 8.5) > cw2 - 26:
                label = label[:-2]
            c.drawString(tx + 11, ty, label)
    else:
        # Few enough guides that a plain text list would leave the panel looking empty.
        # Each entry becomes a row card instead, sized to divide the panel evenly — so
        # three guides fill the space as convincingly as eight.
        n = len(titles)
        area_top = panel_top - 40
        area_h = area_top - area_bottom
        step = area_h / n
        card_h = step - 8
        cx0, cw3 = MX + 14, CW - 28
        for i, (num, t) in enumerate(titles):
            top = area_top - i * step
            bot = top - card_h
            c.setFillColor(PNL2)
            c.roundRect(cx0, bot, cw3, card_h, radius=4, fill=1, stroke=0)
            mid = bot + card_h / 2
            c.setFillColor(GRN)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(cx0 + 12, mid + 2, 'v')
            c.setFillColor(OG)
            c.setFont('Helvetica-Bold', 12)
            c.drawString(cx0 + 27, mid + 2, '%02d' % num)
            c.setFillColor(CREAM)
            c.setFont('Helvetica-Bold', 11)
            c.drawString(cx0 + 52, mid + 2, t)
            blurb = BLURB.get(num, '')
            if blurb:
                c.setFillColor(MGR)
                c.setFont('Helvetica', 8.5)
                c.drawString(cx0 + 52, mid - 12, blurb)

    # Value strip — the three things a buyer wants confirmed before clicking.
    vy = BAR_H + VALUE_GAP
    c.setFillColor(PNL2)
    c.roundRect(MX, vy, CW, VALUE_H, radius=5, fill=1, stroke=0)
    props = ['Instant PDF download', 'Printable cheat sheets', 'Plain English, no jargon']
    pw = CW / len(props)
    for i, prop in enumerate(props):
        px = MX + pw * i + 16
        c.setFillColor(GRN)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(px, vy + VALUE_H / 2 - 4, 'v')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 9)
        c.drawString(px + 13, vy + VALUE_H / 2 - 4, prop)

    # Bottom bar
    c.setFillColor(OG)
    c.rect(0, 0, W, BAR_H, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 16, vol['tagline'])
    c.showPage()


def contents_page(c, vol, entries):
    """entries = list of (guide_num, title, start_page)"""
    pg_bg(c)
    hdr(c)
    y = H - 52
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(MX, y, 'Contents')
    y -= 22
    c.setFillColor(MGR)
    c.setFont('Helvetica', 9.5)
    c.drawString(MX, y, '%s  ·  %s' % (vol['badge'].title(), vol['title']))
    y -= 26

    compact = len(entries) > 14
    rh = 30 if not compact else 24
    for num, title, start in entries:
        c.setFillColor(PNL2 if num % 2 == 0 else PNL)
        c.roundRect(MX, y - rh + 4, CW, rh - 3, radius=3, fill=1, stroke=0)
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 11 if not compact else 10)
        c.drawString(MX + 10, y - rh + 15 if not compact else y - rh + 12, '%02d' % num)
        c.setFillColor(CREAM)
        c.setFont('Helvetica-Bold', 10.5 if not compact else 9.5)
        c.drawString(MX + 36, y - rh + (16 if not compact else 12), title)
        if not compact:
            c.setFillColor(MGR)
            c.setFont('Helvetica', 8.5)
            c.drawString(MX + 36, y - rh + 5, BLURB.get(num, ''))
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 9)
        c.drawRightString(W - MX - 10, y - rh + (15 if not compact else 12), 'p.%d' % start)
        y -= rh

    # How to use this volume
    y -= 12
    if y > 120:
        lines = ['Each guide is self-contained — start anywhere. Guides are ordered',
                 'easiest to hardest, so reading front to back builds on itself.',
                 'Every guide ends with a one-page cheat sheet you can print.']
        ph = len(lines) * 16 + 46
        c.setFillColor(PNL)
        c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 12, y - 24, 'HOW TO USE THIS VOLUME')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        ty = y - 42
        for line in lines:
            c.drawString(MX + 12, ty, line)
            ty -= 16

    _state['label'] = 'Claude AI Field Guide Series  ·  %s' % vol['title']
    vol_ftr(c)
    c.showPage()


def build_volume(vol):
    mods = {}
    for g in vol['guides']:
        mods[g] = importlib.import_module('build_guide%02d' % g)
    titles = [(g, mods[g].GUIDE) for g in vol['guides']]

    total_pages = 2 + 6 * len(vol['guides'])
    entries = []
    p = 3
    for g in vol['guides']:
        entries.append((g, mods[g].GUIDE, p))
        p += 6

    out = os.path.join(OUTDIR, vol['file'])
    c = canvas.Canvas(out, pagesize=LETTER)
    c.setTitle('Claude AI Field Guide — %s' % vol['title'])
    c.setAuthor('Claude AI Field Guide Series')
    c.setSubject(vol['sub'])

    _state['p'] = 1
    volume_cover(c, vol, titles, total_pages)
    _state['p'] = 2
    contents_page(c, vol, entries)

    p = 3
    for g in vol['guides']:
        m = mods[g]
        m.ftr = make_ftr()
        _state['label'] = 'Guide %02d  ·  %s' % (g, m.GUIDE)
        for fn in (m.cover, m.page2, m.page3, m.page4, m.page5, m.page6):
            _state['p'] = p
            fn(c)
            p += 1

    c.save()
    return out, p - 1


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    for vol in VOLUMES:
        out, pages = build_volume(vol)
        print('%-6s %-52s %3d pages' % (vol['key'], os.path.basename(out), pages))


if __name__ == '__main__':
    main()
