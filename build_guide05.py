#!/usr/bin/env python3
"""Guide 05: Claude Integrations (Slack, Excel, PowerPoint, Word) — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_05_Integrations.pdf'
GUIDE = 'Claude Integrations'

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
    bw, bh2 = c.stringWidth('GUIDE 05 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 05 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude Integrations')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Slack, Excel, PowerPoint, Word & Outlook')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Add Claude to your Slack workspace and use it in any channel',
        'Install Claude add-ins for Excel, Word, and PowerPoint',
        'Build spreadsheets, audit formulas, and run analysis in Excel',
        'Draft and revise documents with tracked changes in Word',
        'Build on-brand slides inside your existing PowerPoint templates',
        'Triage your Outlook inbox and draft replies in seconds',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires: Paid plan (Pro, Max, Team, or Enterprise)  •  Slack or Microsoft 365')
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
    intro = ('Claude does not have to live only in the browser. By mid-2026, Claude works '
             'natively inside Slack, Excel, Word, PowerPoint, and Outlook. This means you '
             'can get AI assistance exactly where your work already happens — no copy-pasting '
             'between tabs, no context loss.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('Slack setup',        'Add Claude Tag to any channel in minutes'),
        ('Excel integration',  'Build models, audit formulas, run analysis inside Excel'),
        ('Word integration',   'Draft and edit with tracked changes from a sidebar'),
        ('PowerPoint',         'Create on-brand slides inside existing templates'),
        ('Outlook (beta)',     'Triage inbox and draft replies without leaving Outlook'),
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
        'Teams who live in Slack and want Claude available without switching apps',
        'Analysts, accountants, and researchers who work heavily in Excel',
        'Writers, lawyers, and consultants who produce documents in Word',
        'Presenters and marketers who build decks in PowerPoint',
    ]
    for item in audience:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Before You Start — What You Need', [
        'An active paid plan: Pro, Max, Team, or Enterprise (Free plan cannot use integrations)',
        'For Slack: admin access to your Slack workspace (to install the app)',
        'For Microsoft 365: Excel, Word, PowerPoint, or Outlook on Windows or macOS',
        'Microsoft 365 add-ins available on desktop apps and Microsoft 365 web versions',
    ], CW)
    c.showPage()


# ── Page 3: Claude in Slack ───────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Claude in Slack — Claude Tag')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Claude Tag is the primary Slack experience as of mid-2026:')

    steps = [
        ('Go to the Slack App Marketplace', [
            'In Slack, click "Apps" in the left sidebar.',
            'Search for "Claude" — look for the official Anthropic app.',
            'Click "Add to Slack" and follow the OAuth prompts.',
        ]),
        ('Invite Claude to a Channel', [
            'Open any Slack channel where you want Claude available.',
            'Type /invite @Claude and press Enter.',
            'Claude is now a member of that channel.',
        ]),
        ('Talk to Claude in Channels', [
            'Tag Claude in a message: @Claude what is the summary of this thread?',
            'Claude reads the channel context and responds in the thread.',
            'Use Claude Tag in any channel it has been invited to.',
        ]),
        ('Message Claude Directly', [
            'Click Claude in your Slack contacts list for a private DM.',
            'Use the DM for personal tasks: drafting, research, quick Q&A.',
            'DM conversations are private to you.',
        ]),
        ('Use Claude in Your Workflow', [
            'Tag Claude in a thread to get a quick summary of a long discussion.',
            'Ask Claude to draft a reply to a message and paste it in.',
            'Use Claude to explain technical content posted in a channel.',
        ]),
    ]
    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    tip_lines = wrap(
        'For org-wide rollout, a Slack admin can deploy Claude to all workspaces '
        'at once from the Slack Admin Center → App Management. '
        'Individual users can also install in their own DMs without admin rights.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Team-Wide vs Personal Install', tip_lines, CW)
    c.showPage()


# ── Page 4: Microsoft 365 — Excel & Word ─────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Microsoft 365 — Excel & Word')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Install once from Microsoft AppSource — works on desktop and the web:')
    y -= 58

    info_panel(c, MX, y, 'How to Install Any M365 Add-In', [
        '1. Open Excel, Word, or PowerPoint.',
        '2. Go to Insert → Add-ins → Get Add-ins (or visit appsource.microsoft.com).',
        '3. Search "Claude" and click Add on the official Anthropic add-in.',
        '4. Sign in with your Anthropic account when the sidebar appears.',
        '5. Claude is now available in the sidebar of that Office app.',
    ], CW)
    y -= 120

    # Excel section
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Claude for Excel')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    excel_intro = ('Claude reads your spreadsheet directly from the sidebar — no copy-paste. '
                   'It understands your data structure and can build, audit, and modify formulas '
                   'without breaking what you already have.')
    for line in wrap(excel_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    excel_uses = [
        ('"Build a financial model for [scenario] using this data"',      'Claude generates formulas, headers, and structure'),
        ('"Audit the formulas in column D and explain any issues"',       'Catches errors, circular refs, and logic mistakes'),
        ('"Run sensitivity analysis on cell B12 from 5% to 25%"',        'Creates a sensitivity table automatically'),
        ('"Add a VLOOKUP to match these two tables by employee ID"',      'Writes and inserts the formula for you'),
    ]
    for prompt, what in excel_uses:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, prompt)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 12, what)
        y -= 28
    y -= 8

    # Word section
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Claude for Word')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    word_intro = ('Claude works in a sidebar alongside your document. Edits appear as '
                  'tracked changes so you can review and accept them — Claude never '
                  'silently overwrites your work.')
    for line in wrap(word_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    word_uses = [
        ('"Draft a first version of a proposal for [client/topic]"',     'Creates a full draft in the document'),
        ('"Make this section more concise without losing key points"',   'Edits appear as tracked changes'),
        ('"Add an executive summary to the top of this document"',       'Inserts new section with formatting preserved'),
        ('"Rewrite in plain language — this is for a general audience"', 'Simplifies technical or legal language'),
    ]
    for prompt, what in word_uses:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, prompt)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 12, what)
        y -= 28
    c.showPage()


# ── Page 5: PowerPoint & Outlook ─────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Microsoft 365 — PowerPoint & Outlook')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Claude for PowerPoint')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ppt_intro = ('Claude builds slides inside your existing presentation — respecting your '
                 'slide master, layouts, fonts, and brand colors. No generic templates, '
                 'no copy-paste. Just describe what you need.')
    for line in wrap(ppt_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    ppt_uses = [
        ('"Add 3 slides summarising this Word doc I\'ll paste"',        'Pulls content from your source material'),
        ('"Create a competitive analysis slide with 4 columns"',        'Builds a branded comparison table'),
        ('"Rewrite slide 7 — it\'s too wordy for a 3-minute pitch"',   'Condenses and reformats within your template'),
        ('"Add speaker notes to every slide based on the content"',     'Writes notes slide-by-slide automatically'),
    ]
    for prompt, what in ppt_uses:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, prompt)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 12, what)
        y -= 28
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Claude for Outlook (Public Beta)')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    out_intro = ('Claude can read your inbox and draft replies from within Outlook. '
                 'It understands thread context so replies are accurate and appropriately toned.')
    for line in wrap(out_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    out_uses = [
        ('"Triage my inbox — what needs attention today?"',             'Categorises emails by urgency and action needed'),
        ('"Draft a polite decline to this meeting request"',            'Writes a context-aware reply ready to edit'),
        ('"Summarise this 20-email thread in 3 bullet points"',        'Reads the full thread and distils key points'),
        ('"Reply to this asking for the Q3 report by Friday"',         'Drafts a follow-up you can send in one click'),
    ]
    for prompt, what in out_uses:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, prompt)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 12, what)
        y -= 28
    y -= 6

    # Plan requirements
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Plan Requirements — All Integrations')
    y -= 8
    t_rows = [
        ['Free',       'Not available',     'Integrations require a paid plan'],
        ['Pro',        'Full access',        'All M365 apps + Slack'],
        ['Max',        'Full access',        'All M365 apps + Slack + higher usage'],
        ['Team',       'Full access',        'Org-wide admin controls + usage dashboard'],
        ['Enterprise', 'Full access',        'Custom policy, SSO, Bedrock/Vertex hosting option'],
    ]
    y = tbl(c, MX, y, ['Plan', 'Access', 'Notes'], t_rows, [70, 90, CW - 160])
    y -= 10

    warn_lines = wrap(
        'Outlook support is in public beta as of 2026 — it may have rough edges. '
        'Excel, Word, and PowerPoint add-ins are generally available.',
        10, CW - 28)
    warn_box(c, MX, y, 'Outlook is Beta', warn_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Integrations')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Add Claude to Slack',        'Slack App Marketplace → search "Claude" → Add to Slack'),
        ('Invite Claude to channel',   'In the channel type: /invite @Claude'),
        ('Tag Claude in a thread',     '@Claude followed by your question or task'),
        ('Install M365 add-in',        'Insert → Add-ins → Get Add-ins → search "Claude"'),
        ('Open Claude sidebar',        'Click the Claude add-in in your Office app ribbon'),
        ('Review tracked changes',     'Word: Review tab → Accept / Reject Changes'),
        ('Switch M365 apps',           'Context syncs across Excel, Word, PowerPoint, Outlook'),
        ('Upgrade plan',               'claude.ai → left sidebar → Upgrade'),
    ]
    url_items = [
        ('Slack App',       'Slack App Marketplace → search "Claude by Anthropic"'),
        ('M365 Add-ins',    'appsource.microsoft.com → search "Claude"'),
        ('M365 overview',   'claude.com/claude-for-microsoft-365'),
        ('Slack overview',  'support.claude.com → "Use Claude in Slack"'),
        ('Pricing',         'claude.ai/pricing'),
        ('Help center',     'support.anthropic.com'),
        ('Status',          'status.anthropic.com'),
        ('Enterprise info', 'anthropic.com/enterprise'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Actions', left_items),
        (MX + cw2 + 10, 'Links & Resources', url_items),
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
        ['Integrations not available',  'Upgrade to a paid plan — Free plan cannot use integrations'],
        ['Claude not in Slack channel', 'Run /invite @Claude in the channel first'],
        ['M365 add-in sidebar missing', 'Home ribbon → My Add-ins → click Claude to open sidebar'],
        ['Edits not showing in Word',   'Enable Track Changes: Review → Track Changes → On'],
        ['Cross-app sync not working',  'Sign out and back in so all apps share the same session'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Solution'], t_rows, [158, CW - 158])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 06 — Installing Node.js (Mac, Windows & Linux)')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 05 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
