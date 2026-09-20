#!/usr/bin/env python3
"""Build The Claude Prompt Vault — PDF book + copy-paste Markdown/text files.

Source of truth is prompt_vault_data.py. Run:  python build_prompt_vault.py
Outputs to C:\\Projects\\UserGuide\\outputs\\ :
    Claude_Prompt_Vault.pdf          the browsable book
    Claude_Prompt_Vault.md           copy-paste markdown (Notion/Obsidian ready)
    Claude_Prompt_Vault.txt          plain text fallback
"""
import os
import re

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth

from prompt_vault_data import CATEGORIES, VAULT_TITLE, VAULT_SUB, total_prompts

OUTDIR = r'C:\Projects\UserGuide\outputs'

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX

BG     = HexColor('#0F0F1A')
OG     = HexColor('#E07A38')
OGL    = HexColor('#F5A66B')
CREAM  = HexColor('#F5F0E8')
LGR    = HexColor('#D4CFC7')
MGR    = HexColor('#9B9690')
PNL    = HexColor('#1C1C2E')
PNL2   = HexColor('#161625')
GRN    = HexColor('#5CB85C')
WHT    = HexColor('#FFFFFF')
DOG    = HexColor('#C86820')
DDOG   = HexColor('#B85C18')
CODEBG = HexColor('#0A0A15')

BODY_F, BODY_S, LH = 'Helvetica', 9, 12.5
TITLE_F, TITLE_S = 'Helvetica-Bold', 10.5
PAD = 10
CARD_GAP = 10
SEC_H = 46
TOP_Y = H - 42
BOT_Y = 46
TOKEN = re.compile(r'(\[[^\]]*\])')


def wrap(text, size, width, font=BODY_F):
    return simpleSplit(text, font, size, width)


def _words(para):
    """Split into whitespace-separated words. A [PLACEHOLDER] stays atomic, and any
    punctuation touching it stays glued to it — so "[TOPIC]." never becomes "[TOPIC] ."."""
    words, glue = [], False
    for seg in TOKEN.split(para):
        if not seg:
            continue
        if seg.startswith('[') and seg.endswith(']'):
            if glue and words:
                words[-1] += seg
            else:
                words.append(seg)
            glue = True
        else:
            toks = seg.split()
            if not toks:
                glue = False
                continue
            if glue and not seg[:1].isspace() and words:
                words[-1] += toks[0]
                toks = toks[1:]
            words.extend(toks)
            glue = not seg[-1:].isspace()
    return words


def line_width(line):
    """True rendered width of a line as draw_rich will paint it."""
    total = 0.0
    for part in TOKEN.split(line):
        if not part:
            continue
        ph = part.startswith('[') and part.endswith(']')
        total += stringWidth(part, 'Helvetica-Bold' if ph else BODY_F, BODY_S)
    return total


def rich_wrap(para, width):
    """Greedy wrap measuring placeholders with the bold metrics they are drawn in."""
    space = stringWidth(' ', BODY_F, BODY_S)
    lines, cur, curw = [], [], 0.0
    for word in _words(para):
        w = line_width(word)
        add = w if not cur else w + space
        if cur and curw + add > width:
            lines.append(' '.join(cur))
            cur, curw = [word], w
        else:
            cur.append(word)
            curw += add
    if cur:
        lines.append(' '.join(cur))
    return lines


def prompt_lines(text, width):
    """Wrap a prompt body, preserving blank-line paragraph breaks."""
    out = []
    for i, para in enumerate(text.split('\n\n')):
        if i:
            out.append('')
        out.extend(rich_wrap(' '.join(para.split()), width))
    return out


def card_height(lines):
    return PAD * 2 + 14 + 4 + len(lines) * LH


def pg_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def hdr(c):
    c.setFillColor(OG)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)


def ftr(c, n, label):
    c.setFillColor(PNL)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica', 8)
    c.drawString(MX, 7, label)
    c.setFillColor(MGR)
    c.drawRightString(W - MX, 7, 'Page %d' % n)


def draw_rich(c, x, y, line):
    """Draw a line, colouring [PLACEHOLDERS] in orange."""
    cx = x
    for part in TOKEN.split(line):
        if not part:
            continue
        if part.startswith('[') and part.endswith(']'):
            c.setFillColor(OG)
            c.setFont('Helvetica-Bold', BODY_S)
        else:
            c.setFillColor(LGR)
            c.setFont(BODY_F, BODY_S)
        c.drawString(cx, y, part)
        cx += stringWidth(part, c._fontname, BODY_S)


# ---------------------------------------------------------------- layout pass

def measure():
    """Compute the page each category starts on, and the total page count."""
    starts = []
    page = 4
    y = TOP_Y
    for name, blurb, items in CATEGORIES:
        if y - SEC_H < BOT_Y + 80:
            page += 1
            y = TOP_Y
        starts.append(page)
        y -= SEC_H
        for _, text in items:
            lines = prompt_lines(text, CW - PAD * 2)
            ch = card_height(lines)
            if y - ch < BOT_Y:
                page += 1
                y = TOP_Y
            y -= ch + CARD_GAP
    return starts, page


# ------------------------------------------------------------------ PDF pages

# SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
# and spliced in by rebuild_covers.py. This function is retained so a from-source
# rebuild still produces a complete document; run rebuild_covers.py afterwards.
def cover(c, pages):
    pg_bg(c)
    c.setFillColor(OG)
    c.rect(0, H - 150, W, 150, fill=1, stroke=0)
    c.setFillColor(DOG)
    c.circle(W - 68, H - 48, 56, fill=1, stroke=0)
    c.circle(W - 140, H - 124, 30, fill=1, stroke=0)
    c.setFillColor(DDOG)
    c.circle(60, H - 126, 22, fill=1, stroke=0)

    c.setFillColor(DDOG)
    c.roundRect(MX, H - 66, 168, 24, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 10, H - 59, 'COPY-PASTE PROMPT PACK')
    c.setFont('Helvetica-Bold', 8)
    c.drawString(MX, H - 92, 'CLAUDE AI FIELD GUIDE SERIES')
    c.setFont('Helvetica', 8)
    c.drawString(MX, H - 108, '2026 EDITION')

    y = H - 208
    c.setFillColor(CREAM)
    c.setFont('Helvetica-Bold', 30)
    for line in wrap(VAULT_TITLE, 30, CW, 'Helvetica-Bold'):
        c.drawString(MX, y, line)
        y -= 36
    c.setFillColor(OGL)
    c.setFont('Helvetica', 14)
    y -= 2
    for line in wrap(VAULT_SUB, 14, CW):
        c.drawString(MX, y, line)
        y -= 19

    y -= 20
    c.setFillColor(PNL)
    c.roundRect(MX, y - 52, CW, 52, radius=5, fill=1, stroke=0)
    stats = [(str(total_prompts()), 'PROMPTS'), (str(len(CATEGORIES)), 'CATEGORIES'),
             (str(pages), 'PAGES'), ('3', 'FILE FORMATS')]
    colw = CW / len(stats)
    for i, (big, small) in enumerate(stats):
        cx = MX + colw * i + colw / 2
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 19)
        c.drawCentredString(cx, y - 27, big)
        c.setFillColor(MGR)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cx, y - 42, small)
    y -= 52

    y -= 20
    rows = (len(CATEGORIES) + 1) // 2
    ph = rows * 16 + 44
    c.setFillColor(PNL)
    c.roundRect(MX, y - ph, CW, ph, radius=5, fill=1, stroke=0)
    c.setFillColor(OG)
    c.rect(MX, y - ph, 4, ph, fill=1, stroke=0)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(MX + 14, y - 22, "WHAT'S INSIDE")
    cw2 = (CW - 34) / 2
    for i, (name, _, items) in enumerate(CATEGORIES):
        col, row = divmod(i, rows)
        tx = MX + 14 + col * cw2
        ty = y - 44 - row * 16
        c.setFillColor(GRN)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(tx, ty, 'v')
        c.setFillColor(LGR)
        c.setFont('Helvetica', 9.5)
        c.drawString(tx + 12, ty, '%s  (%d)' % (name, len(items)))
    y -= ph

    # Sample teaser — anchored to the bottom of the page so any slack falls in the
    # middle as breathing room rather than as dead space under the last element.
    samples = [CATEGORIES[0][2][0], CATEGORIES[4][2][1]]
    blocks = [(t, prompt_lines(x, CW - 44)[:3]) for t, x in samples]
    bh = 30 + sum(16 + len(ls) * LH + 12 for _, ls in blocks) + 14
    top = 70 + bh
    c.setFillColor(CODEBG)
    c.roundRect(MX, 70, CW, bh, radius=5, fill=1, stroke=0)
    c.setStrokeColor(OG)
    c.setLineWidth(0.75)
    c.roundRect(MX, 70, CW, bh, radius=5, fill=0, stroke=1)
    c.setFillColor(OGL)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(MX + 16, top - 18, 'TWO OF THE 200')
    ty = top - 38
    for t, ls in blocks:
        c.setFillColor(MGR)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(MX + 16, ty, t.upper())
        ty -= 16
        for line in ls:
            draw_rich(c, MX + 16, ty, line)
            ty -= LH
        ty -= 12
    c.setFillColor(MGR)
    c.setFont('Helvetica-Oblique', 8)
    c.drawRightString(W - MX - 16, 80, 'orange = the blank you fill in')

    c.setFillColor(OG)
    c.rect(0, 0, W, 40, fill=1, stroke=0)
    c.setFillColor(WHT)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 16, 'PDF  ·  MARKDOWN  ·  PLAIN TEXT  —  PASTE STRAIGHT INTO CLAUDE')
    c.showPage()


def howto(c):
    pg_bg(c)
    hdr(c)
    y = H - 52
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(MX, y, 'How to use this vault')
    y -= 30

    intro = ('Every prompt here is written to be pasted directly into Claude and edited. '
             'Anything in [SQUARE BRACKETS] is a blank for you to fill in — that is the only '
             'part you need to change. The .md and .txt versions in your download contain the '
             'same 200 prompts as plain text, so you can search them or drop them into Notion.')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 10.5)
    for line in wrap(intro, 10.5, CW):
        c.drawString(MX, y, line)
        y -= 15
    y -= 14

    rules = [
        ('1. Fill every bracket', 'A prompt with [TOPIC] left in it will get you a generic answer. '
                                  'The brackets are where your specificity goes.'),
        ('2. Add your context', 'Paste the actual document, code or data underneath the prompt. '
                                'Claude is far better at editing something real than inventing from nothing.'),
        ('3. Say what "good" looks like', 'Length, format, audience and tone. If you do not specify them, '
                                          'you get the average of everything Claude has seen.'),
        ('4. Iterate instead of restarting', 'Reply "shorter, and cut the third point" rather than '
                                             'rewriting the prompt. The conversation is the tool.'),
        ('5. Ask for the reasoning', 'For judgement calls, add "show your reasoning and say what would '
                                     'change your mind." It exposes weak conclusions.'),
    ]
    for head, body in rules:
        lines = wrap(body, 10, CW - 24)
        bh = len(lines) * 14 + 34
        c.setFillColor(PNL)
        c.roundRect(MX, y - bh, CW, bh, radius=4, fill=1, stroke=0)
        c.setFillColor(OG)
        c.rect(MX, y - bh, 3, bh, fill=1, stroke=0)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(MX + 14, y - 18, head)
        c.setFillColor(LGR)
        c.setFont('Helvetica', 10)
        ty = y - 34
        for line in lines:
            c.drawString(MX + 14, ty, line)
            ty -= 14
        y -= bh + 10

    lines = ['Role  — who Claude should be   |   Task  — the single thing to do',
             'Context — the material to work from   |   Constraints — length, tone, limits',
             'Format — exactly how the answer should be laid out']
    bh = len(lines) * 15 + 40
    c.setFillColor(HexColor('#0D2B0D'))
    c.roundRect(MX, y - bh, CW, bh, radius=4, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.rect(MX, y - bh, 4, bh, fill=1, stroke=0)
    c.setFillColor(GRN)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, y - 18, 'THE 5 PARTS OF A STRONG PROMPT')
    c.setFillColor(LGR)
    c.setFont('Helvetica', 9.5)
    ty = y - 36
    for line in lines:
        c.drawString(MX + 14, ty, line)
        ty -= 15

    ftr(c, 2, 'The Claude Prompt Vault  ·  How to use')
    c.showPage()


def contents(c, starts):
    pg_bg(c)
    hdr(c)
    y = H - 52
    c.setFillColor(OG)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(MX, y, 'Contents')
    y -= 34
    for i, (name, blurb, items) in enumerate(CATEGORIES):
        rh = 44
        c.setFillColor(PNL2 if i % 2 == 0 else PNL)
        c.roundRect(MX, y - rh + 4, CW, rh - 4, radius=3, fill=1, stroke=0)
        c.setFillColor(OG)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(MX + 12, y - rh + 24, '%02d' % (i + 1))
        c.setFillColor(CREAM)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(MX + 40, y - rh + 25, name)
        c.setFillColor(MGR)
        c.setFont('Helvetica', 8.5)
        c.drawString(MX + 40, y - rh + 12, blurb)
        c.setFillColor(OGL)
        c.setFont('Helvetica-Bold', 9)
        c.drawRightString(W - MX - 12, y - rh + 25, 'p.%d' % starts[i])
        c.setFillColor(MGR)
        c.setFont('Helvetica', 8)
        c.drawRightString(W - MX - 12, y - rh + 12, '%d prompts' % len(items))
        y -= rh + 4
    ftr(c, 3, 'The Claude Prompt Vault  ·  Contents')
    c.showPage()


def body_pages(c):
    page = 4
    y = TOP_Y
    label = ''

    def newpage():
        nonlocal page, y
        ftr(c, page, label)
        c.showPage()
        page += 1
        pg_bg(c)
        hdr(c)
        y = TOP_Y

    pg_bg(c)
    hdr(c)
    for ci, (name, blurb, items) in enumerate(CATEGORIES):
        if y - SEC_H < BOT_Y + 80:
            newpage()
        label = 'The Claude Prompt Vault  ·  %s' % name
        # Section band
        c.setFillColor(OG)
        c.roundRect(MX, y - SEC_H + 8, CW, SEC_H - 8, radius=4, fill=1, stroke=0)
        c.setFillColor(WHT)
        c.setFont('Helvetica-Bold', 14)
        c.drawString(MX + 12, y - 22, '%02d  %s' % (ci + 1, name.upper()))
        c.setFont('Helvetica', 8.5)
        c.drawString(MX + 12, y - 34, blurb)
        c.setFont('Helvetica-Bold', 9)
        c.drawRightString(W - MX - 12, y - 22, '%d PROMPTS' % len(items))
        y -= SEC_H

        for pi, (title, text) in enumerate(items):
            lines = prompt_lines(text, CW - PAD * 2)
            ch = card_height(lines)
            if y - ch < BOT_Y:
                newpage()
            c.setFillColor(PNL if pi % 2 == 0 else PNL2)
            c.roundRect(MX, y - ch, CW, ch, radius=4, fill=1, stroke=0)
            c.setFillColor(OGL)
            c.setFont(TITLE_F, TITLE_S)
            c.drawString(MX + PAD, y - PAD - 10, title)
            c.setFillColor(MGR)
            c.setFont('Helvetica-Bold', 8)
            c.drawRightString(W - MX - PAD, y - PAD - 10, '%02d.%02d' % (ci + 1, pi + 1))
            ty = y - PAD - 26
            for line in lines:
                if line:
                    draw_rich(c, MX + PAD, ty, line)
                ty -= LH
            y -= ch + CARD_GAP

    ftr(c, page, label)
    c.showPage()
    return page


# ------------------------------------------------------------------- exports

def export_md(path):
    L = ['# %s' % VAULT_TITLE, '', '*%s*' % VAULT_SUB, '',
         '%d prompts across %d categories. Anything in `[SQUARE BRACKETS]` is a blank to fill in.'
         % (total_prompts(), len(CATEGORIES)), '',
         'Part of the Claude AI Field Guide Series · 2026 Edition', '', '---', '', '## Contents', '']
    for i, (name, blurb, items) in enumerate(CATEGORIES):
        anchor = name.lower().replace(' & ', '--').replace(' ', '-')
        L.append('%d. [%s](#%s) — %d prompts — %s' % (i + 1, name, anchor, len(items), blurb))
    L += ['', '---', '']
    for i, (name, blurb, items) in enumerate(CATEGORIES):
        L += ['## %s' % name, '', '_%s_' % blurb, '']
        for j, (title, text) in enumerate(items):
            L += ['### %d.%d %s' % (i + 1, j + 1, title), '', '```text', text.strip(), '```', '']
        L += ['---', '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def export_txt(path):
    L = [VAULT_TITLE.upper(), VAULT_SUB, '',
         '%d prompts / %d categories. [SQUARE BRACKETS] = fill in the blank.' % (total_prompts(), len(CATEGORIES)),
         'Claude AI Field Guide Series - 2026 Edition', '']
    for i, (name, blurb, items) in enumerate(CATEGORIES):
        L += ['=' * 74, '%02d  %s  (%d prompts)' % (i + 1, name.upper(), len(items)), blurb, '=' * 74, '']
        for j, (title, text) in enumerate(items):
            L += ['[%d.%d] %s' % (i + 1, j + 1, title), '-' * 74, text.strip(), '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def verify_no_overflow():
    """Guard against the drawString overflow noted in CLAUDE.md."""
    limit = CW - PAD * 2
    bad = []
    for name, _, items in CATEGORIES:
        for title, text in items:
            if stringWidth(title, TITLE_F, TITLE_S) > limit - 40:
                bad.append(('title', name, title))
            for line in prompt_lines(text, limit):
                if line_width(line) > limit + 0.5:
                    bad.append(('body', title, line))
    return bad


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    bad = verify_no_overflow()
    if bad:
        for kind, where, what in bad:
            print('OVERFLOW %-6s %-28s %s' % (kind, where, what))
        raise SystemExit('%d overflowing lines — fix before shipping' % len(bad))
    starts, last = measure()

    pdf = os.path.join(OUTDIR, 'Claude_Prompt_Vault.pdf')
    c = canvas.Canvas(pdf, pagesize=LETTER)
    c.setTitle(VAULT_TITLE)
    c.setAuthor('Claude AI Field Guide Series')
    c.setSubject(VAULT_SUB)
    cover(c, last)
    howto(c)
    contents(c, starts)
    actual = body_pages(c)
    c.save()

    md = os.path.join(OUTDIR, 'Claude_Prompt_Vault.md')
    txt = os.path.join(OUTDIR, 'Claude_Prompt_Vault.txt')
    export_md(md)
    export_txt(txt)

    print('%-34s %3d pages  (predicted %d)' % (os.path.basename(pdf), actual, last))
    print('%-34s %d KB' % (os.path.basename(md), os.path.getsize(md) / 1024))
    print('%-34s %d KB' % (os.path.basename(txt), os.path.getsize(txt) / 1024))
    print('%d prompts / %d categories' % (total_prompts(), len(CATEGORIES)))


if __name__ == '__main__':
    main()
