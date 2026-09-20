#!/usr/bin/env python3
"""Start Here: Your Claude AI Learning Roadmap — free lead magnet / library index."""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_00_Start_Here.pdf'
GUIDE = 'Start Here — Learning Roadmap'

BG      = HexColor('#0F0F1A')
OG      = HexColor('#E07A38')
OGL     = HexColor('#F5A66B')
CREAM   = HexColor('#F5F0E8')
LGR     = HexColor('#D4CFC7')
MGR     = HexColor('#9B9690')
PNL     = HexColor('#1C1C2E')
PNL2    = HexColor('#161625')
GRN     = HexColor('#5CB85C')
AMB     = HexColor('#F59E0B')
WHT     = HexColor('#FFFFFF')
DOG     = HexColor('#C86820')
DDOG    = HexColor('#B85C18')
DBGRN   = HexColor('#0D2B0D')
CODE_BG = HexColor('#0A0A15')
PUR     = HexColor('#8B5CF6')


def wrap(text, size, width, font='Helvetica'):
    return simpleSplit(text, font, size, width)

def pg_bg(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)

def hdr(c):
    c.setFillColor(OG); c.rect(0, H - 6, W, 6, fill=1, stroke=0)

def ftr(c, n):
    c.setFillColor(PNL); c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica', 8)
    c.drawString(MX, 7, f'Claude AI Field Guide Series  ·  {GUIDE}')
    c.setFillColor(MGR); c.drawRightString(W - MX, 7, f'Page {n}')

def tbl(c, x, y, headers, rows, col_w):
    rh, pad = 22, 7; tw = sum(col_w)
    c.setFillColor(OG); c.rect(x, y - rh, tw, rh, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    cx = x
    for i, h in enumerate(headers):
        c.drawString(cx + pad, y - rh + 7, h); cx += col_w[i]
    for ri, row in enumerate(rows):
        ry = y - rh * (ri + 2)
        c.setFillColor(PNL2 if ri % 2 == 0 else PNL); c.rect(x, ry, tw, rh, fill=1, stroke=0)
        cx = x
        for ci, cell in enumerate(row):
            c.setFillColor(OGL if ci == 0 else LGR)
            c.setFont('Helvetica-Bold' if ci == 0 else 'Helvetica', 9)
            c.drawString(cx + pad, ry + 7, str(cell)); cx += col_w[ci]
    return y - rh * (len(rows) + 1)


# ── Page 1: Welcome + Choose Your Path ────────────────────────────────────────

# SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
# and spliced in by rebuild_covers.py. This function is retained so a from-source
# rebuild still produces a complete document; run rebuild_covers.py afterwards.
def page1(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    # Derived, never hardcoded — a fixed width with centred text spills out both sides.
    bw, bh2 = c.stringWidth('FREE ROADMAP  ·  START HERE', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'FREE ROADMAP  ·  START HERE')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 30)
    c.drawString(MX, H - 176, 'Start Here')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Your Map to the Complete Claude AI Field Guide Library')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 214, W - MX, H - 214)

    y = H - 234
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('This library is 23 plain-English guides covering every way to use Claude AI — '
             'from your first chat to orchestrating fleets of agents. You do not need to read '
             'them in order. Pick the path that matches where you are today, and follow the '
             'arrows. Each guide is a standalone 6-page PDF you can finish in one sitting.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 12

    c.setFillColor(OG); c.setFont('Helvetica-Bold', 14)
    c.drawString(MX, y, 'Choose Your Path'); y -= 22

    paths = [
        (GRN, 'NEW TO CLAUDE', 'I just want to use Claude well.',
         'Start: Volume 1 (Guides 1-5) — web, mobile, desktop, Chrome, integrations.',
         'Then: Guide 20 (Prompting) to get dramatically better answers.'),
        (OG, 'ASPIRING DEVELOPER', 'I want to set up the coding tools.',
         'Start: Volume 2 (Guides 6-9) — Node.js, Git, Docker, VS Code.',
         'Then: Guide 10 (Claude Code) to start building with an AI pair.'),
        (PUR, 'CLAUDE CODE USER', 'I code with Claude and want to go deeper.',
         'Start: Volumes 3-4 (Guides 10-17) — Claude Code, hooks, MCP, skills.',
         'Then: Guide 21 (Orchestration) to run many agents at once.'),
        (AMB, 'BUILDER / POWER USER', 'I am shipping automations and agents.',
         'Start: Volume 5 (Guides 18-19) — the API and automations.',
         'Then: Volume 6 (Guides 21-22) — orchestration and evaluation.'),
    ]
    for accent, tag, who, l1, l2 in paths:
        ph = 74
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=5, fill=1, stroke=0)
        c.setFillColor(accent); c.rect(MX, y - ph, 5, ph, fill=1, stroke=0)
        c.setFillColor(accent); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 16, y - 18, tag)
        c.setFillColor(MGR); c.setFont('Helvetica-Oblique', 9); c.drawString(MX + 150, y - 18, who)
        c.setFillColor(CREAM); c.setFont('Helvetica', 9); c.drawString(MX + 16, y - 38, l1)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 16, y - 54, l2)
        y -= ph + 8

    c.setFillColor(OG); c.rect(0, 0, W, 32, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 11, 'Turn the page for the complete library map  →')
    c.showPage()


# ── Page 2: Complete library map + bundles ────────────────────────────────────

def vol_block(c, x, y, title, guides, w):
    """Draw a volume header + its guide list. Returns new y."""
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(x, y, title); y -= 6
    c.setStrokeColor(HexColor('#3A2A1A')); c.setLineWidth(0.5)
    c.line(x, y, x + w, y); y -= 14
    for num, name in guides:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(x, y, num)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(x + 22, y, name)
        y -= 15
    return y - 8

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The Complete Library Map')
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX, y - 36, '23 guides across 6 volumes. This roadmap is free. The guides are sold as volumes, or as one complete library.')
    y -= 56

    colw = (CW - 20) / 2
    lx, rx = MX, MX + colw + 20
    ly = ry = y

    ly = vol_block(c, lx, ly, 'VOLUME 1 — Getting Into Claude', [
        ('01', 'Claude on the Web (claude.ai)'),
        ('02', 'Claude Mobile App (iOS & Android)'),
        ('03', 'Claude Desktop App (Mac & Windows)'),
        ('04', 'Claude in Chrome (Extension)'),
        ('05', 'Claude Integrations (Slack, Excel...)'),
    ], colw)
    ly = vol_block(c, lx, ly, 'VOLUME 2 — Developer Setup', [
        ('06', 'Installing Node.js'),
        ('07', 'Git & GitHub for Claude Users'),
        ('08', 'Docker Basics for AI Projects'),
        ('09', 'VS Code Setup for Claude'),
    ], colw)
    ly = vol_block(c, lx, ly, 'VOLUME 3 — Claude Code & Agents', [
        ('10', 'Claude Code in VS Code'),
        ('11', 'CLAUDE.md Files That Work'),
        ('12', 'Subagents & Hooks'),
        ('13', 'How Agentic Loops Work'),
    ], colw)

    ry = vol_block(c, rx, ry, 'VOLUME 4 — MCP, Plugins & Skills', [
        ('14', 'MCP Servers 101'),
        ('15', 'Installing & Using MCP Servers'),
        ('16', 'Claude Plugins Guide'),
        ('17', 'Claude Skills — Create Your Own'),
    ], colw)
    ry = vol_block(c, rx, ry, 'VOLUME 5 — Automation & API', [
        ('18', 'Claude API Basics'),
        ('19', 'Building Automations with Claude'),
        ('20', 'Prompting Masterclass'),
    ], colw)
    ry = vol_block(c, rx, ry, 'VOLUME 6 — Advanced Add-Ons', [
        ('21', 'Multi-Agent Orchestration'),
        ('22', 'Evaluating & Testing Claude Agents'),
        ('23', 'Claude Cost & Token Management'),
        ('..', 'More advanced guides in progress'),
    ], colw)

    y = min(ly, ry) - 4
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'What You Can Buy')
    y -= 6
    # Prices must match what is actually listed. This table previously advertised a
    # "$79 Complete Library, Guides 01-20" that has never existed at that price or that
    # scope — a free lead magnet quoting the wrong price is worse than no lead magnet.
    rows = [
        ['Volume 1', '01-05', 'Getting into Claude — no coding needed', '$9.99'],
        ['Volume 2', '06-09', 'Developer setup: Node, Git, Docker, VS Code', '$9.99'],
        ['Volume 3', '10-13', 'Claude Code, CLAUDE.md, hooks, agentic loops', '$12.99'],
        ['Volume 4', '14-17', 'MCP servers, plugins and skills', '$12.99'],
        ['Volume 5', '18-20', 'The API, automations and prompting', '$9.99'],
        ['Volume 6', '21-23', 'Orchestration, evaluation, cost control', '$9.99'],
        ['Complete Library', 'All 23', 'Everything above — 140 pages, one PDF', '$29.99'],
    ]
    y = tbl(c, MX, y, ['Product', 'Guides', 'What it covers', 'Price'],
            rows, [100, 58, 280, CW - 438])
    y -= 14

    c.setFillColor(MGR); c.setFont('Helvetica', 8.5)
    c.drawString(MX, y, 'Also available: Prompt Vault (200 prompts) · Cheat Sheet Pack '
                        '(12 printables) · AI Cost Calculator · Claude Code Config Pack')
    y -= 20

    cta_h = 62
    c.setFillColor(OG); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 13)
    c.drawCentredString(W / 2, y - 22, 'Pick your path and start today')
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(W / 2, y - 41, 'etsy.com/shop/FranksMarketDesigns')
    c.setFillColor(CREAM); c.setFont('Helvetica', 9)
    c.drawCentredString(W / 2, y - 55, 'The Claude AI Field Guide Series  ·  Updated for 2026')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle('Claude AI Field Guide — Start Here Roadmap')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Free library roadmap and index')
    page1(cv); page2(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
