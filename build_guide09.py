#!/usr/bin/env python3
"""Guide 09: VS Code Setup for Claude — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_09_VSCode.pdf'
GUIDE = 'VS Code Setup for Claude'

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
DBAMB   = HexColor('#2B1A00')
CODE_BG = HexColor('#0A0A15')


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

def info_panel(c, x, y, heading, lines, w):
    pad = 12; ph = len(lines) * 16 + pad * 2 + 22
    c.setFillColor(PNL); c.roundRect(x, y - ph, w, ph, radius=4, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(x + pad, y - pad - 12, heading)
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ty = y - pad - 30
    for line in lines:
        c.drawString(x + pad, ty, line); ty -= 16
    return y - ph

def code_block(c, x, y, lines, w):
    pad = 10; lh = 14
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODE_BG); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG); c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
    ty = y - pad - 10
    for line in lines:
        col = MGR if line.startswith('//') or line.startswith('#') else (OGL if line.startswith('"') else GRN)
        c.setFillColor(col); c.setFont('Courier', 10)
        c.drawString(x + pad, ty, line); ty -= lh
    return y - bh

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
    bw, bh2 = c.stringWidth('GUIDE 09 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 09 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'VS Code Setup')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'The Perfect Development Environment for Claude')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Download and install VS Code (free) on Mac, Windows, or Linux',
        'Tour the VS Code interface — every panel and shortcut explained',
        'Install the official Claude Code extension by Anthropic',
        'Set up 4 essential companion extensions: GitLens, ESLint, Prettier, Error Lens',
        'Configure settings.json for a clean, productive coding environment',
        'Keyboard shortcuts that save hours every week',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Free & open source  •  Mac, Windows & Linux  •  Requires VS Code 1.98+')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Why VS Code ───────────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Why VS Code Is the Best Editor for Claude Work')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('VS Code (Visual Studio Code) is a free, open-source code editor from Microsoft. '
             "It's the world's most popular development environment and the officially "
             'recommended editor for Claude Code. The Claude Code extension brings '
             'AI assistance directly into your editor, showing diffs inline and '
             'reading whichever file you have open.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('Install VS Code',       'Download and set up in under 5 minutes'),
        ('Interface tour',        'Explorer, Terminal, Source Control, Extensions panels'),
        ('Claude Code extension', 'The official Anthropic extension — how it works'),
        ('Key extensions',        'GitLens, ESLint, Prettier, Error Lens'),
        ('settings.json basics',  'The 10 settings that matter most'),
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
        'Anyone who wants to use Claude Code with a proper development environment',
        'Beginners who have never used a code editor before',
        'People who write code occasionally and want Claude to help',
        'Developers switching to VS Code from another editor',
    ]
    for item in audience:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Before You Start — What You Need', [
        'A computer running Mac, Windows, or Linux',
        'VS Code 1.98.0 or higher (required by the Claude Code extension)',
        'Node.js installed (covered in Guide 06) — needed for Claude Code CLI',
        'An Anthropic account (free) to authenticate Claude Code',
    ], CW)
    c.showPage()


# ── Page 3: Install & Interface Tour ─────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing VS Code & Interface Tour')

    steps = [
        ('Download VS Code', [
            'Go to code.visualstudio.com and click "Download for [your OS]".',
            'The download is free, under 100 MB, and works on all platforms.',
        ]),
        ('Install It', [
            'Mac: drag VS Code to the Applications folder and open it.',
            'Windows: run the installer — accept the defaults.',
            'Linux: use the .deb / .rpm package or snap install code.',
        ]),
        ('Open a Folder (Your Project)', [
            'File → Open Folder → select your project directory.',
            'VS Code treats the folder as your "workspace".',
        ]),
        ('Open the Integrated Terminal', [
            'Press Ctrl+` (backtick) or Terminal → New Terminal.',
            'This terminal opens in your project folder automatically.',
            'All your git and npm commands run here.',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    # Interface tour
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Interface Panel Tour')
    y -= 14
    panels = [
        ('Activity Bar',      'Left edge. Icons for Explorer, Search, Source Control, Extensions, Claude.'),
        ('Explorer (Ctrl+Shift+E)', 'File tree of your open folder. Click files to open them.'),
        ('Editor Area',       'Center. Open files as tabs. Split into multiple columns.'),
        ('Source Control (Ctrl+Shift+G)', 'Git integration — stage, commit, push without the terminal.'),
        ('Terminal (Ctrl+`)', 'Bottom. Run any command in your project directory.'),
        ('Status Bar',        'Bottom edge. Shows branch name, errors, line/column number.'),
    ]
    for name, desc in panels:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, name)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 190, y, '—  ' + desc[:70])
        y -= 17

    y -= 4
    tip_lines = wrap(
        'Press Ctrl+Shift+P (Cmd+Shift+P on Mac) to open the Command Palette — '
        'type any action name to run it. This is the most powerful shortcut in VS Code.',
        10, CW - 28)
    tip_box(c, MX, y, 'The Command Palette: Your Swiss Army Knife', tip_lines, CW)
    c.showPage()


# ── Page 4: Extensions ────────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Essential Extensions for Claude Work')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Install each by pressing Ctrl+Shift+X and searching by name:')
    y -= 60

    extensions = [
        ('Claude Code',
         'Publisher: Anthropic',
         'The official Claude Code extension. Brings Claude into VS Code with inline diff '
         'views, context-aware prompting, and file-aware conversations. Requires VS Code 1.98+.',
         True),
        ('GitLens',
         'Publisher: GitKraken',
         'Shows who changed each line (git blame), full commit history per file, and '
         'visual branch comparisons. Makes git history searchable and readable.',
         False),
        ('ESLint',
         'Publisher: Microsoft',
         'Highlights JavaScript/TypeScript errors and style issues as you type, '
         'based on your project\'s lint rules. Catches bugs before Claude does.',
         False),
        ('Prettier',
         'Publisher: Prettier',
         'Auto-formats your code on save — consistent indentation, quotes, and spacing '
         'across all files. Eliminates all style debates in code review.',
         False),
        ('Error Lens',
         'Publisher: Alexander',
         'Shows error and warning messages inline on the same line where they occur, '
         'instead of requiring you to hover. Makes problems impossible to miss.',
         False),
    ]

    for i, (name, publisher, desc, is_primary) in enumerate(extensions):
        card_h = 72
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        if is_primary:
            c.setFillColor(OG); c.rect(MX, y - card_h, 4, card_h, fill=1, stroke=0)

        c.setFillColor(OGL if is_primary else CREAM)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 14, y - 16, name)
        c.setFillColor(MGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 14, y - 30, publisher)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        dl = wrap(desc, 10, CW - 28)
        dy = y - 45
        for dl_line in dl[:2]:
            c.drawString(MX + 14, dy, dl_line); dy -= 15
        y -= card_h + 6

    tip_lines = wrap(
        'To install all 5 at once, open the Command Palette (Ctrl+Shift+P), '
        'type "Extensions: Install Extensions" and search each name. Takes under 2 minutes total.',
        10, CW - 28)
    tip_box(c, MX, y, 'Install All 5 in Under 2 Minutes', tip_lines, CW)
    c.showPage()


# ── Page 5: Settings & Claude Code Extension ──────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Settings & Claude Code in VS Code')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Recommended settings.json Settings')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Open with: Ctrl+Shift+P → "Open User Settings (JSON)":')
    y -= 14
    y = code_block(c, MX, y, [
        '{',
        '  "editor.formatOnSave": true,',
        '  "editor.defaultFormatter": "esbenp.prettier-vscode",',
        '  "editor.fontSize": 14,',
        '  "editor.tabSize": 2,',
        '  "editor.wordWrap": "on",',
        '  "terminal.integrated.fontSize": 13,',
        '  "files.autoSave": "afterDelay",',
        '  "git.confirmSync": false,',
        '  "editor.minimap.enabled": false',
        '}',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'How the Claude Code Extension Works in VS Code')
    y -= 18

    features = [
        ('Automatic file context',
         'Claude knows which file you have open — no need to copy and paste code.',
         'Just ask: "Explain this function" and Claude reads the current file.'),
        ('Text selection as context',
         'Select any code, then type your question in the Claude panel.',
         'The selected text is automatically included in Claude\'s context.'),
        ('Inline diff views',
         'When Claude edits a file, VS Code shows the change as a diff.',
         'You see exactly what will be added or removed before accepting.'),
        ('Integrated terminal commands',
         'Claude can suggest terminal commands and run them with your approval.',
         'Results feed back into the conversation automatically.'),
    ]

    for title, line1, line2 in features:
        card_h = 62
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + 8, y - 36, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(MX + 18, y - 29, str(features.index((title, line1, line2)) + 1))
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 34, y - 16, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 34, y - 30, line1)
        c.setFillColor(MGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 34, y - 44, line2)
        y -= card_h + 6

    tip_lines = wrap(
        'The Claude Code extension works best when you open a folder (not just a file). '
        'With a folder open, Claude has context about your full project structure.',
        10, CW - 28)
    tip_box(c, MX, y, 'Always Open a Folder, Not Just a File', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — VS Code for Claude')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Command Palette',         'Ctrl+Shift+P  /  Cmd+Shift+P'),
        ('Open Terminal',           'Ctrl+`  (backtick)'),
        ('Explorer panel',          'Ctrl+Shift+E'),
        ('Extensions panel',        'Ctrl+Shift+X'),
        ('Source Control / Git',    'Ctrl+Shift+G'),
        ('Open Settings (JSON)',    'Ctrl+Shift+P → "Open User Settings (JSON)"'),
        ('Format file (Prettier)',  'Shift+Alt+F  /  Shift+Option+F'),
        ('Open Claude panel',       'Click Claude icon in Activity Bar'),
    ]
    url_items = [
        ('Download VS Code',   'code.visualstudio.com'),
        ('Min version',        'VS Code 1.98.0 (for Claude Code extension)'),
        ('Claude extension',   'Marketplace: search "Claude Code" by Anthropic'),
        ('GitLens',            'Marketplace: search "GitLens" by GitKraken'),
        ('ESLint',             'Marketplace: search "ESLint" by Microsoft'),
        ('Prettier',           'Marketplace: search "Prettier - Code formatter"'),
        ('Error Lens',         'Marketplace: search "Error Lens" by Alexander'),
        ('VS Code docs',       'code.visualstudio.com/docs'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Shortcuts', left_items),
        (MX + cw2 + 10, 'Links & Resources', url_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL); c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(px + 10, iy, a)
            c.setFillColor(GRN if px == MX else OGL)
            c.setFont('Courier' if px == MX else 'Helvetica', 9)
            c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Issues & Quick Fixes')
    y -= 8
    t_rows = [
        ['Claude extension not showing',    'Ensure VS Code is version 1.98+ — Help → About to check'],
        ['Prettier not formatting on save',  'Check settings.json has "editor.formatOnSave": true'],
        ['Terminal not opening',             'View → Terminal, or reinstall VS Code if the shortcut fails'],
        ['Git not detected',                 'Open a folder containing a .git directory first'],
        ['Extension install failed',         'Check internet connection; try Ctrl+Shift+P → Reload Window'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [172, CW - 172])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 10 — Claude Code in VS Code')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 09 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
