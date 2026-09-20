#!/usr/bin/env python3
"""Guide 15: Installing & Using MCP Servers — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_15_MCPInstall.pdf'
GUIDE = 'Installing & Using MCP Servers'

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
    pad = 10; lh = 13
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODE_BG); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG); c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
    ty = y - pad - 10
    for line in lines:
        col = MGR if (line.strip().startswith('//') or line.strip().startswith('#')) else GRN
        c.setFillColor(col); c.setFont('Courier', 9)
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
    bw, bh2 = c.stringWidth('GUIDE 15 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 15 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 28)
    c.drawString(MX, H - 175, 'Installing MCP Servers')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Step-by-Step Setup for GitHub, Filesystem & Brave Search')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Exact JSON config entries for 3 essential MCP servers',
        'GitHub MCP: read repos, open issues, manage PRs from Claude',
        'Filesystem MCP: give Claude read/write access to local folders',
        'Brave Search MCP: live web search inside Claude conversations',
        'Where config files live on Mac and Windows',
        'Security rules: what goes in the config vs what stays in .env',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires Node.js + Claude Desktop or Claude Code  •  Mac & Windows')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Setup & Config File ───────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Before You Start')

    steps = [
        ('Install Node.js', [
            'All three servers in this guide run via npx (comes with Node.js).',
            'Install Node.js 22 LTS from nodejs.org if you haven\'t yet (Guide 06).',
            'Verify: open a terminal and run: node --version',
        ]),
        ('Open the Config File', [
            'Mac:     ~/Library/Application Support/Claude/claude_desktop_config.json',
            'Windows: %APPDATA%\\Claude\\claude_desktop_config.json',
            'If the file doesn\'t exist yet, create it with the content shown below.',
        ]),
        ('Start with the Base Config', [
            'Your config file must be valid JSON — one missing comma breaks it.',
            'Start with the empty shell below, then add each server block.',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    y = code_block(c, MX, y, [
        '// claude_desktop_config.json — base structure',
        '{',
        '  "mcpServers": {',
        '    // Add server entries here',
        '  }',
        '}',
    ], CW)
    y -= 12

    info_panel(c, MX, y, 'Config File Rules', [
        'Must be valid JSON — use a JSON validator if unsure (jsonlint.com)',
        'Never commit this file to a public git repo — it contains API keys',
        'Restart Claude Desktop completely after every config change',
        'Claude Code: add an "mcpServers" key to .claude/settings.json instead',
    ], CW)
    c.showPage()


# ── Page 3: Filesystem MCP ────────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Server 1 — Filesystem MCP')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38,
                 'Gives Claude read and write access to folders on your machine. No API key needed.')
    y -= 56

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'What It Does')
    y -= 18
    abilities = [
        'Read any file in the allowed folder (without you pasting the contents)',
        'Write new files and edit existing ones',
        'List directory contents and search for files by name',
        'Move, copy, and delete files (with your confirmation)',
    ]
    for ab in abilities:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, ab)
        y -= 17
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'JSON Config Entry')
    y -= 14
    y = code_block(c, MX, y, [
        '"filesystem": {',
        '  "command": "npx",',
        '  "args": [',
        '    "-y",',
        '    "@modelcontextprotocol/server-filesystem",',
        '    "/Users/yourname/Projects"',
        '    // Windows: "C:\\\\Users\\\\YourName\\\\Projects"',
        '  ]',
        '}',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Key Points')
    y -= 14
    points = [
        ('Allowed path',     'Replace /Users/yourname/Projects with your actual folder path.'),
        ('Multiple folders', 'Add more paths as extra items in the "args" array.'),
        ('No API key',       'Filesystem MCP needs no credentials — just a folder path.'),
        ('Scope',            'Claude can only access the folders you list — nothing else.'),
    ]
    for label, desc in points:
        c.setFillColor(PNL2); c.roundRect(MX, y - 28, CW, 28, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 22, desc)
        y -= 32
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Try It — Prompts That Work After Install')
    y -= 14
    prompts = [
        '"Read my README.md and summarise the project"',
        '"List all .py files in the src folder"',
        '"Create a new file called notes.md with my meeting notes"',
    ]
    for p in prompts:
        c.setFillColor(PNL); c.roundRect(MX, y - 22, CW, 22, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Helvetica', 10); c.drawString(MX + 10, y - 14, p)
        y -= 26
    c.showPage()


# ── Page 4: GitHub MCP ────────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Server 2 — GitHub MCP')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Read repos, open issues, manage PRs, and search code — all from inside Claude.')
    y -= 56

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Step 1 — Create a GitHub Personal Access Token')
    y -= 18
    pat_steps = [
        'Go to github.com → Settings → Developer settings → Personal access tokens.',
        'Click "Tokens (classic)" → "Generate new token (classic)".',
        'Name it "Claude MCP" and set expiry (90 days recommended).',
        'Check scopes: repo, read:org, read:user  (minimum required).',
        'Click Generate — copy the token starting with ghp_ immediately.',
        'Important: you cannot view this token again after you leave the page.',
    ]
    for step in pat_steps:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, y, step)
        y -= 16
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Step 2 — Add to Config File')
    y -= 14
    y = code_block(c, MX, y, [
        '"github": {',
        '  "command": "docker",',
        '  "args": ["run", "-i", "--rm", "-e",',
        '           "GITHUB_PERSONAL_ACCESS_TOKEN",',
        '           "ghcr.io/github/github-mcp-server"],',
        '  "env": {',
        '    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"',
        '  }',
        '}',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'What You Can Do After Install')
    y -= 14
    actions = [
        '"List the open issues in my repo myname/myproject"',
        '"Create a new issue titled: Add dark mode support"',
        '"Summarise the last 5 commits to the main branch"',
        '"Show me all open pull requests and their status"',
        '"Search for the function parseUser across my codebase"',
    ]
    for action in actions:
        c.setFillColor(PNL); c.roundRect(MX, y - 22, CW, 22, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Helvetica', 10); c.drawString(MX + 10, y - 14, action)
        y -= 26
    y -= 10

    warn_lines = wrap(
        'Keep your GitHub PAT secret. Never share it, never paste it into a prompt, '
        'and never commit it to git. If exposed, revoke it immediately at '
        'github.com/settings/tokens and generate a new one.',
        10, CW - 28)
    warn_box(c, MX, y, 'Keep Your Token Secret', warn_lines, CW)
    c.showPage()


# ── Page 5: Brave Search MCP ──────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Server 3 — Brave Search MCP')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Real-time web search inside Claude. Metered — see pricing below.')
    y -= 56

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Step 1 — Get a Brave Search API Key')
    y -= 18
    # Brave retired the free tier on 12 Feb 2026. Everything is metered now, with a
    # monthly credit that only applies if you attribute Brave on your site.
    brave_steps = [
        'Go to search.brave.com/api and create an account.',
        'All plans are metered — roughly $5 per 1,000 queries.',
        '$5/month in credits is available if you attribute Brave Search.',
        'Click "Create Subscription" → copy the key (it looks like BSA...).',
    ]
    for step in brave_steps:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, y, step)
        y -= 17
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Step 2 — Add to Config File')
    y -= 14
    y = code_block(c, MX, y, [
        '"brave-search": {',
        '  "command": "npx",',
        '  "args": ["-y", "@brave/brave-search-mcp-server"],',
        '  "env": {',
        '    "BRAVE_API_KEY": "your_brave_api_key_here"',
        '  }',
        '}',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Complete 3-Server Config (Copy-Paste Ready)')
    y -= 14
    y = code_block(c, MX, y, [
        '{',
        '  "mcpServers": {',
        '    "filesystem": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-filesystem",',
        '               "/Users/yourname/Projects"]',
        '    },',
        '    "github": {',
        '      "command": "docker",',
        '      "args": ["run", "-i", "--rm", "-e",',
        '               "GITHUB_PERSONAL_ACCESS_TOKEN",',
        '               "ghcr.io/github/github-mcp-server"],',
        '      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }',
        '    },',
        '    "brave-search": {',
        '      "command": "npx",',
        '      "args": ["-y", "@brave/brave-search-mcp-server"],',
        '      "env": { "BRAVE_API_KEY": "BSA..." }',
        '    }',
        '  }',
        '}',
    ], CW)
    y -= 12

    tip_lines = wrap(
        'After saving the config, restart Claude Desktop fully (Quit from menu bar, '
        'then reopen). The new servers appear in the Claude panel under the plugin icon.',
        10, CW - 28)
    tip_box(c, MX, y, 'Always Restart After Editing the Config', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Installing MCP Servers')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Mac config path',   '~/Library/Application Support/Claude/'),
        ('Windows config path','%APPDATA%\\\\Claude\\\\'),
        ('Config filename',   'claude_desktop_config.json'),
        ('Restart required',  'Yes — after every config change'),
        ('Filesystem: key',   'No API key needed — just a folder path'),
        ('GitHub: key type',  'Personal Access Token (PAT) from github.com'),
        ('Brave: pricing',    'Metered — approx $5 per 1,000 queries'),
        ('Brave: key source', 'search.brave.com/api'),
    ]
    right_items = [
        ('Filesystem npm pkg', '@modelcontextprotocol/server-filesystem'),
        ('GitHub server',      'ghcr.io/github/github-mcp-server'),
        ('Brave npm pkg',      '@brave/brave-search-mcp-server'),
        ('Run command',        'npx -y <package>'),
        ('Node.js required',   'Yes — v18+ (v22 LTS recommended)'),
        ('Claude Code config', '.claude/settings.json → "mcpServers" key'),
        ('Global config',      '~/.claude.json → "mcpServers" key'),
        ('Security',           'Never commit config file to public repos'),
    ]

    for px, panel_title, items in [
        (MX, 'Config Details', left_items),
        (MX + cw2 + 10, 'Package Names', right_items),
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
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Issues & Fixes')
    y -= 8
    t_rows = [
        ['Server not appearing in Claude',  'Restart Claude Desktop completely (not just reload)'],
        ['JSON parse error on startup',      'Validate JSON at jsonlint.com — missing comma is common'],
        ['GitHub auth error',               'Check PAT scopes include "repo" — regenerate if needed'],
        ['Brave "invalid key" error',       'Confirm key from search.brave.com/api dashboard'],
        ['Filesystem "access denied"',      'Check the folder path exists and use absolute paths'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [172, CW - 172])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 16 — Claude Plugins Guide')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 15 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
