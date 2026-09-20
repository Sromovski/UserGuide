#!/usr/bin/env python3
"""Guide 20: Prompting Masterclass — Claude AI Field Guide Series (Finale)"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_20_Prompting.pdf'
GUIDE = 'Prompting Masterclass'

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

def ftr(c, n):
    c.setFillColor(PNL); c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica', 8)
    c.drawString(MX, 7, f'Claude AI Field Guide Series  ·  {GUIDE}')
    c.setFillColor(MGR); c.drawRightString(W - MX, 7, f'Page {n}')

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
    bw, bh2 = c.stringWidth('GUIDE 20 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 20 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 28)
    c.drawString(MX, H - 175, 'Prompting Masterclass')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, '7 Techniques + 30 Copy-Paste Templates — Get 10x Better Results')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Prompt anatomy: the 5 parts every effective prompt must have',
        'System prompts: the contract format that makes Claude reliable',
        'XML tags: why <context>, <example>, and <answer> work better than prose',
        'Chain-of-thought: the technique that boosts accuracy by 19 points on hard tasks',
        'Few-shot examples: 3-5 examples that calibrate Claude\'s output perfectly',
        '30 ready-to-use prompt templates across writing, code, analysis, and more',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Works with claude.ai, Claude Code, and the API  •  Part of the 23-guide series')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  All 23 Guides')
    c.showPage()


# ── Page 2: Prompt Anatomy + System Prompts ────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Prompt Anatomy & The System Prompt Contract')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The 5 Parts of an Effective Prompt')
    y -= 14
    parts = [
        ('Role',        'Tell Claude what kind of expert it is playing.',
         'Example: "You are a senior Python engineer reviewing production code."'),
        ('Task',        'Describe the specific job clearly and concisely.',
         'Example: "Review the function below for bugs, performance, and security."'),
        ('Context',     'Provide the raw material Claude needs — data, code, text.',
         'Example: "Here is the function:\\n<code>...</code>"'),
        ('Constraints', 'Limit scope, format, length, or tone.',
         'Example: "Reply only with a bullet list. Maximum 5 items. No explanations."'),
        ('Output Format','Describe exactly how the result should look.',
         'Example: "Format: ISSUE TYPE | SEVERITY | LINE NUMBER | DESCRIPTION"'),
    ]
    for i, (label, desc, ex) in enumerate(parts):
        ph = 62
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + 8, y - 22, 24, 16, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 8); c.drawCentredString(MX + 20, y - 13, str(i + 1))
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 38, y - 14, label)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 38, y - 28, desc)
        c.setFillColor(MGR); c.setFont('Helvetica-Oblique', 9); c.drawString(MX + 38, y - 42, ex)
        y -= ph + 5
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'The System Prompt Contract Format')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'For API use, put persistent instructions in the system prompt as a "contract":')
    y -= 14
    y = code_block(c, MX, y, [
        '# System Prompt Contract Template',
        'You are a [ROLE] helping [USER TYPE] with [DOMAIN].',
        '',
        'SUCCESS CRITERIA:',
        '- [What "done well" looks like]',
        '- [Quality bar]',
        '',
        'CONSTRAINTS:',
        '- [What to avoid / scope limits]',
        '- [Tone and length rules]',
        '',
        'OUTPUT FORMAT:',
        '[Exact structure of your response]',
        '',
        'UNCERTAINTY:',
        'If unclear, ask ONE clarifying question before proceeding.',
    ], CW)
    c.showPage()


# ── Page 3: XML Tags & Chain of Thought ──────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'XML Tags & Chain-of-Thought Prompting')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Why XML Tags Work for Claude')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    xml_desc = ('XML tags are the most reliable way to structure prompts for Claude. They '
                'mark clear boundaries between instructions, context and examples.')
    for line in wrap(xml_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    xml_tags = [
        ('<instructions>',  'Wrap your main instructions — keeps them separate from data'),
        ('<context>',       'Wrap background information or source material'),
        ('<example>',       'Wrap few-shot examples — use multiple <example> tags'),
        ('<thinking>',      'Ask Claude to show its reasoning before the answer'),
        ('<answer>',        'Mark the final answer clearly, separate from reasoning'),
        ('<format>',        'Describe the exact output structure you want'),
    ]
    y -= 4
    # Use tbl()'s return value — the hardcoded offset here was 36pt taller than the
    # table actually is, which is most of why this page overran the footer.
    y = tbl(c, MX, y, ['Tag', 'Purpose'], xml_tags, [118, CW - 118])
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Example — XML-Structured Prompt')
    y -= 14
    y = code_block(c, MX, y, [
        '<instructions>',
        'Classify the email below as: REFUND / TECH_SUPPORT / COMPLAINT / OTHER.',
        'Reply with one word only.',
        '</instructions>',
        '<example>',
        'Email: "My payment failed but I was charged twice."',
        'Classification: REFUND',
        '</example>',
        '<context>',
        'Email: "The app crashes every time I open settings."',
        '</context>',
    ], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Chain-of-Thought (CoT) Prompting')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    cot_desc = ('Chain-of-thought asks Claude to reason step by step before answering — '
                'a +19 point accuracy boost on hard reasoning tasks.')
    for line in wrap(cot_desc, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    y = code_block(c, MX, y, [
        '# Chain-of-Thought prompt',
        'Think through this problem step by step in <thinking> tags,',
        'then give your final answer in <answer> tags.',
        '',
        '<thinking>',
        '[Claude reasons through the problem here]',
        '</thinking>',
        '<answer>',
        '[Final concise answer here]',
        '</answer>',
    ], CW)
    y -= 10

    tip_lines = wrap(
        'Skip explicit CoT instructions for extended thinking models — '
        'they already reason internally and CoT tags do not improve them.',
        10, CW - 28)
    tip_box(c, MX, y, 'CoT Not Needed for Reasoning Models', tip_lines, CW)
    c.showPage()


# ── Page 4: Techniques Reference ─────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, '7 Essential Prompting Techniques')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 38, 'Use these in combination — they compound:')
    y -= 56

    techniques = [
        ('Few-Shot Examples',
         '3-5 input/output examples before your actual request.',
         'Best for: output format control, style matching, classification tasks.',
         'Add via <example> tags. Diverse examples outperform similar ones.'),
        ('Role Assignment',
         '"You are a [expert role] helping [audience]..."',
         'Best for: creative, analytical, and open-ended tasks.',
         'Has little effect on factual QA — use context instead.'),
        ('Negative Constraints',
         '"Do not use jargon. Do not summarise. Do not add caveats."',
         'Best for: removing unwanted patterns Claude tends to default to.',
         'Explicit negatives are more reliable than hoping Claude infers them.'),
        ('Output Schema',
         'Show Claude the exact JSON, table, or bullet structure you want.',
         'Best for: any structured output fed into code or another system.',
         'Add one example of the schema with placeholder values.'),
        ('Temperature Control',
         'temperature=0 for consistent/precise; 1.0 for creative/varied.',
         'Best for: structured tasks use 0; brainstorming and writing use 0.7+.',
         'Only available via the API — not in claude.ai chat.'),
        ('Context Anchoring',
         'Wrap source material in <context> tags before the task.',
         'Best for: summaries, Q&A, analysis over documents.',
         'Prevents Claude from hallucinating data not in the context.'),
        ('Iterative Refinement',
         '"That\'s good. Now make it shorter / more formal / add examples."',
         'Best for: creative work, long-form writing, complex code.',
         'Claude holds the full draft in context — refine incrementally.'),
    ]

    for title, desc, best_for, note in techniques:
        ph = 72
        c.setFillColor(PNL); c.roundRect(MX, y - ph, CW, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 14, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9); c.drawString(MX + 14, y - 27, desc)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 9); c.drawString(MX + 14, y - 41, best_for)
        c.setFillColor(MGR); c.setFont('Helvetica-Oblique', 9); c.drawString(MX + 14, y - 55, note)
        y -= ph + 5
    c.showPage()


# ── Page 5: 30 Prompt Templates ──────────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, '30 Copy-Paste Prompt Templates')
    c.setFillColor(LGR); c.setFont('Helvetica', 9)
    c.drawString(MX, y - 36, 'Replace [brackets] with your own content. Combine techniques as needed.')
    y -= 52

    categories = [
        ('Writing & Content', [
            '"Rewrite the following in a [formal/casual/concise] tone. Keep under [N] words:\\n[TEXT]"',
            '"Write a [blog post/email/tweet] about [TOPIC] for [AUDIENCE]. Hook: [OPENING LINE]."',
            '"Summarise [TEXT] in 5 bullet points. Start each with a verb. No filler."',
            '"Give me 10 title variations for: [DRAFT TITLE]. Prioritise clarity over cleverness."',
            '"Edit for clarity only. Do not change meaning or tone:\\n[TEXT]"',
            '"Write a [DOCUMENT TYPE] using this outline: [OUTLINE]. Length: ~[N] words."',
        ]),
        ('Code & Engineering', [
            '"Review this code for bugs and security issues. List by severity (CRITICAL/WARN/INFO):\\n[CODE]"',
            '"Refactor the following function for readability. Keep behaviour identical:\\n[CODE]"',
            '"Write unit tests for the function below. Cover: happy path, edge cases, error cases:\\n[CODE]"',
            '"Explain what this code does to a junior developer in plain English:\\n[CODE]"',
            '"Convert this [LANGUAGE A] code to [LANGUAGE B]. Keep variable names consistent:\\n[CODE]"',
            '"Debug this error. Explain cause and fix with working code:\\nError: [ERROR]\\nCode: [CODE]"',
        ]),
        ('Analysis & Research', [
            '"Compare [A] and [B] across these dimensions: [DIM1], [DIM2], [DIM3]. Table format."',
            '"Extract all [ENTITY TYPE] from the text below. Return as JSON array:\\n[TEXT]"',
            '"What are the 3 strongest counterarguments to: [POSITION]? Rate each 1-10 for strength."',
            '"Analyse the sentiment of each review below. Format: REVIEW ID | SENTIMENT | SCORE:\\n[REVIEWS]"',
            '"Identify the top 5 risks in this plan. For each: risk, likelihood (H/M/L), mitigation:\\n[PLAN]"',
            '"Translate this data into 3 clear insights a non-technical executive can act on:\\n[DATA]"',
        ]),
        ('Productivity & Planning', [
            '"Turn these meeting notes into action items with owner and deadline:\\n[NOTES]"',
            '"Create a [N]-week learning plan to reach [GOAL]. Include resources and weekly milestones."',
            '"Draft a [job type] job description. Focus on outcomes not tasks. No corporate filler."',
            '"Write 5 [email/message] templates for the scenario: [SCENARIO]. Different tones each."',
            '"Given this goal: [GOAL], give me 3 alternative approaches with trade-offs for each."',
            '"Prepare 10 interview questions for a [ROLE] candidate. Include 2 behavioural questions."',
        ]),
        ('Creative & Ideation', [
            '"Give me 20 [product names / headlines / taglines] for [BRAND/PRODUCT]. Be bold."',
            '"Write a [SHORT STORY/SCENE] from the perspective of [CHARACTER] in [SETTING]."',
            '"Generate 10 \"what if\" ideas for [INDUSTRY/PRODUCT]. No filter — wild is fine."',
            '"Create a mind map (nested bullets) of everything related to [TOPIC]. Go 3 levels deep."',
            '"Describe [CONCEPT] using only analogies. No technical terms. 3 analogies total."',
            '"Write the first paragraph of [GENRE] story that opens with: [OPENING LINE]"',
        ]),
    ]

    # 5 categories x 6 templates at the old 18pt/28pt spacing came to exactly 710pt —
    # the full content height — so the last row landed under the footer bar. Tightened
    # to leave real clearance.
    for cat_name, templates in categories:
        cat_h = len(templates) * 17 + 24
        c.setFillColor(PNL); c.roundRect(MX, y - cat_h, CW, cat_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 10, y - 15, cat_name)
        ty = y - 28
        for tmpl in templates:
            c.setFillColor(LGR); c.setFont('Helvetica', 8)
            tl = wrap(tmpl, 8, CW - 32)
            c.drawString(MX + 18, ty, tl[0] if tl else tmpl)
            ty -= 17
        y -= cat_h + 6
    c.showPage()


# ── Page 6: Final Quick Reference + Series End ────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Prompt Engineering Quick Reference')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Optimal length',      '150-300 words for most prompts'),
        ('Few-shot count',      '3-5 examples (diverse beats similar)'),
        ('Structure method',    'XML tags — not Markdown headings'),
        ('CoT boost',           '+19 pts on hard reasoning (MMLU-Pro)'),
        ('Skip CoT for',        'Reasoning models (they do it internally)'),
        ('Role assignment',     'Useful for creative; low impact on factual'),
        ('Negatives work',      '"Do not X" is more reliable than hoping'),
        ('Temperature 0',       'Structured/precise tasks (API only)'),
    ]
    right_items = [
        ('Technique 1', 'Few-shot: 3-5 <example> tags'),
        ('Technique 2', 'Role: "You are a [expert]..."'),
        ('Technique 3', 'CoT: <thinking> + <answer> tags'),
        ('Technique 4', 'XML structure: <context>, <instructions>'),
        ('Technique 5', 'Output schema: show exact format'),
        ('Technique 6', 'Negatives: explicit "do not" constraints'),
        ('Technique 7', 'Iterate: refine output conversationally'),
        ('Docs',        'platform.claude.com/docs/prompt-engineering'),
    ]

    for px, panel_title, items in [
        (MX, 'Key Facts', left_items),
        (MX + cw2 + 10, '7 Techniques', right_items),
    ]:
        ph = len(items) * 24 + 34
        c.setFillColor(PNL); c.roundRect(px, y - ph, cw2, ph, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(px + 10, y - 18, panel_title)
        iy = y - 36
        for a, b in items:
            c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 9); c.drawString(px + 10, iy, a)
            c.setFillColor(OGL); c.setFont('Helvetica', 9)
            c.drawString(px + 10, iy - 12, b)
            iy -= 24

    panel_h = len(left_items) * 24 + 34
    y -= panel_h + 16
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Before / After — Weak vs Strong Prompt')
    y -= 8
    before_after = [
        ['Weak: "Write about climate change."',
         'Strong: "Write a 250-word op-ed for a business audience arguing that carbon pricing is the most efficient climate policy. Tone: analytical, not alarmist. End with a call to action for CFOs."'],
        ['Weak: "Fix my code."',
         'Strong: "The function below returns wrong results for negative inputs. Identify the bug and provide a corrected version with an explanation of the fix.\\n<code>...</code>"'],
    ]
    for row in before_after:
        rh = 40
        c.setFillColor(PNL2); c.roundRect(MX, y - rh, CW, rh, radius=3, fill=1, stroke=0)
        cw_half = CW / 2 - 5
        c.setFillColor(HexColor('#2B0A0A')); c.roundRect(MX + 4, y - rh + 4, cw_half, rh - 8, radius=3, fill=1, stroke=0)
        c.setFillColor(DBGRN); c.roundRect(MX + cw_half + 10, y - rh + 4, cw_half, rh - 8, radius=3, fill=1, stroke=0)
        c.setFillColor(HexColor('#FF6B6B')); c.setFont('Helvetica-Bold', 8); c.drawString(MX + 8, y - 12, 'WEAK')
        c.setFillColor(LGR); c.setFont('Helvetica', 7)
        w_lines = wrap(row[0], 7, cw_half - 8)
        wy = y - 22
        for wl in w_lines[:2]:
            c.drawString(MX + 8, wy, wl); wy -= 10
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 8); c.drawString(MX + cw_half + 14, y - 12, 'STRONG')
        c.setFillColor(LGR); c.setFont('Helvetica', 7)
        s_lines = wrap(row[1], 7, cw_half - 8)
        sy = y - 22
        for sl in s_lines[:3]:
            c.drawString(MX + cw_half + 14, sy, sl); sy -= 10
        y -= rh + 6

    y -= 12
    # Series end CTA
    cta_h = 64
    c.setFillColor(OG); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 14)
    c.drawCentredString(W / 2, y - 20, 'End of the Claude AI Field Guide Series')
    c.setFillColor(CREAM); c.setFont('Helvetica', 10)
    c.drawCentredString(W / 2, y - 36, 'All 23 guides at etsy.com/shop/FranksMarketDesigns')
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(W / 2, y - 52, 'Complete Library Bundle — All 23 Guides in One Download')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 20 of 20 — Series Finale')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
