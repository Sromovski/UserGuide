#!/usr/bin/env python3
"""Guide 18: Claude API Basics — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_18_API.pdf'
GUIDE = 'Claude API Basics'

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
        col = MGR if (line.strip().startswith('#') or line.strip().startswith('//')) else GRN
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
    bw, bh2 = c.stringWidth('GUIDE 18 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 18 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Claude API Basics')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Get Your API Key, Make Your First Call, Understand Pricing')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Get your API key from console.anthropic.com in under 2 minutes',
        'Make your first API call with curl — no code required',
        'The same call in Python using the official Anthropic SDK',
        'Full model pricing table: Haiku 4.5, Sonnet 4.6, Opus 4.8',
        'Understanding tokens — what they are and how to estimate costs',
        'Rate limits, error codes, and prompt caching explained',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Pay-as-you-go  •  No subscription required  •  Python & curl examples')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Get an API Key ────────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Getting Your API Key')

    steps = [
        ('Create an Anthropic Console Account', [
            'Go to console.anthropic.com and sign up (or sign in).',
            'The Console is separate from claude.ai — it\'s the developer dashboard.',
            'Email verification required.',
        ]),
        ('Add a Payment Method', [
            'API access is pay-as-you-go — billed on usage, not a subscription.',
            'Go to Billing → Add payment method.',
            'Minimum top-up is $5 for new accounts.',
        ]),
        ('Generate an API Key', [
            'Go to API Keys in the left sidebar.',
            'Click "Create Key" → give it a name (e.g. "my-project").',
            'Copy the key immediately — it starts with sk-ant-...',
            'You cannot view the key again after this page closes.',
        ]),
        ('Store the Key Securely', [
            'Never paste the key into code or commit it to git.',
            'Store it as an environment variable: ANTHROPIC_API_KEY',
            'On Mac/Linux: add to ~/.zshrc or ~/.bashrc',
            'On Windows: add to System Environment Variables',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    y = code_block(c, MX, y, [
        '# Set the API key as an environment variable (Mac/Linux)',
        'export ANTHROPIC_API_KEY="sk-ant-your-key-here"',
        '',
        '# Windows PowerShell',
        '$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"',
    ], CW)
    y -= 12

    warn_lines = wrap(
        'Treat your API key like a password. If it is ever exposed (e.g. committed '
        'to a public repo), revoke it immediately in the Console and generate a new one.',
        10, CW - 28)
    warn_box(c, MX, y, 'API Key Security — Never Put It in Code', warn_lines, CW)
    c.showPage()


# ── Page 3: First API Call ────────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Your First API Call')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Two ways to call the API — pick whichever you are comfortable with:')
    y -= 56

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Option A — curl (no code needed, just a terminal)')
    y -= 14
    y = code_block(c, MX, y, [
        'curl https://api.anthropic.com/v1/messages \\',
        '  --header "x-api-key: $ANTHROPIC_API_KEY" \\',
        '  --header "anthropic-version: 2023-06-01" \\',
        '  --header "content-type: application/json" \\',
        '  --data \'{',
        '    "model": "claude-haiku-4-5-20251001",',
        '    "max_tokens": 1024,',
        '    "messages": [',
        '      {"role": "user", "content": "Hello, Claude!"}',
        '    ]',
        '  }\'',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Option B — Python with the Anthropic SDK')
    y -= 14
    y = code_block(c, MX, y, [
        '# Install the SDK first: pip install anthropic',
        'import anthropic',
        '',
        'client = anthropic.Anthropic()',
        '# Uses ANTHROPIC_API_KEY env var automatically',
        '',
        'message = client.messages.create(',
        '    model="claude-haiku-4-5-20251001",',
        '    max_tokens=1024,',
        '    messages=[',
        '        {"role": "user", "content": "Hello, Claude!"}',
        '    ]',
        ')',
        '',
        'print(message.content[0].text)',
    ], CW)
    y -= 12

    info_panel(c, MX, y, 'Key Request Parameters', [
        'model:       Which Claude model to use (see pricing page for IDs)',
        'max_tokens:  Maximum tokens in the response (cap, not target)',
        'messages:    Array of {role, content} turns (user, assistant, user...)',
        'system:      Optional — instructions that apply to the whole conversation',
        'temperature: 0.0 (focused/deterministic) to 1.0 (creative/varied) — default 1.0',
    ], CW)
    c.showPage()


# ── Page 4: Models & Pricing ──────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Models & Pricing (June 2026)')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'All prices are per million tokens. Verify current rates at console.anthropic.com/pricing')
    y -= 56

    # Model cards
    models = [
        ('claude-haiku-4-5-20251001',   'Haiku 4.5',   '$1.00',  '$5.00',  '200K',
         'Fast and affordable. Great for classification, extraction, and high-volume tasks.'),
        ('claude-sonnet-4-6',           'Sonnet 4.6',  '$3.00',  '$15.00', '1M',
         'Balanced performance and cost. Recommended default for most applications.'),
        ('claude-opus-4-8',             'Opus 4.8',    '$5.00',  '$25.00', '1M',
         'Highest capability. Use for complex reasoning, research, and long-context tasks.'),
    ]
    for model_id, name, inp, out, ctx, desc in models:
        mh = 82
        c.setFillColor(PNL); c.roundRect(MX, y - mh, CW, mh, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - mh, 4, mh, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 12); c.drawString(MX + 14, y - 16, name)
        c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 14, y - 30, model_id)
        # Price boxes
        for label, price, px in [('Input/M tokens', inp, MX + 14), ('Output/M tokens', out, MX + 150)]:
            c.setFillColor(PNL2); c.roundRect(px, y - 62, 120, 26, radius=3, fill=1, stroke=0)
            c.setFillColor(MGR); c.setFont('Helvetica', 8); c.drawString(px + 6, y - 45, label)
            c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(px + 6, y - 59, price)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9)
        c.drawString(MX + 290, y - 45, f'Context: {ctx}')
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(desc, 9, CW - 28)
        dy = y - 68
        for dl_line in dl[:1]:
            c.drawString(MX + 14, dy, dl_line); dy -= 13
        y -= mh + 8

    y -= 8
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Cost-Saving Features')
    y -= 8
    savings = [
        ['Prompt Caching',        '90% off input tokens on cache hits (after first call)'],
        ['Message Batches API',   '50% off all tokens — for async/non-urgent requests'],
        ['Haiku for high volume', '3x cheaper than Sonnet — great for classification tasks'],
        ['max_tokens tuning',     'Set max_tokens to what you actually need, not 4096'],
    ]
    tbl(c, MX, y, ['Feature', 'Benefit'], savings, [142, CW - 142])
    c.showPage()


# ── Page 5: Tokens, Limits & Error Handling ──────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Tokens, Rate Limits & Error Handling')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Understanding Tokens')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    tok_desc = ('A token is roughly 4 characters of English text, or 0.75 words. '
                '"Hello, world!" is about 4 tokens. Tokens are counted for both '
                'input (your prompt + system) and output (Claude\'s response). '
                'You pay for both.')
    for line in wrap(tok_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 6

    tok_examples = [
        ('Short message',     '~50 tokens',         'e.g. "Summarise this in one sentence"'),
        ('A typical prompt',  '~300-500 tokens',    'System + user message with context'),
        ('A page of text',    '~750 tokens',        'About 500 words'),
        ('A code file',       '~1,000-3,000 tokens','Depends on length and language'),
        ('1M context window', '~750,000 words',     'About 1,500 pages of text'),
    ]
    y -= 4
    tbl(c, MX, y, ['Type', 'Approx Tokens', 'Notes'], tok_examples, [120, 110, CW - 230])
    y -= len(tok_examples) * 22 + 44 + 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Rate Limits')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    rate_desc = ('Rate limits vary by tier. New accounts start on Tier 1. '
                 'Limits increase automatically as you spend more. Check current limits '
                 'in the Console under API → Limits.')
    for line in wrap(rate_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Error Codes')
    y -= 8
    errors = [
        ['401 Unauthorized',    'Invalid or missing API key — check ANTHROPIC_API_KEY'],
        ['429 Too Many Requests','Rate limit hit — add exponential backoff retry logic'],
        ['529 Overloaded',       'API overloaded — retry with backoff; try Haiku as fallback'],
        ['400 Bad Request',      'Invalid request format — check JSON structure and model ID'],
    ]
    y = tbl(c, MX, y, ['Error Code', 'Meaning & Fix'], errors, [138, CW - 138])
    y -= 14

    y = code_block(c, MX, y, [
        '# Simple retry with backoff (Python)',
        'import time, anthropic',
        'client = anthropic.Anthropic()',
        '',
        'for attempt in range(3):',
        '    try:',
        '        msg = client.messages.create(...)',
        '        break',
        '    except anthropic.RateLimitError:',
        '        time.sleep(2 ** attempt)  # 1s, 2s, 4s',
    ], CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude API')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Console URL',        'console.anthropic.com'),
        ('API base URL',       'api.anthropic.com/v1/messages'),
        ('SDK install',        'pip install anthropic'),
        ('Key env var',        'ANTHROPIC_API_KEY'),
        ('Haiku 4.5 price',   '$1 / $5 per 1M tokens (in/out)'),
        ('Sonnet 4.6 price',  '$3 / $15 per 1M tokens (in/out)'),
        ('Opus 4.8 price',    '$5 / $25 per 1M tokens (in/out)'),
        ('Cache hit price',   '10% of normal input rate'),
    ]
    right_items = [
        ('Haiku 4.5 ID',     'claude-haiku-4-5-20251001'),
        ('Sonnet 4.6 ID',    'claude-sonnet-4-6'),
        ('Opus 4.8 ID',      'claude-opus-4-8'),
        ('Context: Haiku',   '200K tokens'),
        ('Context: Sonnet',  '1M tokens'),
        ('Context: Opus',    '1M tokens'),
        ('Batches discount', '50% off — async/non-urgent only'),
        ('Pricing page',     'console.anthropic.com/pricing'),
    ]

    for px, panel_title, items in [
        (MX, 'Setup & Pricing', left_items),
        (MX + cw2 + 10, 'Model IDs & Context', right_items),
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
    qa_rows = [
        ['Do I need a Claude subscription?', 'No — API billing is separate via the Console'],
        ['Which model should I start with?', 'Haiku for speed/cost, Sonnet for balance, Opus for depth'],
        ['How do I estimate my cost?',       'Count tokens with anthropic.count_tokens() before calling'],
        ['Is there a free tier?',            'No permanent free tier — new accounts get a small credit'],
        ['What is prompt caching?',          'Cache your system prompt and pay 10% on repeat calls'],
    ]
    y = tbl(c, MX, y, ['Question', 'Answer'], qa_rows, [172, CW - 172])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 19 — Building Automations with Claude')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 18 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
