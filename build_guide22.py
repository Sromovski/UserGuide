#!/usr/bin/env python3
"""Guide 22: Evaluating & Testing Claude Agents — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_22_Evaluation.pdf'
GUIDE = 'Evaluating & Testing Claude Agents'

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
    bw, bh2 = c.stringWidth('GUIDE 22  — ADVANCED ADD-ON', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 22  — ADVANCED ADD-ON')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 25)
    c.drawString(MX, H - 174, 'Evaluating & Testing Claude Agents')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Know Your Agent Works — Before You Ship It')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Why "it looks right" is not enough — from vibes to measurement',
        'Build a gold-standard eval set: test cases, inputs, expected outputs',
        'Three grading methods: exact match, code checks, and LLM-as-judge',
        'Write rubrics that score task completion, tool use, and planning',
        'Judge biases to avoid: position, verbosity, self-preference, rubric drift',
        'Wire evals into CI with Promptfoo & DeepEval — catch regressions early',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'For Claude Code power users  •  Pairs with Guide 21 (Orchestration) and Guide 20 (Prompting)')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  The Complete Field Guide Series')
    c.showPage()


# ── Page 2: Why eval matters + the loop + three axes ──────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'From Vibes to Measurement')
    y -= 44

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('"It looks right" is how most agents ship — and how they silently break. '
             'An evaluation ("eval") is a repeatable test that scores your agent on real '
             'tasks with known good answers. Evals turn a gut feeling into a number you '
             'can track, compare, and defend when you change a prompt or model.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The Evaluation Loop')
    y -= 20
    loop = [
        ('Collect', 'Gather real tasks + known good answers (your "gold set").'),
        ('Run', 'Send each task through the agent; capture its output and tool calls.'),
        ('Grade', 'Score each output — exact match, a code check, or an LLM judge.'),
        ('Compare', 'Track the score. Did this change help, hurt, or do nothing?'),
    ]
    for i, (label, desc) in enumerate(loop):
        ph = 34
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.circle(MX + 20, y - 17, 11, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10); c.drawCentredString(MX + 20, y - 21, str(i + 1))
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 40, y - 15, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 100, y - 15, desc)
        y -= ph + 6
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Three Axes of Agent Quality')
    y -= 6
    rows = [
        ['Task completion', 'Did it produce the correct, complete result?'],
        ['Tool selection', 'Did it call the right tools, with the right inputs?'],
        ['Planning', 'Was the path efficient, or did it wander and backtrack?'],
    ]
    y = tbl(c, MX, y, ['Axis', 'The question it answers'], rows, [130, CW - 130])
    y -= 16

    info_panel(c, MX, y, 'Start Small — 20 Cases Beat Zero', [
        'You do not need thousands of test cases. 20-50 well-chosen tasks that cover',
        'your common paths and known failure modes will catch most regressions.',
        'Add a new case every time you find a bug — your eval set grows with reality.',
    ], CW)
    c.showPage()


# ── Page 3: Building an eval set ───────────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Building Your Eval Set')
    y -= 42

    y = step_card(c, MX, y, 1, 'Collect real tasks, not toy ones', [
        'Pull actual inputs your agent will face — real emails, real code, real queries.',
        'Include the hard edge cases and the bugs you have already hit in the wild.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Write the expected answer (the gold)', [
        'For each task, record what "correct" looks like. Exact string, a set of facts',
        'that must appear, or a checklist a judge can grade against.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 3, 'Pick a grading method per case', [
        'Deterministic tasks → exact match or a code check. Open-ended tasks → an',
        'LLM judge with a rubric. Mix methods across your set as needed.',
    ], CW)
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Choosing a Grading Method')
    y -= 6
    rows = [
        ['Exact match', 'Fast, free, 0 bias', 'Classification, extraction, fixed answers'],
        ['Code check', 'Assertions in code', 'Valid JSON, schema, "contains X", ranges'],
        ['LLM judge', 'Scores by rubric', 'Writing, summaries, reasoning, open-ended'],
        ['Human review', 'Slow, gold standard', 'Validating the judge; final sign-off'],
    ]
    y = tbl(c, MX, y, ['Method', 'Nature', 'Best for'], rows, [95, 130, CW - 225])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'A Test Case in Practice')
    y -= 14
    y = code_block(c, MX, y, [
        '# One eval case (JSON)',
        '{',
        '  "input": "Classify: My payment failed but I was charged twice.",',
        '  "expected": "REFUND",',
        '  "grader": "exact_match"',
        '}',
        '# Open-ended case graded by a judge instead:',
        '{',
        '  "input": "Summarise this 2-page report in 3 bullets: ...",',
        '  "rubric": "Covers all 3 key findings; <= 3 bullets; no invented facts",',
        '  "grader": "llm_judge"',
        '}',
    ], CW)
    y -= 12

    tip_box(c, MX, y, 'Version Your Eval Set', wrap(
        'Keep eval cases in your repo next to the code. When a case changes, you can '
        'see it in the diff — and every score becomes comparable across commits.',
        10, CW - 28), CW)
    c.showPage()


# ── Page 4: LLM-as-judge deep dive ────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'LLM-as-Judge: Grading With Claude')
    y -= 42

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('When answers are open-ended, use a second Claude call as the grader. Give it '
             'a clear rubric and ask it to reason before scoring. A strong judge model '
             '(e.g. Opus) grading a rubric is remarkably consistent — if you avoid the '
             'known biases below.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'A Judge Prompt That Works')
    y -= 14
    y = code_block(c, MX, y, [
        'You are grading an AI summary against a rubric. Score 1-5.',
        '',
        'RUBRIC:',
        '- 5: Covers all key findings, no invented facts, within length.',
        '- 3: Misses one finding OR slightly too long.',
        '- 1: Missing findings OR contains facts not in the source.',
        '',
        'Reason step by step in <thinking>, then output only:',
        'SCORE: <n>  |  REASON: <one line>',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Judge Biases to Design Around')
    y -= 6
    rows = [
        ['Position bias', 'Favours whichever answer comes first', 'Randomise / swap order, average'],
        ['Verbosity bias', 'Rates longer answers higher', 'Score against rubric, not length'],
        ['Self-preference', 'Prefers its own model\'s style', 'Use a strong, neutral judge model'],
        ['Rubric drift', 'Standards wander across a batch', 'Fixed rubric; one axis at a time'],
    ]
    y = tbl(c, MX, y, ['Bias', 'What it does', 'Counter'], rows, [110, 210, CW - 320])
    y -= 16

    warn_box(c, MX, y, 'Validate the Judge Before You Trust It', wrap(
        'Grade a small gold set by hand, then have the judge grade the same set. '
        'If they do not agree ~90% of the time, fix the rubric before you rely on the '
        'judge for the full dataset. An unvalidated judge just launders your bias.',
        10, CW - 28), CW)
    c.showPage()


# ── Page 5: Tools & CI ────────────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Tools & Running Evals in CI')
    y -= 42

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Where to Run Evals')
    y -= 6
    rows = [
        ['Console Evals', 'Anthropic Console', 'No-code: test prompts on a dataset in the UI'],
        ['Promptfoo', 'Open-source CLI', 'YAML test cases, assertions, CI-friendly'],
        ['DeepEval', 'Open-source (Python)', 'pytest-style agent + RAG metrics'],
        ['Custom script', 'Your own harness', 'Full control; loop cases, call judge, log'],
    ]
    y = tbl(c, MX, y, ['Tool', 'Type', 'Best for'], rows, [110, 130, CW - 240])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'A Promptfoo Config (YAML)')
    y -= 14
    y = code_block(c, MX, y, [
        '# promptfooconfig.yaml',
        'prompts: [file://prompt.txt]',
        'providers: [anthropic:messages:claude-sonnet-4-6]',
        'tests:',
        '  - vars: { input: "payment failed, charged twice" }',
        '    assert:',
        '      - type: equals',
        '        value: REFUND',
        '  - vars: { input: "summarise this report ..." }',
        '    assert:',
        '      - type: llm-rubric',
        '        value: Covers all 3 findings, no invented facts',
    ], CW)
    y -= 14

    y = step_card(c, MX, y, 1, 'Set a pass threshold, not just a score', [
        'Fail the build if the pass rate drops below a bar you set — e.g. task',
        'completion >= 0.85, tool accuracy >= 0.90. Numbers make regressions visible.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Run evals on every prompt or model change', [
        'Add the eval command to CI so a merge cannot silently lower quality.',
        'Compare the new score to the last green run before you ship.',
    ], CW)
    y -= 10

    tip_box(c, MX, y, 'Every Bug Becomes a Test', wrap(
        'When users hit a failure, add that exact case to the eval set with the correct '
        'answer. Your suite then guarantees that specific bug can never come back.',
        10, CW - 28), CW)
    c.showPage()


# ── Page 6: Quick reference + troubleshooting + CTA ───────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Evaluation Quick Reference')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Eval loop',      'Collect -> Run -> Grade -> Compare'),
        ('Start size',     '20-50 real cases beats zero'),
        ('Deterministic',  'Exact match or a code assertion'),
        ('Open-ended',     'LLM judge + a written rubric'),
        ('Judge model',    'Strong + neutral (e.g. Opus)'),
        ('Validate judge', 'Agree ~90% with a hand-graded set'),
        ('CI gate',        'Fail build below your threshold'),
        ('Grow the set',   'Every bug becomes a new case'),
    ]
    right_items = [
        ('3 axes', 'Task completion, tool use, planning'),
        ('Exact match', 'Fast, free, zero bias'),
        ('Code check', 'JSON/schema/contains/range asserts'),
        ('LLM judge', 'Rubric, reason then score'),
        ('Position bias', 'Swap answer order, average'),
        ('Verbosity bias', 'Grade rubric, not length'),
        ('Tools', 'Console Evals, Promptfoo, DeepEval'),
        ('Docs', 'docs.claude.com  /  promptfoo.dev'),
    ]
    for px, panel_title, items in [
        (MX, 'Rules of Thumb', left_items),
        (MX + cw2 + 10, 'Method & Bias Map', right_items),
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
        ['Scores swing run to run', 'Set temperature=0 for grading; fix the rubric'],
        ['Judge disagrees with you', 'Sharpen rubric; validate on a gold set first'],
        ['Longer answers always win', 'Score against rubric, cap length in the prompt'],
        ['Passing evals, failing users', 'Add real failing cases to the eval set'],
        ['Evals too slow for CI', 'Run a small smoke set per PR, full set nightly'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], rows, [200, CW - 200])
    y -= 20

    cta_h = 58
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 16, y - 20, 'Next in the series: Guide 23 — Claude Cost & Token Management')
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 16, y - 38, 'Context windows, prompt caching economics, the Batch API, and keeping agent bills predictable.')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 22 — Advanced Add-On: Evaluating & Testing Claude Agents')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
