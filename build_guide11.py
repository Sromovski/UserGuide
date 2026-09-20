#!/usr/bin/env python3
"""Guide 11: CLAUDE.md Files — Build Plans That Work — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_11_CLAUDEmd.pdf'
GUIDE = 'CLAUDE.md Files — Build Plans That Work'

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
        col = MGR if line.startswith('#') else (OGL if line.startswith('##') else GRN)
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

def cover(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    bw, bh2 = c.stringWidth('GUIDE 11 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 11 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 28)
    c.drawString(MX, H - 175, 'CLAUDE.md Files')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Give Claude a Memory — Build Plans That Work Every Time')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What a CLAUDE.md file is and why Claude reads it automatically',
        'The 6 sections every effective CLAUDE.md must have',
        'How to write commands, architecture, and conventions Claude will follow',
        'The progressive disclosure trick that keeps your file under 200 lines',
        'CLAUDE.md vs hooks — when to use which for project rules',
        'A complete CLAUDE.md template you can copy and adapt today',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Works with any Claude Code project  •  Mac, Windows & Linux  •  No coding required')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Is CLAUDE.md ─────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is a CLAUDE.md File?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('CLAUDE.md is a plain Markdown file you place at the root of your project. '
             'Claude Code automatically reads it at the start of every session, before '
             'you type a single prompt. It gives Claude persistent project memory: '
             'your tech stack, your build commands, your architecture, and rules '
             'Claude should always follow — without you repeating them every time.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'The Key Insight', [
        'Claude Code has no memory between sessions by default.',
        'Every time you open a project, Claude starts fresh.',
        'CLAUDE.md is the fix: a persistent briefing that loads automatically.',
        'Think of it as writing a memo to Claude before every conversation.',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Where Claude Looks for CLAUDE.md Files')
    y -= 22
    locations = [
        ('~/CLAUDE.md',          'Home directory — applies to ALL your projects (global defaults)'),
        ('./CLAUDE.md',          'Project root — the main file for this project'),
        ('./src/CLAUDE.md',      'Subdirectory files — loaded when Claude works in that folder'),
        ('./.claude/CLAUDE.md',  'Hidden .claude folder — same as project root but keeps root clean'),
    ]
    for path, desc in locations:
        c.setFillColor(PNL); c.roundRect(MX, y - 30, CW, 30, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier-Bold', 10); c.drawString(MX + 10, y - 18, path)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 180, y - 18, '— ' + desc)
        y -= 34

    y -= 12
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Why It Matters for Agentic Work')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    reasons = [
        'Agentic loops (multi-step tasks) need project context to make good decisions.',
        'Without CLAUDE.md, Claude guesses at your conventions and often guesses wrong.',
        'A good CLAUDE.md reduces back-and-forth, keeps code consistent, and saves tokens.',
        'It is the difference between Claude as a smart autocomplete and Claude as a team member.',
    ]
    for r in reasons:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 10, y, '▸')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, y, r)
        y -= 16
    c.showPage()


# ── Page 3: The 6 Essential Sections ─────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The 6 Sections Every Effective CLAUDE.md Needs')
    y -= 40

    sections = [
        ('Tech Stack',        [
            'Framework, language, and key library versions.',
            'Example: "Node.js 22, React 19, TypeScript 5.8, PostgreSQL 17"',
        ]),
        ('Commands',          [
            'The exact commands to build, test, lint, and run the project.',
            'Not guesses — copy them from your package.json or Makefile.',
            'Example: "Build: npm run build  |  Test: npm test  |  Lint: npm run lint"',
        ]),
        ('Architecture',      [
            'The 3–5 directories that matter most and what each one does.',
            'Point to files by path. Claude will read them. Do not describe them in prose.',
            'Example: "src/api/ — all Express route handlers  |  src/lib/ — shared utilities"',
        ]),
        ('Conventions',       [
            'Patterns your team enforces that a linter cannot catch.',
            'Example: "All async functions must use try/catch. No console.log in production."',
        ]),
        ('Boundaries',        [
            'Files and folders Claude must not modify.',
            'Example: "Do not touch legacy/  |  Do not edit generated/  |  No changes to .env files"',
        ]),
        ('Build Rules',       [
            'Agentic workflow rules: how Claude should approach tasks in this project.',
            'Example: "Always run tests after edits. Ask before adding new dependencies."',
        ]),
    ]

    for i, (title, lines) in enumerate(sections):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 5

    y -= 8
    warn_lines = wrap(
        'Keep your CLAUDE.md under 200 lines. Every line consumes context budget '
        'on every turn. A bloated CLAUDE.md can push out space for the actual code '
        'Claude needs to read. Be concise: commands not explanations, paths not prose.',
        10, CW - 28)
    warn_box(c, MX, y, 'Context Budget Warning: Keep It Under 200 Lines', warn_lines, CW)
    c.showPage()


# ── Page 4: Template ──────────────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Complete CLAUDE.md Template')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Copy this into your project root and fill in your details:')
    y -= 56

    y = code_block(c, MX, y, [
        '# PROJECT NAME — Claude AI Build Plan',
        '',
        '## TECH STACK',
        'Language: [Python 3.12 / Node.js 22 / etc.]',
        'Framework: [FastAPI / React / etc.]',
        'Database: [PostgreSQL 17 / SQLite / etc.]',
        '',
        '## COMMANDS',
        'Build:  [npm run build / python -m build]',
        'Test:   [npm test / pytest]',
        'Lint:   [npm run lint / ruff check .]',
        'Run:    [npm start / uvicorn main:app --reload]',
        '',
        '## ARCHITECTURE',
        'src/         — application source code',
        'src/api/     — route handlers and controllers',
        'src/lib/     — shared utility functions',
        'tests/       — test files mirror src/ structure',
        'docs/        — documentation and ADRs',
        '',
        '## CONVENTIONS',
        '- All functions must have type hints (Python) or JSDoc (JS)',
        '- Error handling: use try/catch, never swallow exceptions silently',
        '- No commented-out code in commits',
        '',
        '## BOUNDARIES',
        '- Do NOT edit files in generated/ or vendor/',
        '- Do NOT modify .env or any secrets files',
        '',
        '## BUILD RULES',
        '- Run tests after any code change before marking task done',
        '- Ask before adding new dependencies',
        '- One feature per PR — keep commits atomic',
    ], CW)

    y -= 12
    tip_lines = wrap(
        'Progressive disclosure: if a section gets long, move the details to a separate '
        'file (e.g. docs/architecture.md) and add one line to CLAUDE.md: '
        '"See docs/architecture.md for full layout." Claude will read it when needed.',
        10, CW - 28)
    tip_box(c, MX, y, 'Keep It Short with Progressive Disclosure', tip_lines, CW)
    c.showPage()


# ── Page 5: CLAUDE.md vs Hooks ────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'CLAUDE.md vs Hooks — When to Use Which')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('CLAUDE.md is advisory: Claude reads it and usually follows it. '
             'Hooks are deterministic: shell commands that run automatically at key '
             'moments in the agentic loop. Use CLAUDE.md for context and conventions; '
             'use hooks for rules that must always be enforced.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 12

    t_rows = [
        ['What it is',      'Markdown file Claude reads at session start', 'Shell commands that run during the loop'],
        ['Enforcement',     'Advisory — Claude follows ~70-90% of the time', 'Deterministic — always runs, cannot be skipped'],
        ['Use for',         'Stack, architecture, conventions, preferences', 'Linting, testing, security checks, auto-format'],
        ['Lives in',        'CLAUDE.md file in your project root', 'Settings → Hooks in Claude Code config'],
        ['Runs when',       'Start of every session (auto-loaded)', 'PreToolUse, PostToolUse, Stop, Notification'],
        ['Example',         '"Always use try/catch"', 'Run eslint --fix after every file edit'],
    ]
    y = tbl(c, MX, y, ['Aspect', 'CLAUDE.md', 'Hooks'], t_rows, [96, 194, CW - 290])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Practical Decision Rule')
    y -= 18
    rules = [
        ('Use CLAUDE.md when...', [
            '"I want Claude to know what framework we use"',
            '"I want Claude to follow our naming conventions"',
            '"I want Claude to avoid editing legacy code"',
        ]),
        ('Use Hooks when...', [
            '"I want tests to run after every code change, no exceptions"',
            '"I want linting applied to every file Claude edits"',
            '"I want a security scan before any git commit"',
        ]),
    ]
    for title, examples in rules:
        c.setFillColor(PNL); c.roundRect(MX, y - 80, CW, 80, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 12, y - 16, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        ey = y - 34
        for ex in examples:
            c.setFillColor(GRN); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 12, ey, '›')
            c.setFillColor(MGR); c.setFont('Helvetica', 10); c.drawString(MX + 24, ey, ex)
            ey -= 16
        y -= 90

    y -= 6
    tip_lines = wrap(
        'A good mental model: CLAUDE.md is what you\'d put in a team wiki. '
        'Hooks are what you\'d put in a CI/CD pipeline. Both together give you '
        'context (wiki) plus guarantees (CI).',
        10, CW - 28)
    tip_box(c, MX, y, 'Wiki + CI = CLAUDE.md + Hooks', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — CLAUDE.md Cheat Sheet')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('File name',         'CLAUDE.md  (case sensitive)'),
        ('Location',          'Project root, OR ~/CLAUDE.md for global'),
        ('Max recommended',   '~200 lines total'),
        ('Auto-loaded',       'Yes — every Claude Code session'),
        ('Format',            'Plain Markdown — headings, bullets, code'),
        ('Sub-project files', 'Add CLAUDE.md to any subdirectory'),
        ('Secrets in file',   'Never — use .env for secrets'),
        ('Hooks vs CLAUDE.md','Hooks = enforce; CLAUDE.md = advise'),
    ]
    url_items = [
        ('Section 1',  'Tech Stack — language, framework, versions'),
        ('Section 2',  'Commands — exact build, test, lint, run'),
        ('Section 3',  'Architecture — key dirs and what they do'),
        ('Section 4',  'Conventions — patterns Claude should follow'),
        ('Section 5',  'Boundaries — what Claude must not change'),
        ('Section 6',  'Build Rules — workflow and agentic rules'),
        ('Best practice', 'Use file paths, not prose descriptions'),
        ('Docs',       'docs.claude.com'),
    ]

    for px, panel_title, items in [
        (MX, 'Key Facts', left_items),
        (MX + cw2 + 10, 'The 6 Sections', url_items),
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
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Mistakes & Fixes')
    y -= 8
    t_rows = [
        ['File too long (500+ lines)',    'Use progressive disclosure — link to detail files'],
        ['Claude ignores the file',       'Check filename is exactly CLAUDE.md in project root'],
        ['Rules too vague ("be careful")', 'Use exact commands and file paths — be specific'],
        ['Putting secrets in the file',   'Move to .env — CLAUDE.md is checked into git'],
        ['Conflict with subdirectory file','Root CLAUDE.md + sub CLAUDE.md both load and merge'],
    ]
    y = tbl(c, MX, y, ['Mistake', 'Fix'], t_rows, [178, CW - 178])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 12 — Subagents & Hooks in Claude Code')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 11 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
