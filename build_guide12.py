#!/usr/bin/env python3
"""Guide 12: Subagents & Hooks in Claude Code — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_12_Hooks.pdf'
GUIDE = 'Subagents & Hooks in Claude Code'

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
    bw, bh2 = c.stringWidth('GUIDE 12 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 12 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 28)
    c.drawString(MX, H - 175, 'Subagents & Hooks')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Automate and Enforce Rules in Your Agentic Loop')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What subagents are and when Claude spawns them automatically',
        'The 8 core hook lifecycle events: when they fire and what they can do',
        'PreToolUse: block or modify tool calls before they run',
        'PostToolUse: run linting and tests automatically after every edit',
        'Stop & Notification: alerts when Claude finishes or needs attention',
        'Complete settings.json hook configuration with working examples',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires Claude Code CLI  •  Configuration via settings.json  •  Any OS')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Subagents ─────────────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Subagents — Claude Working in Parallel')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('A subagent is a separate Claude instance that the main Claude spawns '
             'to handle a specific subtask. This allows Claude to divide complex '
             'work — researching in one thread while coding in another, or running '
             'multiple independent tasks simultaneously to finish faster.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 12

    info_panel(c, MX, y, 'When Does Claude Spawn a Subagent?', [
        'When a task can be parallelised: e.g. "write tests for all 5 modules at once"',
        'When a step requires deep focus in isolation from the main context',
        'When you explicitly use the Agent tool in Claude Code SDK',
        'When the agentic loop determines a subtask is better handled independently',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'How Subagents Work')
    y -= 14

    flow = [
        ('Main Claude receives a task', [
            'You prompt: "Add unit tests for the auth module and the user module".',
            'Claude decides this can run as two parallel subagents.',
        ]),
        ('Subagents are spawned', [
            'Each subagent gets its own context and tool access.',
            'They can read files, write code, and run commands independently.',
        ]),
        ('Results return to main Claude', [
            'Each subagent completes and sends its result back.',
            'Main Claude merges the results and presents a final answer.',
            'PostToolUse hooks fire after each subagent completes (SubagentStop event).',
        ]),
    ]
    for i, (title, lines) in enumerate(flow):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    y -= 8
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Subagent vs Main Agent — Key Differences')
    y -= 8
    t_rows = [
        ['Context',     'Full conversation history',         'Scoped to its subtask only'],
        ['Tools',       'All tools (Read, Edit, Bash, etc.)', 'Same tools — isolated scope'],
        ['Duration',    'Entire session',                    'One task then terminates'],
        ['Hook event',  'PostToolUse (Agent tool)',          'SubagentStop on completion'],
    ]
    tbl(c, MX, y, ['Aspect', 'Main Agent', 'Subagent'], t_rows, [96, 194, CW - 290])
    c.showPage()


# ── Page 3: Hook Events ───────────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The 8 Core Hook Lifecycle Events')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Claude Code has 30+ hook events. These 8 cover almost everything — set them in settings.json:')
    y -= 56

    events = [
        ('SessionStart',   'Once per session',
         'Fires when Claude Code starts. Good for loading context or welcome messages.'),
        ('SessionEnd',     'Once per session',
         'Fires when the session closes. Use for cleanup, logging, or cost summaries.'),
        ('UserPromptSubmit','Every turn',
         'Fires when you press Enter. Pre-process or validate your prompt before Claude sees it.'),
        ('PreToolUse',     'Every tool call',
         'Fires before any tool runs. Block dangerous commands, enforce permissions, log actions.'),
        ('PostToolUse',    'Every tool call',
         'Fires after a tool completes. Run linters, tests, or format code automatically.'),
        ('Stop',           'Every turn',
         'Fires when Claude finishes responding. Send notifications, trigger next steps.'),
        ('StopFailure',    'On API error',
         'Fires when the turn ends because of an API error — not a general failure hook.'),
        ('Notification',   'On specific events',
         'Fires for: permission_prompt, idle_prompt, auth_success, elicitation_dialog.'),
    ]

    for event, timing, desc in events:
        ph = 44
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.setFont('Courier-Bold', 11); c.drawString(MX + 12, y - 14, event)
        c.setFillColor(MGR); c.setFont('Helvetica', 9); c.drawString(MX + 12, y - 28, timing)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        dl = wrap(desc, 10, CW - 160)
        dy2 = y - 14
        for dl_line in dl:
            c.drawString(MX + 160, dy2, dl_line); dy2 -= 14
        y -= ph + 4

    y -= 6
    info_panel(c, MX, y, 'Where Hooks Are Configured', [
        '.claude/settings.json     — committed to git, shared with the team',
        '.claude/settings.local.json — gitignored, personal/machine-specific hooks only',
        'Both files load automatically. Local file values override shared file values.',
    ], CW)
    c.showPage()


# ── Page 4: Hook Configuration Examples ──────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Hook Configuration Examples')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Add these inside the "hooks" object in .claude/settings.json:')
    y -= 56

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Example 1 — Run ESLint after every file edit (PostToolUse)')
    y -= 14
    # A hook receives its context as JSON on stdin — there is no ${file} substitution
    # and no $CLAUDE_FILE_PATHS variable. Read the path with jq.
    y = code_block(c, MX, y, [
        '"PostToolUse": [',
        '  {',
        '    "matcher": "Edit|Write",',
        '    "hooks": [',
        '      {',
        '        "type": "command",',
        '        "command": "jq -r \'.tool_input.file_path\' | xargs npx eslint --fix",',
        '        "timeout": 30',
        '      }',
        '    ]',
        '  }',
        ']',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Example 2 — Block dangerous Bash commands (PreToolUse)')
    y -= 14
    y = code_block(c, MX, y, [
        '"PreToolUse": [',
        '  {',
        '    "matcher": "Bash",',
        '    "hooks": [',
        '      {',
        '        "type": "command",',
        '        "command": "python guard.py --check-command",',
        '        "timeout": 5',
        '      }',
        '    ]',
        '  }',
        ']',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Example 3 — Notify when Claude finishes (Stop)')
    y -= 14
    y = code_block(c, MX, y, [
        '"Stop": [',
        '  {',
        '    "matcher": "",',
        '    "hooks": [',
        '      {',
        '        "type": "command",',
        '        "command": "curl -d \'Claude is done\' ntfy.sh/my-topic"',
        '      }',
        '    ]',
        '  }',
        ']',
    ], CW)
    y -= 12

    tip_lines = wrap(
        'The "matcher" field filters which tools or events trigger the hook. '
        'Use "Edit|Write" to match file editing tools, "Bash" for shell commands, '
        'or "" (empty) to match everything.',
        10, CW - 28)
    tip_box(c, MX, y, 'Understanding the Matcher Field', tip_lines, CW)
    c.showPage()


# ── Page 5: Practical Patterns ────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Practical Hook Patterns')
    y -= 40

    patterns = [
        ('Auto-format on save',
         'PostToolUse + matcher "Edit|Write"',
         ['Run Prettier, Black, or gofmt after every file edit.',
          'Keeps code formatted without a separate format step.']),
        ('Auto-run tests after edits',
         'PostToolUse + matcher "Edit|Write|Bash"',
         ['Run pytest or npm test after code changes.',
          'If tests fail, the output feeds back to Claude automatically.']),
        ('Guard dangerous shell commands',
         'PreToolUse + matcher "Bash"',
         ['Check the command against a blocklist before running it.',
          'Return exit code 2 to block; 0 to allow.']),
        ('Desktop notification on completion',
         'Stop event',
         ['Send a system notification when Claude finishes a long task.',
          'Works with ntfy.sh (push), osascript (Mac), or notify-send (Linux).']),
        ('Log all file changes',
         'PostToolUse + matcher "Edit|Write"',
         ['Append a log entry (timestamp, file, brief description) to changes.log.',
          'Useful for auditing what Claude changed during a session.']),
        ('Cost summary on session end',
         'SessionEnd event',
         ['Print total tokens used and estimated cost when closing Claude.',
          'Helps track spending on long agentic sessions.']),
    ]

    for title, hook_type, lines in patterns:
        card_h = 58 + len(lines) * 14
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - card_h, 4, card_h, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, y - 16, title)
        c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 14, y - 30, hook_type)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        ly = y - 46
        for line in lines:
            c.drawString(MX + 14, ly, line); ly -= 14
        y -= card_h + 6
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Subagents & Hooks')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Shared config file',   '.claude/settings.json'),
        ('Personal config file', '.claude/settings.local.json'),
        ('Block a tool call',    'Hook returns exit code 2'),
        ('Non-blocking error',   'Hook returns exit code 1 (run continues)'),
        ('Allow a tool call',    'Hook returns exit code 0'),
        ('Match all tools',      '"matcher": ""  (empty string)'),
        ('Match file edits',     '"matcher": "Edit|Write"'),
        ('Match shell commands', '"matcher": "Bash"'),
        ('Timeout (default)',    '60 seconds per hook command'),
    ]
    right_items = [
        ('SessionStart',        'Session opens'),
        ('SessionEnd',          'Session closes'),
        ('UserPromptSubmit',    'You press Enter'),
        ('PreToolUse',          'Before any tool runs'),
        ('PostToolUse',         'After any tool completes'),
        ('Stop',                'Claude finishes a turn'),
        ('StopFailure',         'Turn ends from an API error'),
        ('Notification',        'Permission prompt, idle, auth events'),
    ]

    for px, panel_title, items in [
        (MX, 'Key Settings', left_items),
        (MX + cw2 + 10, 'When Hook Events Fire', right_items),
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
        ['Hook not running',           'Check settings.json syntax (must be valid JSON)'],
        ['Command not found in hook',  'Use full paths: /usr/bin/python3 not just python'],
        ['Hook runs but does nothing', 'Add echo statements to debug; check timeout value'],
        ['Want to skip a hook once',   'No skip option — hooks always run by design'],
        ['Block all writes to a dir',  'PreToolUse: read path from stdin JSON, exit 2'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [168, CW - 168])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 13 — How Agentic Loops Work')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 12 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
