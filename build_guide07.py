#!/usr/bin/env python3
"""Guide 07: Git & GitHub for Claude Users — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_07_Git.pdf'
GUIDE = 'Git & GitHub for Claude Users'

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
    c.setFillColor(GRN); c.setFont('Courier', 10)
    ty = y - pad - 10
    for line in lines:
        col = MGR if line.startswith('#') else GRN
        c.setFillColor(col); c.drawString(x + pad, ty, line); ty -= lh
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
    bw, bh2 = c.stringWidth('GUIDE 07 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 07 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Git & GitHub')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Version Control for Claude Users — Starting from Zero')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'Plain-English glossary: repo, branch, commit, PR, fork — all explained',
        'Install Git 2.49 on Mac, Windows, and Linux',
        'Configure your name and email so commits are attributed correctly',
        'Create a GitHub account and your first repository',
        'The 7 git commands you will use 90% of the time',
        'Push your first project to GitHub step by step',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'No prior terminal experience needed  •  Free tools  •  Mac, Windows & Linux')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Glossary & Why It Matters ────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is Git? — Plain-English Glossary')
    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Git is a version control system — it tracks every change you make to your '
             'files and lets you go back in time if something breaks. GitHub is a website '
             'that stores your Git projects online so they are backed up and shareable. '
             'Claude Code uses Git automatically to track AI-generated changes.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Key Terms Explained')
    y -= 14

    terms = [
        ('Repository (repo)', 'A folder that Git watches. Every file change inside it is tracked.'),
        ('Commit',            'A saved snapshot of your project at a specific moment in time.'),
        ('Branch',            'A separate version of your project where you try out changes safely.'),
        ('Main / master',     'The primary branch — the official, stable version of your project.'),
        ('Push',              'Upload your local commits to GitHub (the remote copy).'),
        ('Pull',              'Download the latest commits from GitHub to your computer.'),
        ('Clone',             'Download a GitHub repo to your computer for the first time.'),
        ('Pull Request (PR)', 'A request to merge changes from one branch into another.'),
        ('Fork',              'Your personal copy of someone else\'s GitHub repository.'),
        ('Merge',             'Combine changes from one branch into another.'),
    ]
    cw2 = (CW - 10) / 2
    row_y = y - 4; card_h = 38
    for i, (term, defn) in enumerate(terms):
        col = i % 2
        if col == 0 and i > 0:
            row_y -= card_h + 5
        cx = MX + col * (cw2 + 10)
        c.setFillColor(PNL); c.roundRect(cx, row_y - card_h, cw2, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(cx + 10, row_y - 14, term)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(defn, 9, cw2 - 20)
        dy = row_y - 27
        for dl_line in dl[:1]:
            c.drawString(cx + 10, dy, dl_line)

    y = row_y - card_h - 14
    info_panel(c, MX, y, 'The Big Picture in One Sentence', [
        'Git saves your work history locally.  GitHub stores it in the cloud.',
        'Claude Code commits changes automatically — Git lets you review every one.',
    ], CW)
    c.showPage()


# ── Page 3: Install Git & Configure ──────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing Git & First-Time Setup')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Git 2.49 is the latest version. Install for your platform:')
    y -= 60

    # Install section
    cw2 = (CW - 10) / 2
    installs = [
        ('Mac', [
            'brew install git',
            '# or download from git-scm.com',
        ]),
        ('Windows', [
            '# Download Git for Windows from git-scm.com',
            '# Run the installer with default settings',
        ]),
        ('Linux (Ubuntu/Debian)', [
            'sudo apt update && sudo apt install git',
        ]),
    ]
    for i, (platform, cmds) in enumerate(installs):
        col = i % 2 if i < 2 else 0
        cx = MX + col * (cw2 + 10) if i < 2 else MX
        w = cw2 if i < 2 else CW
        if i == 2:
            y -= 90
        c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10)
        c.drawString(cx, y, platform)
        bh = len(cmds) * 14 + 20; panel_y = y - 14
        c.setFillColor(CODE_BG); c.roundRect(cx, panel_y - bh, w, bh, radius=4, fill=1, stroke=0)
        c.setStrokeColor(OG); c.setLineWidth(0.5)
        c.roundRect(cx, panel_y - bh, w, bh, radius=4, fill=0, stroke=1)
        ty = panel_y - 10
        for cmd in cmds:
            col2 = MGR if cmd.startswith('#') else GRN
            c.setFillColor(col2); c.setFont('Courier', 9)
            c.drawString(cx + 8, ty, cmd); ty -= 14
    y -= 8

    # Verify
    c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX, y, 'Verify: open a new terminal and run:')
    y -= 14
    y = code_block(c, MX, y, ['git --version    # expected: git version 2.49.x (or similar)'], CW)
    y -= 14

    # First-time config
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'First-Time Configuration (Do This Once)')
    y -= 16
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Tell Git who you are — this attaches your name to every commit:')
    y -= 14
    y = code_block(c, MX, y, [
        'git config --global user.name "Your Name"',
        'git config --global user.email "you@example.com"',
        '',
        '# Set VS Code as your default editor (optional but recommended):',
        'git config --global core.editor "code --wait"',
    ], CW)
    y -= 14

    y = step_card(c, MX, y, 1, 'Create a GitHub Account', [
        'Go to github.com and click "Sign up".',
        'Choose a username — this will be your public developer identity.',
        'Verify your email when GitHub sends a confirmation.',
    ], CW)
    y -= 8

    y = step_card(c, MX, y, 2, 'Authenticate Git with GitHub', [
        'Install the GitHub CLI: winget install GitHub.cli (Windows) or brew install gh (Mac).',
        'Then run: gh auth login and follow the prompts.',
        'This lets git push work without typing passwords.',
    ], CW)
    y -= 8

    tip_lines = wrap(
        'GitHub CLI (gh) is separate from git. It is optional but makes authentication, '
        'creating repos, and opening PRs much faster from the terminal.',
        10, CW - 28)
    tip_box(c, MX, y, 'Install GitHub CLI for a Better Experience', tip_lines, CW)
    c.showPage()


# ── Page 4: Core Git Commands ─────────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'The 7 Git Commands You Need Daily')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Learn these 7 commands and you can handle 90% of version control tasks:')
    y -= 60

    commands = [
        ('git init',
         'Turn a regular folder into a Git repository.',
         ['cd my-project', 'git init']),
        ('git status',
         'See which files have changed since your last commit.',
         ['git status']),
        ('git add',
         'Stage files to include in your next commit.',
         ['git add filename.py       # one file', 'git add .                  # all changes']),
        ('git commit',
         'Save a snapshot with a descriptive message.',
         ['git commit -m "Add user login feature"']),
        ('git push',
         'Upload your commits to GitHub.',
         ['git push origin main']),
        ('git pull',
         'Download the latest changes from GitHub.',
         ['git pull']),
        ('git clone',
         'Download a repo from GitHub to your computer.',
         ['git clone https://github.com/username/repo.git']),
    ]

    for num, (cmd, desc, code) in enumerate(commands):
        pad, badge = 8, 22
        code_h = len(code) * 14 + 16
        card_h = 52 + code_h
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + pad, y - pad - badge, badge, badge, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(MX + pad + badge / 2, y - pad - badge + 6, str(num + 1))
        c.setFillColor(GRN); c.setFont('Courier-Bold', 12)
        c.drawString(MX + pad + badge + 8, y - 14, cmd)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + pad + badge + 8, y - 28, desc)
        # Code snippet
        cy = y - 42
        c.setFillColor(CODE_BG); c.roundRect(MX + pad + badge + 8, cy - code_h, CW - pad * 2 - badge - 16, code_h, radius=3, fill=1, stroke=0)
        c.setFillColor(GRN); c.setFont('Courier', 9)
        ty2 = cy - 8
        for line in code:
            col2 = MGR if line.startswith('#') else GRN
            c.setFillColor(col2); c.drawString(MX + pad + badge + 16, ty2, line); ty2 -= 14
        y -= card_h + 5
    c.showPage()


# ── Page 5: First Project Walkthrough ────────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Walkthrough — Push Your First Project to GitHub')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Follow these steps from start to finish:')

    steps = [
        ('Create a folder and initialise Git', [
            'mkdir my-first-project && cd my-first-project',
            'git init',
        ]),
        ('Create a file', [
            'Create a file (e.g. README.md) with any text editor.',
            'This is the file we will track and push to GitHub.',
        ]),
        ('Stage and commit the file', [
            'git add .',
            'git commit -m "Initial commit"',
        ]),
        ('Create a GitHub repo', [
            'Go to github.com → click "+" → "New repository".',
            'Name it my-first-project. Leave it empty (no README).',
            'Copy the HTTPS URL shown on the next page.',
        ]),
        ('Connect your local repo to GitHub', [
            'git remote add origin https://github.com/YOU/my-first-project.git',
            'git branch -M main',
            'git push -u origin main',
        ]),
    ]

    y -= 60
    for i, (title, lines) in enumerate(steps):
        # Separate code lines from text lines
        text_lines = [l for l in lines if not (l.startswith('git ') or l.startswith('mkdir') or l.startswith('cd '))]
        code_lines = [l for l in lines if l.startswith('git ') or l.startswith('mkdir') or l.startswith('cd ')]
        all_lines = text_lines + ([] if not code_lines else [])
        y = step_card(c, MX, y, i + 1, title, text_lines if text_lines else ['See command below:'], CW)
        if code_lines:
            y -= 4
            y = code_block(c, MX, y, code_lines, CW)
        y -= 6

    tip_lines = wrap(
        'After your first push, refresh github.com/YOU/my-first-project — '
        'you will see your file live on the internet. Share the URL with anyone.',
        10, CW - 28)
    tip_box(c, MX, y - 4, 'Your Code Is Now Live on GitHub', tip_lines, CW)
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Git & GitHub')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Check status',          'git status'),
        ('Stage all changes',     'git add .'),
        ('Commit with message',   'git commit -m "message"'),
        ('Push to GitHub',        'git push'),
        ('Pull from GitHub',      'git pull'),
        ('View commit history',   'git log --oneline'),
        ('Create a new branch',   'git checkout -b new-branch'),
        ('Switch branches',       'git checkout main'),
    ]
    url_items = [
        ('Git download',        'git-scm.com'),
        ('Git version (2026)',  'Git 2.49'),
        ('GitHub sign up',      'github.com'),
        ('GitHub CLI',          'cli.github.com'),
        ('GitHub CLI install',  'winget install GitHub.cli  (Windows)'),
        ('GitHub CLI install',  'brew install gh  (Mac)'),
        ('GitHub Docs',         'docs.github.com'),
        ('Git cheat sheet',     'education.github.com/git-cheat-sheet'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Commands', left_items),
        (MX + cw2 + 10, 'Links & Versions', url_items),
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
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Common Issues & Quick Fixes')
    y -= 8
    t_rows = [
        ['git: command not found',     'Restart terminal after install; or reinstall Git'],
        ['"fatal: not a git repository"', 'Run git init first, or cd into your project folder'],
        ['"rejected" on git push',     'Run git pull first to get latest changes, then push again'],
        ['Wrong email on commits',     'git config --global user.email "right@email.com"'],
        ['Forgot to stage a file',     'git add filename, then git commit --amend (if last commit)'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [190, CW - 190])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 08 — Docker Basics for AI Projects')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 07 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
