#!/usr/bin/env python3
"""Guide 08: Docker Basics for AI Projects — Claude AI Field Guide Series"""
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = LETTER
MX = 0.65 * inch
CW = W - 2 * MX
OUT = r'C:\Projects\UserGuide\outputs\Claude_Field_Guide_08_Docker.pdf'
GUIDE = 'Docker Basics for AI Projects'

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
        col = MGR if line.startswith('#') else GRN
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
    bw, bh2 = c.stringWidth('GUIDE 08 OF 23', 'Helvetica-Bold', 10) + 24, 22
    c.setFillColor(DDOG); c.roundRect(MX, H - 70, bw, bh2, radius=4, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(MX + bw / 2, H - 61, 'GUIDE 08 OF 23')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 34)
    c.drawString(MX, H - 175, 'Docker Basics')
    c.setFillColor(OGL); c.setFont('Helvetica', 14)
    c.drawString(MX, H - 200, 'Containers for AI Projects — From Zero to Running')
    c.setStrokeColor(OG); c.setLineWidth(1.5)
    c.line(MX, H - 216, W - MX, H - 216)
    box_top = H - 230; box_h = 190
    c.setFillColor(PNL); c.roundRect(MX, box_top - box_h, CW, box_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, box_top - box_h, 4, box_h, fill=1, stroke=0)
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
    c.drawString(MX + 14, box_top - 18, "WHAT'S INSIDE")
    bullets = [
        'What containers are — the lunchbox analogy that makes it click',
        'Containers vs virtual machines: a plain-English comparison',
        'Install Docker Desktop free (Mac, Windows, Linux)',
        'Run hello-world to verify your install in under 2 minutes',
        'Essential Docker commands: run, pull, build, ps, stop, compose',
        'Write your first docker-compose.yml for an AI project',
    ]
    by = box_top - 40
    for b in bullets:
        c.setFillColor(GRN); c.setFont('Helvetica-Bold', 11); c.drawString(MX + 14, by, '✓')
        c.setFillColor(LGR); c.setFont('Helvetica', 10); c.drawString(MX + 30, by, b)
        by -= 27
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX, H - 442, 'Free for personal use  •  Mac, Windows & Linux  •  No prior experience needed')
    c.setFillColor(OG); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(W / 2, 12, 'etsy.com/shop/FranksMarketDesigns  •  23-Guide Field Guide Series')
    c.showPage()


# ── Page 2: Why This Matters ──────────────────────────────────────────────────

def page2(c):
    pg_bg(c); hdr(c); ftr(c, 2)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'What Is Docker and Why Should You Care?')

    c.setFillColor(LGR); c.setFont('Helvetica', 11)
    intro = ('Docker packages your application and everything it needs — code, libraries, '
             'settings — into a single portable unit called a container. That container '
             'runs identically on your laptop, your colleague\'s machine, and any cloud '
             'server. "Works on my machine" stops being an excuse.')
    iy = y - 44
    for line in wrap(intro, 11, CW):
        c.drawString(MX, iy, line); iy -= 17
    y = iy - 10

    info_panel(c, MX, y, 'The Lunchbox Analogy', [
        'A container is like a lunchbox for your app.',
        'The lunchbox holds everything the app needs: food (code), utensils (dependencies),',
        'and a napkin (config). No matter whose desk you open it on, lunch is the same.',
        'Docker is the factory that makes and manages the lunchboxes.',
    ], CW)
    y -= 96

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, 'Containers vs Virtual Machines')
    y -= 8
    t_rows = [
        ['Start time',     'Seconds',                    'Minutes'],
        ['Size',           'Megabytes',                  'Gigabytes'],
        ['Share OS kernel','Yes (lightweight)',           'No (each has its own)'],
        ['Portability',    'Run anywhere Docker runs',    'Platform-specific formats'],
        ['Use case',       'Dev tools, APIs, AI services','Full OS isolation needed'],
    ]
    y = tbl(c, MX, y, ['Factor', 'Container (Docker)', 'Virtual Machine'], t_rows, [110, 180, CW - 290])
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12); c.drawString(MX, y, "What You'll Learn")
    y -= 22
    learns = [
        ('Install Docker Desktop',   'Free for personal, education & small business use'),
        ('Run containers',           'Pull images and launch them with one command'),
        ('Build images',             'Package your own code into a container'),
        ('Use Docker Compose',       'Run multi-container setups with one file'),
        ('AI project patterns',      'Common Docker setups for Claude API projects'),
    ]
    for title, desc in learns:
        c.setFillColor(OG); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 10, y, f'▸  {title}')
        c.setFillColor(LGR); c.setFont('Helvetica', 10)
        c.drawString(MX + 168, y, f'— {desc}')
        y -= 18
    y -= 12
    info_panel(c, MX, y, 'Licensing — Is Docker Desktop Free?', [
        'Free for: personal use, students, education, open source, small businesses',
        '  (small = fewer than 250 employees AND under $10 million revenue)',
        'Paid plans from $9/month: required for larger commercial organisations.',
        'CLI tools (docker engine, compose) are always free and open source.',
    ], CW)
    c.showPage()


# ── Page 3: Install Docker Desktop ───────────────────────────────────────────

def page3(c):
    pg_bg(c); hdr(c); ftr(c, 3)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Installing Docker Desktop')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'Docker Desktop gives you Docker Engine, Compose, and a GUI in one install:')

    steps = [
        ('Download Docker Desktop', [
            'Go to docker.com/products/docker-desktop and click Download.',
            'Choose your platform: Mac (Apple Silicon or Intel), Windows, or Linux.',
            'The download is roughly 500 MB.',
        ]),
        ('Install on Mac', [
            'Open the downloaded .dmg file.',
            'Drag Docker to the Applications folder.',
            'Open Docker from Applications — it runs as a menu bar app.',
        ]),
        ('Install on Windows', [
            'Run Docker Desktop Installer.exe.',
            'Ensure WSL 2 backend is selected (recommended, the default).',
            'Click OK and wait for the install to complete, then restart.',
        ]),
        ('Install on Linux', [
            'Docker Desktop for Linux: download the .deb or .rpm from docker.com.',
            'Or install Docker Engine directly: docs.docker.com/engine/install.',
            'Engine is free and open source on all Linux distros.',
        ]),
        ('Verify the Install', [
            'Open a terminal (or PowerShell on Windows).',
            'Run: docker run hello-world',
            'You should see "Hello from Docker!" — install is complete.',
        ]),
    ]
    y -= 62
    for i, (title, lines) in enumerate(steps):
        y = step_card(c, MX, y, i + 1, title, lines, CW)
        y -= 6

    y = code_block(c, MX, y, [
        '# Verify Docker is working',
        'docker run hello-world',
        '',
        '# Check versions',
        'docker --version',
        'docker compose version',
    ], CW)
    y -= 8

    warn_lines = wrap(
        'On Windows, if WSL 2 is not installed, Docker will prompt you to install it. '
        'Follow the link it provides — this is a one-time setup that takes about 5 minutes.',
        10, CW - 28)
    warn_box(c, MX, y, 'Windows: WSL 2 Required', warn_lines, CW)
    c.showPage()


# ── Page 4: Core Docker Commands ─────────────────────────────────────────────

def page4(c):
    pg_bg(c); hdr(c); ftr(c, 4)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Essential Docker Commands')
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y - 40, 'These commands cover 90% of day-to-day Docker usage:')
    y -= 58

    commands = [
        ('docker pull <image>',   'Download an image from Docker Hub.',
         ['docker pull python:3.12', 'docker pull node:22-alpine']),
        ('docker run <image>',    'Create and start a container from an image.',
         ['docker run -it python:3.12 bash   # interactive shell',
          'docker run -d -p 8080:80 nginx    # background, port mapped']),
        ('docker ps',             'List running containers.',
         ['docker ps              # running only', 'docker ps -a            # all containers']),
        ('docker stop <id>',      'Stop a running container.',
         ['docker stop abc123     # use container ID from docker ps']),
        ('docker build',          'Build an image from a Dockerfile.',
         ['docker build -t my-app:latest .']),
        ('docker logs <id>',      'View output from a running container.',
         ['docker logs abc123', 'docker logs -f abc123  # follow live output']),
    ]

    for num, (cmd, desc, code) in enumerate(commands):
        code_h = len(code) * 14 + 16
        card_h = 52 + code_h
        pad, badge = 8, 22
        c.setFillColor(PNL); c.roundRect(MX, y - card_h, CW, card_h, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + pad, y - pad - badge, badge, badge, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(MX + pad + badge / 2, y - pad - badge + 6, str(num + 1))
        c.setFillColor(GRN); c.setFont('Courier-Bold', 11)
        c.drawString(MX + pad + badge + 8, y - 14, cmd)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        c.drawString(MX + pad + badge + 8, y - 27, desc)
        cy = y - 42; cw = CW - pad * 2 - badge - 16
        c.setFillColor(CODE_BG); c.roundRect(MX + pad + badge + 8, cy - code_h, cw, code_h, radius=3, fill=1, stroke=0)
        ty2 = cy - 8
        for line in code:
            col2 = MGR if line.startswith('#') else GRN
            c.setFillColor(col2); c.setFont('Courier', 9)
            c.drawString(MX + pad + badge + 16, ty2, line); ty2 -= 14
        y -= card_h + 5
    c.showPage()


# ── Page 5: Docker Compose & AI Patterns ─────────────────────────────────────

def page5(c):
    pg_bg(c); hdr(c); ftr(c, 5)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Docker Compose & AI Project Patterns')
    y -= 40

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'What Is Docker Compose?')
    y -= 18
    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    compose_intro = ('Docker Compose lets you define and run multi-container applications '
                     'with a single YAML file (docker-compose.yml). One command starts '
                     'everything: your app, database, and any supporting services.')
    for line in wrap(compose_intro, 10, CW):
        c.drawString(MX, y, line); y -= 15
    y -= 8

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 11)
    c.drawString(MX, y, 'Example: Simple Python + API Server (docker-compose.yml)')
    y -= 12
    y = code_block(c, MX, y, [
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
    ], CW)
    y -= 10

    c.setFillColor(LGR); c.setFont('Helvetica', 10)
    c.drawString(MX, y, 'Start everything with one command:')
    y -= 14
    y = code_block(c, MX, y, ['docker compose up'], CW)
    y -= 14

    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 12)
    c.drawString(MX, y, 'Common AI Project Patterns')
    y -= 14

    patterns = [
        ('Isolated Python environment',
         'Run your Claude API scripts in Python 3.12 with all dependencies, '
         'without touching your system Python.'),
        ('Node.js API wrapper',
         'Containerise a Node.js server that calls the Anthropic SDK, '
         'share it with teammates without setup steps.'),
        ('Vector database + app',
         'Compose file with your app + a vector DB (e.g. Qdrant) '
         'that Claude uses for RAG — start both with one command.'),
        ('Reproducible demos',
         'Ship a docker-compose.yml with your AI project so anyone '
         'can run it with docker compose up — zero local setup.'),
    ]
    for i, (title, desc) in enumerate(patterns):
        c.setFillColor(PNL); c.roundRect(MX, y - 50, CW, 50, radius=4, fill=1, stroke=0)
        c.setFillColor(OG); c.roundRect(MX + 8, y - 36, 20, 20, radius=3, fill=1, stroke=0)
        c.setFillColor(WHT); c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(MX + 18, y - 29, str(i + 1))
        c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 10)
        c.drawString(MX + 34, y - 16, title)
        c.setFillColor(LGR); c.setFont('Helvetica', 9)
        dl = wrap(desc, 9, CW - 44)
        dy = y - 30
        for dl_line in dl[:2]:
            c.drawString(MX + 34, dy, dl_line); dy -= 13
        y -= 58
    c.showPage()


# ── Page 6: Quick Reference ───────────────────────────────────────────────────

def page6(c):
    pg_bg(c); hdr(c); ftr(c, 6)
    y = H - 30
    c.setFillColor(OG); c.setFont('Helvetica-Bold', 15)
    c.drawString(MX, y - 20, 'Quick Reference — Docker')
    y -= 40

    cw2 = (CW - 10) / 2
    left_items = [
        ('Verify install',          'docker run hello-world'),
        ('Pull an image',           'docker pull <image>:<tag>'),
        ('Run interactively',       'docker run -it <image> bash'),
        ('Run in background',       'docker run -d <image>'),
        ('List running containers', 'docker ps'),
        ('Stop a container',        'docker stop <id>'),
        ('Start Compose stack',     'docker compose up'),
        ('Stop Compose stack',      'docker compose down'),
    ]
    url_items = [
        ('Download page',      'docker.com/products/docker-desktop'),
        ('Docker Hub images',  'hub.docker.com'),
        ('Official docs',      'docs.docker.com'),
        ('Compose reference',  'docs.docker.com/compose'),
        ('Free for',           'Personal, education, open source, <250 emp'),
        ('Paid from',          '$9/month (Pro plan, annual billing)'),
        ('Engine (always free)','docs.docker.com/engine/install'),
        ('Play with Docker',   'labs.play-with-docker.com (online sandbox)'),
    ]

    for px, panel_title, items in [
        (MX, 'Essential Commands', left_items),
        (MX + cw2 + 10, 'Links & Pricing', url_items),
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
        ['Docker Desktop won\'t start',  'Ensure WSL 2 is enabled (Windows) or Rosetta installed (Mac M1)'],
        ['Permission denied on Linux',   'Add your user to the docker group: sudo usermod -aG docker $USER'],
        ['"Cannot connect to daemon"',   'Docker Desktop is not running — start it from Applications/Start menu'],
        ['Container exits immediately',  'Run docker logs <id> to see why — often a missing ENV variable'],
        ['Port already in use',          'Change the host port: -p 8081:80 instead of -p 8080:80'],
    ]
    y = tbl(c, MX, y, ['Problem', 'Fix'], t_rows, [168, CW - 168])
    y -= 14

    cta_h = 54
    c.setFillColor(PNL); c.roundRect(MX, y - cta_h, CW, cta_h, radius=6, fill=1, stroke=0)
    c.setFillColor(OG); c.rect(MX, y - cta_h, 4, cta_h, fill=1, stroke=0)
    c.setFillColor(OGL); c.setFont('Helvetica-Bold', 10); c.drawString(MX + 14, y - 17, 'Next in the Series:')
    c.setFillColor(CREAM); c.setFont('Helvetica-Bold', 13)
    c.drawString(MX + 14, y - 33, 'Guide 09 — VS Code Setup for Claude')
    c.setFillColor(MGR); c.setFont('Helvetica', 9)
    c.drawString(MX + 14, y - 49, 'More guides at etsy.com/shop/FranksMarketDesigns  •  23-guide series')
    c.showPage()


def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cv = canvas.Canvas(OUT, pagesize=LETTER)
    cv.setTitle(f'Claude AI Field Guide — {GUIDE}')
    cv.setAuthor('Claude AI Field Guide Series')
    cv.setSubject('Guide 08 of 20')
    cover(cv); page2(cv); page3(cv); page4(cv); page5(cv); page6(cv)
    cv.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
