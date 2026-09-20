#!/usr/bin/env python3
"""Guide 17: Claude Skills — Create Your Own — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_17_Skills.pdf'
GUIDE = 'Claude Skills — Create Your Own'

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
    bw, bh2 = c.stringWidth('GUIDE 17 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 17 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 30)
    c.drawString(MX, H - 175, 'Claude Skills')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Create Reusable Instruction Packs for Any Task')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What a skill is: a folder with a SKILL.md that Claude reads automatically',
        'The SKILL.md frontmatter format: name, description, allowed-tools',
        'How Claude decides when to load a skill — the description is the trigger',
        'Step-by-step: create and install your first custom skill in under 5 minutes',
        'A complete SKILL.md template you can copy and adapt immediately',
        'Official Anthropic skills and the 330+ community skills on GitHub',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Requires Claude Code CLI  •  Skills live in ~/.claude/skills/  •  Any OS')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: What Are Skills ───────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Are Claude Code Skills?')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('A Claude Code skill is a reusable instruction pack that Claude loads '
             'automatically when the task matches its description. Instead of re-typing '
             'the same detailed prompt every session, you write it once in a SKILL.md '
             'file and Claude picks it up whenever it\'s relevant.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'Skills vs CLAUDE.md — What Is the Difference?', [
        'CLAUDE.md: project-level context (stack, commands, architecture).',
        'Skills: task-level behaviour — a specific set of instructions for a specific job.',
        'CLAUDE.md is always loaded. A skill loads only when it is relevant.',
        'Example: a "code-review" skill loads when Claude reviews code, not when writing docs.',
    ], CW)
    y -= 90

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'What a Skill Can Do')
    y -= 22
    abilities = [
        ('Enforce a workflow',    'Always run tests, always update a changelog, always type-check'),
        ('Add expert knowledge',  'Load deep instructions for a specific domain (e.g. SQL review)'),
        ('Bundle templates',      'Include example files that Claude uses as references'),
        ('Restrict tools',        'Allow-list only the tools the skill needs (e.g. Read + Grep only)'),
        ('Speed up repetition',   'Write a standup-report skill — invoke it every morning in one prompt'),
    ]
    for title, desc in abilities:
        c.setFillColor(PNL); c.roundRect(MX, y - 30, CW, 30, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y - 18, '✓')
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 24, y - 10, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 24, y - 22, desc)
        y -= 34

    y -= 10
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Where Skills Live')
    y -= 18
    locations = [
        ('~/.claude/skills/',          'Global — available in ALL your projects'),
        ('.claude/skills/ (project)',   'Project-local — only in this repo'),
        ('~/.claude/skills/skill-name/','Each skill gets its own subdirectory'),
        ('SKILL.md inside the folder',  'The only required file — everything else is optional'),
    ]
    for path, desc in locations:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 10, y - 10, path)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 10, y - 21, desc)
        y -= 30
    c.showPage()


# ── Page 3: SKILL.md Format ───────────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The SKILL.md Format')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Every skill starts with YAML frontmatter between --- markers, then the instructions:')
    y -= 56

    y = code_block(c, MX, y, [
        '---',
        'name: code-review',
        'description: >',
        '  Use this skill when reviewing code, assessing a pull request,',
        '  or evaluating code quality. Covers style, logic, and security.',
        'allowed-tools: Read Grep Glob',
        '---',
        '',
        '# Code Review Instructions',
        '',
        '## What to Check',
        '- Logic correctness: does the code do what the comment says?',
        '- Security: no hardcoded secrets, no SQL injection risks',
        '- Style: follows project conventions (see CLAUDE.md)',
        '- Test coverage: is there a test for the new behaviour?',
        '',
        '## Output Format',
        'List issues by severity: CRITICAL → WARNING → SUGGESTION',
        'End with a one-line verdict: APPROVE / REQUEST CHANGES',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Frontmatter Fields Explained')
    y -= 8
    fields = [
        ('name',                    'Required. Kebab-case identifier. Used in /skill commands.'),
        ('description',             'Critical. Claude reads this to decide whether to load the skill.'),
        ('allowed-tools',           'Optional. Whitelist of tools (Read, Grep, Bash, etc.). All if omitted.'),
        ('disable-model-invocation','Optional. true = run without calling the model (for pure shell scripts).'),
    ]
    for field, desc in fields:
        c.setFillColor(PNL); c.roundRect(MX, y - 38, CW, 38, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier-Bold', 10); c.drawString(MX + 10, y - 12, field)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(desc, 9, CW - 28)
        dy = y - 25
        for dl_line in dl[:2]:
            c.drawString(MX + 10, dy, dl_line); dy -= 13
        y -= 42

    y -= 8
    warn_lines = wrap(
        'The description field is how Claude decides when to load the skill. '
        'Be specific: include the trigger scenarios ("when reviewing", "when writing SQL"), '
        'the output it produces, and keywords Claude will encounter in prompts.',
        10, CW - 28)
    warn_box(c, MX, y, 'The Description Field Is the Trigger — Be Specific', warn_lines, CW)
    c.showPage()


# ── Page 4: Create Your First Skill ──────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Create Your First Skill in 4 Steps')

    steps = [
        ('Create the Skill Directory', [
            'Open a terminal and run:',
            '  mkdir -p ~/.claude/skills/my-skill',
        ]),
        ('Create the SKILL.md File', [
            'Create ~/.claude/skills/my-skill/SKILL.md',
            'Paste in the template from the next section.',
            'Fill in your own name, description, and instructions.',
        ]),
        ('Reload Claude Code', [
            'Type /skills in Claude Code to see all loaded skills.',
            'Your new skill should appear in the list.',
            'No restart needed — skills are loaded on demand.',
        ]),
        ('Test Your Skill', [
            'Type a prompt that matches your skill\'s description.',
            'Claude will load the skill instructions automatically.',
            'Or invoke it directly: /skill my-skill',
        ]),
    ]
    y -= 40
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    y -= 8
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX, y, 'Minimal Working Skill Template')
    y -= 14
    y = code_block(c, MX, y, [
        '---',
        'name: my-skill',
        'description: >',
        '  Use this skill when [TRIGGER SCENARIO].',
        '  It [WHAT IT DOES] and produces [OUTPUT FORMAT].',
        '---',
        '',
        '# My Skill',
        '',
        '## Instructions',
        '- Step 1: [What Claude should do first]',
        '- Step 2: [Next step]',
        '- Step 3: [Final step]',
        '',
        '## Output Format',
        '[Describe what the response should look like]',
    ], CW)
    y -= 12

    tip_lines = wrap(
        'Use Anthropic\'s Skill Creator to build skills interactively. '
        'Type "create a new skill" in Claude Code and it will walk you through '
        'an interactive Q&A that generates a complete, properly structured skill.',
        10, CW - 28)
    tip_box(c, MX, y, "Use the Skill Creator — It's the Easiest Way", tip_lines, CW)
    c.showPage()


# ── Page 5: Examples & Community ─────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Skill Examples & Community Resources')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Pre-Built Skills from Anthropic')
    y -= 14
    official = [
        ('Excel Workflow',     'Read, analyse, and write Excel files with structured output'),
        ('PowerPoint Builder', 'Generate PowerPoint slide decks from outline text'),
        ('Word Document',      'Create formatted Word documents from plain-text instructions'),
        ('PDF Analysis',       'Extract, summarise, and compare PDF content'),
        ('Code Review',        'Full code review with severity-ranked issue list'),
        ('Git Commit Helper',  'Generate conventional commit messages from staged changes'),
    ]
    for name, desc in official:
        c.setFillColor(PNL); c.roundRect(MX, y - 30, CW, 30, radius=3, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + 8, y - 24, 8, 8, radius=2, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 24, y - 10, name)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 24, y - 22, desc)
        y -= 34

    y -= 10
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Ideas for Custom Skills')
    y -= 14
    custom = [
        ('daily-standup',      'Pull recent git commits and generate a standup report'),
        ('pr-description',     'Read a diff and write a complete PR description'),
        ('test-generator',     'Given a function, write comprehensive unit tests'),
        ('security-scan',      'Review code for OWASP top 10 vulnerabilities'),
        ('changelog-update',   'Add a changelog entry for the current commit'),
        ('api-docs',           'Generate API documentation from code comments'),
        ('refactor-guide',     'Break down a large refactor into ordered steps'),
    ]
    for name, desc in custom:
        c.setFillColor(PNL2); c.roundRect(MX, y - 26, CW, 26, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier', 9); c.drawString(MX + 10, y - 10, name)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 120, y - 10, '— ' + desc)
        y -= 30

    y -= 10
    info_panel(c, MX, y, 'Finding Community Skills', [
        'Official: github.com/anthropics/skills  — Anthropic\'s public skill library',
        'Community: github.com/alirezarezvani/claude-skills — 330+ skills, actively maintained',
        'Browse and download any skill, then drop the folder into ~/.claude/skills/',
        'Use /skills in Claude Code to list all currently loaded skills.',
    ], CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Claude Skills')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Global install path',  '~/.claude/skills/skill-name/'),
        ('Project install path', '.claude/skills/skill-name/'),
        ('Required file',        'SKILL.md  (in the skill folder)'),
        ('List all skills',      '/skills'),
        ('Invoke a skill',       '/skill skill-name'),
        ('Skill Creator',        'Prompt: "create a new skill"'),
        ('Official skills',      'github.com/anthropics/skills'),
        ('Community skills',     'github.com/alirezarezvani/claude-skills'),
    ]
    right_items = [
        ('Frontmatter: name',        'Kebab-case identifier for the skill'),
        ('Frontmatter: description', 'Trigger text — be very specific'),
        ('Frontmatter: allowed-tools','Whitelist: Read Grep Bash etc.'),
        ('Auto-load',               'Claude loads when description matches task'),
        ('Keep body short',         'Skill loads every turn — token cost adds up'),
        ('Optional extras',         'Templates, examples, scripts in same folder'),
        ('Scope',                   'Global (~/) or per-project (.claude/)'),
        ('Test skill',              'Type a matching prompt or use /skill name'),
    ]

    for px, panel_title, items in [
        (MX, 'File Paths & Commands', left_items),
        (MX + cw2 + 10, 'SKILL.md Reference', right_items),
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
        ['Skill not appearing in /skills',   'Check folder is in ~/.claude/skills/ (not a subfolder of subfolder)'],
        ['Skill never triggers automatically','Make the description more specific and add trigger keywords'],
        ['Skill triggers on wrong tasks',    'Narrow the description — remove vague phrases like "general use"'],
        ['Tool blocked by allowed-tools',    'Add the tool name to allowed-tools in frontmatter'],
        ['Skill body too long',              'Move detail to reference files and link them from SKILL.md'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [174, CW - 174])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 18 — Claude API Basics')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 17 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
