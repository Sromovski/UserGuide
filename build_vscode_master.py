#!/usr/bin/env python3
"""
Build a single consolidated Word document that teaches someone how to use
Claude inside VS Code, drawing together all 23 Claude AI Field Guides into
one logically ordered technical manual.

Output: C:\\Projects\\UserGuide\\outputs\\Claude_in_VS_Code_Complete_Guide.docx
"""
import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r'C:\Projects\UserGuide\outputs\Claude_in_VS_Code_Complete_Guide.docx'

# ── Palette (professional light theme with the series' orange accent) ──────────
ORANGE   = RGBColor(0xC2, 0x5B, 0x1E)   # headings / accent
DARKSLATE= RGBColor(0x1F, 0x2A, 0x37)   # H2/H3 text
BODY     = RGBColor(0x22, 0x26, 0x2B)
MUTED    = RGBColor(0x60, 0x6A, 0x74)
CODE_FG  = RGBColor(0x1B, 0x2B, 0x1B)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

CODE_SHADE = 'F2F1EC'   # code block background
TIP_SHADE  = 'E7F3E7'
NOTE_SHADE = 'FDF3E2'
WARN_SHADE = 'FBE8E4'
KEY_SHADE  = 'ECEEF1'
HDR_SHADE  = 'C25B1E'   # table header fill


# ── Low-level helpers ─────────────────────────────────────────────────────────
def _shade(paragraph_or_cell, fill):
    """Apply a background shading fill to a paragraph or table cell."""
    if hasattr(paragraph_or_cell, 'paragraph_format'):  # paragraph
        pPr = paragraph_or_cell._p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill)
        pPr.append(shd)
    else:  # cell
        tcPr = paragraph_or_cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill)
        tcPr.append(shd)


def _border(paragraph, color='C25B1E', size='18', side='left'):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    b = OxmlElement(f'w:{side}')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), size)
    b.set(qn('w:space'), '8'); b.set(qn('w:color'), color)
    pbdr.append(b)
    pPr.append(pbdr)


def _spacing(p, before=4, after=4, line=None):
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = line


# ── Content helpers ────────────────────────────────────────────────────────────
def body(doc, text, before=3, after=6, size=10.5, color=BODY, italic=False, bold=False):
    p = doc.add_paragraph()
    _spacing(p, before, after, 1.15)
    r = p.add_run(text)
    r.font.size = Pt(size); r.font.color.rgb = color
    r.font.name = 'Calibri'; r.italic = italic; r.bold = bold
    return p


def bullets(doc, items, size=10.5):
    for it in items:
        p = doc.add_paragraph(style='List Bullet')
        _spacing(p, 1, 1, 1.1)
        # allow (bold, rest) tuple
        if isinstance(it, tuple):
            r = p.add_run(it[0] + ' '); r.bold = True
            r.font.size = Pt(size); r.font.color.rgb = BODY; r.font.name = 'Calibri'
            r2 = p.add_run(it[1]); r2.font.size = Pt(size)
            r2.font.color.rgb = BODY; r2.font.name = 'Calibri'
        else:
            r = p.add_run(it)
            r.font.size = Pt(size); r.font.color.rgb = BODY; r.font.name = 'Calibri'


def steps(doc, items, size=10.5):
    for it in items:
        p = doc.add_paragraph(style='List Number')
        _spacing(p, 1, 1, 1.1)
        r = p.add_run(it)
        r.font.size = Pt(size); r.font.color.rgb = BODY; r.font.name = 'Calibri'


def code(doc, lines):
    """Monospace shaded code block. Comments (# or //) rendered muted."""
    p = doc.add_paragraph()
    _spacing(p, 6, 6, 1.0)
    _shade(p, CODE_SHADE)
    _border(p, color='D8D5CC', size='6', side='left')
    p.paragraph_format.left_indent = Pt(6)
    for i, ln in enumerate(lines):
        run = p.add_run(('' if i == 0 else '\n') + ln)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        r = run._element.rPr.rFonts
        r.set(qn('w:ascii'), 'Consolas'); r.set(qn('w:hAnsi'), 'Consolas')
        if ln.strip().startswith('#') or ln.strip().startswith('//'):
            run.font.color.rgb = MUTED
        else:
            run.font.color.rgb = CODE_FG
    return p


def callout(doc, kind, heading, text_lines):
    """kind: 'tip' | 'note' | 'warn' | 'key'."""
    fills = {'tip': TIP_SHADE, 'note': NOTE_SHADE, 'warn': WARN_SHADE, 'key': KEY_SHADE}
    labels = {'tip': 'TIP', 'note': 'NOTE', 'warn': 'WATCH OUT', 'key': 'KEY IDEA'}
    borders = {'tip': '4E9A4E', 'note': 'D98A00', 'warn': 'C0392B', 'key': '5A6A78'}
    fill = fills[kind]
    p = doc.add_paragraph()
    _spacing(p, 6, 6, 1.12)
    _shade(p, fill)
    _border(p, color=borders[kind], size='18', side='left')
    p.paragraph_format.left_indent = Pt(8)
    p.paragraph_format.right_indent = Pt(6)
    lab = p.add_run(labels[kind] + '  ')
    lab.bold = True; lab.font.size = Pt(9)
    lab.font.name = 'Calibri'
    lab.font.color.rgb = RGBColor.from_string(borders[kind])
    hd = p.add_run((heading + '  ') if heading else '')
    hd.bold = True; hd.font.size = Pt(10); hd.font.name = 'Calibri'; hd.font.color.rgb = DARKSLATE
    if isinstance(text_lines, str):
        text_lines = [text_lines]
    body_txt = ' '.join(text_lines)
    tr = p.add_run(body_txt)
    tr.font.size = Pt(10); tr.font.name = 'Calibri'; tr.font.color.rgb = BODY
    return p


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.style = 'Table Grid'
    # header
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        _shade(hdr[i], HDR_SHADE)
        para = hdr[i].paragraphs[0]
        _spacing(para, 2, 2, 1.0)
        run = para.add_run(h)
        run.bold = True; run.font.size = Pt(9.5)
        run.font.color.rgb = WHITE; run.font.name = 'Calibri'
    # rows
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for ci, val in enumerate(row):
            if ci % 1 == 0 and ri % 2 == 1:
                _shade(cells[ci], 'F4F3EF')
            para = cells[ci].paragraphs[0]
            _spacing(para, 2, 2, 1.05)
            mono = ci == 0 and str(val).strip().startswith(('/', 'npm', 'git', 'claude',
                   'docker', 'node', 'nvm', '@', '-', 'brew', 'sudo', 'export', 'curl',
                   'pip', '~', '.', 'mkdir', 'code'))
            run = para.add_run(str(val))
            if ci == 0:
                run.bold = True
                run.font.color.rgb = ORANGE
            else:
                run.font.color.rgb = BODY
            run.font.size = Pt(9.5)
            run.font.name = 'Consolas' if mono else 'Calibri'
            if mono:
                rf = run._element.rPr.rFonts
                rf.set(qn('w:ascii'), 'Consolas'); rf.set(qn('w:hAnsi'), 'Consolas')
    if widths:
        for i, w in enumerate(widths):
            for cell in t.columns[i].cells:
                cell.width = Inches(w)
    _spacing(doc.add_paragraph(), 0, 2)
    return t


# ── Structural headings ────────────────────────────────────────────────────────
def part_heading(doc, num, title):
    doc.add_page_break()
    p = doc.add_paragraph()
    _spacing(p, 24, 2)
    r = p.add_run(f'PART {num}')
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = MUTED; r.font.name = 'Calibri'
    p2 = doc.add_paragraph()
    _spacing(p2, 0, 6)
    _border(p2, color='C25B1E', size='24', side='bottom')
    r2 = p2.add_run(title)
    r2.bold = True; r2.font.size = Pt(24); r2.font.color.rgb = ORANGE; r2.font.name = 'Calibri'


def chapter(doc, num, title):
    h = doc.add_heading(level=1)
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(6)
    r = h.add_run(f'{num}.  {title}')
    r.font.color.rgb = ORANGE; r.font.name = 'Calibri Light'; r.font.size = Pt(19)


def h2(doc, title):
    h = doc.add_heading(level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(3)
    r = h.add_run(title)
    r.font.color.rgb = DARKSLATE; r.font.name = 'Calibri'; r.font.size = Pt(13.5); r.bold = True


def h3(doc, title):
    h = doc.add_heading(level=3)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    r = h.add_run(title)
    r.font.color.rgb = RGBColor(0x40, 0x4A, 0x54); r.font.name = 'Calibri'; r.font.size = Pt(11.5); r.bold = True


# ══════════════════════════════════════════════════════════════════════════════
def build():
    doc = Document()

    # base style
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'; normal.font.size = Pt(10.5)
    normal.font.color.rgb = BODY

    section = doc.sections[0]
    section.top_margin = Inches(0.9)
    section.bottom_margin = Inches(0.9)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # ── COVER ──────────────────────────────────────────────────────────────────
    for _ in range(3):
        _spacing(doc.add_paragraph(), 0, 0)
    tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = tp.add_run('THE COMPLETE FIELD GUIDE')
    r.bold = True; r.font.size = Pt(13); r.font.color.rgb = MUTED; r.font.name = 'Calibri'
    tt = doc.add_paragraph(); tt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(tt, 6, 2)
    r = tt.add_run('Using Claude Inside VS Code')
    r.bold = True; r.font.size = Pt(34); r.font.color.rgb = ORANGE; r.font.name = 'Calibri Light'
    st = doc.add_paragraph(); st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(st, 2, 20)
    r = st.add_run('From Your First Chat to Agentic Coding, MCP, Automation & Scale')
    r.font.size = Pt(14); r.font.color.rgb = DARKSLATE; r.font.name = 'Calibri'; r.italic = True

    bar = doc.add_paragraph(); bar.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _border(bar, color='C25B1E', size='24', side='bottom')
    _spacing(bar, 0, 16)

    intro = doc.add_paragraph(); intro.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(intro, 6, 6, 1.2)
    r = intro.add_run(
        'A single, ordered path through everything you need to go from installing the tools to '
        'running fleets of AI coding agents — consolidated from the 23-guide Claude AI Field Guide '
        'Series into one technical reference. Every chapter includes the common commands and '
        'ready-to-use examples for that topic.')
    r.font.size = Pt(11); r.font.color.rgb = BODY; r.font.name = 'Calibri'

    meta = doc.add_paragraph(); meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _spacing(meta, 30, 0)
    r = meta.add_run('Updated for 2026  ·  Windows, macOS & Linux  ·  Claude Opus 4.8 / Sonnet 4.6 / Haiku 4.5')
    r.font.size = Pt(10); r.font.color.rgb = MUTED; r.font.name = 'Calibri'

    # ── TABLE OF CONTENTS ────────────────────────────────────────────────────────
    doc.add_page_break()
    chapter_toc = [
        ('PART I — Foundations: What Claude Is and Where It Lives', True),
        ('1.  Meet Claude: Models, Plans, and Surfaces', False),
        ('2.  Everyday Claude: Web, Mobile, Desktop, Chrome & Office', False),
        ('PART II — Setting Up Your Development Environment', True),
        ('3.  Installing Node.js', False),
        ('4.  Git & GitHub for Claude Users', False),
        ('5.  Docker Basics for AI Projects', False),
        ('6.  VS Code Setup for Claude', False),
        ('PART III — Claude Code in VS Code', True),
        ('7.  Installing Claude Code & Your First Edit', False),
        ('8.  Slash Commands & Keyboard Shortcuts', False),
        ('9.  CLAUDE.md — Give Claude a Project Memory', False),
        ('10.  Subagents & Hooks', False),
        ('11.  How Agentic Loops Work', False),
        ('PART IV — Extending Claude: MCP, Plugins & Skills', True),
        ('12.  MCP Servers 101', False),
        ('13.  Installing & Using MCP Servers', False),
        ('14.  Claude Plugins', False),
        ('15.  Claude Skills — Create Your Own', False),
        ('PART V — Automation & the API', True),
        ('16.  Claude API Basics', False),
        ('17.  Building Automations with Claude', False),
        ('PART VI — Getting Better Results & Scaling Up', True),
        ('18.  Prompting Masterclass', False),
        ('19.  Multi-Agent Orchestration', False),
        ('20.  Evaluating & Testing Claude Agents', False),
        ('21.  Cost & Token Management', False),
        ('Appendix A — Master Command Cheat Sheet', False),
        ('Appendix B — Troubleshooting Quick Reference', False),
    ]
    th = doc.add_paragraph()
    _spacing(th, 0, 10)
    r = th.add_run('Contents')
    r.bold = True; r.font.size = Pt(22); r.font.color.rgb = ORANGE; r.font.name = 'Calibri Light'
    for label, is_part in chapter_toc:
        p = doc.add_paragraph()
        _spacing(p, 3 if is_part else 0, 1, 1.05)
        r = p.add_run(label)
        r.font.name = 'Calibri'
        if is_part:
            r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = DARKSLATE
        else:
            r.font.size = Pt(10.5); r.font.color.rgb = BODY
            p.paragraph_format.left_indent = Pt(14)

    how = doc.add_paragraph()
    _spacing(how, 16, 0)
    callout(doc, 'note', 'How to read this guide',
            ['You do not have to read cover to cover. If you only want to code with Claude in VS Code, '
             'start at Part II, set up your environment, then work through Part III. Parts IV–VI go '
             'deeper as you need them. Each chapter ends with a commands table and worked examples.'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PART I
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'I', 'Foundations: What Claude Is and Where It Lives')

    # ── Chapter 1 ────────────────────────────────────────────────────────────────
    chapter(doc, 1, 'Meet Claude: Models, Plans, and Surfaces')
    body(doc, 'Claude is a family of AI assistants built by Anthropic with a focus on being helpful, '
              'harmless, and honest. Before you wire Claude into VS Code, it helps to know the three '
              'things that shape every interaction: which model you are talking to, which plan you are '
              'on, and which surface (app) you are using.')

    h2(doc, 'The Models (2026)')
    body(doc, 'Every Claude surface ultimately runs one of these models. You pick the model to trade off '
              'speed, cost, and raw capability.')
    table(doc, ['Model', 'Model ID', 'Context', 'Best for'], [
        ['Haiku 4.5', 'claude-haiku-4-5-20251001', '200K', 'Fast, cheap: classification, extraction, high-volume work'],
        ['Sonnet 4.6', 'claude-sonnet-4-6', '1M', 'Balanced default for most applications and coding'],
        ['Opus 4.8', 'claude-opus-4-8', '1M', 'Highest capability: complex reasoning, research, long context'],
    ], widths=[1.1, 2.3, 0.7, 3.0])

    h2(doc, 'The Plans')
    body(doc, 'The claude.ai subscription (below) is separate from API billing (Chapter 16). Claude Code '
              'runs on either a paid plan OR an API key — you pick one.')
    table(doc, ['Plan', 'Price', 'What you get'], [
        ['Free', '$0/mo', 'Sonnet 4.6, web search, file uploads, Artifacts, memory. Daily rolling limits.'],
        ['Pro', '$20/mo', 'Everything in Free + Opus, Projects, Research mode, Voice, Cowork, MS365. 5x usage.'],
        ['Max 5x / 20x', '$100–$200/mo', 'Same features as Pro, with 5x or 20x the usage ceiling for heavy users.'],
        ['Team', '$25+/seat', 'Org-wide access, shared Projects, admin controls, usage dashboard.'],
        ['Enterprise', 'Custom', 'SSO, custom data policies, Bedrock/Vertex hosting, priority support.'],
    ], widths=[1.3, 1.2, 4.0])
    callout(doc, 'warn', 'Paid plan required for Claude Code.',
            ['The free tier on claude.ai does NOT include Claude Code access. You need Pro, Max, Team, '
             'or Enterprise — or API billing via the Anthropic Console.'])

    h2(doc, 'The Surfaces — Every Way to Reach Claude')
    body(doc, 'This guide is about VS Code, but Claude lives in many places. They all sync to the same '
              'account, so your conversations and Projects follow you across devices.')
    table(doc, ['Surface', 'What it is for', 'Covered in'], [
        ['claude.ai (web)', 'Fastest start — chat, writing, analysis. No file access.', 'Chapter 2'],
        ['Mobile app', 'Claude on iOS/Android: voice mode, camera input, on the go.', 'Chapter 2'],
        ['Desktop app', 'Native Mac/Windows app: panels, terminal, MCP extensions, Cowork.', 'Chapter 2'],
        ['Claude in Chrome', 'Browser agent that reads pages and automates web tasks.', 'Chapter 2'],
        ['Office & Slack', 'Claude inside Excel, Word, PowerPoint, Outlook, and Slack.', 'Chapter 2'],
        ['Claude Code', 'Agentic coding in the terminal and VS Code — the heart of this guide.', 'Part III'],
        ['The API', 'Programmatic access for your own apps and automations.', 'Part V'],
    ], widths=[1.5, 3.5, 1.2])

    # ── Chapter 2 ────────────────────────────────────────────────────────────────
    chapter(doc, 2, 'Everyday Claude: Web, Mobile, Desktop, Chrome & Office')
    body(doc, 'You will do your deepest work in VS Code, but the other surfaces are worth knowing — they '
              'are where you plan, research, and handle quick tasks that do not need a codebase. This '
              'chapter is a fast tour; skip ahead to Part II if you only want the coding setup.')

    h2(doc, 'Claude on the Web (claude.ai)')
    body(doc, 'No download, no setup. Open a browser, sign up in under three minutes (use Google or Apple '
              'sign-in to skip email verification), and start typing. Ten things worth trying on day one:')
    table(doc, ['Try this', 'Example prompt'], [
        ['Explain something', '"Explain how the internet works to a 10-year-old"'],
        ['Summarize a document', 'Upload a PDF → "Summarise the key points"'],
        ['Write with you', '"Help me write a professional email declining a meeting"'],
        ['Live web research', 'Toggle search → "What is happening with [topic] in 2026?"'],
        ['Write simple code', '"Write Python to rename all files in a folder by date"'],
        ['Build an Artifact', '"Create a dark-theme HTML to-do list app"'],
    ], widths=[1.8, 4.4])
    callout(doc, 'tip', 'Build on context.',
            ['Claude remembers the whole conversation — build on earlier answers without repeating '
             'yourself. On Pro, use Projects to keep persistent context across many sessions on one topic.'])

    h2(doc, 'The Mobile App (iOS & Android)')
    body(doc, 'Free to download from the App Store or Google Play ("Claude by Anthropic"). Log in with the '
              'same account and everything syncs. Two standout mobile features:')
    bullets(doc, [
        ('Voice mode:', 'tap the microphone to have a natural spoken conversation. Five voice personalities '
                        '(Buttery, Airy, Mellow, Glassy, Professional). English only as of 2026.'),
        ('Camera input:', 'point at a menu, whiteboard, chart, sign, or screen of code and ask about it — '
                          '"Summarise these notes into action items," "Translate this," "Find the bug."'),
    ])

    h2(doc, 'The Desktop App (Mac & Windows)')
    body(doc, 'Download from claude.ai/download (macOS 11+ or Windows 10 64-bit+). The April 2026 redesign '
              'added a developer-grade multi-panel layout: a sessions sidebar (run sessions in parallel), '
              'a built-in terminal, a file editor, a diff viewer, and a preview pane. It also offers '
              'one-click MCP extensions (Google Drive, Slack, GitHub, Filesystem, Linear, Notion) and '
              'Cowork, which runs code in an isolated sandbox limited to folders you explicitly connect.')

    h2(doc, 'Claude in Chrome')
    body(doc, 'A browser agent that lives in a side panel and can see the current page. Install from the '
              'Chrome Web Store (or claude.com/claude-for-chrome). It is in beta for paid plans. It can '
              'summarize pages, extract structured data, fill forms, and run multi-step tasks across tabs.')
    callout(doc, 'note', 'Tell Claude your goal, not the clicks.',
            ['"Research 5 competitors and summarise each" beats step-by-step clicking instructions. '
             'Claude can see page text, links, and form labels — but never your passwords, autofill, or '
             'incognito tabs, and only while the panel is open.'])

    h2(doc, 'Claude in Office & Slack')
    body(doc, 'On a paid plan you can add Claude to Slack (the "Claude Tag": /invite @Claude to a channel, '
              'then @Claude your question) and install Microsoft 365 add-ins for Excel, Word, PowerPoint, '
              'and Outlook from AppSource. In Excel it builds and audits formulas; in Word it edits with '
              'tracked changes; in PowerPoint it builds on-brand slides inside your template; in Outlook '
              '(beta) it triages your inbox and drafts replies.')

    # ═══════════════════════════════════════════════════════════════════════════
    # PART II
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'II', 'Setting Up Your Development Environment')
    body(doc, 'Claude Code needs a small stack of standard developer tools underneath it. This part installs '
              'them in the order that matters: Node.js (which provides the installer for Claude Code), Git '
              '(which Claude Code uses to track changes), optionally Docker, and finally VS Code itself.')

    # ── Chapter 3 ────────────────────────────────────────────────────────────────
    chapter(doc, 3, 'Installing Node.js')
    callout(doc, 'key', '', ['Node.js lets you run JavaScript tools outside a browser. Claude Code, the '
            'Anthropic SDK, and most AI dev tools require it. Installing Node also installs npm — the '
            'package manager you will use to install Claude Code. You do not need to write any JavaScript.'])
    body(doc, 'Think of Node.js as a car engine: you do not need to understand how it works to drive. '
              'Claude Code is the car; Node is the engine underneath. Install it once and forget about it.')

    h2(doc, 'Which Version?')
    bullets(doc, [
        ('Node.js 24 — Active LTS.', 'The safe choice. Install this unless you have a specific reason not to.'),
        ('Node.js 26 — Current.', 'Newer, becomes LTS in October 2026. For early adopters.'),
        ('Node.js 22 — Maintenance LTS.', 'Still supported but retiring in 2027.'),
    ])

    h2(doc, 'Install on macOS (recommended: nvm)')
    body(doc, 'Open Terminal and run these in order. nvm (Node Version Manager) lets you switch versions easily.')
    code(doc, [
        '# 1. Install Homebrew (skip if you already have it)',
        '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        '',
        '# 2. Install nvm, then add it to your shell profile (~/.zshrc)',
        'brew install nvm',
        'export NVM_DIR="$HOME/.nvm"',
        '[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \\. "/opt/homebrew/opt/nvm/nvm.sh"',
        '',
        '# 3. Install and use the LTS release, then verify',
        'nvm install lts',
        'nvm use lts',
        'node -v     # expected: v24.x.x',
        'npm -v      # expected: 10.x.x or higher',
    ])
    body(doc, 'Prefer not to use nvm? Download the LTS installer directly from nodejs.org and run the .pkg.')

    h2(doc, 'Install on Windows')
    body(doc, 'Easiest path — the direct installer:')
    steps(doc, [
        'Go to nodejs.org and click "Download Node.js (LTS)".',
        'Run the .msi installer and accept all defaults.',
        'Open a NEW PowerShell window (search "PowerShell" in Start).',
        'Run node -v (should show v24.x.x) and npm -v (10.x.x or higher).',
    ])
    body(doc, 'For version management use nvm-windows (github.com/coreybutler/nvm-windows) — nvm for Mac/Linux '
              'does NOT work on Windows.')
    callout(doc, 'warn', 'Run PowerShell as Administrator with nvm-windows.',
            ['Regular PowerShell will get "access denied" errors when switching Node versions.'])

    h2(doc, 'Install on Linux / WSL')
    code(doc, [
        '# Install nvm, restart the terminal, then:',
        'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/HEAD/install.sh | bash',
        'nvm install lts',
        'nvm use lts',
        'node -v',
    ])
    callout(doc, 'tip', 'Always test in a fresh terminal.',
            ['After installing, run node -v and npm -v in a NEW terminal window. Old windows do not pick '
             'up the updated PATH.'])

    h2(doc, 'Common npm Commands')
    table(doc, ['Command', 'What it does'], [
        ['npm install -g @anthropic-ai/claude-code', 'Install Claude Code globally (all projects)'],
        ['npm install <package>', 'Install a package in the current project'],
        ['npm install -g <package>', 'Install a package globally'],
        ['npm list -g', 'List globally installed packages'],
        ['npm update -g <package>', 'Update a globally installed package'],
        ['node -v  /  npm -v', 'Check your Node / npm version'],
    ], widths=[3.2, 3.0])

    h2(doc, 'Common Errors')
    table(doc, ['Problem', 'Fix'], [
        ['"node: command not found"', 'Restart the terminal; if still missing, reinstall Node.js.'],
        ['"EACCES" / permission denied on -g install', 'Do NOT use sudo. Set npm prefix: npm config set prefix ~/.npm-global and add it to PATH.'],
        ['nvm: command not found after install', 'Source your profile: source ~/.zshrc, then retry.'],
        ['Wrong version active', 'nvm use 24 (or your target version).'],
    ], widths=[2.6, 3.6])

    # ── Chapter 4 ────────────────────────────────────────────────────────────────
    chapter(doc, 4, 'Git & GitHub for Claude Users')
    callout(doc, 'key', '', ['Git is a version-control system: it tracks every change to your files and lets '
            'you go back in time if something breaks. GitHub is a website that stores Git projects online. '
            'Claude Code uses Git automatically to track the changes it makes — so Git lets you review '
            'every AI edit.'])

    h2(doc, 'Plain-English Glossary')
    table(doc, ['Term', 'Meaning'], [
        ['Repository (repo)', 'A folder Git watches. Every file change inside is tracked.'],
        ['Commit', 'A saved snapshot of your project at a moment in time.'],
        ['Branch', 'A separate version of your project where you try changes safely.'],
        ['main / master', 'The primary, stable branch.'],
        ['Push / Pull', 'Upload commits to GitHub / download the latest from GitHub.'],
        ['Clone', 'Download a GitHub repo to your computer for the first time.'],
        ['Pull Request (PR)', 'A request to merge changes from one branch into another.'],
        ['Fork', "Your personal copy of someone else's repository."],
    ], widths=[1.7, 4.5])

    h2(doc, 'Install & First-Time Setup')
    code(doc, [
        '# macOS',
        'brew install git          # or download from git-scm.com',
        '# Windows: download Git for Windows from git-scm.com, run installer',
        '# Linux',
        'sudo apt update && sudo apt install git',
        '',
        'git --version             # expect: git version 2.49.x',
        '',
        '# Tell Git who you are (do this once)',
        'git config --global user.name "Your Name"',
        'git config --global user.email "you@example.com"',
        'git config --global core.editor "code --wait"   # use VS Code as editor',
    ])
    body(doc, 'Create a free account at github.com, then authenticate. The GitHub CLI (gh) makes this easiest:')
    code(doc, [
        'winget install GitHub.cli     # Windows',
        'brew install gh               # macOS',
        'gh auth login                 # follow the prompts',
    ])

    h2(doc, 'The 7 Commands You Use 90% of the Time')
    table(doc, ['Command', 'What it does'], [
        ['git init', 'Turn a regular folder into a Git repository.'],
        ['git status', 'See which files changed since your last commit.'],
        ['git add .', 'Stage files (all changes) for your next commit.'],
        ['git commit -m "message"', 'Save a snapshot with a descriptive message.'],
        ['git push', 'Upload your commits to GitHub.'],
        ['git pull', 'Download the latest changes from GitHub.'],
        ['git clone <url>', 'Download a repo from GitHub to your computer.'],
    ], widths=[2.4, 3.8])

    h2(doc, 'Example: Push Your First Project')
    code(doc, [
        'mkdir my-first-project && cd my-first-project',
        'git init',
        '# create a file (e.g. README.md) with any text editor',
        'git add .',
        'git commit -m "Initial commit"',
        '',
        '# create an empty repo on github.com, copy its HTTPS URL, then:',
        'git remote add origin https://github.com/YOU/my-first-project.git',
        'git branch -M main',
        'git push -u origin main',
    ])
    table(doc, ['Problem', 'Fix'], [
        ['"fatal: not a git repository"', 'Run git init first, or cd into your project folder.'],
        ['"rejected" on git push', 'Run git pull first to merge remote changes, then push again.'],
        ['Wrong email on commits', 'git config --global user.email "right@email.com"'],
    ], widths=[2.6, 3.6])

    # ── Chapter 5 ────────────────────────────────────────────────────────────────
    chapter(doc, 5, 'Docker Basics for AI Projects')
    callout(doc, 'key', '', ['Docker packages your app and everything it needs — code, libraries, settings — '
            'into a single portable unit called a container that runs identically anywhere. "Works on my '
            'machine" stops being an excuse. This chapter is optional for basic Claude Code use but valuable '
            'once you build shareable AI services.'])
    body(doc, 'The lunchbox analogy: a container is a lunchbox for your app, holding the food (code), '
              'utensils (dependencies), and napkin (config). No matter whose desk you open it on, lunch is '
              'the same. Docker is the factory that makes and manages the lunchboxes.')

    h2(doc, 'Containers vs Virtual Machines')
    table(doc, ['Factor', 'Container (Docker)', 'Virtual Machine'], [
        ['Start time', 'Seconds', 'Minutes'],
        ['Size', 'Megabytes', 'Gigabytes'],
        ['Shares OS kernel', 'Yes (lightweight)', 'No (each has its own)'],
        ['Use case', 'Dev tools, APIs, AI services', 'Full OS isolation needed'],
    ], widths=[1.5, 2.5, 2.2])
    callout(doc, 'note', 'Licensing.',
            ['Docker Desktop is free for personal use, students, education, open source, and small business '
             '(under 250 employees AND under $10M revenue). Paid plans start at $9/month for larger '
             'organisations. The CLI tools (engine, compose) are always free and open source.'])

    h2(doc, 'Essential Commands')
    table(doc, ['Command', 'What it does'], [
        ['docker run hello-world', 'Verify your install.'],
        ['docker pull <image>:<tag>', 'Download an image from Docker Hub.'],
        ['docker run -it <image> bash', 'Run a container interactively.'],
        ['docker run -d -p 8080:80 <image>', 'Run in the background with a mapped port.'],
        ['docker ps  /  docker ps -a', 'List running / all containers.'],
        ['docker stop <id>', 'Stop a running container.'],
        ['docker build -t my-app:latest .', 'Build an image from a Dockerfile.'],
        ['docker logs -f <id>', 'Follow a container\'s live output.'],
        ['docker compose up / down', 'Start / stop a multi-container stack.'],
    ], widths=[2.9, 3.3])

    h2(doc, 'Example: docker-compose.yml for a Claude API Project')
    code(doc, [
        'version: "3.9"',
        'services:',
        '  app:',
        '    build: .',
        '    ports:',
        '      - "3000:3000"',
        '    environment:',
        '      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}',
        '    volumes:',
        '      - .:/app',
        '',
        '# start everything with one command:',
        'docker compose up',
    ])

    # ── Chapter 6 ────────────────────────────────────────────────────────────────
    chapter(doc, 6, 'VS Code Setup for Claude')
    body(doc, 'VS Code (Visual Studio Code) is a free, open-source editor from Microsoft — the world\'s most '
              'popular development environment and the officially recommended editor for Claude Code. The '
              'Claude Code extension brings AI assistance directly into your editor with inline diffs and '
              'automatic file context.')
    callout(doc, 'note', 'Requirements.',
            ['VS Code 1.98.0 or higher (required by the Claude Code extension), Node.js installed '
             '(Chapter 3), and an Anthropic account. Download VS Code free at code.visualstudio.com.'])

    h2(doc, 'Interface Tour')
    table(doc, ['Panel', 'Shortcut', 'What it does'], [
        ['Activity Bar', '—', 'Left edge: Explorer, Search, Source Control, Extensions, Claude.'],
        ['Explorer', 'Ctrl+Shift+E', 'File tree of your open folder.'],
        ['Source Control', 'Ctrl+Shift+G', 'Git integration — stage, commit, push without the terminal.'],
        ['Extensions', 'Ctrl+Shift+X', 'Search and install extensions.'],
        ['Terminal', 'Ctrl+` (backtick)', 'Run any command in your project directory.'],
        ['Command Palette', 'Ctrl+Shift+P', 'Run any action by name — the most powerful shortcut.'],
    ], widths=[1.5, 1.5, 3.2])

    h2(doc, 'Five Essential Extensions')
    table(doc, ['Extension', 'Publisher', 'Why'], [
        ['Claude Code', 'Anthropic', 'The official extension — inline diffs, context-aware prompting.'],
        ['GitLens', 'GitKraken', 'Git blame per line, file history, branch comparison.'],
        ['ESLint', 'Microsoft', 'Flags JS/TS errors and style issues as you type.'],
        ['Prettier', 'Prettier', 'Auto-formats code on save for consistent style.'],
        ['Error Lens', 'Alexander', 'Shows error messages inline on the same line.'],
    ], widths=[1.4, 1.3, 3.5])

    h2(doc, 'Recommended settings.json')
    body(doc, 'Open with Ctrl+Shift+P → "Open User Settings (JSON)":')
    code(doc, [
        '{',
        '  "editor.formatOnSave": true,',
        '  "editor.defaultFormatter": "esbenp.prettier-vscode",',
        '  "editor.fontSize": 14,',
        '  "editor.tabSize": 2,',
        '  "editor.wordWrap": "on",',
        '  "terminal.integrated.fontSize": 13,',
        '  "files.autoSave": "afterDelay",',
        '  "git.confirmSync": false,',
        '  "editor.minimap.enabled": false',
        '}',
    ])
    callout(doc, 'tip', 'Always open a folder, not just a file.',
            ['With a folder open, Claude has context about your full project structure. File → Open Folder → '
             'select your project directory.'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PART III
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'III', 'Claude Code in VS Code')
    body(doc, 'This is the core of the guide. Claude Code is Anthropic\'s official agentic coding tool: it '
              'reads and edits files, runs terminal commands, searches your codebase, and reasons about your '
              'project — all from plain-English prompts. The rest of this part takes you from install to a '
              'first edit, then through the features that make it powerful: slash commands, CLAUDE.md, hooks, '
              'and the agentic loop.')

    # ── Chapter 7 ────────────────────────────────────────────────────────────────
    chapter(doc, 7, 'Installing Claude Code & Your First Edit')
    h2(doc, 'Claude Code vs Claude on the Web')
    bullets(doc, [
        ('claude.ai (web/app):', 'great for questions, writing, and analysis. No file access.'),
        ('Claude Code (CLI + extension):', 'reads and edits files, runs commands, searches your codebase. '
                                           'Think of it as Claude that lives inside your project.'),
    ])
    body(doc, 'What Claude Code can do: read/write/edit any file, run terminal commands (with your approval), '
              'search your whole codebase, explain code and suggest refactors, work as an agent that breaks a '
              'task into steps, and show you a diff before applying any change.')

    h2(doc, 'Install (5 Steps)')
    steps(doc, [
        'Install the CLI: run the command below in a terminal. Do NOT use sudo — if you hit a permission error, use nvm (Chapter 3).',
        'Verify: claude --version should print a version number.',
        'Install the VS Code extension: press Ctrl+Shift+X, search "Claude Code", install the one by Anthropic. A Claude icon appears in the Activity Bar.',
        'Authenticate: click the Claude icon → "Sign In". A browser opens to claude.ai — log in, then return to VS Code.',
        'Set up terminal integration: in the Claude panel, type /terminal-setup so Shift+Enter inserts a newline instead of submitting.',
    ])
    code(doc, [
        '# Step 1: install the Claude Code CLI',
        'npm install -g @anthropic-ai/claude-code',
        '',
        '# Step 2: verify',
        'claude --version',
    ])
    callout(doc, 'tip', 'Using an API key instead of a Claude account.',
            ['Set ANTHROPIC_API_KEY in your environment, then open VS Code from that same terminal session '
             'so the variable is inherited.'])

    h2(doc, 'Your First Edit — The Core Workflow')
    body(doc, 'Open a folder → ask Claude → review the diff → accept or reject.')
    steps(doc, [
        'Open a folder: File → Open Folder → your project. Claude Code works at the folder level.',
        'Open the Claude panel: click the Claude icon in the Activity Bar. A chat panel opens on the right.',
        'Give Claude a task in plain English (examples below).',
        'The trust dialog: the first time Claude edits a file, approve trust for this folder ("Allow").',
        'Review the diff: green = additions, red = deletions. Click Accept to apply or Reject to discard.',
    ])
    h3(doc, 'Example prompts for a first edit')
    code(doc, [
        '"Add a function that calculates the total of an array"',
        '"Fix the bug on line 42 of utils.js"',
        '"Explain what the parse() function does"',
    ])
    callout(doc, 'note', 'Context is automatic.',
            ['The file open in your editor is automatically included in Claude\'s context. Select code with '
             'your cursor and it is added to the prompt. You can also drag files into the panel. More '
             'context = better suggestions.'])

    # ── Chapter 8 ────────────────────────────────────────────────────────────────
    chapter(doc, 8, 'Slash Commands & Keyboard Shortcuts')
    body(doc, 'Type / in the Claude panel to see every command. These are the ones you will actually use.')
    table(doc, ['Command', 'What it does'], [
        ['/help', 'Show all slash commands with a brief description of each.'],
        ['/clear', 'Clear the conversation history. File edits already made are kept.'],
        ['/compact', 'Summarise older messages to shrink context while keeping key decisions.'],
        ['/status', 'Show version, model, auth status, and token usage.'],
        ['/cost', 'Display token usage and estimated cost for the session.'],
        ['/doctor', 'Run a diagnostics check if Claude Code stops responding.'],
        ['/terminal-setup', 'Configure VS Code keybindings for multi-line prompts.'],
        ['/plugins', 'Open the Manage Plugins interface to enable/disable MCP servers.'],
        ['/skills', 'List all currently loaded skills (Chapter 15).'],
        ['/routines', 'Open the Routines panel for cloud automations (Chapter 17).'],
    ], widths=[1.9, 4.3])

    h2(doc, 'Keyboard Shortcuts in the Claude Panel')
    table(doc, ['Key', 'Action'], [
        ['Enter', 'Send your message / submit the prompt.'],
        ['Shift+Enter', 'New line in the prompt (after /terminal-setup).'],
        ['Up / Down arrows', 'Navigate your prompt history.'],
        ['Ctrl+L', 'Clear the conversation (same as /clear).'],
        ['Escape', "Cancel Claude's current response mid-stream."],
        ['Ctrl+C', 'Exit Claude Code entirely (edits already made are kept).'],
    ], widths=[1.7, 4.5])

    # ── Chapter 9 ────────────────────────────────────────────────────────────────
    chapter(doc, 9, 'CLAUDE.md — Give Claude a Project Memory')
    callout(doc, 'key', '', ['CLAUDE.md is a plain Markdown file at the root of your project. Claude Code reads '
            'it automatically at the start of every session, before you type a prompt. It gives Claude '
            'persistent project memory: your stack, build commands, architecture, and rules — without you '
            'repeating them every time.'])
    body(doc, 'By default Claude Code has no memory between sessions. Every time you open a project it starts '
              'fresh. CLAUDE.md is the fix — a briefing that loads automatically. It is the difference between '
              'Claude as smart autocomplete and Claude as a team member.')

    h2(doc, 'Where Claude Looks')
    table(doc, ['Location', 'Scope'], [
        ['~/CLAUDE.md', 'Home directory — applies to ALL your projects (global defaults).'],
        ['./CLAUDE.md', 'Project root — the main file for this project.'],
        ['./src/CLAUDE.md', 'Subdirectory — loaded when Claude works in that folder.'],
        ['./.claude/CLAUDE.md', 'Hidden folder — same as root but keeps the root clean.'],
    ], widths=[1.9, 4.3])
    callout(doc, 'warn', 'Keep it under 200 lines.',
            ['Every line consumes context budget on every turn. A bloated CLAUDE.md pushes out space for the '
             'actual code Claude needs. Be concise: commands not explanations, paths not prose. If a section '
             'grows, move detail to a linked file (progressive disclosure).'])

    h2(doc, 'The 6 Sections Every CLAUDE.md Needs — Template')
    code(doc, [
        '# PROJECT NAME - Claude AI Build Plan',
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
        'src/         - application source code',
        'src/api/     - route handlers and controllers',
        'src/lib/     - shared utility functions',
        'tests/       - test files mirror src/ structure',
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
        '- Run tests after any code change before marking a task done',
        '- Ask before adding new dependencies',
        '- One feature per PR - keep commits atomic',
    ])
    callout(doc, 'warn', 'Never put secrets in CLAUDE.md.',
            ['It is checked into git. Keep API keys and passwords in .env instead.'])

    h2(doc, 'CLAUDE.md vs Hooks — When to Use Which')
    table(doc, ['Aspect', 'CLAUDE.md', 'Hooks'], [
        ['Enforcement', 'Advisory — followed ~70–90% of the time', 'Deterministic — always runs, cannot be skipped'],
        ['Use for', 'Stack, architecture, conventions, preferences', 'Linting, testing, security checks, auto-format'],
        ['Runs when', 'Start of every session (auto-loaded)', 'PreToolUse, PostToolUse, Stop, Notification'],
        ['Mental model', 'A team wiki (context)', 'A CI/CD pipeline (guarantees)'],
    ], widths=[1.3, 2.5, 2.4])

    # ── Chapter 10 ───────────────────────────────────────────────────────────────
    chapter(doc, 10, 'Subagents & Hooks')
    h2(doc, 'Subagents — Claude Working in Parallel')
    body(doc, 'A subagent is a separate Claude instance the main Claude spawns to handle a specific subtask. '
              'This lets Claude divide complex work — researching in one thread while coding in another, or '
              'running several independent tasks at once to finish faster. Claude spawns them automatically '
              'when a task can be parallelised or a step needs isolated focus.')
    table(doc, ['Aspect', 'Main Agent', 'Subagent'], [
        ['Context', 'Full conversation history', 'Scoped to its subtask only'],
        ['Tools', 'All tools (Read, Edit, Bash, ...)', 'Same tools, isolated scope'],
        ['Duration', 'Entire session', 'One task, then terminates'],
    ], widths=[1.3, 2.4, 2.5])

    h2(doc, 'The 8 Hook Lifecycle Events')
    body(doc, 'Hooks are shell commands that fire automatically at key moments. Configure them in '
              '.claude/settings.json.')
    table(doc, ['Event', 'Fires', 'Use it for'], [
        ['SessionStart', 'Once per session', 'Load context or a welcome message.'],
        ['SessionEnd', 'Once per session', 'Cleanup, logging, cost summaries.'],
        ['UserPromptSubmit', 'Every turn', 'Pre-process or validate your prompt.'],
        ['PreToolUse', 'Every tool call', 'Block dangerous commands, enforce permissions, log.'],
        ['PostToolUse', 'Every tool call', 'Run linters, tests, or format code automatically.'],
        ['Stop', 'Every turn', 'Send notifications, trigger next steps.'],
        ['StopFailure', 'On error', 'Alert or attempt recovery.'],
        ['Notification', 'On specific events', 'permission_prompt, idle, auth_success, dialogs.'],
    ], widths=[1.5, 1.5, 3.2])
    callout(doc, 'note', 'Two config files.',
            ['.claude/settings.json is committed to git and shared with the team. '
             '.claude/settings.local.json is gitignored and personal. Both load; local overrides shared.'])

    h2(doc, 'Working Hook Examples (.claude/settings.json)')
    code(doc, [
        '{',
        '  "hooks": {',
        '    "PostToolUse": [{',
        '      "matcher": "Edit|Write",',
        '      "hooks": [{ "type": "command",',
        '                  "command": "npx eslint --fix ${file}",',
        '                  "timeout": 30 }]',
        '    }],',
        '    "PreToolUse": [{',
        '      "matcher": "Bash",',
        '      "hooks": [{ "type": "command",',
        '                  "command": "python guard.py --check-command",',
        '                  "timeout": 5 }]',
        '    }],',
        '    "Stop": [{',
        '      "matcher": "",',
        '      "hooks": [{ "type": "command",',
        '                  "command": "curl -d \'Claude is done\' ntfy.sh/my-topic" }]',
        '    }]',
        '  }',
        '}',
    ])
    h3(doc, 'The matcher field')
    table(doc, ['Matcher', 'Matches'], [
        ['"Edit|Write"', 'File-editing tools.'],
        ['"Bash"', 'Shell commands.'],
        ['"" (empty)', 'Everything.'],
    ], widths=[1.8, 4.4])
    body(doc, 'A hook that returns exit code 0 allows the tool call; a non-zero exit code (1) blocks it. '
              'Default timeout is 60 seconds per hook. Use full paths (/usr/bin/python3) inside hooks.')

    # ── Chapter 11 ───────────────────────────────────────────────────────────────
    chapter(doc, 11, 'How Agentic Loops Work')
    body(doc, 'A single Claude response is just a reply. An agentic loop is what happens when Claude takes '
              'multiple actions — reading files, running commands, writing code — to complete a goal that '
              'cannot be done in one step. Claude plans, acts, sees what happened, and decides what to do '
              'next, repeating until done or a stopping condition is met.')

    h2(doc, 'The 4-Step Loop')
    table(doc, ['Step', 'What happens'], [
        ['1. Receive', 'Claude gets your prompt + full history + system instructions + tool definitions.'],
        ['2. Evaluate', 'Claude decides: answer directly, or call one/more tools.'],
        ['3. Tool Call', 'A tool runs (Read, Edit, Bash, Grep...); its output is appended to history.'],
        ['4. Decide', 'Claude reads the result and decides again: another tool, or a final answer.'],
    ], widths=[1.4, 4.8])

    h2(doc, 'The Tools Available in the Loop')
    table(doc, ['Tool', 'Purpose'], [
        ['Read / Write / Edit', 'Read a file / create-overwrite / make a targeted change.'],
        ['Bash', 'Run a shell command and capture output.'],
        ['Grep / Glob', 'Search file contents / find files by name pattern.'],
        ['Agent', 'Spawn a subagent for a parallel task.'],
        ['WebFetch', 'Fetch content from a URL.'],
    ], widths=[1.9, 4.3])

    h2(doc, 'Example Loop Trace — "Fix the broken test"')
    table(doc, ['Turn', 'Tool', 'Action'], [
        ['1', 'Read', 'Read the failing test file to understand the error.'],
        ['2', 'Read', 'Read the source file the test is testing.'],
        ['3', 'Bash', 'Run the test suite to see the actual error output.'],
        ['4', 'Edit', 'Apply the fix to the source file.'],
        ['5', 'Bash', 'Run the tests again to verify the fix works.'],
        ['6', 'Stop', 'Report: "Tests passing. Fixed on line 42."'],
    ], widths=[0.8, 1.0, 4.4])

    h2(doc, 'Stopping Conditions & Cost Control')
    body(doc, 'The loop is not infinite. It stops when: the task is complete (Claude calls Stop), --max-turns '
              'is reached, the token budget (max_budget_usd) is exceeded, a PreToolUse hook returns non-zero, '
              'or you press Escape.')
    callout(doc, 'warn', 'Context grows every iteration.',
            ['Every tool result is re-sent to the model on the next call. A loop can accumulate 50,000+ '
             'tokens by iteration 20, and each iteration costs more than the last.'])
    table(doc, ['Lever', 'How'], [
        ['/status', 'Check current token count and estimated cost at any time.'],
        ['/compact', 'Summarise history — a 60–80% context reduction. Run it before long tasks.'],
        ['Explicit stop criteria', 'In your prompt: "After making edits, run the tests once and then stop."'],
        ['--max-turns N', 'CLI/SDK flag: hard cap on the number of tool calls.'],
        ['max_budget_usd', 'API parameter: halt the loop if cost exceeds a limit.'],
        ['Escape', 'Interrupt the loop immediately; edits made so far are kept.'],
    ], widths=[1.9, 4.3])
    callout(doc, 'tip', 'Always cap unattended runs.',
            ['For overnight automation, always set max_budget_usd. An unexpected infinite loop can be very '
             'costly without a spend cap.'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PART IV
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'IV', 'Extending Claude: MCP, Plugins & Skills')
    body(doc, 'Out of the box Claude Code reads and edits your files. To connect it to the wider world — '
              'GitHub, databases, web search, your own tools — you use MCP servers. Plugins and skills add '
              'further capability with less setup. This part covers all three.')

    # ── Chapter 12 ───────────────────────────────────────────────────────────────
    chapter(doc, 12, 'MCP Servers 101')
    callout(doc, 'key', '', ['MCP — the Model Context Protocol — is an open standard created by Anthropic in '
            'late 2024. It is a common language that lets Claude connect to external tools, data, and '
            'services. It is "USB for AI tools": one protocol, any tool, any model. Over 16,000 servers '
            'exist as of mid-2026.'])

    h2(doc, 'The Three-Layer Architecture')
    table(doc, ['Layer', 'What it is'], [
        ['Host', 'The app Claude lives in — Claude Desktop or Claude Code (VS Code).'],
        ['Client', 'Lives inside the Host; manages the connection to one specific server.'],
        ['Server', 'A separate program (local or remote) that exposes Tools, Resources, and Prompts.'],
    ], widths=[1.3, 4.9])
    h3(doc, 'How a request flows')
    steps(doc, [
        'You type: "Summarise the open issues in my GitHub repo."',
        'Claude (Host) recognises this needs the GitHub MCP server.',
        'The Client calls the server: list_issues(repo="myname/myrepo").',
        'The Server contacts the GitHub API and returns the issues.',
        'The Client passes the result back; Claude writes your summary.',
    ])

    h2(doc, 'The Three MCP Primitives')
    table(doc, ['Primitive', 'What it is', 'Example'], [
        ['Tools', 'Actions Claude can take (functions it calls)', 'create_github_issue(title)'],
        ['Resources', 'Read-only data the server provides', 'file://path/to/file'],
        ['Prompts', 'Pre-built instruction templates', '/summarise-pr'],
    ], widths=[1.2, 2.6, 2.4])
    body(doc, 'Most servers expose Tools only; Resources and Prompts are optional extras. Transport is '
              'JSON-RPC 2.0 over stdio or HTTP+SSE (which supports remote servers).')

    h2(doc, 'The Config Key & Where Servers Are Registered')
    code(doc, [
        '"mcpServers": {',
        '  "github": {',
        '    "command": "npx",',
        '    "args": ["-y", "@modelcontextprotocol/server-github"],',
        '    "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here" }',
        '  },',
        '  "filesystem": {',
        '    "command": "npx",',
        '    "args": ["-y", "@modelcontextprotocol/server-filesystem",',
        '             "/Users/you/projects"]',
        '  }',
        '}',
    ])
    table(doc, ['Where', 'Path'], [
        ['Claude Desktop (Mac)', '~/Library/Application Support/Claude/claude_desktop_config.json'],
        ['Claude Desktop (Windows)', '%APPDATA%\\Claude\\claude_desktop_config.json'],
        ['Claude Code (per project)', '.claude/settings.json → "mcpServers" key'],
        ['Claude Code (global)', '~/.claude.json → "mcpServers" key'],
    ], widths=[1.9, 4.3])
    body(doc, 'Find servers at modelcontextprotocol.io/servers (official), github.com/modelcontextprotocol/'
              'servers, and mcp.so (community marketplace). Most ship as npm or PyPI packages.')

    # ── Chapter 13 ───────────────────────────────────────────────────────────────
    chapter(doc, 13, 'Installing & Using MCP Servers')
    body(doc, 'This chapter installs three essential servers. All run via npx (bundled with Node.js), so make '
              'sure Node is installed (Chapter 3). The config file must be valid JSON — one missing comma '
              'breaks it. Validate at jsonlint.com if unsure, and restart Claude Desktop completely after '
              'every change.')

    h2(doc, 'Server 1 — Filesystem (no API key)')
    body(doc, 'Gives Claude read/write access to folders you list — and nothing else. It can read files '
              'without you pasting them, write and edit files, and list/search directories.')
    code(doc, [
        '"filesystem": {',
        '  "command": "npx",',
        '  "args": ["-y", "@modelcontextprotocol/server-filesystem",',
        '           "/Users/yourname/Projects"]',
        '}',
    ])
    h3(doc, 'Prompts that work after install')
    code(doc, [
        '"Read my README.md and summarise the project"',
        '"List all .py files in the src folder"',
        '"Create a new file called notes.md with my meeting notes"',
    ])

    h2(doc, 'Server 2 — GitHub (Personal Access Token)')
    steps(doc, [
        'On github.com: Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic).',
        'Name it "Claude MCP", set expiry (90 days), and check scopes: repo, read:org, read:user.',
        'Generate, then copy the token (starts with ghp_) immediately — you cannot view it again.',
    ])
    code(doc, [
        '"github": {',
        '  "command": "npx",',
        '  "args": ["-y", "@modelcontextprotocol/server-github"],',
        '  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here" }',
        '}',
    ])
    h3(doc, 'What you can do after install')
    code(doc, [
        '"List the open issues in my repo myname/myproject"',
        '"Create a new issue titled: Add dark mode support"',
        '"Summarise the last 5 commits to the main branch"',
        '"Search for the function parseUser across my codebase"',
    ])
    callout(doc, 'warn', 'Keep your token secret.',
            ['Never share it, paste it into a prompt, or commit it to git. If exposed, revoke it immediately '
             'at github.com/settings/tokens and generate a new one.'])

    h2(doc, 'Server 3 — Brave Search (free web search)')
    body(doc, 'Real-time web search inside Claude. Free tier: 2,000 queries/month, no credit card. Get a key '
              'at search.brave.com/api (looks like BSA...).')

    h2(doc, 'Complete 3-Server Config (copy-paste ready)')
    code(doc, [
        '{',
        '  "mcpServers": {',
        '    "filesystem": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-filesystem",',
        '               "/Users/yourname/Projects"]',
        '    },',
        '    "github": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-github"],',
        '      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }',
        '    },',
        '    "brave-search": {',
        '      "command": "npx",',
        '      "args": ["-y", "@modelcontextprotocol/server-brave-search"],',
        '      "env": { "BRAVE_API_KEY": "BSA..." }',
        '    }',
        '  }',
        '}',
    ])
    callout(doc, 'note', 'Restart after editing.',
            ['Quit Claude Desktop fully (from the menu bar) and reopen it. The new servers appear under the '
             'plugin icon. For Claude Code, add the "mcpServers" key to .claude/settings.json instead.'])

    # ── Chapter 14 ───────────────────────────────────────────────────────────────
    chapter(doc, 14, 'Claude Plugins')
    body(doc, 'In the claude.ai context, "plugins" are built-in capabilities you toggle on in a conversation — '
              'web search, code execution, Artifacts, and Connectors. Unlike MCP servers (which you install), '
              'plugins are one-click with no setup. Enable them via the puzzle-piece icon in the input '
              'toolbar; they are per-conversation and reset when you start a new chat.')

    h2(doc, 'Plugins vs MCP Servers')
    table(doc, ['Aspect', 'Plugins (claude.ai)', 'MCP Servers'], [
        ['What they are', 'Built-in toggles in claude.ai', 'Programs you install and configure'],
        ['Setup', 'One click in the conversation UI', 'Edit JSON config file, restart'],
        ['Who uses them', 'Everyone — no technical setup', 'Developers and power users'],
        ['Examples', 'Web Search, Code Exec, Artifacts', 'GitHub, Filesystem, Brave Search'],
    ], widths=[1.4, 2.4, 2.4])

    h2(doc, 'The Four Plugins')
    table(doc, ['Plugin', 'What it does', 'Plan'], [
        ['Web Search', 'Real-time web queries with inline source citations.', 'All plans'],
        ['Code Execution', 'Runs Python (NumPy/pandas/matplotlib) in the chat to crunch data and make charts.', 'Pro+'],
        ['Artifacts', 'Persistent HTML/charts/docs in a side panel; up to 20MB; shareable URL; can call APIs/MCP.', 'All (richer on paid)'],
        ['Connectors', 'Managed MCP integrations — no config files.', 'Pro+ (limited on Free)'],
    ], widths=[1.3, 3.6, 1.3])
    callout(doc, 'tip', 'Analyse a CSV in 30 seconds.',
            ['Turn on Code Execution, drag a CSV into the chat, and ask: "Summarise this data and plot a bar '
             'chart of the top 10 rows." Claude processes the file and shows the chart inline.'])

    h2(doc, 'Connectors')
    body(doc, 'Connectors are MCP-powered, managed integrations enabled from the claude.ai Connectors panel. '
              'Available connectors include Gmail, Google Drive, Slack, GitHub, Notion, Stripe, and Zapier '
              '(which reaches 7,000+ other apps). Browse the full list at claude.com/plugins.')

    # ── Chapter 15 ───────────────────────────────────────────────────────────────
    chapter(doc, 15, 'Claude Skills — Create Your Own')
    callout(doc, 'key', '', ['A Claude Code skill is a reusable instruction pack that Claude loads '
            'automatically when a task matches its description. Instead of re-typing the same detailed prompt '
            'every session, you write it once in a SKILL.md file and Claude picks it up when relevant.'])
    body(doc, 'Skills vs CLAUDE.md: CLAUDE.md is project-level context that is always loaded. A skill is '
              'task-level behaviour that loads only when relevant — a "code-review" skill loads when Claude '
              'reviews code, not when it writes docs.')

    h2(doc, 'Where Skills Live')
    table(doc, ['Path', 'Scope'], [
        ['~/.claude/skills/skill-name/', 'Global — available in ALL your projects.'],
        ['.claude/skills/skill-name/', 'Project-local — only in this repo.'],
        ['SKILL.md inside the folder', 'The only required file; everything else is optional.'],
    ], widths=[2.4, 3.8])

    h2(doc, 'The SKILL.md Format')
    body(doc, 'YAML frontmatter between --- markers, then the instructions:')
    code(doc, [
        '---',
        'name: code-review',
        'description: >',
        '  Use this skill when reviewing code, assessing a pull request,',
        '  or evaluating code quality. Covers style, logic, and security.',
        'allowed-tools: Read Grep Glob',
        '---',
        '# Code Review Instructions',
        '## What to Check',
        '- Logic correctness: does the code do what the comment says?',
        '- Security: no hardcoded secrets, no SQL injection risks',
        '- Style: follows project conventions (see CLAUDE.md)',
        '- Test coverage: is there a test for the new behaviour?',
        '## Output Format',
        'List issues by severity: CRITICAL -> WARNING -> SUGGESTION',
        'End with a one-line verdict: APPROVE / REQUEST CHANGES',
    ])
    table(doc, ['Field', 'Meaning'], [
        ['name', 'Required. Kebab-case identifier, used in /skill commands.'],
        ['description', 'Critical — this is the trigger. Claude reads it to decide whether to load the skill.'],
        ['allowed-tools', 'Optional whitelist (Read, Grep, Bash...). All tools if omitted.'],
        ['disable-model-invocation', 'Optional. true = run without the model (pure shell scripts).'],
    ], widths=[1.9, 4.3])
    callout(doc, 'tip', 'The description is the trigger — be specific.',
            ['Include the trigger scenarios ("when reviewing", "when writing SQL"), the output it produces, '
             'and keywords Claude will meet in prompts. Vague descriptions never fire or fire on the wrong '
             'tasks.'])

    h2(doc, 'Create Your First Skill in 4 Steps')
    code(doc, [
        '# 1. Create the skill directory',
        'mkdir -p ~/.claude/skills/my-skill',
        '# 2. Create ~/.claude/skills/my-skill/SKILL.md and paste a template',
        '# 3. Type /skills in Claude Code to confirm it loaded (no restart needed)',
        '# 4. Test: type a matching prompt, or invoke directly: /skill my-skill',
    ])
    body(doc, 'Fastest path: type "create a new skill" in Claude Code to use Anthropic\'s Skill Creator, an '
              'interactive Q&A that generates a complete skill. Find official skills at github.com/anthropics/'
              'skills and 330+ community skills at github.com/alirezarezvani/claude-skills.')
    callout(doc, 'warn', 'Keep the body short.',
            ['A skill loads every turn while active, so tokens add up. Move long detail into reference files '
             'and link them from SKILL.md.'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PART V
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'V', 'Automation & the API')
    body(doc, 'So far Claude has run interactively. To build your own apps and run tasks unattended, you use '
              'the API directly or Claude Code Routines. This part covers both.')

    # ── Chapter 16 ───────────────────────────────────────────────────────────────
    chapter(doc, 16, 'Claude API Basics')
    body(doc, 'The API is pay-as-you-go and billed separately from any claude.ai subscription. Get a key at '
              'console.anthropic.com (the developer dashboard), add a payment method (minimum $5 top-up), '
              'and create a key — it starts with sk-ant- and cannot be viewed again after the page closes.')
    callout(doc, 'warn', 'Never put your key in code.',
            ['Treat it like a password. Store it as the ANTHROPIC_API_KEY environment variable. If it leaks '
             '(e.g. committed to a public repo), revoke it in the Console immediately and generate a new one.'])
    code(doc, [
        '# Mac/Linux',
        'export ANTHROPIC_API_KEY="sk-ant-your-key-here"',
        '# Windows PowerShell',
        '$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"',
    ])

    h2(doc, 'Your First Call')
    h3(doc, 'Option A — curl (no code)')
    code(doc, [
        'curl https://api.anthropic.com/v1/messages \\',
        '  --header "x-api-key: $ANTHROPIC_API_KEY" \\',
        '  --header "anthropic-version: 2023-06-01" \\',
        '  --header "content-type: application/json" \\',
        '  --data \'{',
        '    "model": "claude-haiku-4-5-20251001",',
        '    "max_tokens": 1024,',
        '    "messages": [{"role": "user", "content": "Hello, Claude!"}]',
        '  }\'',
    ])
    h3(doc, 'Option B — Python SDK')
    code(doc, [
        '# pip install anthropic',
        'import anthropic',
        '',
        'client = anthropic.Anthropic()   # uses ANTHROPIC_API_KEY automatically',
        'message = client.messages.create(',
        '    model="claude-haiku-4-5-20251001",',
        '    max_tokens=1024,',
        '    messages=[{"role": "user", "content": "Hello, Claude!"}],',
        ')',
        'print(message.content[0].text)',
    ])
    h3(doc, 'Key request parameters')
    table(doc, ['Parameter', 'Meaning'], [
        ['model', 'Which Claude model to use (see IDs below).'],
        ['max_tokens', 'Maximum tokens in the response (a cap, not a target).'],
        ['messages', 'Array of {role, content} turns (user, assistant, user...).'],
        ['system', 'Optional instructions that apply to the whole conversation.'],
        ['temperature', '0.0 (focused/deterministic) to 1.0 (creative/varied).'],
    ], widths=[1.5, 4.7])

    h2(doc, 'Models & Pricing (per 1M tokens)')
    table(doc, ['Model', 'Model ID', 'Input', 'Output'], [
        ['Haiku 4.5', 'claude-haiku-4-5-20251001', '$1.00', '$5.00'],
        ['Sonnet 4.6', 'claude-sonnet-4-6', '$3.00', '$15.00'],
        ['Opus 4.8', 'claude-opus-4-8', '$5.00', '$25.00'],
    ], widths=[1.1, 2.4, 0.9, 0.9])
    body(doc, 'A token is roughly 4 characters of English, or 0.75 words. You pay for both input (your prompt '
              '+ system + history) and output (Claude\'s reply). Cost-savers: prompt caching (90% off input '
              'on cache hits), the Message Batches API (50% off, async), and using Haiku for high-volume work.')

    h2(doc, 'Error Codes & Retries')
    table(doc, ['Code', 'Meaning & fix'], [
        ['401 Unauthorized', 'Invalid or missing API key — check ANTHROPIC_API_KEY.'],
        ['429 Too Many Requests', 'Rate limit hit — add exponential backoff.'],
        ['529 Overloaded', 'API overloaded — retry with backoff; try Haiku as fallback.'],
        ['400 Bad Request', 'Invalid request — check JSON structure and model ID.'],
    ], widths=[1.7, 4.5])
    code(doc, [
        '# Simple retry with exponential backoff (Python)',
        'import time, anthropic',
        'client = anthropic.Anthropic()',
        'for attempt in range(3):',
        '    try:',
        '        msg = client.messages.create(...)',
        '        break',
        '    except anthropic.RateLimitError:',
        '        time.sleep(2 ** attempt)   # 1s, 2s, 4s',
    ])

    # ── Chapter 17 ───────────────────────────────────────────────────────────────
    chapter(doc, 17, 'Building Automations with Claude')
    body(doc, 'Claude Code Routines (launched April 2026, research preview) move automated tasks to the '
              'cloud. Write a prompt, connect a repository, set a trigger, and the task runs on Anthropic\'s '
              'infrastructure — even when your laptop is closed. A routine = saved config + prompt + '
              'repos/connectors + trigger.')

    h2(doc, 'Three Trigger Types')
    table(doc, ['Trigger', 'Fires on', 'Use for'], [
        ['Scheduled', 'Hourly / Daily / Weekday / Weekly (your timezone)', 'Daily digest, weekly report, nightly cleanup, standup.'],
        ['API', 'A POST to the routine\'s HTTP endpoint', 'Monitoring alerts, form submissions, event-driven tasks.'],
        ['GitHub', 'push, pull_request, issues, workflow_run', 'Auto-label issues, review PRs, respond to failing CI.'],
    ], widths=[1.1, 2.6, 2.5])

    h2(doc, 'Example: A Scheduled Daily Digest')
    steps(doc, [
        'In Claude Code, type /routines → New Routine.',
        'Write the prompt like a clear brief: "Read the GitHub issues opened in the last 24 hours. Summarise the top 5 by activity. Post a Slack message to #daily-digest."',
        'Connect the GitHub repo and any Connectors (e.g. Slack MCP to post output).',
        'Set the trigger: Scheduled → Daily → 08:00 AM.',
        'Save; a session log appears in the Routines panel after the first run.',
    ])

    h2(doc, 'Example: Fire a Routine via API')
    code(doc, [
        'curl -X POST \\',
        '  https://api.anthropic.com/v1/claude_code/routines/trig_01ABC.../fire \\',
        '  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \\',
        '  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \\',
        '  -H "anthropic-version: 2023-06-01" \\',
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"text": "Sentry alert SEN-4521 fired in production."}\'',
    ])

    h2(doc, 'Example: A Traditional API Pipeline (Python)')
    code(doc, [
        'import anthropic',
        'client = anthropic.Anthropic()',
        '',
        'def run_daily_digest():',
        '    data = fetch_todays_github_issues()      # your function',
        '    response = client.messages.create(',
        '        model="claude-haiku-4-5-20251001",   # fast + cheap for daily runs',
        '        max_tokens=512,',
        '        system="You are a concise technical summariser.",',
        '        messages=[{"role": "user",',
        '            "content": f"Summarise these issues in 5 bullets:\\n{data}"}],',
        '    )',
        '    post_to_slack(response.content[0].text)   # your function',
        '',
        'run_daily_digest()',
    ])

    h2(doc, 'Scheduling Options')
    table(doc, ['Option', 'How'], [
        ['Claude Code Routines', 'Easiest — configure in UI, runs on Anthropic cloud, no server.'],
        ['cron (Mac/Linux)', 'crontab: 0 8 * * * python /path/digest.py'],
        ['Task Scheduler (Win)', 'Schedule a task in the Task Scheduler app.'],
        ['GitHub Actions', 'on: schedule: - cron: "0 8 * * *"'],
        ['Zapier / Make', 'No-code: trigger a webhook or HTTP call to the API.'],
    ], widths=[1.9, 4.3])
    callout(doc, 'warn', 'Always cap automated runs.',
            ['Set max_tokens (a runaway response without a cap can cost far more than expected) and '
             'max_budget_usd for Routines to prevent cost spikes from unexpected input data.'])

    # ═══════════════════════════════════════════════════════════════════════════
    # PART VI
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'VI', 'Getting Better Results & Scaling Up')
    body(doc, 'The final part is about quality and scale: writing prompts that get dramatically better '
              'answers, coordinating many agents at once, proving your agents actually work, and keeping the '
              'bill under control.')

    # ── Chapter 18 ───────────────────────────────────────────────────────────────
    chapter(doc, 18, 'Prompting Masterclass')
    h2(doc, 'The 5 Parts of an Effective Prompt')
    table(doc, ['Part', 'What it does', 'Example'], [
        ['Role', 'Tell Claude what expert it is playing.', '"You are a senior Python engineer..."'],
        ['Task', 'Describe the specific job clearly.', '"Review the function below for bugs."'],
        ['Context', 'Provide the raw material.', '"Here is the function: <code>...</code>"'],
        ['Constraints', 'Limit scope, format, length, tone.', '"Reply only with a bullet list. Max 5 items."'],
        ['Output Format', 'Describe exactly how the result should look.', '"Format: TYPE | SEVERITY | LINE | DESC"'],
    ], widths=[1.1, 2.4, 2.7])

    h2(doc, 'Why XML Tags Work')
    body(doc, 'XML tags are the most reliable way to structure prompts for Claude — they create clear '
              'boundaries between instruction, context, and examples, removing ambiguity about what is data '
              'and what is instruction. Use them instead of Markdown headings.')
    code(doc, [
        '<instructions>',
        'Classify the customer email below as: REFUND / TECH_SUPPORT / COMPLAINT / OTHER.',
        'Reply with one word only.',
        '</instructions>',
        '<example>',
        'Email: "My payment failed but I was charged twice."',
        'Classification: REFUND',
        '</example>',
        '<context>',
        'Email: "The app crashes every time I open settings."',
        '</context>',
    ])

    h2(doc, 'Chain-of-Thought')
    body(doc, 'Asking Claude to reason step by step before answering gives a +19-point accuracy boost on hard '
              'reasoning tasks (MMLU-Pro). Separate the reasoning from the result with tags:')
    code(doc, [
        'Think through this problem step by step in <thinking> tags,',
        'then give your final answer in <answer> tags.',
    ])
    callout(doc, 'note', 'Skip CoT for reasoning models.',
            ['Extended-thinking models already reason internally, so explicit <thinking> tags do not improve '
             'them.'])

    h2(doc, 'The 7 Essential Techniques')
    table(doc, ['Technique', 'How / when'], [
        ['Few-shot', '3–5 <example> tags. Best for output format and classification. Diverse beats similar.'],
        ['Role assignment', '"You are a [expert]..." Useful for creative/analytical work; low impact on factual QA.'],
        ['Chain-of-thought', '<thinking> + <answer> tags for hard reasoning.'],
        ['XML structure', '<context>, <instructions>, <example> to remove ambiguity.'],
        ['Output schema', 'Show the exact JSON/table/bullet structure you want.'],
        ['Negative constraints', '"Do not use jargon." Explicit negatives beat hoping Claude infers them.'],
        ['Iterative refinement', '"Now make it shorter / more formal." Refine conversationally.'],
    ], widths=[1.6, 4.6])

    h2(doc, 'System Prompt "Contract" (API)')
    code(doc, [
        'You are a [ROLE] helping [USER TYPE] with [DOMAIN].',
        'SUCCESS CRITERIA:',
        '- [What "done well" looks like]',
        'CONSTRAINTS:',
        '- [What to avoid / scope limits]',
        'OUTPUT FORMAT:',
        '[Exact structure of your response]',
        'UNCERTAINTY:',
        'If unclear, ask ONE clarifying question before proceeding.',
    ])

    h2(doc, 'Weak vs Strong — A Concrete Contrast')
    table(doc, ['Weak', 'Strong'], [
        ['"Write about climate change."',
         '"Write a 250-word op-ed for a business audience arguing carbon pricing is the most efficient climate policy. Tone: analytical, not alarmist. End with a call to action for CFOs."'],
        ['"Fix my code."',
         '"The function below returns wrong results for negative inputs. Identify the bug and provide a corrected version with an explanation. <code>...</code>"'],
    ], widths=[2.0, 4.2])
    body(doc, 'Rules of thumb: optimal prompt length is 150–300 words; use 3–5 diverse few-shot examples; '
              'structure with XML tags, not Markdown; temperature 0 for structured/precise tasks (API only).')

    # ── Chapter 19 ───────────────────────────────────────────────────────────────
    chapter(doc, 19, 'Multi-Agent Orchestration')
    callout(doc, 'key', '', ['A single agent works step by step in one context window. Orchestration splits a '
            'big job across many agents that run at the same time or in stages, then combines their results. '
            'It trades tokens for speed, breadth, and confidence. Builds on Chapters 10 and 11.'])

    h2(doc, 'The Three Orchestration Tools')
    table(doc, ['Tool', 'What it is'], [
        ['Subagents', 'Isolated Claude instances with their own context, tools, and model. Best for delegating a self-contained subtask.'],
        ['Agent Teams', 'One session is the "lead" coordinating teammates via a shared task list. Best for long projects.'],
        ['Workflows', 'Deterministic scripts that fan out agents by code. Dynamic Workflows (June 2026) let the lead plan and launch tens of agents.'],
    ], widths=[1.4, 4.8])

    h2(doc, 'The Building Blocks')
    table(doc, ['Primitive', 'Behaviour', 'Reach for it when...'], [
        ['Delegate', 'One agent, one job', 'Keep a noisy subtask out of main context.'],
        ['Parallel', 'Barrier — awaits all results', 'You need every result together (dedup, early-exit on count).'],
        ['Pipeline', 'No barrier — streams', 'Multi-stage work with no cross-item dependency (the default).'],
    ], widths=[1.2, 2.3, 2.7])
    body(doc, 'Pipeline is the default: each item flows through all stages independently, so item A can be in '
              'stage 3 while item B is still in stage 1. Wall-clock equals the slowest single chain, not the '
              'sum of the slowest step per stage.')

    h2(doc, 'Coordination Patterns That Raise Quality')
    bullets(doc, [
        ('Adversarial verify:', 'spawn N skeptics per finding, each prompted to refute it; kill it unless it survives a majority.'),
        ('Judge panel:', 'generate N attempts from different angles, score with parallel judges, synthesize from the winner.'),
        ('Loop-until-dry:', 'keep spawning finders until K rounds surface nothing new — beats a fixed count.'),
        ('Multi-modal sweep:', 'parallel agents each search a different way (by file, by content, by entity).'),
        ('Completeness critic:', 'a final agent asks "what is missing?" — its findings become the next round.'),
        ('Perspective-diverse verify:', 'give each verifier a distinct lens (correctness, security, reproducibility).'),
    ])
    callout(doc, 'tip', 'Scale the pattern to the ask.',
            ['"Find any bugs" needs a few finders and a single verify vote. "Thoroughly audit this" earns a '
             'larger finder pool, a 3–5 vote adversarial pass, and a synthesis stage.'])

    h2(doc, 'Define a Reusable Custom Subagent')
    body(doc, 'Drop a Markdown file in .claude/agents/ with YAML frontmatter:')
    code(doc, [
        '# .claude/agents/reviewer.md',
        '---',
        'name: reviewer',
        'description: Reviews a diff for correctness bugs. Use after edits.',
        'tools: Read, Grep, Glob        # omit to inherit all tools',
        'model: sonnet                  # or opus / haiku / inherit',
        '---',
        'You are a meticulous code reviewer. Report only confirmed bugs,',
        'most severe first. Your final message IS the result.',
    ])
    callout(doc, 'warn', 'Isolate parallel file edits.',
            ['Agents that write to the same files at once will clobber each other. Give each its own git '
             'worktree (isolation: worktree). It costs setup time and disk, so use it only for parallel '
             'mutation.'])

    # ── Chapter 20 ───────────────────────────────────────────────────────────────
    chapter(doc, 20, 'Evaluating & Testing Claude Agents')
    callout(doc, 'key', '', ['"It looks right" is how most agents ship — and how they silently break. An '
            'evaluation ("eval") is a repeatable test that scores your agent on real tasks with known good '
            'answers. Evals turn a gut feeling into a number you can track and defend when you change a '
            'prompt or model.'])

    h2(doc, 'The Evaluation Loop')
    table(doc, ['Step', 'What you do'], [
        ['Collect', 'Gather real tasks + known good answers (your "gold set").'],
        ['Run', "Send each task through the agent; capture output and tool calls."],
        ['Grade', 'Score each output — exact match, a code check, or an LLM judge.'],
        ['Compare', 'Track the score. Did this change help, hurt, or do nothing?'],
    ], widths=[1.3, 4.9])
    callout(doc, 'tip', '20 cases beat zero.',
            ['You do not need thousands of test cases. 20–50 well-chosen tasks covering your common paths and '
             'known failure modes catch most regressions. Add a new case every time you find a bug.'])

    h2(doc, 'Three Grading Methods')
    table(doc, ['Method', 'Nature', 'Best for'], [
        ['Exact match', 'Fast, free, zero bias', 'Classification, extraction, fixed answers.'],
        ['Code check', 'Assertions in code', 'Valid JSON, schema, "contains X", ranges.'],
        ['LLM judge', 'Scores by rubric', 'Writing, summaries, reasoning, open-ended.'],
        ['Human review', 'Slow, gold standard', 'Validating the judge; final sign-off.'],
    ], widths=[1.3, 1.8, 3.1])

    h2(doc, 'A Judge Prompt That Works')
    code(doc, [
        'You are grading an AI summary against a rubric. Score 1-5.',
        'RUBRIC:',
        '- 5: Covers all key findings, no invented facts, within length.',
        '- 3: Misses one finding OR slightly too long.',
        '- 1: Missing findings OR contains facts not in the source.',
        'Reason step by step in <thinking>, then output only:',
        'SCORE: <n>  |  REASON: <one line>',
    ])
    h3(doc, 'Judge biases to design around')
    table(doc, ['Bias', 'Counter'], [
        ['Position (favours the first answer)', 'Randomise/swap order, average.'],
        ['Verbosity (rates longer higher)', 'Score against the rubric, not length.'],
        ['Self-preference (prefers its own style)', 'Use a strong, neutral judge model.'],
        ['Rubric drift (standards wander)', 'Fixed rubric; grade one axis at a time.'],
    ], widths=[2.7, 3.5])
    callout(doc, 'warn', 'Validate the judge before you trust it.',
            ['Hand-grade a small gold set, then have the judge grade the same set. If they do not agree ~90% '
             'of the time, fix the rubric first — an unvalidated judge just launders your bias.'])

    h2(doc, 'Wire Evals into CI (Promptfoo)')
    code(doc, [
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
    ])
    body(doc, 'Set a pass threshold (e.g. task completion >= 0.85, tool accuracy >= 0.90) and fail the build '
              'below it. Run a small smoke set per PR and the full set nightly. Every bug a user hits becomes '
              'a new test case, so it can never come back.')

    # ── Chapter 21 ───────────────────────────────────────────────────────────────
    chapter(doc, 21, 'Cost & Token Management')
    body(doc, 'The API charges by the token (~4 characters, or 0.75 words). Every request pays for input '
              '(everything you send: prompt, context, history, tool results) plus output (what Claude writes). '
              'Output is the pricier half, and long conversations re-send the whole history every turn.')

    h2(doc, '2026 Price Table (per 1M tokens)')
    table(doc, ['Model', 'Input', 'Output', 'Cache hit', 'Best for'], [
        ['Haiku 4.5', '$1.00', '$5.00', '$0.10', 'Routing & bulk'],
        ['Sonnet 4.6', '$3.00', '$15.00', '$0.30', 'Balanced default'],
        ['Opus 4.8', '$5.00', '$25.00', '$0.50', 'Hardest reasoning'],
    ], widths=[1.1, 0.8, 0.9, 0.9, 1.8])
    body(doc, 'Cache hit = repeated cached input (90% off). Batch API = 50% off all of the above. The four '
              'things that drive your bill: model choice, output length, context size, and call volume.')

    h2(doc, 'The Big Cost Levers')
    table(doc, ['Lever', 'How much', 'How'], [
        ['Prompt caching', 'Up to 90% off input', 'Reuse a large fixed prefix (system prompt, docs) across calls.'],
        ['Batch API', '50% off all tokens', 'Submit async requests processed within ~24h (evals, bulk tagging).'],
        ['Model routing', 'Up to 5x cheaper', 'Triage with Haiku; escalate only hard cases to Sonnet/Opus.'],
        ['Cap output', 'Direct savings', 'Set max_tokens to what you need; ask Claude to be concise.'],
        ['/compact', '60–80% context cut', 'Summarise the conversation so far in long agent runs.'],
    ], widths=[1.3, 1.5, 3.4])

    h2(doc, 'Turn On Prompt Caching (Python SDK)')
    code(doc, [
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
    ])
    callout(doc, 'tip', 'Order your prompt for cache hits.',
            ['Put the stable, reusable content FIRST (system prompt, documents, examples) and the changing '
             'content LAST (the user question). Caching only helps the unchanged prefix.'])

    h2(doc, 'Cap Runs & Estimate First')
    code(doc, [
        '# Claude Code - stop after 15 turns',
        'claude -p "refactor the auth module" --max-turns 15',
        '',
        '# API - count tokens BEFORE you send (free)',
        'client.messages.count_tokens(',
        '    model="claude-sonnet-4-6",',
        '    messages=[{"role": "user", "content": big_prompt}],',
        ')   # returns input_tokens so you can estimate cost first',
    ])
    callout(doc, 'warn', 'Unbounded loops are the #1 surprise bill.',
            ['An agent running 30 turns on Opus over a growing 50K context can cost dollars per run. Cap loops '
             'with --max-turns AND a spend limit, compact early, and multiply per-call cost by volume before '
             'you launch a batch job: a $0.10 call run 10,000 times is $1,000.'])
    body(doc, 'Monitor live: /cost shows session spend, /status shows context usage. Set monthly spend caps '
              'and email alerts in the Console under Usage & Limits, and use separate API keys per project to '
              'see where the money goes.')

    # ═══════════════════════════════════════════════════════════════════════════
    # APPENDICES
    # ═══════════════════════════════════════════════════════════════════════════
    part_heading(doc, 'A', 'Appendices')

    chapter(doc, 'A', 'Master Command Cheat Sheet')
    h2(doc, 'Setup (terminal)')
    table(doc, ['Command', 'Purpose'], [
        ['npm install -g @anthropic-ai/claude-code', 'Install Claude Code.'],
        ['claude --version', 'Verify the install.'],
        ['claude', 'Launch Claude Code in the current folder.'],
        ['claude -p "task" --max-turns 15', 'Run one prompt headless, capped at 15 turns.'],
        ['node -v  /  npm -v', 'Check Node / npm versions.'],
        ['git init / add / commit / push', 'Core version-control workflow.'],
        ['pip install anthropic', 'Install the Python SDK.'],
        ['docker compose up', 'Start a multi-container stack.'],
    ], widths=[3.0, 3.2])

    h2(doc, 'Claude Code Slash Commands')
    table(doc, ['Command', 'Purpose'], [
        ['/help', 'List all commands.'],
        ['/clear  ·  /compact', 'Clear history · summarise to shrink context.'],
        ['/status  ·  /cost', 'Token usage & auth · session spend.'],
        ['/doctor', 'Diagnostics if Claude Code stalls.'],
        ['/terminal-setup', 'Enable multi-line prompts (Shift+Enter).'],
        ['/plugins  ·  /skills  ·  /routines', 'Manage MCP servers · skills · cloud routines.'],
    ], widths=[2.6, 3.6])

    h2(doc, 'Key Config Files & Locations')
    table(doc, ['File', 'What it holds'], [
        ['./CLAUDE.md', 'Project memory (stack, commands, conventions).'],
        ['.claude/settings.json', 'Shared hooks + "mcpServers" key (committed).'],
        ['.claude/settings.local.json', 'Personal hooks (gitignored).'],
        ['.claude/agents/*.md', 'Custom subagent definitions.'],
        ['~/.claude/skills/<name>/SKILL.md', 'A reusable skill.'],
        ['claude_desktop_config.json', 'Claude Desktop MCP config (Mac: ~/Library/Application Support/Claude/; Win: %APPDATA%\\Claude\\).'],
        ['ANTHROPIC_API_KEY', 'Environment variable for API/auth.'],
    ], widths=[2.5, 3.7])

    chapter(doc, 'B', 'Troubleshooting Quick Reference')
    table(doc, ['Problem', 'Fix'], [
        ['"node: command not found"', 'Restart the terminal; reinstall Node.js if still missing.'],
        ['npm -g "EACCES" permission error', 'Do not use sudo; set npm prefix to ~/.npm-global.'],
        ['Claude Code extension not visible', 'Ensure VS Code is 1.98+ (Help → About).'],
        ['"Not authenticated" error', 'Click the Claude panel icon and sign in again.'],
        ['CLI not found after install', 'Close and reopen your terminal so PATH updates.'],
        ['Trust dialog keeps appearing', 'Approve trust once per folder, not per session.'],
        ['Diff not showing changes', 'Open a folder, not just a single file.'],
        ['Claude ignores CLAUDE.md', 'Filename must be exactly CLAUDE.md in the project root.'],
        ['Hook not running', 'Check settings.json is valid JSON; use full command paths.'],
        ['MCP server not appearing', 'Restart Claude Desktop fully; validate JSON at jsonlint.com.'],
        ['GitHub MCP auth error', 'Confirm the PAT includes the repo scope; regenerate if needed.'],
        ['Skill never triggers', 'Make the description more specific; add trigger keywords.'],
        ['API 401 Unauthorized', 'Check ANTHROPIC_API_KEY is set correctly.'],
        ['Loop keeps going', 'Add an explicit stop instruction; set --max-turns.'],
        ['Bill higher than expected', 'Check output length + call volume; cap both; use /compact.'],
    ], widths=[2.5, 3.7])

    # closing
    close = doc.add_paragraph()
    _spacing(close, 20, 0)
    _border(close, color='C25B1E', size='18', side='top')
    r = close.add_run('You now have the full path — from installing Node.js to orchestrating fleets of agents. '
                      'Open a folder in VS Code, click the Claude icon, and start building.')
    r.italic = True; r.font.size = Pt(10.5); r.font.color.rgb = MUTED; r.font.name = 'Calibri'

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    doc.save(OUT)
    # rough page count is not available without a renderer; report paragraph/table counts
    print(f'Saved: {OUT}')
    print(f'Paragraphs: {len(doc.paragraphs)}  Tables: {len(doc.tables)}')


if __name__ == '__main__':
    build()
