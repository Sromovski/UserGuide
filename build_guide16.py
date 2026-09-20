#!/usr/bin/env python3
"""Guide 16: Claude Plugins Guide — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_16_Plugins.pdf'
GUIDE = 'Claude Plugins Guide'

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
DPUR    = HexColor('#1E0D3A')


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
    bw, bh2 = c.stringWidth('GUIDE 16 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 16 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 30)
    c.drawString(MX, H - 175, 'Claude Plugins Guide')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Web Search, Artifacts, Code Execution & Connectors')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What "plugins" means in the claude.ai context vs MCP servers',
        'Web Search: real-time answers with inline citations — enable it in seconds',
        'Artifacts: persistent, shareable canvases for code, charts, and apps',
        'Code Execution: run Python inside a conversation to crunch real numbers',
        'Connectors: MCP-powered integrations with Gmail, Slack, Notion & more',
        'Plan comparison: which plugins need Free vs Pro vs Max vs Team',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Available at claude.ai  •  Some features require Pro/Max/Team plan')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Plugins vs MCP ────────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Are Claude Plugins?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('In the claude.ai context, "plugins" refers to built-in capabilities you '
             'toggle on in your conversation: web search, code execution, file analysis, '
             'and Connectors. These are different from MCP servers (which are developer '
             'tools you install separately). Plugins are one-click, no setup required.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    t_rows = [
        ['What they are',  'Built-in toggles in claude.ai',         'Programs you install and configure'],
        ['Who uses them',  'Everyone — no technical setup',         'Developers and power users'],
        ['Setup',          'One click in the conversation UI',      'Edit JSON config file, restart'],
        ['Examples',       'Web Search, Code Exec, Artifacts',      'GitHub, Filesystem, Brave Search'],
        ['Where to enable','claude.ai chat interface',              '.claude/settings.json or Desktop config'],
    ]
    y = tbl(c, MX, y, ['Aspect', 'Plugins (claude.ai)', 'MCP Servers'], t_rows, [100, 190, CW - 290])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'How to Enable a Plugin')
    y -= 18
    enable_steps = [
        'Open claude.ai and start or open a conversation.',
        'Click the plugin icon (puzzle piece) in the input toolbar.',
        'A menu shows available plugins — toggle any one on.',
        'The plugin icon turns active (filled). Claude now has that capability.',
        'Plugins are per-conversation — re-enable for each new conversation.',
    ]
    for i, step in enumerate(enable_steps):
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, str(i + 1))
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, step)
        y -= 17
    y -= 12

    info_panel(c, MX, y, 'Plugin Persistence', [
        'Plugins stay on for the duration of a conversation.',
        'They reset to off when you start a new conversation.',
        'You can toggle a plugin off mid-conversation at any time.',
        'Some plugins (like Connectors) remember your connection across sessions.',
    ], CW)
    c.showPage()


# ── Page 3: Web Search & Code Execution ───────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Web Search & Code Execution Plugins')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 13); c.drawString(MX, y, 'Web Search')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro1 = ('When Web Search is on, Claude queries the web in real time and integrates '
              'results into its response with inline URL citations. Available on all tiers '
              '(Free, Pro, Max, Team, Enterprise).')
    for line in wrap(intro1, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 6

    ws_rows = [
        ('What it does',  'Real-time web queries integrated into responses with sources'),
        ('Plan required', 'All plans — Free, Pro, Max, Team, Enterprise'),
        ('How to enable', 'Click plugin icon → toggle Web Search on'),
        ('Citation style','Inline links appear in the response text'),
        ('Best for',      'Current events, prices, docs, recent releases, fact-checking'),
    ]
    for label, desc in ws_rows:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 30
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 13); c.drawString(MX, y, 'Code Execution')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro2 = ('Code Execution lets Claude run Python code inside the conversation to process '
              'data, perform calculations, generate charts, and work with files you upload. '
              'Results appear directly in the response.')
    for line in wrap(intro2, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 6

    ce_rows = [
        ('Language',      'Python (with NumPy, pandas, matplotlib and other common libraries)'),
        ('Plan required', 'Pro, Max, Team, or Enterprise (not Free)'),
        ('How to enable', 'Click plugin icon → toggle Code Execution on'),
        ('Use cases',     'Data analysis, charts, maths, file conversion, CSV processing'),
        ('File upload',   'Drag a CSV, Excel, or image file into the chat for Claude to process'),
    ]
    for label, desc in ce_rows:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 30
    y -= 10

    tip_lines = wrap(
        'Upload a CSV file to the conversation with Code Execution on, '
        'then ask: "Summarise this data and plot a bar chart of the top 10 rows." '
        'Claude will process the file and display the chart inline.',
        10, CW - 28)
    tip_box(c, MX, y, 'Quick Win: Analyse a CSV in 30 Seconds', tip_lines, CW)
    c.showPage()


# ── Page 4: Artifacts ─────────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Artifacts — Persistent Shareable Canvases')
    y -= 40

    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Artifacts are rich outputs that Claude creates alongside the conversation: '
             'interactive HTML pages, charts, formatted documents, and code files. '
             'They appear in a side panel and persist across turns — Claude can '
             'update them as the conversation continues.')
    iy = y
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Chat Artifacts (claude.ai)')
    y -= 14
    chat_rows = [
        ('What they are',   'HTML, charts, formatted docs, code created in claude.ai chat'),
        ('Storage',         'Persistent — up to 20MB per artifact, saved across sessions'),
        ('Interactivity',   'Can call APIs, connect to MCP servers, refresh with live data'),
        ('Sharing',         'Private URL shareable with others'),
        ('Plan required',   'All plans can create artifacts (richer features on paid plans)'),
    ]
    for label, desc in chat_rows:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 30
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Claude Code Artifacts (Beta — June 2026)')
    y -= 14
    code_rows = [
        ('What they are',   'Self-contained interactive HTML pages built from Claude Code sessions'),
        ('Published to',    'Private URL on claude.ai — updates in place as session continues'),
        ('Limit',           'One page per artifact, no backend, no public sharing yet'),
        ('Plan required',   'Team or Enterprise only (org-level feature, beta as of June 2026)'),
        ('Use case',        'Ship a demo, dashboard, or tool page directly from a coding session'),
    ]
    for label, desc in code_rows:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 30
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'What to Ask Claude to Make as an Artifact')
    y -= 14
    examples = [
        '"Create a bar chart of my monthly expenses from this CSV"',
        '"Build an interactive calculator for compound interest"',
        '"Make a formatted one-page project brief I can share"',
        '"Write a self-contained HTML page that shows a live countdown timer"',
    ]
    for ex in examples:
        c.setFillColor(PNL); c.roundRect(MX, y - 22, CW, 22, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Helvetica', 10); c.drawString(MX + 10, y - 14, ex)
        y -= 26
    c.showPage()


# ── Page 5: Connectors & Plan Comparison ─────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Connectors & Plugin Plan Comparison')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 13); c.drawString(MX, y, 'Connectors')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    conn_desc = ('Connectors are how claude.ai plugs into external services. They run on '
                 'the Model Context Protocol. Unlike MCP servers you install yourself, '
                 'Connectors are managed integrations — enable them from the claude.ai '
                 'Connectors panel without touching any config files.')
    for line in wrap(conn_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    connectors = [
        ('Gmail',           'Read emails, draft replies, search inbox'),
        ('Google Drive',    'Access Docs, Sheets, Slides in conversations'),
        ('Slack',           'Search messages, read channels, get context'),
        ('GitHub',          'Browse repos, read code, check issues and PRs'),
        ('Notion',          'Read and write Notion pages and databases'),
        ('Stripe',          'View transactions, customers, and subscriptions'),
        ('Zapier',          'Trigger automations across 7,000+ other apps'),
        ('100s more',       'Browse the full list at claude.com/plugins'),
    ]
    for name, desc in connectors:
        c.setFillColor(PNL2); c.roundRect(MX, y - 24, CW, 24, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 14, name)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 90, y - 14, '— ' + desc)
        y -= 28
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Plugin Plan Comparison')
    y -= 8
    plan_rows = [
        ['Web Search',       'All plans',      'All plans',   'All plans',    'All plans'],
        ['Code Execution',   'No',             'Yes',         'Yes',          'Yes'],
        ['Chat Artifacts',   'Basic',          'Full',        'Full',         'Full'],
        ['Code Artifacts',   'No',             'No',          'No',           'Yes (beta)'],
        ['Connectors (MCP)', 'Limited',        'Yes',         'Yes',          'Yes + admin'],
    ]
    tbl(c, MX, y, ['Plugin', 'Free', 'Pro', 'Max', 'Team/Enterprise'], plan_rows,
        [120, 72, 72, 72, CW - 336])
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Plugins')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Plugins page',       'claude.com/plugins'),
        ('Enable plugins',     'Plugin icon in conversation toolbar'),
        ('Web Search',         'All plans — real-time results with citations'),
        ('Code Execution',     'Pro/Max/Team/Enterprise — Python only'),
        ('Chat Artifacts',     'All plans — up to 20MB, shareable URL'),
        ('Code Artifacts',     'Team/Enterprise only (beta June 2026)'),
        ('Connectors',         'Managed MCP — no JSON config needed'),
        ('Scope',              'Plugin settings reset per conversation'),
    ]
    right_items = [
        ('Web Search use',   'Ask about current events, prices, or docs'),
        ('Code Exec use',    'Upload CSV → analyse data and chart results'),
        ('Artifact use',     'Build interactive pages, calculators, reports'),
        ('Connector use',    'Read Gmail/Notion/GitHub without copy-paste'),
        ('Reset per session','Toggle plugins on at start of each new chat'),
        ('vs MCP servers',   'Plugins = no-setup toggles; MCP = dev install'),
        ('File uploads',     'Drag into chat — Code Exec processes them'),
        ('Cite sources',     'Web Search adds inline links automatically'),
    ]

    for px, panel_title, items in [
        (MX, 'Key Facts', left_items),
        (MX + cw2 + 10, 'How to Use Each', right_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL); c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(px + 10, iy, a)
            c.setFillColor(OGL)
            c.setFont('Helvetica', 9)
            c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Questions')
    y -= 8
    qa_rows = [
        ['Are plugins free?',               'Web Search yes. Code Execution requires paid plan.'],
        ['Why can\'t I see Code Execution?', 'Requires Pro or higher — not available on Free'],
        ['Do plugins use more tokens?',      'Web Search results and code output add to context'],
        ['Where are Connectors enabled?',    'claude.ai → profile icon → Connections (or Plugins)'],
        ['Is Code Exec sandboxed?',          'Yes — isolated from your machine, internet access limited'],
    ]
    y = tbl(c, MX, y, ['Question', 'Answer'], qa_rows, [172, CW - 172])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 17 — Claude Skills: Create Your Own')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 16 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
