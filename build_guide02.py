#!/usr/bin/env python3
"""Guide 02: Claude Mobile App (iOS & Android) — Claude AI Field Guide Series"""
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
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_02_Mobile.pdf'
GUIDE = 'Claude Mobile App'

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


def warn_box(c, x, y, heading, lines, w):
    pad = 10
    bh = len(lines) * 15 + pad * 2 + 20
    c.setFillColor(DBAMB)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(AMB)
    c.rect(x, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(AMB)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x + 14, y - pad - 10, f'NOTE  {heading}')
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

    bw, bh2 = c.stringWidth('GUIDE 02 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG)
    c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 02 OF 23')

    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude Mobile App')
    c.setFillColor(OGL)
    c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Your Complete Guide to Claude on iOS & Android')

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
        'Download and set up Claude on iPhone, iPad, or Android device',
        'Use voice mode — 5 voice personalities, hands-free conversation',
        'Point your camera at anything and ask Claude about it',
        'iOS-exclusive features: Siri Shortcuts and Reminders integration',
        'Android-exclusive features: home screen widgets and deep links',
        'Mobile use cases and quick reference for on-the-go AI',
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
    c.drawString(MX, H - 442, 'Perfect for: Beginners  •  iOS 16+ and Android  •  Free download')

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
    intro = ('The Claude mobile app brings the full power of Claude to your pocket. Whether '
             "you're commuting, traveling, or simply away from your desk, you can have a full "
             'AI conversation, analyze photos, draft messages, and get answers — all without '
             'touching a computer. As of 2026, iOS and Android apps are feature-complete.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line)
        iy -= 17
    y = iy - 10

    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, "What You'll Learn")
    y -= 22

    learns = [
        ('Download & install',    'Get the app on iPhone, iPad, or Android in minutes'),
        ('Navigate the app',      'Messages, Projects, settings — all explained'),
        ('Talk to Claude',        'Voice mode with 5 personalities, hands-free'),
        ('Use your camera',       'Point at anything — menus, signs, whiteboards, code'),
        ('Platform extras',       'iOS Siri Shortcuts, Android widgets, and more'),
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
        'Anyone who already uses claude.ai and wants Claude on their phone',
        'People who prefer voice over typing for AI conversations',
        'Travelers and professionals who need AI assistance on the go',
        'Anyone who wants to point a camera at something and ask questions',
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
        'An iPhone or iPad running iOS 16 or later',
        'An Android phone or tablet (Android 8.0 or later)',
        'An Anthropic account (free) — or create one during setup',
        'A working internet connection (Wi-Fi or mobile data)',
    ], CW)
    c.showPage()


# ── Page 3: Download & Setup ──────────────────────────────────────────────────

def page3(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 3)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Downloading & Setting Up')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'The app is free to download. Follow these steps for your device:')

    steps = [
        ('Open Your App Store', [
            'On iPhone/iPad: open the App Store.',
            'On Android: open the Google Play Store.',
            'Both are free and take under a minute to install.',
        ]),
        ('Search for Claude', [
            'Search for "Claude by Anthropic" — look for the orange logo.',
            'Tap Install (Android) or Get (iOS) to download.',
            'Wait for the download to complete, then tap Open.',
        ]),
        ('Sign In or Create an Account', [
            'Tap "Continue with Google" or "Continue with Apple" for fastest setup.',
            'Or enter your email and password if you already have an account.',
            'New users: tap "Sign up" and follow the on-screen steps.',
        ]),
        ('Allow Permissions', [
            'Microphone — required for voice mode (recommended: allow).',
            'Camera — required for photo analysis (recommended: allow).',
            'Notifications — optional but useful for conversation updates.',
        ]),
        ('Choose Your Plan', [
            'The app opens on the Free plan — no payment needed to start.',
            'Tap the menu icon to upgrade to Pro or Max at any time.',
            'Your plan syncs automatically with the web version.',
        ]),
    ]

    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    tip_lines = wrap(
        'If you already use claude.ai on the web, log in with the same account. '
        'All your conversations and Projects sync automatically across devices.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Sync Across Devices', tip_lines, CW)
    c.showPage()


# ── Page 4: Features — Voice & Camera ────────────────────────────────────────

def page4(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 4)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Key Mobile Features')
    y -= 40

    # Voice Mode section
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Voice Mode — Talk to Claude Hands-Free')
    y -= 20

    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    voice_intro = ('Voice mode lets you have a natural spoken conversation with Claude. '
                   'Tap the microphone icon in the message bar to start. Available on all '
                   'plans including Free.')
    for line in wrap(voice_intro, 10, CW):
        c.drawString(MX, y, line)
        y -= 15
    y -= 8

    # Voice personalities table
    headers = ['Voice', 'Character']
    rows = [
        ['Buttery', 'Warm, smooth, conversational — best for casual chats'],
        ['Airy',    'Light, upbeat, energetic — great for brainstorming'],
        ['Mellow',  'Calm, measured, relaxed — ideal for focused work'],
        ['Glassy',  'Clear, crisp, precise — best for technical topics'],
        ['Professional', 'Formal, confident — suited for business use'],
    ]
    y = tbl(c, MX, y, headers, rows, [90, CW - 90])
    y -= 10

    warn_lines = wrap(
        'Voice mode supports English only as of 2026. Switch to text for '
        'non-English languages. You can mix voice and text in the same conversation.',
        10, CW - 28)
    warn_box(c, MX, y, 'English Only', warn_lines, CW)
    y -= 70

    # Camera section
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Camera & Image Input')
    y -= 18

    c.setFillColor(LGR)
    c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Tap the camera/photo icon to attach an image. What you can do:')
    y -= 20

    camera_uses = [
        ('Snap a restaurant menu',    'Ask: "What dishes are vegetarian?" or "Translate this"'),
        ('Photograph a whiteboard',   'Ask: "Summarize the notes and action items"'),
        ('Point at a chart/graph',    'Ask: "Explain what this data shows"'),
        ('Scan a document',           'Ask: "Extract the key information from this form"'),
        ('Take a photo of code',      'Ask: "What does this code do?" or "Find the bug"'),
        ('Capture a sign (travel)',   'Ask: "Translate this and tell me what it means"'),
    ]
    cw2 = (CW - 10) / 2
    row_y = y
    card_h = 42
    for i, (title, use) in enumerate(camera_uses):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + 6
        cx = MX + col * (cw2 + 10)
        c.setFillColor(PNL)
        c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG)
        c.roundRect(cx + 8, row_y - card_h + 10, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(cx + 18, row_y - card_h + 17, str(i + 1))
        c.setFillColor(CREAM)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(cx + 34, row_y - 15, title)
        c.setFillColor(MGR)
        c.setFont('Helvetica', 8)
        ut = use if len(use) <= 54 else use[:51] + '…'
        c.drawString(cx + 34, row_y - 29, ut)
    c.showPage()


# ── Page 5: iOS vs Android + Use Cases ───────────────────────────────────────

def page5(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 5)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Platform Features & Mobile Use Cases')
    y -= 40

    # iOS vs Android comparison
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'iOS vs Android — Platform Differences')
    y -= 14

    cw2 = (CW - 10) / 2
    panel_h = 164

    ios_items = [
        ('✓', GRN, 'Siri Shortcuts — launch Claude actions by voice'),
        ('✓', GRN, 'Apple Reminders integration'),
        ('✓', GRN, 'Share Sheet — send any content to Claude'),
        ('✓', GRN, 'iPad-optimized split-screen layout'),
        ('✓', GRN, 'iCloud backup of app preferences'),
        ('✓', GRN, 'iOS 16+ required'),
    ]
    android_items = [
        ('✓', GRN, 'Home screen widgets for quick access'),
        ('✓', GRN, 'Third-party messaging app integration'),
        ('✓', GRN, 'Share menu — send content from any app'),
        ('✓', GRN, 'Back-tap shortcuts (Android 13+)'),
        ('✓', GRN, 'Works across all major Android manufacturers'),
        ('✓', GRN, 'Android 8.0+ required'),
    ]

    for px, panel_title, items in [
        (MX, 'iOS (iPhone & iPad)', ios_items),
        (MX + cw2 + 10, 'Android', android_items),
    ]:
        c.setFillColor(PNL)
        c.roundRect(px, y - panel_h, cw2, panel_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(px + 10, y - 18, panel_title)
        iy = y - 38
        for mark, col, text in items:
            c.setFillColor(col)
            c.setFont('Helvetica', 10)
            c.drawString(px + 10, iy, f'{mark}  {text}')
            iy -= 22

    y -= panel_h + 16

    # Mobile use cases
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, '8 Powerful Mobile Use Cases')
    y -= 14

    use_cases = [
        ('Morning briefing',        '"Summarize my day — I have a meeting at 9am on [topic]"'),
        ('Email on the go',         '"Write a polite reply declining this meeting request"'),
        ('Menu translator',         'Photo of menu → "What\'s in this dish? Any allergens?"'),
        ('Meeting notes',           'Whiteboard photo → "Create action items from these notes"'),
        ('Commute learning',        'Voice mode → "Teach me one new concept about investing"'),
        ('Quick research',          '"What are the pros and cons of [topic]?" (web search on)'),
        ('Travel help',             'Sign photo → "Translate and explain this sign"'),
        ('Brainstorm sessions',     'Voice mode → "Help me think through this decision: [topic]"'),
    ]

    row_y = y - 2
    card_h = 42
    cw2 = (CW - 10) / 2
    for i, (title, prompt) in enumerate(use_cases):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + 6
        cx = MX + col * (cw2 + 10)
        c.setFillColor(PNL)
        c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG)
        c.roundRect(cx + 8, row_y - card_h + 10, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT)
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(cx + 18, row_y - card_h + 17, str(i + 1))
        c.setFillColor(CREAM)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(cx + 34, row_y - 15, title)
        c.setFillColor(MGR)
        c.setFont('Helvetica', 8)
        pt = prompt if len(prompt) <= 54 else prompt[:51] + '…'
        c.drawString(cx + 34, row_y - 29, pt)

    y = row_y - card_h - 14
    tip_lines = wrap(
        'Enable notifications for Claude to get alerts when a long response finishes '
        'generating — useful when you switch apps mid-conversation.',
        10, CW - 28)
    tip_box(c, MX, y, 'Stay Updated While Multitasking', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c)
    hdr(c)
    ftr(c, 6)

    y = H - 30
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Mobile App')
    y -= 40

    cw2 = (CW - 10) / 2

    left_items = [
        ('Start voice conversation',  'Tap microphone icon in message bar'),
        ('Attach a photo',            'Tap camera icon → take photo or pick from gallery'),
        ('New conversation',          'Tap pencil/compose icon (top right)'),
        ('Switch AI model',           'Tap model name at top of screen'),
        ('Open a Project',            'Tap hamburger menu → Projects (Pro)'),
        ('Change voice personality',  'Voice mode → tap voice name to switch'),
        ('Share content to Claude',   'Any app → Share → Claude'),
        ('Access Settings',           'Tap your profile photo → Settings'),
    ]
    url_items = [
        ('Download (iOS)',      'App Store → search "Claude by Anthropic"'),
        ('Download (Android)',  'Google Play → search "Claude by Anthropic"'),
        ('Web version',        'claude.ai (syncs with mobile)'),
        ('Help center',        'support.anthropic.com'),
        ('iOS requirements',   'iOS 16 or later'),
        ('Android requirements','Android 8.0 or later'),
        ('Plan management',    'App menu → Manage Subscription'),
        ('Account settings',   'Profile photo → Settings → Account'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Actions', left_items),
        (MX + cw2 + 10, 'Downloads & Info', url_items),
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
        ['Voice mode not working',   'Check microphone permission: Settings → Privacy → Microphone'],
        ['Camera not available',     'Check camera permission: Settings → Privacy → Camera'],
        ['App not syncing',          'Check internet connection. Pull down on chat list to refresh'],
        ['Hit usage limit',          'Wait for the rolling reset or upgrade plan from app menu'],
        ['Conversations not showing','Sign out and back in — sync should restore all history'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Solution'], t_rows, [150, CW - 150])
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
    c.drawString(MX + 14, y - 33, 'Guide 03 — Claude Desktop App (Mac & Windows)')
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
    cv.setSubject('Guide 02 of 20')
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
