#!/usr/bin/env python3
"""Guide 04: Claude in Chrome (Browser Extension) — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_04_Chrome.pdf'
GUIDE = 'Claude in Chrome'

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
    bw, bh2 = c.stringWidth('GUIDE 04 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 04 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude in Chrome')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'The Browser Agent That Works Alongside You')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Install the Claude for Chrome extension from the Web Store',
        'Understand which plans get access — Pro, Max, Team & Enterprise',
        'Read and summarize any page with one click from the side panel',
        'Automate multi-step browser tasks: click, fill, navigate across tabs',
        'Extract data from websites and compile it into tables or reports',
        'Privacy guide — what Claude sees and how to stay in control',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires: Google Chrome  •  Paid plan (Pro, Max, Team, or Enterprise)  •  Beta as of 2026')
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
    intro = ('Claude for Chrome turns Claude into a browser agent — it lives in a side '
             'panel and can see what you see on any webpage. It can read, click, fill '
             'forms, switch tabs, and run multi-step tasks while you stay in control. '
             'As of June 2026 it has 9 million installs and is in beta for paid plans.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('Install the extension',  'Step-by-step from the Chrome Web Store'),
        ('Use the side panel',     'Open Claude alongside any website you visit'),
        ('Summarize pages',        'One-prompt summaries of articles, docs, reports'),
        ('Automate browser tasks', 'Click, fill, navigate — Claude does the steps'),
        ('Extract web data',       'Pull structured data from tables and listings'),
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
        'Anyone on a Pro, Max, Team, or Enterprise plan who uses Chrome',
        'Researchers who want to summarize and extract data from many pages',
        'Professionals who repeat the same multi-step browser tasks daily',
        'Developers who want Claude to navigate docs or test web workflows',
    ]
    for item in audience:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Before You Start — What You Need', [
        'Google Chrome browser (any recent version)',
        'An active Claude paid plan: Pro, Max, Team, or Enterprise',
        'Free plan users: extension installs but agent features are not available',
        'Note: still in beta as of June 2026 — some features may change',
    ], CW)
    c.showPage()


# ── Page 3: Install & Setup ───────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing & Setting Up')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Installation takes about 2 minutes:')
    steps = [
        ('Open the Chrome Web Store', [
            'In Chrome, visit the Chrome Web Store (chrome.google.com/webstore).',
            'Search for "Claude for Chrome" by Anthropic.',
            'Or go directly to claude.com/claude-for-chrome for the link.',
        ]),
        ('Install the Extension', [
            'Click "Add to Chrome" on the official Anthropic listing.',
            'Click "Add extension" when Chrome asks for confirmation.',
            'The Claude icon (orange) appears in your Chrome toolbar.',
        ]),
        ('Sign In', [
            'Click the Claude icon in the toolbar to open the side panel.',
            'Sign in with your Anthropic account (same as claude.ai).',
            'The extension verifies your plan — paid plan required.',
        ]),
        ('Allow Page Access', [
            'Chrome asks if Claude can read pages — click Allow.',
            'You can restrict this to specific sites in Chrome settings later.',
            'Claude only reads a page when the side panel is open and active.',
        ]),
        ('Open the Side Panel', [
            'Visit any webpage and click the Claude icon to open the panel.',
            'The panel slides in on the right side of your browser window.',
            'Claude can now see and interact with the current page.',
        ]),
    ]
    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6
    tip_lines = wrap(
        'Pin the Claude extension to your toolbar so it\'s always one click away: '
        'click the puzzle-piece icon in Chrome → click the pin next to Claude.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Keep Claude Always Visible', tip_lines, CW)
    c.showPage()


# ── Page 4: Core Features ─────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Core Features — What Claude Can Do in Chrome')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Page Summarization & Analysis')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Open the side panel on any page and ask Claude about it:')
    y -= 20

    summ_examples = [
        ('"Summarize this article in 3 bullet points"',         'Works on news, blogs, documentation'),
        ('"What are the key arguments in this paper?"',         'Research papers, PDFs, academic content'),
        ('"Extract all the prices from this product page"',     'E-commerce, comparison shopping'),
        ('"List every action item mentioned on this page"',     'Meeting notes, project pages'),
        ('"Translate and summarize this page"',                 'Non-English content (uses web text)'),
    ]
    for prompt, context in summ_examples:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y, prompt)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 12, context)
        y -= 28
    y -= 6

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Browser Automation — Let Claude Do the Steps')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    auto_intro = ('Tell Claude what you want to accomplish and it performs the steps '
                  'in the browser: clicking, typing, navigating tabs, and filling forms.')
    for line in wrap(auto_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    auto_tasks = [
        ('Research & compile',   '"Search for the 5 top competitors of [company] and summarize each"'),
        ('Form filling',         '"Fill out this contact form with my details: [paste your info]"'),
        ('Tab management',       '"Go through each of my open tabs and summarize what each is about"'),
        ('Price comparison',     '"Check these 3 product URLs and tell me which has the best value"'),
        ('Data extraction',      '"From this job listing page, extract title, salary, and requirements"'),
        ('Booking / scheduling', '"Find the next available slot on this calendar page and note it"'),
    ]
    cw2 = (CW - 10) / 2
    row_y = y; card_h = 44
    for i, (title, task) in enumerate(auto_tasks):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + 6
        cx = MX + col * (cw2 + 10)
        c.setFillColor(PNL); c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(cx + 8, row_y - card_h + 10, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(cx + 18, row_y - card_h + 17, str(i + 1))
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(cx + 34, row_y - 15, title)
        c.setFillColor(MGR); c.setFont('Helvetica', 8)
        t = task if len(task) <= 54 else task[:51] + '…'
        c.drawString(cx + 34, row_y - 29, t)
    c.showPage()


# ── Page 5: Plans, Privacy & Pro Tips ────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Plans, Privacy & Pro Tips')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Which Plan Gets What?')
    y -= 8
    t_rows = [
        ['Free',       'Extension installs',  'No — agent features locked'],
        ['Pro ($20)',  'Full access',          'Limited to Haiku 4.5 model for browsing'],
        ['Max ($100+)','Full access',          'Choose Opus 4.7, Sonnet 4.6, or Haiku 4.5'],
        ['Team',       'Full access',          'Admin controls + shared org usage'],
        ['Enterprise', 'Full access',          'Custom data policies, SSO, priority support'],
    ]
    y = tbl(c, MX, y, ['Plan', 'Extension Access', 'Model & Notes'], t_rows, [80, 100, CW - 180])
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Privacy — What Claude Sees and When')
    y -= 18
    cw2 = (CW - 10) / 2
    sees_h = 130
    c.setFillColor(PNL); c.roundRect(MX, y - sees_h, cw2, sees_h, radius=4, fill=1, stroke=0)
    c.setFillColor(GRN); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y - 18, 'Claude CAN see:')
    sees = ['Page text content', 'Links and button labels', 'Form field labels (not autofill)',
            'Page structure and layout', 'Content of tabs you open in the panel']
    iy = y - 36
    for s in sees:
        c.setFillColor(GRN); c.drawString(MX + 10, iy, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 24, iy, s)
        iy -= 18

    rx = MX + cw2 + 10
    c.setFillColor(PNL); c.roundRect(rx, y - sees_h, cw2, sees_h, radius=4, fill=1, stroke=0)
    c.setFillColor(AMB); c.setFont('Helvetica-Bold', 10); c.drawString(rx + 10, y - 18, 'Claude CANNOT see:')
    cannot = ['Saved passwords or autofill data', 'Private browsing / incognito tabs',
              'Other browser extensions\' data', 'Pages where you close the panel',
              'Content on other apps or your desktop']
    iy = y - 36
    for s in cannot:
        c.setFillColor(AMB); c.drawString(rx + 10, iy, '✗')
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(rx + 24, iy, s)
        iy -= 18

    y -= sees_h + 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Pro Tips')
    y -= 18

    tips = [
        'Tell Claude your goal, not the steps — "Research 5 competitors" beats clicking instructions.',
        'Use "don\'t click anything, just read and report" when you only need summaries.',
        'For multi-tab tasks, open all target tabs first, then ask Claude to process them.',
        'Combine with claude.ai Projects to save research results across sessions.',
        'On Pro, Haiku 4.5 is fast — use it for page reads; switch to claude.ai for Opus tasks.',
    ]
    for tip in tips:
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        tl = wrap(tip, 10, CW - 28)
        c.drawString(MX + 24, y, tl[0])
        if len(tl) > 1:
            c.drawString(MX + 24, y - 14, tl[1])
            y -= 14
        y -= 20

    y -= 4
    warn_lines = wrap(
        'Claude for Chrome is still in beta as of June 2026. Features, model access, '
        'and plan requirements may change. Check claude.com/claude-for-chrome for the latest.',
        10, CW - 28)
    warn_box(c, MX, y, 'Beta Product', warn_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude in Chrome')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Open side panel',          'Click Claude icon in Chrome toolbar'),
        ('Close side panel',         'Click Claude icon again, or press X in panel'),
        ('Pin to toolbar',           'Puzzle-piece icon → pin Claude'),
        ('Read current page',        'Panel open → type your question about the page'),
        ('Let Claude click/navigate','Describe the task — Claude acts in the browser'),
        ('Restrict page access',     'Chrome settings → Extensions → Claude → Site access'),
        ('Change model (Max)',        'Panel settings → Model → choose Opus/Sonnet/Haiku'),
        ('View extension settings',  'Click Claude icon → gear icon → Settings'),
    ]
    url_items = [
        ('Extension page',     'chrome.google.com/webstore (search "Claude by Anthropic")'),
        ('Direct link',        'claude.com/claude-for-chrome'),
        ('Plan upgrade',       'claude.ai → left sidebar → Upgrade'),
        ('Help center',        'support.anthropic.com'),
        ('Privacy policy',     'anthropic.com/privacy'),
        ('Release notes',      'support.anthropic.com → Release Notes'),
        ('Report a bug',       'Side panel → gear icon → Send feedback'),
        ('Web version',        'claude.ai (Projects sync with extension)'),
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
        ['Features greyed out',      'Extension needs a paid plan (Pro, Max, Team, Enterprise)'],
        ['Claude can\'t read page',  'Click Allow when Chrome asks for page access permission'],
        ['Side panel not opening',   'Unpin and re-pin the extension, or reinstall from Web Store'],
        ['Automation stopped early', 'The page may require a login — sign in then retry the task'],
        ['Wrong model showing',      'Only Max/Team/Enterprise can switch models; Pro uses Haiku 4.5'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Solution'], t_rows, [152, CW - 152])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 05 — Claude Integrations (Slack, Excel, PowerPoint)')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 04 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
