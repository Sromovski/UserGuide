#!/usr/bin/env python3
"""Guide 06: Installing Node.js — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_06_NodeJS.pdf'
GUIDE = 'Installing Node.js'

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

def code_block(c, x, y, lines, w):
    """Monospace code block. Returns bottom y."""
    pad = 10; lh = 14
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODE_BG); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG); c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
    c.setFillColor(GRN); c.setFont('Courier', 10)
    ty = y - pad - 10
    for line in lines:
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

# SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
# and spliced in by rebuild_covers.py. This function is retained so a from-source
# rebuild still produces a complete document; run rebuild_covers.py afterwards.
def cover(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    bw, bh2 = c.stringWidth('GUIDE 06 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 06 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Installing Node.js')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'The First Step for Every Claude Developer')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What Node.js is — explained in plain English (no jargon)',
        'Why you need it to use Claude Code and the Anthropic API',
        'Install Node.js LTS on Mac, Windows, and Linux step by step',
        'Use nvm / nvm-windows to manage multiple Node.js versions',
        'Verify your install with node -v and npm -v',
        'Common errors and how to fix PATH and version conflicts',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'No coding experience needed  •  Mac, Windows & Linux  •  Free & open source')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Why This Matters ──────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is Node.js and Why Do You Need It?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Node.js lets you run JavaScript code on your computer — outside of a browser. '
             'Think of it like a runtime engine that powers command-line tools. Claude Code '
             '(the CLI), the Anthropic SDK, and most AI developer tools require Node.js '
             'to be installed before they work. You do not need to write JavaScript.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'A Plain-English Analogy', [
        'Node.js is like a car engine. You do not need to understand how an engine works',
        'to drive a car — you just need one installed. Claude Code and the Anthropic SDK',
        'are the car. Node.js is the engine underneath. Install it once, forget about it.',
    ], CW)
    y -= 78

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('LTS vs Current',       'Which version to install and why LTS is the safe choice'),
        ('Direct vs nvm install', 'When to use the simple installer vs the version manager'),
        ('Mac install',          'Homebrew + nvm — the recommended approach'),
        ('Windows install',      'Official installer or nvm-windows'),
        ('Linux install',        'apt / nvm — works on Ubuntu, Debian and WSL'),
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
        'Complete beginners who have never used a command line before',
        'Anyone setting up Claude Code (the CLI) for the first time',
        'Developers coming from Python or other languages installing Node for the first time',
        'Anyone who sees "node: command not found" and wants to fix it',
    ]
    for item in audience:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Versions to Know (June 2026)', [
        'Node.js 24 — Active LTS (Long-Term Support). Recommended for most users.',
        'Node.js 26 — Current release. Newer, but not yet LTS. For early adopters.',
        'Node.js 22 — Maintenance LTS. Still supported but will be retired in 2027.',
        'Rule: always install LTS unless you have a specific reason to use Current.',
    ], CW)
    c.showPage()


# ── Page 3: Mac Install ───────────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing on Mac (Recommended Method: nvm)')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Open Terminal (Applications → Utilities → Terminal) and run these commands:')

    y -= 58
    y = step_card(c, MX, y, 1, 'Install Homebrew (skip if already installed)', [
        'A package manager for Mac — see brew.sh for the current install command.',
    ], CW)
    y -= 5
    # Split on a backslash continuation: as one line this ran ~50pt past the right
    # margin and off the paper. Still a single command when pasted.
    y = code_block(c, MX, y, [
        '/bin/bash -c "$(curl -fsSL \\',
        '  https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Install nvm via Homebrew', [
        'nvm (Node Version Manager) lets you switch Node.js versions easily.',
    ], CW)
    y -= 5
    y = code_block(c, MX, y, ['brew install nvm'], CW)
    y -= 6

    y = step_card(c, MX, y, 3, 'Add nvm to Your Shell Profile', [
        'Add these lines to ~/.zshrc (or ~/.bash_profile on older Macs):',
    ], CW)
    y -= 5
    y = code_block(c, MX, y, [
        'export NVM_DIR="$HOME/.nvm"',
        '[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \\. "/opt/homebrew/opt/nvm/nvm.sh"',
    ], CW)
    # Clear the block's bottom edge — at -6 this caption sat on top of the border.
    y -= 16
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX, y, 'Then restart Terminal or run: source ~/.zshrc')
    y -= 14

    y = step_card(c, MX, y, 4, 'Install Node.js LTS', [
        'This installs Node.js 24 (the current Active LTS release):',
    ], CW)
    y -= 5
    y = code_block(c, MX, y, ['nvm install lts', 'nvm use lts'], CW)
    y -= 6

    y = step_card(c, MX, y, 5, 'Verify the Install', [
        'Run these two commands — both should print a version number:',
    ], CW)
    y -= 5
    y = code_block(c, MX, y, ['node -v    # expected: v24.x.x', 'npm -v     # expected: 10.x.x or higher'], CW)
    y -= 6

    tip_lines = wrap(
        'Prefer not to use nvm? Download the LTS installer from nodejs.org and run '
        'the .pkg file.', 10, CW - 28)
    tip_box(c, MX, y, 'Simpler Mac Option: Direct Installer', tip_lines, CW)
    c.showPage()


# ── Page 4: Windows & Linux ───────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing on Windows & Linux')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Windows — Option A: Direct Installer (Easiest)')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Best if you only need one Node.js version:')
    y -= 18
    win_steps = [
        '1. Go to nodejs.org and click "Download Node.js (LTS)".',
        '2. Run the downloaded .msi installer — accept all defaults.',
        '3. Open a new PowerShell window (search "PowerShell" in Start).',
        '4. Type: node -v    →  should show v24.x.x',
        '5. Type: npm -v     →  should show 10.x.x or higher',
    ]
    for s in win_steps:
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 10, y, s); y -= 16
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Windows — Option B: nvm-windows (For Version Management)')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'nvm on Mac/Linux does NOT work on Windows — use nvm-windows instead:')
    y -= 16
    nvm_win = [
        '1. Go to github.com/coreybutler/nvm-windows and download nvm-setup.zip.',
        '2. Unzip and run nvm-setup.exe — follow the installer wizard.',
        '3. Open PowerShell as Administrator (right-click → Run as administrator).',
    ]
    for s in nvm_win:
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 10, y, s); y -= 16
    y -= 4
    y = code_block(c, MX, y, ['nvm install lts', 'nvm use lts', 'node -v'], CW)
    y -= 12

    warn_lines = wrap(
        'Always run PowerShell as Administrator when using nvm-windows. '
        'Regular PowerShell will get "access denied" errors when switching versions.',
        10, CW - 28)
    y = warn_box(c, MX, y, 'Windows: Run as Administrator', warn_lines, CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Linux (Ubuntu / Debian / WSL)')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Recommended: install nvm, then use it to get the LTS version:')
    y -= 16
    y = code_block(c, MX, y, [
        '# Install nvm',
        'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/HEAD/install.sh | bash',
        '',
        '# Restart terminal, then:',
        'nvm install lts',
        'nvm use lts',
        'node -v',
    ], CW)
    y -= 10

    tip_lines = wrap(
        'On Windows, if you use WSL (Windows Subsystem for Linux), follow the Linux '
        'instructions inside your WSL terminal — do not mix Windows and WSL Node installs.',
        10, CW - 28)
    tip_box(c, MX, y, 'WSL Users: Use the Linux Method Inside WSL', tip_lines, CW)
    c.showPage()


# ── Page 5: npm Basics & Common Errors ───────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'npm Basics & Common Errors')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'What Is npm?')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    npm_intro = ('npm (Node Package Manager) is installed automatically with Node.js. '
                 'It is the tool you use to install packages — including Claude Code. '
                 'Think of it like an app store for developer tools.')
    for line in wrap(npm_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    cmd_rows = [
        ['npm install -g @anthropic-ai/claude-code', 'Install Claude Code globally'],
        ['npm install <package>',                    'Install a package in current project'],
        ['npm install -g <package>',                 'Install a package globally (all projects)'],
        ['npm list -g',                              'List globally installed packages'],
        ['npm update -g <package>',                  'Update a globally installed package'],
        ['npm -v',                                   'Check your npm version'],
    ]
    y = tbl(c, MX, y, ['Command', 'What It Does'], cmd_rows, [250, CW - 250])
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Common Errors & Fixes')
    y -= 8

    errors = [
        ('"node: command not found"',
         ['Node.js is not installed, or it is not on your PATH.',
          'Fix: reinstall Node.js and restart your terminal.']),
        ('"permission denied" on npm install -g',
         ['On Mac/Linux, avoid using sudo with npm. Instead, configure npm\'s prefix:',
          'Run: npm config set prefix ~/.npm-global and add it to your PATH.']),
        ('nvm: command not found (after install)',
         ['The nvm lines were not added to your shell profile.',
          'Run: source ~/.zshrc (or restart Terminal), then try again.']),
        ('Multiple Node versions conflict',
         ['Run: nvm list to see installed versions.',
          'Run: nvm use 24 (or whatever LTS version you need) to switch.']),
    ]
    for err_title, err_lines in errors:
        card_h = 48 + len(err_lines) * 15
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(AMB); c.rect(MX, y - card_h, 4, card_h, fill=1, stroke=0)
        c.setFillColor(AMB); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 14, y - 14, err_title)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        ey = y - 30
        for line in err_lines:
            c.drawString(MX + 14, ey, line); ey -= 15
        y -= card_h + 8

    tip_lines = wrap(
        'After installing Node.js, run: node -v and npm -v in a NEW terminal window '
        '(not the one you used to install). Old windows do not pick up the new PATH.',
        10, CW - 28)
    tip_box(c, MX, y, 'Always Test in a Fresh Terminal', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Node.js & npm')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Check Node.js version',  'node -v'),
        ('Check npm version',      'npm -v'),
        ('List nvm versions',      'nvm list'),
        ('Switch Node version',    'nvm use <version>  (e.g. nvm use 24)'),
        ('Install LTS version',    'nvm install lts'),
        ('Set default version',    'nvm alias default lts'),
        ('Install Claude Code',    'npm install -g @anthropic-ai/claude-code'),
        ('Update Claude Code',     'npm update -g @anthropic-ai/claude-code'),
    ]
    url_items = [
        ('Node.js download',       'nodejs.org → "Download Node.js (LTS)"'),
        ('nvm (Mac/Linux)',         'github.com/nvm-sh/nvm'),
        ('nvm-windows',            'github.com/coreybutler/nvm-windows'),
        ('npm docs',               'docs.npmjs.com'),
        ('Current LTS',            'Node.js 24 (Active LTS as of 2026)'),
        ('Current release',        'Node.js 26 (becomes LTS October 2026)'),
        ('Claude Code install',    'docs.anthropic.com/en/claude-code'),
        ('Node.js changelog',      'nodejs.org/en/blog/release'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Commands', left_items),
        (MX + cw2 + 10, 'Links & Info', url_items),
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
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Quick Troubleshooting')
    y -= 8
    t_rows = [
        ['node -v gives nothing',       'Restart terminal; if still missing, reinstall Node.js'],
        ['"EACCES" permission error',   'Do not use sudo; fix npm prefix (see Page 5)'],
        ['nvm not found after install', 'Source your profile: source ~/.zshrc then retry'],
        ['Wrong version active',        'nvm use 24 (or your target version)'],
        ['npm install fails on Windows','Run PowerShell as Administrator'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [180, CW - 180])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 07 — Git & GitHub for Claude Users')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 06 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
