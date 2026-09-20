#!/usr/bin/env python3
"""Guide 03: Claude Desktop App (Mac & Windows) — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_03_Desktop.pdf'
GUIDE = 'Claude Desktop App'

BG    = HexColor('#0F0F1A')
OG    = HexColor('#E07A38')
OGL   = HexColor('#F5A66B')
CREAM = HexColor('#F5F0E8')
LGR   = HexColor('#D4CFC7')
MGR   = HexColor('#9B9690')
PNL   = HexColor('#1C1C2E')
PNL2  = HexColor('#161625')
GRN   = HexColor('#5CB85C')
AMB   = HexColor('#F59E0B')
WHT   = HexColor('#FFFFFF')
DOG   = HexColor('#C86820')
DDOG  = HexColor('#B85C18')
DBGRN = HexColor('#0D2B0D')
DBAMB = HexColor('#2B1A00')


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

def step_card(c, x, y, num, title, lines, w):
    pad, badge = 10, 26
    card_h = 48 + len(lines) * 15
    c.setFillColor(PNL); c.roundRect(x, y - card_h, w, card_h, radius=4, fill=1, stroke=0)
    c.setFillColor(OG); c.roundRect(x + pad, y - pad - badge, badge, badge, radius=3, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(x + pad + badge / 2, y - pad - badge + 7, str(num))
    tx = x + pad + badge + 8
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 11); c.drawString(tx, y - pad - 12, title)
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    by = y - pad - 28
    for line in lines:
        c.drawString(tx, by, line); by -= 15
    return y - card_h

def tip_box(c, x, y, heading, lines, w):
    pad = 10; bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBGRN); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(GRN); c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(GRN); c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, f'TIP  {heading}')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ty = y - pad - 26
    for line in lines:
        c.drawString(x + 14, ty, line); ty -= 15
    return y - bh

def warn_box(c, x, y, heading, lines, w):
    pad = 10; bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBAMB); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(AMB); c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(AMB); c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, f'NOTE  {heading}')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ty = y - pad - 26
    for line in lines:
        c.drawString(x + 14, ty, line); ty -= 15
    return y - bh

def info_panel(c, x, y, heading, lines, w):
    pad = 12; ph = len(lines) * 16 + pad * 2 + 22
    c.setFillColor(PNL); c.roundRect(x, y - ph, w, ph, radius=4, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(x + pad, y - pad - 12, heading)
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ty = y - pad - 30
    for line in lines:
        c.drawString(x + pad, ty, line); ty -= 16
    return y - ph

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


# ── Cover ─────────────────────────────────────────────────────────────────────

def cover(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    bw, bh2 = c.stringWidth('GUIDE 03 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 03 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude Desktop App')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Your Complete Guide for Mac & Windows')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Download and install on Mac (Big Sur+) or Windows 10+',
        'Tour the redesigned 2026 interface — sessions, panels, sidebar',
        'Access local files directly — no manual uploads needed',
        'Install one-click MCP extensions for Google Drive, Slack & more',
        'Use Cowork to run code in an isolated desktop sandbox',
        'Desktop vs web comparison and keyboard shortcuts cheat sheet',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires: macOS 11 Big Sur+ or Windows 10+  •  Free download at claude.ai/download')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Why This Matters ──────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Why This Matters')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('The Claude desktop app goes further than the browser version. It was '
             'redesigned in April 2026 with a developer-grade interface: parallel '
             'sessions, a built-in terminal, file editor, diff viewer, and one-click '
             'MCP extensions — all in a native app on Mac or Windows.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('Download & install',     'Get the app running on Mac or Windows in minutes'),
        ('Interface tour',         'Sessions sidebar, panels, terminal, diff viewer'),
        ('Local file access',      'Work with files on your computer without uploading'),
        ('MCP extensions',         'One-click connectors for Drive, Slack, and more'),
        ('Cowork / code sandbox',  'Run code locally in an isolated virtual machine'),
    ]
    for title, desc in learns:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 10, y, f'▸  {title}')
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        c.drawString(MX + 168, y, f'— {desc}')
        y -= 18
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Who This Is For')
    y -= 22
    audience = [
        'Anyone who uses claude.ai and wants a faster, native experience',
        'Developers who want Claude alongside their code editor and terminal',
        'Writers and analysts who want to work with local files without uploading',
        'Power users who want MCP extensions and multi-session workflows',
    ]
    for item in audience:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Before You Start — What You Need', [
        'Mac: macOS 11 Big Sur or later (Apple Silicon and Intel supported)',
        'Windows: Windows 10 or later (64-bit)',
        'Anthropic account (free) — create one at claude.ai if needed',
        'An internet connection for download and ongoing Claude access',
    ], CW)
    c.showPage()


# ── Page 3: Download & Install ────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Downloading & Installing')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Installation takes under 2 minutes on either platform:')
    steps = [
        ('Go to the Download Page', [
            'Open your browser and visit claude.ai/download.',
            'The page auto-detects your OS — Mac or Windows.',
        ]),
        ('Download the Installer', [
            'Mac: click "Download for Mac" — gets you a .dmg file.',
            'Windows: click "Download for Windows" — gets you a .exe installer.',
            'File size is roughly 100–150 MB.',
        ]),
        ('Install the App', [
            'Mac: open the .dmg, drag Claude to Applications, then open it.',
            'Windows: run the .exe installer and follow the prompts.',
            'macOS may ask you to confirm opening an app from the internet — click Open.',
        ]),
        ('Sign In', [
            'The app opens to a sign-in screen.',
            'Click "Continue with Google" or "Continue with Apple" for fastest login.',
            'Or enter your Anthropic email and password.',
        ]),
        ('Set Up Your Workspace', [
            'The app opens with the Sessions sidebar on the left.',
            'Your existing Projects and conversations sync from the web automatically.',
            'Set a global keyboard shortcut under Settings → Keyboard Shortcut.',
        ]),
    ]
    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6
    tip_lines = wrap(
        'On Mac, set a system-wide keyboard shortcut (e.g. Cmd+Shift+Space) to '
        'open Claude from any app instantly — no click needed.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Always-Available Shortcut', tip_lines, CW)
    c.showPage()


# ── Page 4: Interface Tour ────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Interface Tour — The 2026 Desktop App')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'The April 2026 redesign introduced a developer-grade multi-panel layout:')
    y -= 58

    panels = [
        ('Sessions Sidebar',
         'Left panel. Shows all active and recent sessions. Filter by status, '
         'Project, or environment. Run multiple sessions in parallel.'),
        ('Chat Panel',
         'Center panel. Your conversation with Claude. Drag to resize. '
         'Supports text, file drops, and Artifact previews inline.'),
        ('Integrated Terminal',
         'Bottom panel (toggle). Run tests, builds, and shell commands without '
         'leaving the app. Output appears directly in the session.'),
        ('File Editor',
         'Right panel (toggle). Make spot edits to local files. Claude can '
         'suggest edits and you apply them with one click.'),
        ('Diff Viewer',
         'Appears when Claude modifies files. Shows before/after with '
         'line-level highlighting — optimised for large changesets.'),
        ('Preview Pane',
         'Renders HTML files, PDFs, and live local app servers. '
         'See your changes without switching to a browser.'),
    ]

    cw2 = (CW - 10) / 2
    row_y = y
    card_h = 60
    for i, (title, desc) in enumerate(panels):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + 8
        cx = MX + col * (cw2 + 10)
        c.setFillColor(PNL); c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(cx + 8, row_y - 38, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(cx + 18, row_y - 31, str(i + 1))
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10)
        c.drawString(cx + 34, row_y - 17, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        desc_lines = wrap(desc, 9, cw2 - 44)
        dy = row_y - 31
        for dl in desc_lines[:2]:
            c.drawString(cx + 34, dy, dl); dy -= 13

    y = row_y - card_h - 16

    # Desktop vs Web comparison
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Desktop App vs Web Browser — Key Differences')
    y -= 8
    t_rows = [
        ['Local file access',    'Direct — no upload needed', 'Upload required'],
        ['MCP extensions',       'One-click install in-app',  'Configure via settings.json'],
        ['Terminal',             'Built in',                  'None'],
        ['Parallel sessions',    'Yes — side by side',        'One tab at a time'],
        ['Global shortcut',      'System-wide hotkey',        'Must switch to browser'],
        ['Offline use',          'No (needs internet)',        'No (needs internet)'],
    ]
    y = tbl(c, MX, y, ['Feature', 'Desktop App', 'Web (claude.ai)'],
            t_rows, [140, 170, CW - 310])

    y -= 12
    tip_lines = wrap(
        'All panels are drag-and-drop resizable. Arrange them to match your workflow — '
        'terminal at the bottom, file editor on the right, chat in the center.',
        10, CW - 28)
    tip_box(c, MX, y, 'Customise Your Layout', tip_lines, CW)
    c.showPage()


# ── Page 5: MCP Extensions & Cowork ──────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'MCP Extensions & Local Cowork')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'One-Click MCP Extensions')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ext_intro = ('MCP (Model Context Protocol) extensions give Claude access to your '
                 'external tools and data. In the desktop app, you can browse and '
                 'install verified extensions with a single click — no config files needed.')
    for line in wrap(ext_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    exts = [
        ('Google Drive',   'Read and write Docs, Sheets, and Slides in your Drive'),
        ('Slack',          'Read channel history, search messages, and post replies'),
        ('GitHub',         'Browse repos, read files, create PRs and issues'),
        ('Filesystem',     'Read and write local files in folders you approve'),
        ('Linear',         'Read issues, update status, create new tickets'),
        ('Notion',         'Read and edit pages and databases in your workspace'),
    ]
    y = tbl(c, MX, y, ['Extension', 'What Claude Can Do'], exts, [100, CW - 100])
    y -= 10

    info_panel(c, MX, y, 'How to Install an Extension', [
        '1. Open Claude Desktop and click Extensions in the left sidebar.',
        '2. Browse the verified extension list or search by name.',
        '3. Click Install next to the extension you want.',
        '4. Authorise access when prompted (e.g. Google OAuth for Drive).',
        '5. Claude can now use that tool — mention it in your conversation.',
    ], CW)
    y -= 130

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Cowork — Run Code in a Desktop Sandbox')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    cowork_intro = ('Cowork lets Claude execute code on your computer inside an isolated '
                    'virtual machine. Claude can read and write files only in the folders '
                    'you explicitly connect — nothing else on your machine is accessible.')
    for line in wrap(cowork_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    uses = [
        'Organise and rename hundreds of files in one folder',
        'Generate a report from a local CSV or Excel file',
        'Run a Python or Node.js script and show you the output',
        'Resize or convert a batch of images',
        'Synthesise research from multiple local documents',
    ]
    for item in uses:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, y, item)
        y -= 17
    y -= 6

    warn_lines = wrap(
        'Cowork only has access to folders you explicitly connect. '
        'It cannot read your desktop, Documents, or any other location unless you grant it. '
        'Review what you share before connecting a folder.',
        10, CW - 28)
    warn_box(c, MX, y, 'Cowork Access Is Limited to What You Share', warn_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Desktop App')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Open new session',        'Click + in Sessions sidebar'),
        ('Global open shortcut',    'Settings → Keyboard Shortcut (set your own)'),
        ('Open file editor',        'View menu → Show File Editor'),
        ('Open terminal',           'View menu → Show Terminal'),
        ('Install MCP extension',   'Sidebar → Extensions → Browse → Install'),
        ('Connect folder (Cowork)', 'Settings → Cowork → Add Folder'),
        ('Switch model',            'Model dropdown at top of chat panel'),
        ('Open Settings',           'Top menu → Claude → Preferences'),
    ]
    right_items = [
        ('Download page',     'claude.ai/download'),
        ('macOS requirement', 'macOS 11 Big Sur or later'),
        ('Windows req.',      'Windows 10 64-bit or later'),
        ('Extensions list',   'In-app: Sidebar → Extensions'),
        ('Help center',       'support.anthropic.com'),
        ('Release notes',     'claude.ai/release-notes'),
        ('Web version',       'claude.ai (syncs automatically)'),
        ('Status page',       'status.anthropic.com'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Actions', left_items),
        (MX + cw2 + 10, 'Key Info & Links', right_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL); c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(px + 10, iy, a)
            c.setFillColor(MGR if px == MX else OGL)
            c.setFont('Helvetica', 9); c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Issues & Quick Fixes')
    y -= 8

    t_rows = [
        ['App won\'t open (Mac)',    'Right-click → Open to bypass Gatekeeper on first launch'],
        ['Sessions not syncing',    'Check internet connection and sign out then back in'],
        ['Extension not working',   'Re-authorise the extension from Sidebar → Extensions'],
        ['Terminal not appearing',  'View menu → Show Terminal, or drag the divider up'],
        ['Cowork won\'t run code',  'Check Settings → Cowork and verify the folder is connected'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Solution'], t_rows, [160, CW - 160])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 04 — Claude in Chrome (Browser Extension)')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 03 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
