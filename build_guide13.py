#!/usr/bin/env python3
"""Guide 13: How Agentic Loops Work — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_13_AgenticLoops.pdf'
GUIDE = 'How Agentic Loops Work'

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
    pad = 10; lh = 14
    bh = len(lines) * lh + pad * 2
    c.setFillColor(CODE_BG); c.roundRect(x, y - bh, w, bh, radius=4, fill=1, stroke=0)
    c.setStrokeColor(OG); c.setLineWidth(0.5)
    c.roundRect(x, y - bh, w, bh, radius=4, fill=0, stroke=1)
    ty = y - pad - 10
    for line in lines:
        col = MGR if line.strip().startswith('#') else GRN
        c.setFillColor(col); c.setFont('Courier', 10)
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
    bw, bh2 = c.stringWidth('GUIDE 13 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 13 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 28)
    c.drawString(MX, H - 175, 'Agentic Loops')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'How Claude Plans, Acts, Decides — and When to Stop')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'The 4-step agentic loop: receive → evaluate → tool call → repeat',
        'How Claude decides which tool to call next at each step',
        'All stopping conditions: task complete, max turns, budget exceeded',
        'Why context grows with each iteration — and how to manage it',
        'Context compaction with /compact — 60-80% reduction explained',
        'Cost control: max-turns flag, budget caps, and model selection',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Claude Code CLI  •  Works with all Claude Code projects  •  Any OS')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Is an Agentic Loop ──────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is an Agentic Loop?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('A single Claude response is just a reply. An agentic loop is what happens '
             'when Claude takes multiple actions — reading files, running commands, '
             'writing code — to complete a goal that cannot be done in one step. '
             'Claude plans, acts, sees what happened, and decides what to do next, '
             'repeating until the task is complete or a stopping condition is met.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The 4-Step Loop — Repeated Until Done')
    y -= 14

    loop_steps = [
        ('1  RECEIVE',   'Claude receives your prompt plus the full conversation history,',
         '             system instructions, and available tool definitions.'),
        ('2  EVALUATE',  'Claude decides what to do: answer directly, call a tool,',
         '             or call multiple tools in sequence or parallel.'),
        ('3  TOOL CALL', 'Claude calls a tool (Read, Edit, Bash, Grep, etc.).',
         '             The tool runs, and its output is appended to the history.'),
        ('4  DECIDE',    'Claude receives the tool result and decides again:',
         '             call another tool, or respond to you with a final answer.'),
    ]

    for label, line1, line2 in loop_steps:
        ph = 52
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        badge_col = OG
        c.setFillColor(badge_col); c.roundRect(MX + 8, y - 40, 58, 28, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(MX + 37, y - 23, label)
        c.setFillColor(CREAM); c.setFont('Helvetica', 10)
        c.drawString(MX + 74, y - 18, line1)
        c.setFillColor(MGR); c.setFont('Helvetica', 10)
        c.drawString(MX + 74, y - 33, line2)
        y -= ph + 6

    y -= 6
    info_panel(c, MX, y, 'The Loop Is Not Infinite — Stopping Conditions', [
        'Claude calls the Stop tool to signal the task is complete.',
        'The --max-turns limit is reached (configurable, default is high).',
        'The token budget (max_budget_usd) is exceeded.',
        'A PreToolUse hook exits with code 2, which blocks the tool call.',
        'You press Escape or Ctrl+C to interrupt mid-loop.',
    ], CW)
    c.showPage()


# ── Page 3: Tool Selection Decision ──────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'How Claude Decides What to Do Next')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('At each step, Claude evaluates the full conversation history — every '
             'prompt, every tool call, every result — and picks the best next action. '
             'This is a model-driven decision, not a programmed flowchart. Claude '
             'reasons about what it knows, what it still needs, and which tool '
             'will get it there.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Available Tools in the Loop')
    y -= 14
    tools = [
        ('Read',    'Read the contents of a file'),
        ('Write',   'Create or overwrite a file'),
        ('Edit',    'Make a targeted change to an existing file'),
        ('Bash',    'Run a shell command and capture output'),
        ('Grep',    'Search file contents for a pattern'),
        ('Glob',    'Find files matching a name pattern'),
        ('Agent',   'Spawn a subagent to handle a parallel task'),
        ('WebFetch','Fetch content from a URL'),
    ]
    for tool, desc in tools:
        c.setFillColor(PNL2); c.roundRect(MX, y - 24, CW, 24, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier-Bold', 10); c.drawString(MX + 10, y - 15, tool)
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 80, y - 15, desc)
        y -= 28

    y -= 8
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'A Typical Loop Trace — "Fix the broken test"')
    y -= 14
    trace = [
        ('Turn 1', 'Read',   'Read the failing test file to understand the error'),
        ('Turn 2', 'Read',   'Read the source file the test is testing'),
        ('Turn 3', 'Bash',   'Run the test suite to see the actual error output'),
        ('Turn 4', 'Edit',   'Apply the fix to the source file'),
        ('Turn 5', 'Bash',   'Run the tests again to verify the fix works'),
        ('Turn 6', 'Stop',   'Report to you: "Tests passing. Fixed on line 42."'),
    ]
    for turn, tool, action in trace:
        c.setFillColor(PNL); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 15, turn)
        c.setFillColor(OG); c.setFont('Courier-Bold', 9); c.drawString(MX + 56, y - 15, tool)
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 110, y - 15, action)
        y -= 30
    c.showPage()


# ── Page 4: Context Growth & Compaction ──────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Context Growth — The Hidden Cost of Loops')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Every tool call adds output to the conversation history. That history is '
             're-sent to the model on every subsequent call. A loop that reads ten '
             'large files can accumulate 50,000+ input tokens by iteration 20 — '
             'and each iteration costs more than the last.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 12

    # Context growth illustration
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'How Context Accumulates Per Iteration')
    y -= 14
    growth = [
        ('Iteration 1',  '~2,000 tokens',   'Prompt + system + first tool result'),
        ('Iteration 5',  '~8,000 tokens',   'History of 4 tool calls added'),
        ('Iteration 10', '~18,000 tokens',  'Still manageable, but growing fast'),
        ('Iteration 20', '~50,000+ tokens', 'Expensive — consider /compact now'),
    ]
    for it, tokens, note in growth:
        c.setFillColor(PNL); c.roundRect(MX, y - 28, CW, 28, radius=3, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y - 17, it)
        c.setFillColor(GRN if 'manageable' in note or '2,000' in tokens else AMB)
        c.setFont('Courier-Bold', 10); c.drawString(MX + 110, y - 17, tokens)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 230, y - 17, note)
        y -= 32
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Context Compaction — How /compact Works')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    compact_desc = ('When you type /compact, Claude generates a concise summary of the '
                    'conversation history — capturing key decisions, file changes, and '
                    'current state — and replaces the full history with that summary. '
                    'This typically reduces context by 60–80%, lowering cost immediately.')
    for line in wrap(compact_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    info_panel(c, MX, y, 'Compaction Keeps', [
        '✓  Key decisions made during the session',
        '✓  File paths that were read or edited',
        '✓  Error messages and their resolutions',
        '✓  The current state of the task',
        '✗  Raw file contents that were read (they are re-read if needed)',
        '✗  Repetitive tool outputs that add no new information',
    ], CW)
    y -= 118

    warn_lines = wrap(
        'Compaction is not automatic by default. Run /compact manually when you '
        'see high token usage (/status) or when the loop starts getting slow.',
        10, CW - 28)
    warn_box(c, MX, y, 'Compaction Is Manual — Watch Your Token Usage', warn_lines, CW)
    c.showPage()


# ── Page 5: Cost Control ──────────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Cost Control for Agentic Loops')
    y -= 40

    strategies = [
        ('Use /compact Before Long Tasks',
         'Before starting a complex multi-step task, run /compact to clear old history.',
         'Saves: removes irrelevant context so Claude focuses on the current task.'),
        ('Check Token Usage with /status',
         'Type /status at any time to see current token count and estimated cost.',
         'If you see the count climbing fast, run /compact or add stopping criteria.'),
        ('Set Explicit Stopping Criteria',
         'In your prompt: "After making all edits, run the tests once and then stop."',
         'Claude follows explicit stop instructions — do not leave stopping open-ended.'),
        ('Use --max-turns Flag (SDK/API)',
         'When calling Claude Code programmatically: --max-turns 10',
         'Hard cap: Claude cannot take more than N tool calls regardless of task state.'),
        ('Use max_budget_usd (API)',
         'Set max_budget_usd in your API call to halt the loop if cost exceeds a limit.',
         'The most reliable cost safeguard for automated (unattended) loop runs.'),
        ('Interrupt with Escape',
         'Press Escape at any point to halt the current loop immediately.',
         'Use Ctrl+C to exit Claude Code entirely. Edits made so far are kept.'),
    ]

    for title, line1, line2 in strategies:
        card_h = 60
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - card_h, 4, card_h, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 16, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 14, y - 30, line1)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 14, y - 44, line2)
        y -= card_h + 6

    tip_lines = wrap(
        'For unattended runs (e.g. overnight automation), always set max_budget_usd. '
        'An unexpected infinite loop can be very costly without a spend cap.',
        10, CW - 28)
    tip_box(c, MX, y, 'Always Cap Unattended Runs', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Agentic Loops')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Check token usage',   '/status'),
        ('Compact context',     '/compact  (60-80% reduction)'),
        ('Interrupt the loop',  'Escape key'),
        ('Exit Claude Code',    'Ctrl+C'),
        ('Set turn limit',      '--max-turns N  (CLI flag)'),
        ('Set spend cap',       'max_budget_usd  (API parameter)'),
        ('Spawn subagent',      'Happens automatically on parallel tasks'),
        ('View cost',           '/cost'),
    ]
    right_items = [
        ('Loop Step 1', 'Receive: prompt + history + tool defs'),
        ('Loop Step 2', 'Evaluate: what tool or response is best?'),
        ('Loop Step 3', 'Tool Call: run tool, append result to history'),
        ('Loop Step 4', 'Decide: next tool, or final answer?'),
        ('Stops when',  'Task complete / max-turns / budget / Escape'),
        ('Context risk','Every iteration adds tokens — use /compact'),
        ('Tools in loop','Read, Write, Edit, Bash, Grep, Glob, Agent'),
        ('Docs',        'docs.claude.com/agent-sdk/agent-loop'),
    ]

    for px, panel_title, items in [
        (MX, 'Commands & Flags', left_items),
        (MX + cw2 + 10, 'Loop Anatomy', right_items),
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
        ['Loop keeps going and not stopping', 'Add explicit stop instruction in your prompt'],
        ['Very high token count after 10 turns','Run /compact to summarise and reset context'],
        ['Claude misses earlier decisions',    'Earlier context was trimmed — use /compact sooner'],
        ['Want to halt without losing edits', 'Press Escape — edits already made are saved'],
        ['Unattended run cost too high',       'Set max_budget_usd in your API call'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [184, CW - 184])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 14 — MCP Servers 101')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 13 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
