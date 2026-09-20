#!/usr/bin/env python3
"""Guide 23: Claude Cost & Token Management — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_23_CostManagement.pdf'
GUIDE = 'Claude Cost & Token Management'

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

def step_card(c, x, y, num, title, lines, w):
    card_h = 48 + len(lines) * 15
    c.setFillColor(PNL); c.roundRect(x, y - card_h, w, card_h, radius=4, fill=1, stroke=0)
    c.setFillColor(OG); c.circle(x + 22, y - 24, 13, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 12)
    c.drawCentredString(x + 22, y - 28, str(num))
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 11)
    c.drawString(x + 44, y - 22, title)
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    ty = y - 40
    for line in lines:
        c.drawString(x + 44, ty, line); ty -= 15
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
    c.drawString(x + 14, y - pad - 10, f'WATCH OUT  {heading}')
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
        col = MGR if line.strip().startswith('#') else GRN
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
    bw, bh2 = c.stringWidth('GUIDE 23  — ADVANCED ADD-ON', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 23  — ADVANCED ADD-ON')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 26)
    c.drawString(MX, H - 175, 'Claude Cost & Token Management')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Keep Your AI Bills Predictable — and Cut Them by 90%')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'How token billing really works — input vs output, and what drives cost',
        '2026 price table for every model, cache hits, and Batch API',
        'Prompt caching: cut repeated-context cost by up to 90%',
        'Model routing: send easy work to Haiku, hard work to Opus',
        'Context windows: why long chats get expensive and how /compact helps',
        'Set hard budget caps and monitor spend before the bill surprises you',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'For API and Claude Code users  •  Pairs with Guide 18 (API) and Guide 13 (Agentic Loops)')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  The Complete Field Guide Series')
    c.showPage()


# ── Page 2: How billing works + price table ───────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'How Claude Billing Actually Works')
    y -= 44

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('The API charges by the token — roughly 3-4 characters, or about 0.75 words. '
             'Every request pays for input tokens (everything you send: prompt, context, '
             'history, tool results) plus output tokens (what Claude writes back). Output is '
             'the pricier half, and long conversations re-send the whole history every turn.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, '2026 Price Table (per 1M tokens)')
    y -= 6
    rows = [
        ['Haiku 4.5', '$1.00', '$5.00', '$0.10', 'Cheap, fast — routing & bulk'],
        ['Sonnet 4.6', '$3.00', '$15.00', '$0.30', 'Balanced default'],
        ['Opus 4.8', '$5.00', '$25.00', '$0.50', 'Hardest reasoning'],
    ]
    y = tbl(c, MX, y, ['Model', 'Input', 'Output', 'Cache hit', 'Best for'],
            rows, [78, 62, 66, 70, CW - 276])
    y -= 8
    c.setFillColor(MGR); c.setFont('Helvetica-Oblique', 9)
    c.drawString(MX, y, 'Cache hit = repeated cached input (90% off). Batch API = 50% off all of the above.')
    y -= 12
    c.drawString(MX, y, 'Prices as of July 2026 — always verify at platform.claude.com/pricing.')
    y -= 22

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The Four Things That Drive Your Bill')
    y -= 20
    drivers = [
        ('Model choice', 'Opus costs 5x Haiku on input, 5x on output. Match model to difficulty.'),
        ('Output length', 'The expensive half. Cap it with max_tokens and "be concise" instructions.'),
        ('Context size', 'Long history + big documents re-billed every single turn.'),
        ('Call volume', 'Agents and loops multiply calls. More turns = more tokens.'),
    ]
    for label, desc in drivers:
        ph = 30
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 19, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 120, y - 19, desc)
        y -= ph + 6
    y -= 4

    info_panel(c, MX, y, 'Subscription vs API — Two Separate Bills', [
        'claude.ai Pro/Max ($20-$200/mo) is a flat subscription for the chat apps.',
        'The API (console.anthropic.com) is pay-as-you-go, billed per token, separate.',
        'Claude Code can run on either a paid plan OR an API key — pick one.',
    ], CW)
    c.showPage()


# ── Page 3: The big cost levers ───────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The Big Cost Levers')
    y -= 42

    y = step_card(c, MX, y, 1, 'Prompt caching — up to 90% off', [
        'Reuse a large fixed prefix (system prompt, docs, examples) across calls.',
        'Cached input is billed at ~10% of normal. Huge win for agents and RAG.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Batch API — 50% off, not urgent', [
        'Submit many requests to process asynchronously (within ~24h).',
        'Every token is half price. Perfect for evals, bulk tagging, backfills.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 3, 'Model routing — right tool, right price', [
        'Triage with Haiku; escalate only hard cases to Sonnet or Opus.',
        'Most tasks do not need your most expensive model.',
    ], CW)
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Turn On Prompt Caching (Python SDK)')
    y -= 14
    y = code_block(c, MX, y, [
        '# Mark the big, stable prefix as cacheable',
        'client.messages.create(',
        '    model="claude-sonnet-4-6",',
        '    system=[{',
        '        "type": "text",',
        '        "text": LONG_SYSTEM_PROMPT,',
        '        "cache_control": {"type": "ephemeral"},   # <- caches it',
        '    }],',
        '    messages=[{"role": "user", "content": user_question}],',
        ')',
        '# Later calls with the same prefix pay ~10% on those tokens.',
    ], CW)
    y -= 12

    tip_box(c, MX, y, 'Order Your Prompt for Cache Hits', wrap(
        'Put the stable, reusable content FIRST (system prompt, documents, examples) and '
        'the changing content LAST (the user question). Caching only helps the unchanged '
        'prefix, so keep the moving parts at the end.', 10, CW - 28), CW)
    c.showPage()


# ── Page 4: Context windows & token growth ────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Context Windows & Runaway Token Growth')
    y -= 44

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('The context window is everything Claude can "see" at once — and every token in '
             'it is re-billed on every turn. A long agent run quietly grows its own context: '
             'by turn 20 a session can hold 50,000+ tokens of history, so each new turn costs '
             'far more than the first. Opus 4.8 and Sonnet 4.6 support a 1M-token window, but '
             'a bigger window is not a licence to fill it.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'How Context Grows in an Agent Loop')
    y -= 6
    rows = [
        ['Turn 1', '~2K tokens', 'Just the task and system prompt'],
        ['Turn 10', '~20K tokens', 'History + tool results pile up'],
        ['Turn 20', '~50K tokens', 'Every turn now re-bills all of it'],
        ['After /compact', '~10-20K', '60-80% smaller — summary replaces raw history'],
    ]
    y = tbl(c, MX, y, ['Point in run', 'Context size', 'What is in it'], rows, [120, 100, CW - 220])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Keep Context (and Cost) Under Control')
    y -= 20
    tactics = [
        ('/compact', 'Summarise the conversation so far — cuts context 60-80%.'),
        ('/clear', 'Start fresh when the topic changes — do not carry dead history.'),
        ('Scope inputs', 'Send only the files or rows Claude needs, not the whole repo.'),
        ('Subagents', 'Delegate noisy subtasks so their output never enters main context.'),
    ]
    for label, desc in tactics:
        ph = 30
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(PUR); c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Courier-Bold', 10); c.drawString(MX + 14, y - 19, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 110, y - 19, desc)
        y -= ph + 6
    y -= 4

    warn_box(c, MX, y, 'Loops Multiply Everything', wrap(
        'An agent that runs 30 turns on Opus over a growing 50K context can cost dollars per '
        'run. Always cap loops with --max-turns and a spend limit, and compact early. '
        'Unbounded loops are the #1 source of surprise bills.', 10, CW - 28), CW)
    c.showPage()


# ── Page 5: Budgeting & monitoring ────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Budgeting & Monitoring Spend')
    y -= 42

    y = step_card(c, MX, y, 1, 'Watch spend live in Claude Code', [
        'Run /cost to see the current session spend, and /status for context usage.',
        'Check them mid-task on long runs — do not wait for the invoice.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Cap agent runs with hard limits', [
        '--max-turns stops a loop after N iterations; a budget cap stops it by dollars.',
        'Set both so a stuck agent can never run away with your money.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 3, 'Set org limits in the Console', [
        'console.anthropic.com -> Usage & Limits: monthly spend caps and email alerts.',
        'Use separate API keys per project to see where the money actually goes.',
    ], CW)
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Cap a Run by Turns and Budget')
    y -= 14
    y = code_block(c, MX, y, [
        '# Claude Code — stop after 15 turns',
        'claude -p "refactor the auth module" --max-turns 15',
        '',
        '# API — count tokens BEFORE you send (free)',
        'client.messages.count_tokens(',
        '    model="claude-sonnet-4-6",',
        '    messages=[{"role": "user", "content": big_prompt}],',
        ')  # returns input_tokens so you can estimate cost first',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'A Quick Cost Estimate')
    y -= 6
    rows = [
        ['10K in + 2K out on Haiku', '$0.02', 'Cheap enough to ignore'],
        ['10K in + 2K out on Opus', '$0.10', '5x the Haiku cost'],
        ['Same, 90% cached input', '$0.055', 'Caching nearly halves it'],
        ['Same, via Batch API', '$0.05', 'Half price, async'],
    ]
    y = tbl(c, MX, y, ['Scenario', 'Approx cost', 'Note'], rows, [200, 90, CW - 290])
    y -= 14

    tip_box(c, MX, y, 'Estimate Before You Scale', wrap(
        'Multiply the per-call cost by your expected volume BEFORE you launch a batch job or '
        'a scheduled agent. A $0.10 call run 10,000 times is $1,000 — know that number first.',
        10, CW - 28), CW)
    c.showPage()


# ── Page 6: Quick reference + troubleshooting + CTA ───────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Cost Management Quick Reference')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Cheapest win',   'Prompt caching — up to 90% off'),
        ('Not urgent?',    'Batch API — 50% off all tokens'),
        ('Right-size',     'Haiku triages; Opus for hard only'),
        ('Output is dear', 'Cap max_tokens; ask for concise'),
        ('Context re-bills', 'Every turn pays for full history'),
        ('Shrink it',      '/compact cuts context 60-80%'),
        ('Cap loops',      '--max-turns + a dollar budget'),
        ('Estimate first', 'count_tokens before you scale'),
    ]
    right_items = [
        ('Haiku 4.5', '$1 / $5 per 1M (in / out)'),
        ('Sonnet 4.6', '$3 / $15 per 1M'),
        ('Opus 4.8', '$5 / $25 per 1M'),
        ('Cache hit', '~10% of input price (90% off)'),
        ('Batch API', 'Half price, async (~24h)'),
        ('See spend', '/cost  ·  /status in Claude Code'),
        ('Org limits', 'Console -> Usage & Limits'),
        ('Docs', 'platform.claude.com/pricing'),
    ]
    for px, panel_title, items in [
        (MX, 'Rules of Thumb', left_items),
        (MX + cw2 + 10, 'Prices & Levers', right_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL); c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(px + 10, iy, a)
            c.setFillColor(OGL); c.setFont('Helvetica', 9); c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Troubleshooting')
    y -= 6
    rows = [
        ['Bill higher than expected', 'Check output length + call volume; cap both'],
        ['Long chats getting slow/pricey', 'Run /compact or /clear to shrink context'],
        ['Caching not saving money', 'Put stable content first; changing parts last'],
        ['Agent ran away on cost', 'Add --max-turns and a spend budget cap'],
        ['Not sure what a job will cost', 'count_tokens x volume before you launch'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], rows, [210, CW - 210])
    y -= 20

    cta_h = 58
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 16, y - 20, 'Next in the series: Guide 24 — Security & Safety for Claude Workflows')
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 16, y - 38, 'Prompt injection, secrets in configs, permission scoping, and trusting MCP servers safely.')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 23 — Advanced Add-On: Claude Cost & Token Management')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
