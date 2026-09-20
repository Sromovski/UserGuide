#!/usr/bin/env python3
"""Guide 19: Building Automations with Claude — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_19_Automations.pdf'
GUIDE = 'Building Automations with Claude'

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

def cover(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    bw, bh2 = c.stringWidth('GUIDE 19 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 19 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 26)
    c.drawString(MX, H - 175, 'Building Automations')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Scheduled Runs, API Triggers & GitHub Webhooks with Claude')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Claude Code Routines: cloud automation released April 2026',
        'Three trigger types: Scheduled, API endpoint, and GitHub webhook',
        'Build a daily digest automation — step-by-step walkthrough',
        'Traditional API pipeline: cron + API call + webhook pattern',
        'Alert-response automation: monitoring tool triggers Claude on error',
        'Cost and safety controls for unattended automations',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires Claude Code + Anthropic API key  •  Works on any OS')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Are Routines ─────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Claude Code Routines — Cloud Automation')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Claude Code Routines (launched April 2026) move automated tasks to the cloud. '
             'Write a prompt, connect a repository, set a trigger, and the task runs '
             'automatically on Anthropic\'s infrastructure — even when your laptop is closed. '
             'No servers to manage, no cron daemons to babysit.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'What a Routine Is', [
        'A routine = saved Claude Code config + prompt + repos/connectors + trigger',
        'When triggered: Anthropic starts a Claude Code container, runs your prompt,',
        '  then persists artifacts or posts results via webhook.',
        'Think of it as a scheduled agentic session that runs itself.',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Three Trigger Types')
    y -= 14

    triggers = [
        ('SCHEDULED',  OG,
         'Hourly, Daily, Weekday, or Weekly',
         'Set a time in your local timezone. Anthropic runs the routine at that time automatically.',
         'Use for: daily digest, weekly report, nightly cleanup, morning standup'),
        ('API',        OGL,
         'POST request to routine endpoint',
         'Each routine gets its own HTTP endpoint with a dedicated bearer token. Call it from '
         'any tool, webhook, or script to trigger Claude immediately.',
         'Use for: monitoring alert response, form submission processing, event-driven tasks'),
        ('GITHUB',     GRN,
         'Repository events (push, PR, issue)',
         'Subscribe a routine to GitHub events. Every matching event starts its own Claude session.',
         'Use for: auto-label issues, review PRs, respond to failing CI, triage bug reports'),
    ]

    for label, color, timing, desc, use_for in triggers:
        ch = 86
        c.setFillColor(PNL); c.roundRect(MX, y - ch, CW, ch, radius=4, fill=1, stroke=0)
        c.setFillColor(color); c.roundRect(MX + 8, y - 28, 70, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8); c.drawCentredString(MX + 43, y - 15, label)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 86, y - 14, timing)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(desc, 9, CW - 20)
        dy = y - 32
        for dl_line in dl[:2]:
            c.drawString(MX + 12, dy, dl_line); dy -= 13
        c.setFillColor(MGR); c.setFont('Helvetica-Oblique', 9); c.drawString(MX + 12, y - 72, use_for)
        y -= ch + 6
    c.showPage()


# ── Page 3: Create a Scheduled Routine ───────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Create a Scheduled Routine — Daily Digest Example')

    steps = [
        ('Open Routines in Claude Code', [
            'In Claude Code, type /routines to open the Routines panel.',
            'Click "New Routine".',
        ]),
        ('Write Your Prompt', [
            'This is what Claude will run each time the routine triggers.',
            'Be specific about the task and the expected output format.',
            'Example: "Read the GitHub issues opened in the last 24 hours.',
            '  Summarise the top 5 by activity. Post a Slack message to #daily-digest."',
        ]),
        ('Connect a Repository & Connectors', [
            'Select the GitHub repo Claude should have access to.',
            'Add any Connectors needed (e.g. Slack MCP to post output).',
        ]),
        ('Set the Trigger', [
            'Choose Scheduled → Daily → 08:00 AM (your timezone).',
            'Save the routine — it appears in your Routines list.',
        ]),
        ('Monitor the First Run', [
            'A session log appears in the Routines panel after the first run.',
            'Open it to see exactly what Claude did and what it produced.',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 5

    y -= 8
    tip_lines = wrap(
        'Write your routine prompt the same way you\'d brief a smart assistant: '
        'specify the data source, the task, the output format, and where to send it. '
        'Claude reads all of these literally — be precise.',
        10, CW - 28)
    tip_box(c, MX, y, 'Write the Routine Prompt Like a Clear Brief', tip_lines, CW)
    c.showPage()


# ── Page 4: API & GitHub Triggers ─────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'API Triggers & GitHub Automation')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'API Trigger — Fire a Routine from Any Tool')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y,
                 'Each routine gets a unique HTTP endpoint. POST to it to start a session:')
    y -= 14
    y = code_block(c, MX, y, [
        '# Fire a routine via API (e.g. from a monitoring alert)',
        'curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01ABC.../fire \\',
        '  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \\',
        '  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \\',
        '  -H "anthropic-version: 2023-06-01" \\',
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"text": "Sentry alert SEN-4521 fired in production."}\'',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Alert-Response Automation — End-to-End Pattern')
    y -= 14
    flow = [
        'Monitoring tool detects an error threshold breach',
        'Tool POSTs to the routine API endpoint with alert details',
        'Claude Code starts in the cloud, reads alert text',
        'Claude pulls the stack trace from your GitHub repo',
        'Claude correlates errors with recent commits (git log)',
        'Claude opens a draft PR with a proposed fix + link to alert',
        'Team receives Slack notification with PR link',
    ]
    for i, step in enumerate(flow):
        c.setFillColor(PNL2); c.roundRect(MX, y - 24, CW, 24, radius=3, fill=1, stroke=0)
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 14, str(i + 1))
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 26, y - 14, step)
        y -= 28
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'GitHub Trigger — React to Repo Events')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Subscribe a routine to GitHub events. Examples:')
    y -= 14
    gh_examples = [
        ('issues.opened',   'Auto-label new issues based on content, assign to correct team member'),
        ('pull_request',    'Review the diff, check for tests, post a structured review comment'),
        ('workflow_run',    'If CI fails, pull logs and open a draft PR with the fix'),
        ('push (to main)',  'Update changelog, notify Slack, trigger a doc rebuild'),
    ]
    for event, action in gh_examples:
        c.setFillColor(PNL); c.roundRect(MX, y - 30, CW, 30, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier-Bold', 9); c.drawString(MX + 10, y - 10, event)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 22, action)
        y -= 34
    c.showPage()


# ── Page 5: API Pipeline (Traditional) ───────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Traditional API Pipeline Pattern')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'For full control, call the Claude API directly from your own script:')
    y -= 56

    y = code_block(c, MX, y, [
        '# Daily digest pipeline — Python',
        'import anthropic, json',
        'from datetime import date',
        '',
        'client = anthropic.Anthropic()',
        '',
        'def run_daily_digest():',
        '    # 1. Gather data (replace with your actual data source)',
        '    data = fetch_todays_github_issues()  # your function',
        '',
        '    # 2. Call Claude',
        '    response = client.messages.create(',
        '        model="claude-haiku-4-5-20251001",  # fast + cheap for daily runs',
        '        max_tokens=512,',
        '        system="You are a concise technical summariser.",',
        '        messages=[{',
        '            "role": "user",',
        '            "content": f"Summarise these issues in 5 bullets:\\n{data}"',
        '        }]',
        '    )',
        '',
        '    # 3. Send result',
        '    summary = response.content[0].text',
        '    post_to_slack(summary)  # your function',
        '',
        'run_daily_digest()',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Scheduling Options')
    y -= 14
    schedulers = [
        ('Claude Code Routines',  'Easiest — configure in UI, runs on Anthropic cloud, no server needed'),
        ('cron (Mac/Linux)',      'Classic — add to crontab: 0 8 * * * python /path/digest.py'),
        ('Task Scheduler (Win)',  'Windows equivalent — Schedule task in Task Scheduler app'),
        ('GitHub Actions',       'Run on schedule: on: schedule: - cron: "0 8 * * *"'),
        ('Zapier / Make',        'No-code option — trigger Python webhook or call API via HTTP step'),
    ]
    for method, desc in schedulers:
        c.setFillColor(PNL2); c.roundRect(MX, y - 28, CW, 28, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 10, y - 10, method)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 32
    y -= 10

    warn_lines = wrap(
        'Always set max_tokens for automated runs — a runaway response without a cap '
        'can cost far more than expected. Also set max_budget_usd for Claude Code Routines '
        'to prevent cost spikes from unexpected input data.',
        10, CW - 28)
    warn_box(c, MX, y, 'Always Cap Automated Runs with max_tokens + Budget Limit', warn_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Automations')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Routines UI',         '/routines  in Claude Code'),
        ('Scheduled trigger',   'Hourly / Daily / Weekday / Weekly'),
        ('API trigger',         'POST to routine HTTP endpoint'),
        ('GitHub trigger',      'Subscribe to: push, PR, issues, CI events'),
        ('Beta header (API)',   'anthropic-beta: experimental-cc-routine-2026-04-01'),
        ('Cheap model for auto','claude-haiku-4-5-20251001'),
        ('Always set',          'max_tokens  and  max_budget_usd'),
        ('Routines docs',       'code.claude.com/docs/en/routines'),
    ]
    right_items = [
        ('Routine = ',          'prompt + repo + connectors + trigger'),
        ('Scheduled timing',    'Your local timezone, daily/weekly options'),
        ('API fire endpoint',   'api.anthropic.com/v1/claude_code/routines/{id}/fire'),
        ('GitHub events',       'issues, pull_request, push, workflow_run'),
        ('Traditional cron',    '0 8 * * * python /path/script.py'),
        ('GitHub Actions cron', 'schedule: - cron: "0 8 * * *"'),
        ('No-code option',      'Zapier / Make → HTTP call to API'),
        ('Session logs',        'Available in Routines panel after each run'),
    ]

    for px, panel_title, items in [
        (MX, 'Routines & Commands', left_items),
        (MX + cw2 + 10, 'Patterns & Endpoints', right_items),
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
        ['Routine doesn\'t trigger',    'Check timezone setting and trigger configuration in Routines panel'],
        ['Claude runs but no output',   'Add explicit output instructions: "Post result to Slack as a message"'],
        ['GitHub trigger fires too often','Narrow the event filter — use specific event types, not all events'],
        ['API trigger returns 401',      'Check bearer token — use the routine-specific token, not your main key'],
        ['Costs higher than expected',   'Add max_tokens + max_budget_usd; use Haiku for routine summarisation'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [174, CW - 174])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 20 — Prompting Masterclass  (Series Finale)')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 19 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
