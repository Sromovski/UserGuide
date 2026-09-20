#!/usr/bin/env python3
"""Guide 01: Claude on the Web (claude.ai) — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
MY = 0.55 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_01_Web.pdf'
GUIDE = 'Claude on the Web'

BG     = HexColor('#0F0F1A')
OG     = HexColor('#E07A38')
OGL    = HexColor('#F5A66B')
CREAM  = HexColor('#F5F0E8')
LGR    = HexColor('#D4CFC7')
MGR    = HexColor('#9B9690')
PNL    = HexColor('#1C1C2E')
PNL2   = HexColor('#161625')
GRN    = HexColor('#5CB85C')
AMB    = HexColor('#F59E0B')
WHT    = HexColor('#FFFFFF')
DOG    = HexColor('#C86820')
DDOG   = HexColor('#B85C18')
DBGRN  = HexColor('#0D2B0D')
DBAMB  = HexColor('#2B1A00')


def wrap(text, size, width, font='Helvetica'):
    return simpleSplit(text, font, size, width)


def pg_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def hdr(c):
    c.setFillColor(OG)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)


def ftr(c, n):
    c.setFillColor(PNL)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica', 8)
    c.drawString(MX, 7, f'Claude AI Field Guide Series  ·  {GUIDE}')
    c.setFillColor(MGR)
    c.drawRightString(W - MX, 7, f'Page {n}')


def step_card(c, x, y, num, title, lines, w):
    pad, badge = 10, 26
    card_h = 48 + len(lines) * 15
    c.setFillColor(PNL)
    c.roundRect(x, y - card_h, w, card_h, radius=4, fill=1, stroke=0)
    c.setFillColor(OG)
    c.roundRect(x + pad, y - pad - badge, badge, badge, radius=3, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(x + pad + badge / 2, y - pad - badge + 7, str(num))
    tx = x + pad + badge + 8
    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(tx, y - pad - 12, title)
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    by = y - pad - 28
    for line in lines:
        c.drawString(tx, by, line)
        by -= 15
    return y - card_h


def tip_box(c, x, y, heading, lines, w):
    pad = 10
    bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBGRN)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, f'TIP  {heading}')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    ty = y - pad - 26
    for line in lines:
        c.drawString(x + 14, ty, line)
        ty -= 15
    return y - bh


def info_panel(c, x, y, heading, lines, w):
    pad = 12
    ph = len(lines) * 16 + pad * 2 + 22
    c.setFillColor(PNL)
    c.roundRect(x, y - ph, w, ph, radius=4, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(x + pad, y - pad - 12, heading)
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    ty = y - pad - 30
    for line in lines:
        c.drawString(x + pad, ty, line)
        ty -= 16
    return y - ph


def tbl(c, x, y, headers, rows, col_w):
    rh, pad = 22, 7
    tw = sum(col_w)
    c.setFillColor(OG)
    c.rect(x, y - rh, tw, rh, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    cx = x
    for i, h in enumerate(headers):
        c.drawString(cx + pad, y - rh + 7, h)
        cx += col_w[i]
    for ri, row in enumerate(rows):
        ry = y - rh * (ri + 2)
        c.setFillColor(PNL2 if ri % 2 == 0 else PNL)
        c.rect(x, ry, tw, rh, fill=1, stroke=0)
        cx = x
        for ci, cell in enumerate(row):
            c.setFillColor(OGL if ci == 0 else LGR)
            c.setFont('Helvetica-Bold' if ci == 0 else 'Helvetica', 9)
            c.drawString(cx + pad, ry + 7, str(cell))
            cx += col_w[ci]
    return y - rh * (len(rows) + 1)


# ── Cover ─────────────────────────────────────────────────────────────────────

# SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
# and spliced in by rebuild_covers.py. This function is retained so a from-source
# rebuild still produces a complete document; run rebuild_covers.py afterwards.
def cover(c):
    pg_bg(c)
    c.setFillColor(OG)
    c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG)
    c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG)
    c.circle(W - 20, H - 105, 45, fill=1, stroke=0)

    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')

    bw, bh2 = c.stringWidth('GUIDE 01 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG)
    c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 01 OF 23')

    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude on the Web')
    c.setFillColor(OGL)
    c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, "Your Complete Beginner's Guide to claude.ai")

    c.setStrokeColor(OG)
    c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)

    box_top = H - 230
    box_h = 190
    c.setFillColor(PNL)
    c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")

    bullets = [
        'Create your free Claude account in under 3 minutes',
        'Understand Free, Pro, Max and Team plan differences',
        'Tour the claude.ai interface — every button explained',
        '10 hands-on things to try in your very first session',
        'Pro tips for better results and smarter conversations',
        'Quick reference cheat sheet and troubleshooting guide',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        c.drawString(MX + 30, by, b)
        by -= 27

    c.setFillColor(MGR)
    c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Perfect for: Complete beginners  •  No coding required  •  All platforms')

    c.setFillColor(OG)
    c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Why This Matters ──────────────────────────────────────────────────

def page2(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 2)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Why This Matters')

    c.setFillColor(LGR)
    c.setFont('Helvetica', 11)
    intro = ('Claude is one of the most capable AI assistants available today — built by '
             'Anthropic with a focus on helpfulness, harmlessness, and honesty. The claude.ai '
             'website is the fastest way to start: no downloads, no setup, just open a browser '
             'and start talking.')
    y -= 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, y, line)
        y -= 17
    y -= 12

    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, "What You'll Learn")
    y -= 22

    learns = [
        ('Set up your account',    'From sign-up to first conversation in minutes'),
        ('Navigate the interface', 'Know every button, panel, and option'),
        ('Choose the right plan',  'Free vs Pro vs Max — what each is worth'),
        ('Get real results fast',  '10 hands-on prompts to try immediately'),
        ('Work smarter',           'Tips most users only discover after months'),
    ]
    for title, desc in learns:
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 10, y, f'▸  {title}')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        c.drawString(MX + 168, y, f'— {desc}')
        y -= 18
    y -= 10

    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Who This Is For')
    y -= 22

    audience = [
        'Anyone curious about AI who has never tried Claude before',
        'People who have used Claude but want to get more out of it',
        'Professionals wanting to speed up writing, research, or analysis',
        'Students, creators, and anyone who works with text and ideas',
    ]
    for item in audience:
        c.setFillColor(GRN)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 10, y, '✓')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        c.drawString(MX + 26, y, item)
        y -= 18
    y -= 12

    info_panel(c, MX, y, 'Before You Start — What You Need', [
        'A device with internet access (computer, tablet, or phone)',
        'Any modern web browser: Chrome, Firefox, Safari, or Edge',
        'An email address to create your account (or Google/Apple login)',
        'No prior AI experience or technical knowledge required',
    ], CW)
    c.showPage()


# ── Page 3: Setting Up Your Account ──────────────────────────────────────────

def page3(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 3)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Setting Up Your Account')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Getting started takes less than 3 minutes:')

    steps = [
        ('Open Your Browser', [
            'Navigate to claude.ai in any modern web browser.',
            'The page loads instantly — no plugin or app download needed.',
        ]),
        ('Create Your Account', [
            'Click "Sign up" in the top right corner of the page.',
            'Enter your email, or continue with Google or Apple account.',
            'Check your inbox and click the verification link Anthropic sends.',
        ]),
        ('Complete Your Profile', [
            'Enter your name when Claude prompts you.',
            'Answer the optional role question — helps Claude tailor responses.',
            'You can skip this and update it later in Settings.',
        ]),
        ('Choose Your Plan', [
            'You start on the Free plan automatically — no credit card needed.',
            'Explore freely and upgrade anytime from the left sidebar.',
            'Free gives plenty of usage to experience everything Claude offers.',
        ]),
        ('Start Your First Chat', [
            'Click the message box at the bottom of the screen.',
            'Type your first question and press Enter or click the arrow.',
            'Claude responds in seconds. Your AI journey has begun.',
        ]),
    ]

    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    tip_lines = wrap(
        'Sign up with Google or Apple to skip email verification entirely — '
        'one click and you are in. One less password to manage.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Sign Up Faster', tip_lines, CW)
    c.showPage()


# ── Page 4: Understanding the Plans ──────────────────────────────────────────

def page4(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 4)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Understanding the Plans')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, "Claude offers five tiers. Here's exactly what each gives you:")

    headers = ['Plan', 'Price', 'Limits', 'Key Features']
    rows = [
        ['Free',     '$0/mo',    'Daily rolling', 'Sonnet 4.6, web search, file uploads, Artifacts, memory'],
        ['Pro',      '$20/mo',   '5× Free',  'All Free + Opus 4.7, Projects, Research mode, Voice, Cowork, MS365'],
        ['Max 5×',  '$100/mo',  '5× Pro', 'Same features as Pro — higher usage for heavy users'],
        ['Max 20×', '$200/mo',  '20× Pro', 'Same features as Pro — highest usage ceiling available'],
        ['Team',     '$25+/seat', 'Per seat',    'Org-wide access, shared projects, admin controls'],
    ]
    col_w = [62, 64, 62, CW - 188]
    y = y - 58
    y = tbl(c, MX, y, headers, rows, col_w)
    y -= 14

    # Side-by-side panels
    cw2 = (CW - 10) / 2
    panel_h = 194

    free_items = [
        ('✓', GRN, 'Claude Sonnet 4.6 (fast, balanced model)'),
        ('✓', GRN, 'Web search built in — toggle in message box'),
        ('✓', GRN, 'File uploads: PDF, images, CSV, code files'),
        ('✓', GRN, 'Artifacts: live previews of code and documents'),
        ('✓', GRN, 'Memory: notes persist across sessions'),
        ('✗', MGR, 'No Projects or Claude Opus access'),
        ('✗', MGR, 'Daily rolling usage limits apply'),
    ]
    pro_items = [
        ('✓', GRN, 'Everything in Free, plus:'),
        ('✓', GRN, 'Claude Opus 4.7 (most capable model)'),
        ('✓', GRN, 'Unlimited Projects — persistent workspaces'),
        ('✓', GRN, 'Research mode — deep multi-step web analysis'),
        ('✓', GRN, 'Voice mode — talk to Claude hands-free'),
        ('✓', GRN, 'Cowork — collaborate with others in real time'),
        ('✓', GRN, 'Microsoft 365 integration (Excel, PowerPoint, Word)'),
    ]

    for panel_x, panel_title, items in [
        (MX, 'Free Plan — What You Get', free_items),
        (MX + cw2 + 10, 'Pro Plan ($20/mo) — What You Get', pro_items),
    ]:
        c.setFillColor(PNL)
        c.roundRect(panel_x, y - panel_h, cw2, panel_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(panel_x + 10, y - 18, panel_title)
        iy = y - 38
        for mark, col, text in items:
            c.setFillColor(col)
            c.setFont('Helvetica', 10)
            c.drawString(panel_x + 10, iy, f'{mark}  {text}')
            iy -= 22

    y -= panel_h + 12

    tip_lines = wrap(
        'Start on Free and explore. If you hit usage limits daily or need Projects '
        'and Opus 4.7, upgrade to Pro at $20/month. Move to Max only when you '
        'consistently exhaust Pro limits.',
        10, CW - 28)
    tip_box(c, MX, y, 'When Should You Upgrade?', tip_lines, CW)
    c.showPage()


# ── Page 5: 10 Things to Try ─────────────────────────────────────────────────

def page5(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 5)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, '10 Things to Try in Your First Session')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Copy any of these prompts directly into Claude:')

    things = [
        ('Explain Something Complex',  '"Explain how the internet works to a 10-year-old"'),
        ('Summarize a Document',       'Upload PDF → type: "Summarize the key points"'),
        ('Write With You',             '"Help me write a professional email declining a meeting"'),
        ('Challenge Your Thinking',    '"What are the flaws in this argument: [paste text]"'),
        ('Live Web Research',          'Toggle search → "What is happening with [topic] in 2026?"'),
        ('Brainstorm Ideas',           '"Give me 20 name ideas for a pet grooming business"'),
        ('Edit Your Writing',          '"Make this paragraph more concise: [paste text]"'),
        ('Write Simple Code',          '"Write Python to rename all files in a folder by date"'),
        ('Build an Artifact',          '"Create a dark-theme HTML to-do list app"'),
        ('Get Feedback',               '"Review this resume bullet and suggest improvements: [paste]"'),
    ]

    cw2 = (CW - 10) / 2
    card_h, gap = 46, 7
    row_y = y - 60

    for i, (title, prompt) in enumerate(things):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + gap
        cx = MX + col * (cw2 + 10)

        c.setFillColor(PNL)
        c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG)
        c.roundRect(cx + 8, row_y - card_h + 10, 22, 22, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT)
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(cx + 19, row_y - card_h + 17, str(i + 1))
        c.setFillColor(CREAM)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(cx + 36, row_y - 17, title)
        c.setFillColor(MGR)
        c.setFont('Helvetica', 8)
        pt = prompt if len(prompt) <= 54 else prompt[:51] + '…'
        c.drawString(cx + 36, row_y - 31, pt)

    y = row_y - card_h - 14

    tip_lines = [
        'Claude remembers your whole conversation — build on earlier answers without repeating context.',
        'Use Projects (Pro) to keep persistent context across many sessions on the same topic.',
    ]
    tip_box(c, MX, y, 'Make Every Session Count', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference Cheat Sheet ──────────────────────────────────────

def page6(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 6)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude on the Web')
    y -= 40

    cw2 = (CW - 10) / 2

    left_items = [
        ('New conversation',    'Pencil icon — top left of the sidebar'),
        ('Upload a file',       'Paperclip icon in the message input box'),
        ('Enable web search',   'Globe icon in the message input box'),
        ('Switch AI model',     'Model name dropdown at top of chat'),
        ('Create a Project',    'Left sidebar → New Project (Pro plan)'),
        ('Use voice mode',      'Microphone icon in message box (Pro)'),
        ('View Artifacts',      'Right panel — appears for code/HTML output'),
        ('Export conversation', 'Three-dots menu → Export'),
    ]
    url_items = [
        ('Main app',       'claude.ai'),
        ('Pricing',        'claude.ai/pricing'),
        ('Desktop app',    'claude.ai/download'),
        ('API console',    'console.anthropic.com'),
        ('Mobile app',     'App Store / Google Play → "Claude"'),
        ('Status',         'status.anthropic.com'),
        ('Help center',    'support.anthropic.com'),
        ('Docs',           'docs.anthropic.com'),
    ]

    for px, panel_title, items in [
        (MX,          'Essential Actions', left_items),
        (MX + cw2 + 10, 'Key URLs & Resources', url_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL)
        c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM)
            c.setFont('Helvetica-Bold', 9)
            c.drawString(px + 10, iy, a)
            c.setFillColor(MGR if px == MX else OGL)
            c.setFont('Helvetica', 9)
            c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16

    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Common Issues & Quick Fixes')
    y -= 8

    t_rows = [
        ['Hit usage limit',       'Wait for the 5-hour rolling reset, or upgrade your plan'],
        ['Response cut off',      'Type "continue" — Claude will pick up where it stopped'],
        ['Getting wrong answers', 'Ask Claude to think step-by-step or cite its sources'],
        ['Slow response',         'Switch from Opus to Sonnet for faster replies on simple tasks'],
        ['Lost a conversation',   'Search the left sidebar — all chats are saved automatically'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Solution'], t_rows, [148, CW - 148])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL)
    c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 02 — Claude Mobile App (iOS & Android)')
    c.setFillColor(MGR)
    c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 01 of 20')
    cover(cv)
    page2(cv)
    page3(cv)
    page4(cv)
    page5(cv)
    page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
