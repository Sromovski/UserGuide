#!/usr/bin/env python3
"""Guide 21: Multi-Agent Orchestration — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_21_Orchestration.pdf'
GUIDE = 'Multi-Agent Orchestration'

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

def cover(c):
    pg_bg(c)
    c.setFillColor(OG); c.rect(0, H - 130, W, 130, fill=1, stroke=0)
    c.setFillColor(DOG); c.circle(W - 55, H - 35, 65, fill=1, stroke=0)
    c.setFillColor(DDOG); c.circle(W - 20, H - 105, 45, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 22, 'CLAUDE AI FIELD GUIDE SERIES')
    bw, bh2 = c.stringWidth('GUIDE 21  — ADVANCED ADD-ON', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 21  — ADVANCED ADD-ON')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 27)
    c.drawString(MX, H - 175, 'Multi-Agent Orchestration')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Coordinate Fleets of Claude Agents — Fan Out, Verify, and Ship Faster')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'The three orchestration tools: subagents, Agent Teams, and Workflows',
        'Fan-out vs pipeline: when to run agents in parallel and when to chain them',
        'Coordination patterns: judge panels, adversarial verify, loop-until-dry',
        'Agent Teams: set up a lead + teammates with a shared task list',
        'Dynamic Workflows: plan and fan out tens of agents in one session',
        'Worktree isolation, cost control, and when NOT to orchestrate',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'For Claude Code power users  •  Builds on Guide 12 (Subagents) and Guide 13 (Agentic Loops)')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  The Complete Field Guide Series')
    c.showPage()


# ── Page 2: What orchestration is + when to use it ────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'From One Agent to a Coordinated Fleet')
    y -= 44

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    intro = ('A single Claude agent works through a task step by step in one context window. '
             'Orchestration means splitting a big job across many agents that run at the same '
             'time or in stages — then combining their results. It trades tokens for speed, '
             'breadth, and confidence.')
    for line in wrap(intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 12

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The Three Orchestration Tools in Claude Code')
    y -= 20
    tools = [
        ('Subagents',
         'Isolated Claude instances spawned from your session.',
         'Each has its own context window, tools, and model. Best for delegating a',
         'self-contained subtask so its file dumps never fill your main context.'),
        ('Agent Teams',
         'One session acts as "team lead" over several teammates.',
         'The lead coordinates work through a shared task list; teammates run in their',
         'own context windows and can hand results to each other. Best for long projects.'),
        ('Workflows',
         'Deterministic scripts that fan out agents by code, not chat.',
         'You write loops, parallel(), and pipeline() steps. Dynamic Workflows (June 2026)',
         'let the lead plan and launch tens to hundreds of agents in one session.'),
    ]
    for title, desc, l2, l3 in tools:
        ph = 66
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, y - 16, title)
        c.setFillColor(OGL); c.setFont('Helvetica-Oblique', 9); c.drawString(MX + 14, y - 30, desc)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 14, y - 44, l2); c.drawString(MX + 14, y - 56, l3)
        y -= ph + 8
    y -= 2

    info_panel(c, MX, y, 'When Orchestration Pays Off', [
        'Comprehensive: decompose a job and cover every part in parallel.',
        'Confident: independent agents verify each other before you commit.',
        'Scale: work too large for one context window (audits, migrations, sweeps).',
    ], CW)
    c.showPage()


# ── Page 3: Primitives — parallel vs pipeline vs delegate ─────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The Building Blocks: Delegate, Fan Out, Pipeline')
    y -= 42

    y = step_card(c, MX, y, 1, 'Delegate a single subtask', [
        'Hand one self-contained job to a subagent and keep only its conclusion.',
        'Use when a search or read would otherwise flood your main context.',
    ], CW)
    y -= 8

    y = step_card(c, MX, y, 2, 'Fan out with parallel (a barrier)', [
        'Launch N agents at once and WAIT for all of them before continuing.',
        'Use only when the next step genuinely needs every result together —',
        'e.g. dedup across all findings, or "0 found, skip the whole next phase".',
    ], CW)
    y -= 8

    y = step_card(c, MX, y, 3, 'Pipeline (no barrier) — the default', [
        'Each item flows through all stages independently; item A can be in stage 3',
        'while item B is still in stage 1. Wall-clock = slowest single chain, not the',
        'sum of the slowest step per stage. Prefer this over a barrier when you can.',
    ], CW)
    y -= 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Parallel vs Pipeline at a Glance')
    y -= 6
    rows = [
        ['Parallel', 'Barrier — awaits all', 'Dedup / merge / early-exit on total count'],
        ['Pipeline', 'No barrier — streams', 'Multi-stage work with no cross-item dependency'],
        ['Delegate', 'One agent, one job', 'Keep a noisy subtask out of main context'],
    ]
    y = tbl(c, MX, y, ['Primitive', 'Behaviour', 'Reach for it when...'], rows, [80, 150, CW - 230])
    y -= 16

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The Canonical Shape — Review, Then Verify')
    y -= 14
    y = code_block(c, MX, y, [
        '# Pipeline: each dimension verifies as soon as its review finishes',
        'results = pipeline(',
        '  DIMENSIONS,',
        '  d => agent(d.prompt, {schema: FINDINGS}),      # stage 1: find',
        '  review => parallel(review.findings.map(f =>    # stage 2: verify',
        '    () => agent("Adversarially verify: " + f.title,',
        '                {schema: VERDICT}))),',
        ')',
        '# "bugs" findings verify while "perf" is still being reviewed.',
    ], CW)
    c.showPage()


# ── Page 4: Coordination patterns ─────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Coordination Patterns That Raise Quality')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Compose these freely — most real orchestrations stack two or three:')
    y -= 56

    patterns = [
        ('Adversarial Verify',
         'Spawn N independent skeptics per finding, each prompted to REFUTE it.',
         'Kill the finding unless it survives a majority. Stops plausible-but-wrong results.'),
        ('Judge Panel',
         'Generate N attempts from different angles; score each with parallel judges.',
         'Synthesize from the winner, grafting the best ideas from runners-up.'),
        ('Loop-Until-Dry',
         'Keep spawning finders until K rounds in a row surface nothing new.',
         'Beats a fixed count — simple caps miss the long tail of edge cases.'),
        ('Multi-Modal Sweep',
         'Parallel agents each search a different way: by file, by content, by entity.',
         'Each is blind to the others; use when one search angle cannot find everything.'),
        ('Completeness Critic',
         'A final agent asks "what is missing — a claim unverified, a source unread?"',
         'Whatever it finds becomes the next round of work. Guards against silent gaps.'),
        ('Perspective-Diverse Verify',
         'Give each verifier a distinct lens: correctness, security, does-it-reproduce.',
         'Diversity catches failure modes that identical redundant checks never would.'),
    ]
    for title, l1, l2 in patterns:
        ph = 60
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(PUR); c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, y - 16, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + 14, y - 32, l1); c.drawString(MX + 14, y - 46, l2)
        y -= ph + 6
    y -= 2

    tip_box(c, MX, y, 'Scale the Pattern to the Ask', wrap(
        'A quick "find any bugs" needs a few finders and a single verify vote. '
        '"Thoroughly audit this" earns a larger finder pool, a 3-5 vote adversarial pass, '
        'and a synthesis stage. Match effort to the request.', 10, CW - 28), CW)
    c.showPage()


# ── Page 5: Practical setup ───────────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Setting It Up in Claude Code')
    y -= 42

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Define a Reusable Custom Subagent')
    y -= 14
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Drop a markdown file in .claude/agents/ with YAML frontmatter:')
    y -= 14
    y = code_block(c, MX, y, [
        '# .claude/agents/reviewer.md',
        '---',
        'name: reviewer',
        'description: Reviews a diff for correctness bugs. Use after edits.',
        'tools: Read, Grep, Glob        # omit to inherit all tools',
        'model: sonnet                  # or opus / haiku / inherit',
        '---',
        'You are a meticulous code reviewer. Report only confirmed bugs,',
        'most severe first. Your final message IS the result — return raw findings.',
    ], CW)
    y -= 14

    y = step_card(c, MX, y, 1, 'Launch agents in parallel', [
        'Send several Agent calls in ONE message so they run concurrently.',
        'As of April 2026 subagents and MCP servers initialize in parallel too.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 2, 'Run an Agent Team for long projects', [
        'One session is the lead; it coordinates teammates via a shared task list.',
        'Teammates run in their own contexts and pass results to each other.',
    ], CW)
    y -= 6

    y = step_card(c, MX, y, 3, 'Reach for Dynamic Workflows at scale', [
        'The lead writes an orchestration script, fans out tens of agents, and',
        'validates results against a rubric before presenting a final answer.',
    ], CW)
    y -= 10

    warn_box(c, MX, y, 'Isolate Parallel File Edits', wrap(
        'Agents that write to the same files at once will clobber each other. '
        'Give each its own git worktree (isolation: worktree) so their changes stay '
        'separate. It costs setup time and disk, so use it only for parallel mutation.',
        10, CW - 28), CW)
    c.showPage()


# ── Page 6: Quick reference + troubleshooting + CTA ───────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Orchestration Quick Reference')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Default',        'Pipeline — stream, no barrier'),
        ('Barrier only if', 'Next step needs ALL prior results'),
        ('Delegate',       'Keep noisy subtasks out of context'),
        ('Parallel launch', 'Many Agent calls in one message'),
        ('Verify',         'N skeptics, majority must survive'),
        ('Isolate edits',  'One git worktree per writing agent'),
        ('Concurrency',    'Capped ~ CPU cores; excess queues'),
        ('Cost',           'More agents = more tokens — scope it'),
    ]
    right_items = [
        ('Subagents', 'Isolated, own context + tools + model'),
        ('Agent Teams', 'Lead + teammates, shared task list'),
        ('Workflows', 'Scripted fan-out: parallel + pipeline'),
        ('Dynamic WF', 'Lead plans + launches tens of agents'),
        ('Judge panel', 'N attempts, scored, synthesized'),
        ('Loop-dry', 'Stop when K rounds find nothing new'),
        ('Critic', 'Final "what is missing?" pass'),
        ('Docs', 'code.claude.com/docs/en/agents'),
    ]
    for px, panel_title, items in [
        (MX, 'Rules of Thumb', left_items),
        (MX + cw2 + 10, 'Tool & Pattern Map', right_items),
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
        ['Agents overwrite files', 'Give each its own git worktree (isolation)'],
        ['Barrier feels slow', 'Switch to a pipeline — drop the barrier'],
        ['Findings look wrong', 'Add an adversarial verify vote per finding'],
        ['Coverage feels thin', 'Add a completeness-critic round'],
        ['Burning too many tokens', 'Fewer finders; single-vote verify; scope it'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], rows, [210, CW - 210])
    y -= 20

    cta_h = 58
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 16, y - 20, 'Next in the series: Guide 22 — Evaluating & Testing Claude Agents')
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 16, y - 38, 'Build eval sets, grade agent output against rubrics, and catch regressions before they ship.')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 21 — Advanced Add-On: Multi-Agent Orchestration')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
