#!/usr/bin/env python3
"""Guide 10: Claude Code in VS Code — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_10_ClaudeCode.pdf'
GUIDE = 'Claude Code in VS Code'

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
    pad = 10; lh = 14
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODE_BG); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG); c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
    ty = y - pad - 10
    for line in lines:
        col = MGR if (line.startswith('#') or line.startswith('//')) else GRN
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
    bw, bh2 = c.stringWidth('GUIDE 10 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 10 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude Code')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'AI-Powered Coding Inside VS Code — From Install to First Edit')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Install the Claude Code CLI and VS Code extension step by step',
        'Authenticate with your Claude account or API key',
        'Make your first AI-assisted code edit in under 5 minutes',
        'Master all essential slash commands: /help, /clear, /compact, /status',
        'Understand the trust dialog and how file permissions work',
        'The file-editing workflow: context → prompt → diff → accept',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires paid Claude plan (Pro/Max/Team/Enterprise) or API key  •  VS Code 1.98+')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Is Claude Code ───────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is Claude Code?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Claude Code is Anthropic\'s official agentic coding tool. It reads and edits '
             'files, runs terminal commands, searches your codebase, and reasons about '
             'your project — all in response to plain-English prompts. The VS Code '
             'extension brings this capability directly into your editor with inline '
             'diff views, automatic file context, and a persistent conversation panel.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'Claude Code vs Claude on the Web', [
        'Claude.ai (web/app): Great for questions, writing, analysis. No file access.',
        'Claude Code (CLI + extension): Reads and edits files, runs commands, searches',
        '  your codebase. Designed for software development workflows.',
        'Think of Claude Code as Claude that lives inside your project.',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Need")
    y -= 22
    reqs = [
        ('VS Code 1.98+',         'The minimum version for the Claude Code extension'),
        ('Node.js installed',     'Required to install the Claude Code CLI via npm'),
        ('A paid Claude plan',    'Pro, Max, Team, or Enterprise — or an API key'),
        ('Anthropic account',     'Sign in at claude.ai to authenticate'),
    ]
    for title, desc in reqs:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 10, y, f'▸  {title}')
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        c.drawString(MX + 148, y, f'— {desc}')
        y -= 18
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'What Claude Code Can Do')
    y -= 22
    abilities = [
        'Read, write, and edit any file in your project',
        'Run terminal commands (with your approval)',
        'Search across your entire codebase for functions, classes, or patterns',
        'Explain existing code, suggest refactors, and catch bugs',
        'Work as an agent: break a task into steps and execute them one by one',
        'Show you a diff of proposed changes before applying them',
    ]
    for ability in abilities:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, ability)
        y -= 18

    y -= 10
    warn_lines = wrap(
        'Claude Code requires a paid Claude subscription (Pro, Max, Team, or Enterprise) '
        'or billing via the Anthropic Console (API key). The free tier on claude.ai does '
        'not include Claude Code access.',
        10, CW - 28)
    warn_box(c, MX, y, 'Paid Plan Required', warn_lines, CW)
    c.showPage()


# ── Page 3: Install Claude Code ───────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing Claude Code')

    steps = [
        ('Install the CLI via npm', [
            'Open a terminal and run the command below.',
            'This installs the claude command globally on your system.',
            'Do NOT use sudo — if you get a permission error, use nvm (Guide 06).',
        ]),
        ('Verify the CLI installed', [
            'Run: claude --version',
            'You should see the Claude Code version number printed.',
        ]),
        ('Install the VS Code Extension', [
            'In VS Code, press Ctrl+Shift+X to open the Extensions panel.',
            'Search for "Claude Code" and install the one by Anthropic.',
            'The Claude icon will appear in the VS Code Activity Bar.',
        ]),
        ('Authenticate', [
            'Click the Claude icon in the Activity Bar to open the panel.',
            'Click "Sign In" — a browser window opens to claude.ai.',
            'Log in with your Claude account (Pro/Max/Team/Enterprise).',
            'Return to VS Code — you are now authenticated.',
        ]),
        ('Set Up Terminal Integration', [
            'In the Claude panel, type: /terminal-setup',
            'This configures VS Code keybindings for multi-line prompts.',
            'Shift+Enter will now insert a newline instead of submitting.',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 5

    y = code_block(c, MX, y, [
        '# Step 1: Install Claude Code CLI',
        'npm install -g @anthropic-ai/claude-code',
        '',
        '# Step 2: Verify install',
        'claude --version',
    ], CW)
    y -= 10

    tip_lines = wrap(
        'Alternative: set ANTHROPIC_API_KEY in your environment to authenticate with '
        'an API key instead of a Claude account. Open VS Code from the same terminal '
        'session so the variable is inherited.',
        10, CW - 28)
    tip_box(c, MX, y, 'Using an API Key Instead of a Claude Account', tip_lines, CW)
    c.showPage()


# ── Page 4: First Edit & The Workflow ─────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Your First Claude Code Edit')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'The core workflow: open a file → ask Claude → review the diff → accept or reject.')
    y -= 62

    workflow = [
        ('Open a Folder in VS Code',  [
            'File → Open Folder → select your project directory.',
            'Claude Code works at the folder level — it can read any file in the project.',
        ]),
        ('Open the Claude Panel',  [
            'Click the Claude icon in the Activity Bar (left sidebar).',
            'A chat panel opens on the right side of VS Code.',
        ]),
        ('Give Claude a Task',  [
            'Type a prompt in plain English. Examples:',
            '"Add a function that calculates the total of an array"',
            '"Fix the bug on line 42 of utils.js"',
            '"Explain what the parse() function does"',
        ]),
        ('The Trust Dialog',  [
            'The first time Claude tries to edit a file, a dialog appears asking',
            'if you trust it to modify files in this folder.',
            'Click "Allow" to proceed — you can always review the diff first.',
        ]),
        ('Review the Diff & Accept',  [
            'Claude shows you a red/green diff of proposed changes.',
            'Green = additions, Red = deletions.',
            'Click "Accept" to apply the change, or "Reject" to discard it.',
        ]),
    ]

    for i, (title, lines) in enumerate(workflow):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 5

    y -= 4
    info_panel(c, MX, y, 'Context Is Automatic', [
        'The file you have open in the editor is automatically included in Claude\'s context.',
        'Select code with your cursor → it\'s added to the prompt automatically.',
        'You can also drag files into the Claude panel to include them explicitly.',
        'The more context Claude has, the better its suggestions will be.',
    ], CW)
    c.showPage()


# ── Page 5: Slash Commands ────────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Slash Commands Reference')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Type / in the Claude panel to see the full list. Key commands:')
    y -= 60

    commands = [
        ('/help',           'Show all available slash commands and a brief description of each.'),
        ('/clear',          'Clear the current conversation history. File edits already made are kept.'),
        ('/compact',        'Summarise older messages to shrink context while keeping key decisions.'),
        ('/status',         'Show current version, model, auth status, and token usage.'),
        ('/doctor',         'Run a diagnostics check — useful if Claude Code stops responding.'),
        ('/terminal-setup', 'Configure VS Code keybindings for multi-line prompt entry.'),
        ('/plugins',        'Open the Manage Plugins interface to enable or disable MCP servers.'),
        ('/cost',           'Display token usage and estimated cost for the current session.'),
    ]
    for cmd, desc in commands:
        ph = 42
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier-Bold', 11); c.drawString(MX + 12, y - 15, cmd)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        dl = wrap(desc, 10, CW - 130)
        dy2 = y - 14
        for dl_line in dl:
            c.drawString(MX + 130, dy2, dl_line); dy2 -= 14
        y -= ph + 4

    y -= 6
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Keyboard Shortcuts in the Claude Panel')
    y -= 14
    shortcuts = [
        ('Enter',          'Send your message / submit the prompt'),
        ('Shift+Enter',    'New line in prompt (after /terminal-setup)'),
        ('↑ / ↓ arrows',  'Navigate through your prompt history'),
        ('Ctrl+L',         'Clear the conversation (same as /clear)'),
        ('Escape',         'Cancel Claude\'s current response mid-stream'),
    ]
    for key, action in shortcuts:
        c.setFillColor(PNL2); c.roundRect(MX, y - 24, CW, 24, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Courier-Bold', 10)
        c.drawString(MX + 10, y - 15, key)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        c.drawString(MX + 160, y - 15, action)
        y -= 28
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Code in VS Code')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Install CLI',          'npm install -g @anthropic-ai/claude-code'),
        ('Verify install',       'claude --version'),
        ('Open Claude panel',    'Click Claude icon in Activity Bar'),
        ('Clear conversation',   '/clear  or  Ctrl+L'),
        ('Compact context',      '/compact'),
        ('Check status',         '/status'),
        ('Run diagnostics',      '/doctor'),
        ('Setup terminal keys',  '/terminal-setup'),
    ]
    url_items = [
        ('Extension name',       '"Claude Code" by Anthropic on VS Code Marketplace'),
        ('Official docs',        'docs.claude.com'),
        ('Min VS Code version',  '1.98.0'),
        ('CLI package',          '@anthropic-ai/claude-code (npm)'),
        ('Required plan',        'Pro / Max / Team / Enterprise — or API key'),
        ('Auth URL',             'claude.ai (browser auth on first launch)'),
        ('API key (alternative)','console.anthropic.com'),
        ('Context included',     'Open file + selected text (automatic)'),
    ]

    for px, panel_title, items in [
        (MX, 'CLI & Commands', left_items),
        (MX + cw2 + 10, 'Setup & Resources', url_items),
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
        ['Extension not visible',     'Check VS Code version is 1.98+ (Help → About)'],
        ['"Not authenticated" error',  'Click the Claude panel icon and sign in again'],
        ['CLI not found after install','Close and reopen your terminal so PATH updates'],
        ['Trust dialog keeps appearing','Approve trust once per folder — not per session'],
        ['Diff not showing changes',   'Make sure you opened a folder, not just a single file'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [172, CW - 172])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 11 — CLAUDE.md Files: Build Plans That Work')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 10 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
