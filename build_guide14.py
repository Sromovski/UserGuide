#!/usr/bin/env python3
"""Guide 14: MCP Servers 101 — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_14_MCP101.pdf'
GUIDE = 'MCP Servers 101'

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
    bw, bh2 = c.stringWidth('GUIDE 14 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 14 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'MCP Servers 101')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'The Plugin System That Connects Claude to Everything')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What MCP is — the USB analogy that makes the concept click instantly',
        'How the three-layer architecture works: Host, Client, Server',
        'The three MCP primitives: Tools, Resources, and Prompts',
        'How Claude discovers what each MCP server can do',
        'The JSON config structure that connects a server to Claude',
        'How to find the 16,000+ MCP servers already available',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Open standard by Anthropic  •  Works with Claude Code & Claude Desktop  •  16,000+ servers')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Is MCP ───────────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is the Model Context Protocol?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('MCP — the Model Context Protocol — is an open standard created by '
             'Anthropic in late 2024. It defines a common language that lets Claude '
             'connect to external tools, data sources, and services. Without MCP, '
             'connecting Claude to a new data source required custom code each time. '
             'With MCP, any app that speaks MCP works with any model that speaks MCP.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'The USB Analogy', [
        'Before USB existed, every device needed a custom connector.',
        'After USB: one standard plug, works with any device from any maker.',
        'MCP is USB for AI tools. One protocol, any tool, any model.',
        'Build an MCP server once — any MCP-compatible AI can use it.',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'What MCP Lets Claude Do')
    y -= 22
    capabilities = [
        ('Read & write files',    'Access local filesystem without you pasting file contents'),
        ('Search the web',        'Run live web searches from inside a conversation'),
        ('Query databases',       'Run SQL queries against your database in real time'),
        ('Use GitHub',            'Read repos, open PRs, manage issues — all from Claude'),
        ('Control browsers',      'Navigate web pages, fill forms, extract data'),
        ('Call any API',          'Any REST API can be wrapped as an MCP tool'),
    ]
    for title, desc in capabilities:
        c.setFillColor(PNL); c.roundRect(MX, y - 30, CW, 30, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y - 18, '✓')
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 24, y - 18, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 160, y - 18, '— ' + desc)
        y -= 34
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Who Builds MCP Servers?')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    builders = [
        'Anthropic — official servers for GitHub, Filesystem, Brave Search, and more',
        'Companies — Zapier, Notion, Linear, Slack, Stripe, and hundreds more',
        'Open source community — 16,000+ servers on GitHub and MCP registries',
        'You — any developer can write and share an MCP server',
    ]
    for b in builders:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, y, b)
        y -= 16
    c.showPage()


# ── Page 3: Architecture ──────────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The Three-Layer MCP Architecture')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Every MCP interaction involves three layers working together:')
    y -= 56

    layers = [
        ('HOST',    OG,
         'Claude Desktop or Claude Code',
         [
             'The application the user interacts with.',
             'Responsible for starting MCP clients and maintaining connections.',
             'Examples: Claude Desktop app, Claude Code CLI, VS Code with Claude extension.',
         ]),
        ('CLIENT',  OGL,
         'Inside the Host — manages one server connection',
         [
             'Lives inside the Host application.',
             'Manages the connection to one specific MCP server.',
             'Negotiates capabilities: asks "what can you do?" and stores the answer.',
         ]),
        ('SERVER',  GRN,
         'External program that provides tools',
         [
             'A separate program running on your machine or remotely.',
             'Exposes Tools, Resources, and Prompts via the MCP protocol.',
             'Examples: GitHub MCP server, Filesystem MCP server, web search server.',
         ]),
    ]

    for label, color, subtitle, lines in layers:
        card_h = 90
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(color); c.rect(MX, y - card_h, 6, card_h, fill=1, stroke=0)
        c.setFillColor(color); c.setFont('Helvetica-Bold', 13); c.drawString(MX + 16, y - 18, label)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 16, y - 32, subtitle)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        ly = y - 48
        for line in lines:
            c.drawString(MX + 16, ly, line); ly -= 14
        y -= card_h + 8

    y -= 8
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'How a Request Flows')
    y -= 14

    flow = [
        'You type: "Summarise the open issues in my GitHub repo"',
        'Claude (Host) recognises this needs the GitHub MCP server',
        'Client calls the server: list_issues(repo="myname/myrepo")',
        'Server contacts GitHub API and returns a list of issues',
        'Client passes the result back to Claude',
        'Claude reads the issues and writes your summary',
    ]
    for i, step in enumerate(flow):
        c.setFillColor(PNL2); c.roundRect(MX, y - 24, CW, 24, radius=3, fill=1, stroke=0)
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 14, str(i + 1))
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y - 14, step)
        y -= 28
    c.showPage()


# ── Page 4: Three MCP Primitives ──────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The Three MCP Primitives')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Every MCP server exposes some combination of these three building blocks:')
    y -= 56

    primitives = [
        ('TOOLS',       OG,
         'Actions Claude can take',
         'Tools are functions the server exposes. Claude calls them to get things done. '
         'A tool has a name, a description, and a set of typed parameters. Examples:',
         [
             'read_file(path)            — read a file from disk',
             'search_web(query)          — perform a live web search',
             'create_github_issue(title) — open a GitHub issue',
         ]),
        ('RESOURCES',   OGL,
         'Data Claude can read',
         'Resources are read-only data that the server makes available. Claude can request '
         'them to get context. Examples:',
         [
             'file://path/to/file        — a local file',
             'database://table/records   — records from a database',
             'api://endpoint/data        — cached API response',
         ]),
        ('PROMPTS',     GRN,
         'Pre-built instruction templates',
         'Prompts are server-defined instruction templates. They appear in slash-command '
         'menus or can be invoked by name. Examples:',
         [
             '/summarise-pr  — pre-built prompt to summarise a pull request',
             '/daily-standup — generates a standup report from recent commits',
         ]),
    ]

    for label, color, subtitle, desc, examples in primitives:
        ch = 52 + len(examples) * 14 + 48
        c.setFillColor(PNL); c.roundRect(MX, y - ch, CW, ch, radius=4, fill=1, stroke=0)
        c.setFillColor(color); c.roundRect(MX + 8, y - 32, 68, 22, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10); c.drawCentredString(MX + 42, y - 19, label)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 84, y - 18, subtitle)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(desc, 9, CW - 20)
        dy = y - 36
        for dl_line in dl[:2]:
            c.drawString(MX + 12, dy, dl_line); dy -= 13
        dy -= 4
        for ex in examples:
            c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 20, dy, ex); dy -= 14
        y -= ch + 8

    y -= 4
    tip_lines = wrap(
        'Most servers you install will expose Tools only. Resources and Prompts are '
        'optional extras that enhance what the server can do. When browsing MCP server '
        'listings, check the README for which primitives are available.',
        10, CW - 28)
    tip_box(c, MX, y, 'Tools Are the Most Common Primitive', tip_lines, CW)
    c.showPage()


# ── Page 5: JSON Config & Discovery ──────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The JSON Config & Finding MCP Servers')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The MCP Configuration File')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Servers are registered in a JSON config file. Claude reads this on startup:')
    y -= 14

    y = code_block(c, MX, y, [
        '{',
        '  "mcpServers": {',
        '    "github": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-github"],',
        '      "env": {',
        '        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"',
        '      }',
        '    },',
        '    "filesystem": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-filesystem",',
        '               "/Users/you/projects"]',
        '    }',
        '  }',
        '}',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Config File Locations')
    y -= 14
    locations = [
        ('Claude Desktop (Mac)',    '~/Library/Application Support/Claude/claude_desktop_config.json'),
        ('Claude Desktop (Windows)','%APPDATA%\\Claude\\claude_desktop_config.json'),
        ('Claude Code (per project)','.claude/settings.json  →  "mcpServers" key'),
        ('Claude Code (global)',    '~/.claude.json  →  "mcpServers" key'),
    ]
    for loc, path in locations:
        c.setFillColor(PNL2); c.roundRect(MX, y - 28, CW, 28, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, loc)
        c.setFillColor(GRN); c.setFont('Courier', 8); c.drawString(MX + 10, y - 22, path)
        y -= 32
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Where to Find MCP Servers')
    y -= 14
    sources = [
        ('modelcontextprotocol.io/servers', 'Official Anthropic registry — curated, verified servers'),
        ('github.com/modelcontextprotocol/servers', 'Official open-source server implementations'),
        ('mcp.so',                          'Community marketplace — 1,000s of servers'),
        ('npmjs.com  (search: mcp-server)', 'Most servers are published as npm packages'),
        ('PyPI  (search: mcp)',             'Python-based MCP servers'),
    ]
    for source, desc in sources:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '▸')
        c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 24, y, source)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 24, y - 12, '  ' + desc)
        y -= 26
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — MCP Servers 101')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Full name',       'Model Context Protocol'),
        ('Created by',      'Anthropic (announced Nov 2024)'),
        ('Protocol type',   'Open standard — any AI can implement it'),
        ('Transport',       'JSON-RPC 2.0 (stdio or HTTP+SSE)'),
        ('Available servers','16,000+ (as of mid-2026)'),
        ('Three primitives','Tools, Resources, Prompts'),
        ('Config key',      '"mcpServers" in JSON config file'),
        ('Docs',            'modelcontextprotocol.io'),
    ]
    right_items = [
        ('Host',      'The app Claude lives in (Desktop, VS Code)'),
        ('Client',    'Manages one server connection within the Host'),
        ('Server',    'External program exposing Tools/Resources/Prompts'),
        ('Tools',     'Functions Claude calls to take action'),
        ('Resources', 'Read-only data the server provides'),
        ('Prompts',   'Pre-built instruction templates on the server'),
        ('Scope',     'Add servers per-project or globally'),
        ('Registry',  'mcp.so  •  modelcontextprotocol.io/servers'),
    ]

    for px, panel_title, items in [
        (MX, 'Key Facts', left_items),
        (MX + cw2 + 10, 'Architecture Glossary', right_items),
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
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Questions')
    y -= 8
    t_rows = [
        ['Is MCP free to use?',          'Yes — open standard, no licensing fees'],
        ['Does MCP work on claude.ai?',   'Claude Code and Claude Desktop only (not the web app)'],
        ['Can I run servers remotely?',   'Yes — HTTP+SSE transport supports remote servers'],
        ['How does Claude find tools?',   'Client asks server on connect; server lists all capabilities'],
        ['What language for servers?',    'Any — Node.js and Python are most common'],
    ]
    y = tbl(c, MX, y, ['Question', 'Answer'], t_rows, [174, CW - 174])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 15 — Installing & Using MCP Servers')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 14 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
