#!/usr/bin/env python3
"""Build the Etsy listing kit: mockup images + listing copy.

Mockups composite REAL rendered pages from the product PDFs (via PyMuPDF) onto a
warm cream background, so the previews show what buyers actually get. Cream rather
than white so the tile has definition against Etsy's white search grid — the dark
PDF pages then carry the contrast.

Run:  python build_etsy_kit.py
Outputs to outputs/etsy/:
    <sku>/01_main.png  02_inside.png  03_included.png     (2000x2000)
    LISTINGS.md   — titles, 13 tags, descriptions, pricing for every SKU
"""
import os
import textwrap

import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r'C:\Projects\UserGuide'
OUT = os.path.join(ROOT, 'outputs')
ETSY = os.path.join(OUT, 'etsy')

S = 2000                      # Etsy square listing image
CREAM  = (247, 242, 234)
INK    = (26, 26, 36)
OGC    = (224, 122, 56)
DOGC   = (184, 92, 24)
MUTED  = (122, 116, 108)
WHITE  = (255, 255, 255)

FONTS = ['seguibl.ttf', 'arialbd.ttf', 'segoeuib.ttf']
FONT_R = ['segoeui.ttf', 'arial.ttf']


def font(size, bold=True):
    for name in (FONTS if bold else FONT_R):
        p = os.path.join(r'C:\Windows\Fonts', name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# =============================================================== SKU CATALOGUE

SKUS = [
    dict(
        sku='01-prompt-vault',
        pdf='Claude_Prompt_Vault.pdf',
        files=['Claude_Prompt_Vault.pdf', 'Claude_Prompt_Vault.md',
               'Claude_Prompt_Vault.txt'],
        headline='200 Claude AI\nPrompts',
        sub='Copy, paste, done.',
        badges=['200 PROMPTS', '29 PAGES', 'PDF + NOTION'],
        spines=['The Claude\nPrompt Vault'],
        price='$8.99',
        etsy_fit='HIGH — prompt packs are the proven seller in this category',
        title='200 Claude AI Prompts Copy and Paste Prompt Pack | ChatGPT Alternative AI Prompt Bundle | Digital Download PDF 2026',
        tags=['claude ai prompts', 'ai prompt pack', 'ai prompts bundle', 'chatgpt prompts',
              'prompt engineering', 'claude ai guide', 'ai for beginners', 'digital download',
              'ai productivity', 'work prompts', 'ai writing prompts', 'small business ai',
              'ai cheat sheet'],
        blurb='200 ready-to-use prompts across 10 everyday categories — writing, email, '
              'business, marketing, coding, data, learning, planning and more.',
        bullets=[
            '200 prompts in 10 categories — every one written to be pasted straight in',
            'Fill-in-the-blank format: everything you change is in [BRACKETS]',
            'Three files included — PDF book, Markdown for Notion, and plain text',
            'A one-page "how to prompt" primer so the prompts keep working when you edit them',
            'Covers writing, email, business, marketing, code, data, learning, planning, ideas',
            'Works with Claude, and with any other AI assistant you already use',
        ],
        included=['Claude_Prompt_Vault.pdf  (29 pages)',
                  'Claude_Prompt_Vault.md  (Notion / Obsidian ready)',
                  'Claude_Prompt_Vault.txt  (plain text)'],
    ),
    dict(
        sku='02-starter-volume',
        volume=1,
        pdf='Claude_Field_Guide_Volume_1_Getting_Started.pdf',
        headline='Claude AI for\nBeginners',
        sub='No tech background needed.',
        badges=['5 GUIDES', '32 PAGES', 'STEP BY STEP'],
        spines=['Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'],
        price='$9.99',
        etsy_fit='HIGH — beginner AI guides sell well to Etsy\'s non-technical audience',
        title='Claude AI for Beginners Complete Starter Guide | AI Tutorial PDF No Coding Required | 32 Page Digital Download 2026',
        tags=['claude ai guide', 'ai for beginners', 'ai tutorial pdf', 'claude ai',
              'ai guide pdf', 'artificial intel', 'digital download', 'ai tools guide',
              'claude tutorial', 'ai cheat sheet', 'tech guide pdf', 'ai productivity',
              'beginners guide'],
        blurb='Everything you need to start using Claude AI — on the web, your phone, your '
              'desktop, in Chrome, and inside Slack and Excel. Explained in plain English.',
        bullets=[
            'Five complete guides in one 32-page book, ordered easiest to hardest',
            'Set up your account and learn the interface without guesswork',
            'Plan comparison table — Free, Pro, Max, Team and Enterprise side by side',
            'Phone, desktop and Chrome extension walkthroughs with every step numbered',
            'Slack, Excel and PowerPoint integrations explained',
            'A printable one-page cheat sheet at the end of every guide',
        ],
        included=['Volume 1 — Getting Into Claude (32 pages)',
                  'Covers: Web, Mobile, Desktop, Chrome, Integrations',
                  '5 printable cheat sheets'],
    ),
    dict(
        sku='03-complete-library',
        pdf='Claude_Field_Guide_COMPLETE_LIBRARY.pdf',
        headline='The Complete\nClaude AI Library',
        sub='23 guides. 140 pages.',
        badges=['23 GUIDES', '140 PAGES', '6 VOLUMES'],
        cover_badge='BEST VALUE',
        spines=['Volumes\n1 – 2', 'The Complete\nLibrary', 'Volumes\n5 – 6'],
        price='$29.99',
        etsy_fit='MEDIUM — page count carries it, but the back half is developer content',
        title='Complete Claude AI Guide Library 140 Pages | 23 Guides Beginner to Advanced AI Bundle | Digital Download PDF 2026',
        tags=['claude ai guide', 'ai guide bundle', 'ai for beginners', 'claude ai',
              'ai tutorial pdf', 'digital download', 'ai tools guide', 'claude code',
              'ai automation', 'prompt engineering', 'tech guide pdf', 'ai cheat sheet',
              'ai learning'],
        blurb='All 23 guides in one 140-page library. Starts at "what is Claude" and ends '
              'at building your own automations. Six volumes, beginner to advanced.',
        bullets=[
            'All 23 field guides in one 140-page PDF with a linked contents page',
            'Volume 1 — using Claude on web, mobile, desktop, Chrome and in Slack/Excel',
            'Volume 2 — the developer setup: Node.js, Git, Docker, VS Code',
            'Volume 3 — Claude Code, CLAUDE.md files, hooks and agentic loops',
            'Volume 4 — MCP servers, plugins and building your own skills',
            'Volumes 5 & 6 — the API, automations, prompting, orchestration and cost control',
        ],
        included=['Complete Library (140 pages, 23 guides, 6 volumes)',
                  '23 printable cheat sheets',
                  'Contents page with every guide and its page number'],
    ),
    dict(
        sku='04-claude-code-volume',
        volume=3,
        pdf='Claude_Field_Guide_Volume_3_Claude_Code.pdf',
        headline='Claude Code\nMastery',
        sub='For developers.',
        badges=['4 GUIDES', '26 PAGES', 'DEVELOPER'],
        spines=['Claude Code\nin VS Code', 'Claude Code\n& Agents', 'Hooks &\nSubagents'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developers do not shop on Etsy',
        title='Claude Code Guide for Developers | CLAUDE.md Hooks and Agentic Workflows | 26 Page Technical PDF Digital Download',
        tags=['claude code', 'developer guide', 'ai coding tools', 'programming pdf',
              'ai automation', 'claude ai guide', 'coding tutorial', 'digital download',
              'ai agents', 'dev tools guide', 'vs code guide', 'tech guide pdf',
              'ai for coders'],
        blurb='The four Claude Code guides in one book: install and auth, CLAUDE.md build '
              'plans, subagents and hooks, and how the agentic loop actually works.',
        bullets=[
            'Install Claude Code and get through auth, trust dialogs and diff review',
            'Write CLAUDE.md build plans Claude actually follows',
            'Subagents and the full hook event list, with annotated settings.json',
            'How the agentic loop runs and every condition that stops it',
            'Slash command reference and context management with /compact',
            'Cost controls: /status, --max-turns and explicit stopping criteria',
        ],
        included=['Volume 3 — Claude Code Mastery (26 pages)',
                  'Covers: Claude Code, CLAUDE.md, Hooks, Agentic Loops',
                  '4 printable cheat sheets'],
    ),
    dict(
        sku='05-config-pack',
        pdf='Claude_Config_Pack_Guide.pdf',
        files=['Claude_Config_Pack.zip', 'Claude_Config_Pack_Guide.pdf'],
        headline='Claude Code\nConfig Pack',
        sub='32 real files. Not screenshots.',
        badges=['32 FILES', '6 HOOKS', 'COPY & PASTE'],
        cover_badge='FOR CLAUDE CODE',
        spines=['Claude Code\nConfig Pack'],
        price='$14.99',
        etsy_fit='LOW on Etsy, HIGHEST on Gumroad — this is the developer willingness-to-pay SKU',
        title='Claude Code Config Pack | CLAUDE.md Templates Hooks and MCP Configs | 32 Ready to Use Files Digital Download',
        tags=['claude code', 'developer tools', 'config templates', 'ai automation',
              'programming files', 'claude ai guide', 'dev productivity', 'digital download',
              'mcp server', 'coding templates', 'ai agents', 'vs code setup',
              'ai for coders'],
        blurb='32 working configuration files for Claude Code — CLAUDE.md templates, hook '
              'recipes, skills and MCP configs. Edit the brackets and go.',
        bullets=[
            '6 CLAUDE.md build-plan templates: Next.js, FastAPI, Node, data science, monorepo',
            '6 hook recipes for .claude/settings.json — Mac, Linux and Windows versions',
            'Guard scripts that block rm -rf, force pushes and destructive SQL',
            'SKILL.md template plus 3 complete working skills you can install today',
            'MCP server configs for both Claude Code and Claude Desktop',
            'Safe permission defaults that cut approval prompts without opening holes',
        ],
        included=['Claude_Config_Pack.zip  (32 files)',
                  'Claude_Config_Pack_Guide.pdf  (6-page install guide)',
                  'CLAUDE.md x6 · hooks x6 · skills x4 · MCP configs x3'],
    ),
    # ---- COPILOT SERIES ----------------------------------------------------
    # Unofficial. Product names deliberately do NOT lead with "GitHub Copilot",
    # and every description carries the not-affiliated line.
    dict(
        sku='20-copilot-v1',
        pdf='Copilot_Field_Guide_Volume_1_Getting_Started.pdf',
        headline='Getting Started\nwith Copilot',
        sub='Install it. Understand what it costs.',
        badges=['5 CHAPTERS', '24 PAGES', '5 EDITORS'],
        cover_badge='VOL 1',
        spines=['The Editors', 'Getting\nStarted', 'Credits\n& Plans'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Copilot Field Guide for Beginners | Install Setup and What It Actually Costs | 24 Page AI Coding PDF 2026',
        tags=['copilot guide', 'ai coding', 'developer guide', 'github copilot',
              'coding tutorial', 'ai for developers', 'programming pdf',
              'digital download', 'vs code guide', 'ai tools guide', 'tech guide pdf',
              'ai productivity', 'coding cheat sheet'],
        blurb='What Copilot actually is, what each part costs after the 2026 billing '
              'change, how to install it in any editor, and how to use completions well.',
        bullets=[
            'The three products wearing one name — and which of them is metered',
            'Plans, AI credits and the June 2026 usage-based billing change explained',
            'Install walkthroughs for VS Code, Visual Studio, JetBrains, Neovim and CLI',
            'Completions and Next Edit Suggestions — the part that is never billed',
            'A guided first hour, from install to your first accepted change',
            'Printable quick reference and a troubleshooting table',
        ],
        included=['Volume 1 — Getting Started (24 pages)',
                  'Unofficial. Not affiliated with GitHub or Microsoft.'],
    ),
    dict(
        sku='21-copilot-v2',
        pdf='Copilot_Field_Guide_Volume_2_Chat_and_Agents.pdf',
        headline='Copilot Chat\n& Agent Mode',
        sub='The metered half, used well.',
        badges=['5 CHAPTERS', '26 PAGES', '3 MODES'],
        cover_badge='VOL 2',
        spines=['Ask, Edit,\nAgent', 'Chat &\nAgent Mode', 'Slash\nCommands'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Copilot Chat and Agent Mode Guide | Slash Commands Context and Multi File Edits | 26 Page Developer PDF 2026',
        tags=['copilot guide', 'ai agents', 'ai coding', 'developer guide',
              'github copilot', 'ai automation', 'prompt engineering',
              'digital download', 'vs code guide', 'coding tutorial', 'ai for coders',
              'tech guide pdf', 'ai productivity'],
        blurb='Ask, edit and agent mode — what each is for, how to drive them with slash '
              'commands and context references, and how to review what they write.',
        bullets=[
            'The three chat modes, and why picking the wrong one wastes credits',
            'Slash commands, @ participants and # context references in full',
            'Agent mode: writing a task it can actually finish',
            'Tool approval and what auto-approval really means before you enable it',
            'Reviewing multi-file changes — and when to reject the whole set',
            'Prompting patterns that work, and the two-attempt rule',
        ],
        included=['Volume 2 — Chat & Agent Mode (26 pages)',
                  'Unofficial. Not affiliated with GitHub or Microsoft.'],
    ),
    dict(
        sku='22-copilot-v3',
        pdf='Copilot_Field_Guide_Volume_3_CLI_and_Coding_Agent.pdf',
        headline='Copilot CLI &\nCoding Agent',
        sub='In your terminal. And without you.',
        badges=['5 CHAPTERS', '26 PAGES', 'CLI + CLOUD'],
        cover_badge='VOL 3',
        spines=['The CLI', 'CLI & Coding\nAgent', 'Pull\nRequests'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Copilot CLI and Coding Agent Guide | Assign Issues Review Pull Requests Automate | 26 Page Developer PDF 2026',
        tags=['copilot guide', 'ai agents', 'developer guide', 'github copilot',
              'ai automation', 'command line', 'devops guide', 'digital download',
              'ai coding', 'pull request', 'coding tutorial', 'tech guide pdf',
              'ai for coders'],
        blurb='Copilot in the terminal, and the cloud agent that takes an issue, writes '
              'the code and opens the pull request while you do something else.',
        bullets=[
            'Installing and using the CLI — explain before you run, not after it breaks',
            'The cloud coding agent, and every documented hard limit it works within',
            'Five ways to hand it work, including assigning a GitHub issue',
            'The five issue headings that make a task it can actually finish',
            'Reviewing an agent pull request, and steering it mid-run',
            'Branch protection, CI approval and a sensible starting posture',
        ],
        included=['Volume 3 — CLI & the Coding Agent (26 pages)',
                  'Unofficial. Not affiliated with GitHub or Microsoft.'],
    ),
    dict(
        sku='23-copilot-v4',
        pdf='Copilot_Field_Guide_Volume_4_Customisation.pdf',
        headline='Copilot\nCustomisation',
        sub='Stop repeating your conventions.',
        badges=['5 CHAPTERS', '26 PAGES', '7 FILE TYPES'],
        cover_badge='VOL 4',
        spines=['Instruction\nFiles', 'Customisation', 'MCP &\nHooks'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Copilot Customisation Guide | Instruction Files Prompt Files Custom Agents MCP and Hooks | 26 Page PDF 2026',
        tags=['copilot guide', 'developer guide', 'ai coding', 'github copilot',
              'mcp server', 'ai automation', 'config templates', 'digital download',
              'coding templates', 'ai agents', 'dev productivity', 'tech guide pdf',
              'ai for coders'],
        blurb='Instruction files, prompt files, custom agents, skills, MCP servers and '
              'hooks — the seven ways to make Copilot follow your conventions by default.',
        bullets=[
            'The one file every repository should have, and how to write it well',
            'All seven customisation types with their exact naming conventions',
            'Prompt files: turn a prompt that worked into a slash command',
            'Custom agents with restricted tools — a real control, not a request',
            'MCP servers, and treating one as the permission grant it actually is',
            'Hooks: the difference between persuading a model and guaranteeing it',
        ],
        included=['Volume 4 — Customisation (26 pages)',
                  'Unofficial. Not affiliated with GitHub or Microsoft.'],
    ),
    dict(
        sku='24-copilot-v5',
        pdf='Copilot_Field_Guide_Volume_5_Credits_Cost_and_Teams.pdf',
        headline='Copilot Credits,\nCost & Teams',
        sub='What it costs at scale.',
        badges=['5 CHAPTERS', '26 PAGES', 'FOR TEAMS'],
        cover_badge='VOL 5',
        spines=['Credits\nExplained', 'Cost &\nTeams', 'Budgets\n& Pools'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer and admin content',
        title='Copilot Cost and Team Admin Guide | AI Credits Budgets Pooling and Rollout | 26 Page Developer PDF 2026',
        tags=['copilot guide', 'developer guide', 'ai budgeting', 'github copilot',
              'cost management', 'team management', 'ai for business',
              'digital download', 'ai coding', 'devops guide', 'tech guide pdf',
              'ai productivity', 'engineering lead'],
        blurb='What Copilot costs once a team is using it — how credits pool, where the '
              'money actually goes, and how to cap it before the first invoice.',
        bullets=[
            'How AI credits work, and why credits track model usage not button presses',
            'Pooling — why you watch the pool, not individual people',
            'The promotional credit rates that end on 1 September 2026',
            'Four levels of budget, and the overage default that surprises teams',
            'Reading your usage, and forecasting a rollout from real numbers',
            'Business vs Enterprise, policy management and the governance questions',
        ],
        included=['Volume 5 — Credits, Cost & Teams (26 pages)',
                  'Unofficial. Not affiliated with GitHub or Microsoft.'],
    ),
    # ---- CODEX SERIES ------------------------------------------------------
    # Unofficial. Names do not lead with "OpenAI Codex"; descriptions carry the
    # not-affiliated line.
    dict(
        sku='30-codex-v1',
        pdf='Codex_Field_Guide_Volume_1_Getting_Started.pdf',
        headline='Getting Started\nwith Codex',
        sub='An agent that finishes tasks.',
        badges=['5 CHAPTERS', '26 PAGES', '5 SURFACES'],
        cover_badge='VOL 1',
        spines=['Install\n& Setup', 'Getting\nStarted', 'Plans &\nLimits'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Codex Field Guide for Beginners | Install Plans Limits and Your First Task | 26 Page AI Coding PDF 2026',
        tags=['codex guide', 'ai coding', 'developer guide', 'openai codex',
              'ai agents', 'coding tutorial', 'programming pdf', 'digital download',
              'ai for developers', 'ai tools guide', 'tech guide pdf',
              'ai productivity', 'command line'],
        blurb='What Codex is, where it runs, what the plans actually buy, and how to get '
              'one real task done from install to reviewed change.',
        bullets=[
            'Why an agent is a different tool to an autocomplete, and what that changes',
            'All five surfaces — CLI, VS Code, web, iOS and Bedrock — and when to use each',
            'The 5-hour rolling usage window, and why it is not a monthly quota',
            'Plans from Go to Pro 20x, and where cloud delegation actually starts',
            'A guided first task, with the four parts that make one finishable',
            'Quick reference and a troubleshooting table',
        ],
        included=['Volume 1 — Getting Started (26 pages)',
                  'Unofficial. Not affiliated with OpenAI.'],
    ),
    dict(
        sku='31-codex-v2',
        pdf='Codex_Field_Guide_Volume_2_The_CLI.pdf',
        headline='The Codex CLI',
        sub='Permissions, commands, automation.',
        badges=['5 CHAPTERS', '26 PAGES', '9 COMMANDS'],
        cover_badge='VOL 2',
        spines=['Commands', 'The Codex\nCLI', 'Permissions\n& Sandbox'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Codex CLI Guide | Permissions Sandbox Commands and codex exec Automation | 26 Page Developer PDF 2026',
        tags=['codex guide', 'command line', 'developer guide', 'openai codex',
              'ai coding', 'ai automation', 'terminal guide', 'digital download',
              'devops guide', 'ai agents', 'coding tutorial', 'tech guide pdf',
              'ai for coders'],
        blurb='The terminal surface in depth — permission modes, the sandbox and writable '
              'roots, every command, and running Codex non-interactively in CI.',
        bullets=[
            'Installing and signing in, without piping a script blindly into a shell',
            'Permission modes and writable roots — the most consequential setting there is',
            'Where auto-approval is genuinely reasonable, and where it is not',
            'Every command: /init, /status, /permissions, /model, /review and the rest',
            'codex exec for scripts, pipelines and CI, with a safe automation pattern',
            'Session hygiene, reasoning effort, and keeping a long session coherent',
        ],
        included=['Volume 2 — The Codex CLI (26 pages)',
                  'Unofficial. Not affiliated with OpenAI.'],
    ),
    dict(
        sku='32-codex-v3',
        pdf='Codex_Field_Guide_Volume_3_AGENTS_Subagents_MCP.pdf',
        headline='AGENTS.md,\nSubagents & MCP',
        sub='Stop repeating your conventions.',
        badges=['5 CHAPTERS', '26 PAGES', '3 MECHANISMS'],
        cover_badge='VOL 3',
        spines=['AGENTS.md', 'Subagents\n& MCP', 'MCP\nServers'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Codex AGENTS.md Subagents and MCP Guide | Configuration Templates and Parallel Agents | 26 Page PDF 2026',
        tags=['codex guide', 'agents md', 'developer guide', 'openai codex',
              'mcp server', 'ai agents', 'config templates', 'digital download',
              'ai coding', 'coding templates', 'dev productivity', 'tech guide pdf',
              'ai for coders'],
        blurb='AGENTS.md, subagents and MCP servers — how to configure Codex so it follows '
              'your conventions, works in parallel, and can see your real data.',
        bullets=[
            'AGENTS.md: plain markdown, hierarchical, and the closest file wins',
            'What earns its place in the file — and why most improvements are deletions',
            'The one section worth writing the whole file for',
            'Subagents as TOML, why they are user-triggered, and how they inherit sandbox',
            'Scoping tools and sandboxes per role, so you can reason about capability',
            'MCP servers as a permission grant, and which are actually worth connecting',
        ],
        included=['Volume 3 — AGENTS.md, Subagents & MCP (26 pages)',
                  'Unofficial. Not affiliated with OpenAI.'],
    ),
    dict(
        sku='33-codex-v4',
        pdf='Codex_Field_Guide_Volume_4_Delegation_Review_Cost.pdf',
        headline='Codex Delegation,\nReview & Cost',
        sub='Hand it over. Check it. Pace it.',
        badges=['5 CHAPTERS', '26 PAGES', 'THE CAPSTONE'],
        cover_badge='VOL 4',
        spines=['Delegation', 'Review\n& Cost', 'Usage\nLimits'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — developer content',
        title='Codex Delegation Review and Cost Guide | Cloud Tasks Code Review and Usage Limits | 26 Page PDF 2026',
        tags=['codex guide', 'ai agents', 'developer guide', 'openai codex',
              'code review', 'ai automation', 'cost management', 'digital download',
              'ai coding', 'devops guide', 'engineering lead', 'tech guide pdf',
              'ai for coders'],
        blurb='Handing work to Codex and walking away, reviewing a diff you did not watch '
              'being written, and keeping the whole thing inside the usage window.',
        bullets=[
            'What to delegate and what to keep local — the contractor test',
            'The five brief headings that make a task finishable without you watching',
            'Automated code review, and why the loop still needs a person in it',
            'Reading a diff you did not watch: what to check and when to reject',
            'Where consumption actually goes, and the levers that matter in order',
            'Choosing a tier, and the unusual arithmetic of Pro 20x',
        ],
        included=['Volume 4 — Delegation, Review & Cost (26 pages)',
                  'Unofficial. Not affiliated with OpenAI.'],
    ),
    dict(
        # FREE lead magnet. Gumroad-only — Etsy has no free listing tier. Its whole job
        # is to send people to the shop, so the CTA carries the shop URL.
        sku='12-start-here',
        pdf='Claude_Field_Guide_00_Start_Here.pdf',
        headline='Start Here\nFree Roadmap',
        sub='Which guide do you actually need?',
        badges=['FREE', '2 PAGES', 'ROADMAP'],
        cover_badge='FREE',
        spines=['Start Here'],
        price='$0.00',
        etsy_fit='N/A — Gumroad only, Etsy has no free tier',
        title='FREE Claude AI Learning Roadmap | Which Guide Do You Need | 23 Guide Library Map Digital Download',
        tags=['claude ai', 'free download', 'ai roadmap', 'ai for beginners',
              'claude ai guide', 'learning path', 'ai guide pdf', 'digital download',
              'free ai guide', 'study guide', 'tech roadmap', 'ai learning',
              'claude tutorial'],
        blurb='A free two-page map of the whole Claude AI Field Guide library — four '
              'starting paths, all 23 guides by volume, and what each one covers.',
        bullets=[
            'Four colour-coded starting paths — pick the one that matches where you are',
            'Every one of the 23 guides listed by volume, with what it covers',
            'What each volume costs, so you can see the whole library at a glance',
            'Completely free — no email required, nothing held back',
            'Two pages. Read it in three minutes and know exactly where to start',
            'Updated for 2026',
        ],
        included=['Claude_Field_Guide_00_Start_Here.pdf  (2 pages)',
                  'Free — no strings'],
    ),
    dict(
        sku='10-cheat-sheet-pack',
        pdf='Claude_Cheat_Sheet_Pack.pdf',
        headline='Claude AI\nCheat Sheets',
        sub='12 pages. Print them. Pin them up.',
        badges=['12 SHEETS', 'PRINTABLE', 'LIGHT THEME'],
        cover_badge='PRINTABLE',
        spines=['Claude Code\nCommands', 'Cheat Sheet\nPack', 'MCP &\nHooks'],
        price='$6.99',
        etsy_fit='HIGHEST — printables are the strongest-selling digital category on Etsy',
        title='Claude AI Cheat Sheet Pack | 12 Printable Reference Sheets for Claude Code MCP and Prompting | Digital Download',
        tags=['claude ai', 'cheat sheet', 'printable pdf', 'ai reference',
              'claude code', 'developer printable', 'ai guide pdf', 'digital download',
              'coding cheat sheet', 'ai for beginners', 'desk reference', 'prompt engineering',
              'tech printable'],
        blurb='Twelve one-page references you can actually print. Light background, low '
              'ink, one topic per sheet — pin up the ones you use and stop re-reading docs.',
        bullets=[
            'Twelve one-page sheets — slash commands, hooks, MCP, prompting, pricing and more',
            'Designed for paper: light background and low ink coverage, not a dark screen theme',
            'Every sheet is self-contained — print only the ones you need',
            'Hook exit codes done right: 2 blocks, 1 does NOT (the mistake almost everyone makes)',
            'Current model IDs and per-million-token pricing on one page',
            'Git, Node, npm and Docker command references for the setup you had to do anyway',
        ],
        included=['Claude_Cheat_Sheet_Pack.pdf  (13 pages: cover + 12 sheets)',
                  'US Letter, prints without scaling',
                  'Light print-friendly theme'],
    ),
    dict(
        sku='11-cost-calculator',
        # `pdf` is the mockup source; `files` is what the buyer actually downloads.
        pdf='AI_Cost_Calculator_Preview.pdf',
        files=['AI_Cost_Calculator.xlsx'],
        headline='AI Cost\nCalculator',
        sub='Know the bill before it arrives.',
        badges=['SPREADSHEET', 'LIVE FORMULAS', 'EXCEL + SHEETS'],
        cover_badge='EXCEL + SHEETS',
        spines=['AI Cost\nCalculator'],
        price='$7.99',
        etsy_fit='MEDIUM-HIGH — spreadsheet tools sell steadily and this one has no free equivalent',
        title='AI API Cost Calculator Spreadsheet | Compare Claude Model Token Pricing Excel and Google Sheets | Digital Download',
        tags=['cost calculator', 'ai spreadsheet', 'excel template', 'claude ai',
              'google sheets', 'ai budgeting', 'token calculator', 'digital download',
              'api pricing', 'developer tools', 'small business ai', 'ai productivity',
              'budget template'],
        blurb='Type in your monthly usage and see what every Claude model would actually '
              'cost you — with cache and batch discounts applied. Live formulas, not a picture.',
        bullets=[
            'Enter your monthly tokens, get the real monthly cost for every current model',
            'Prompt-cache and Batch API discounts built in — both change the answer a lot',
            'Every figure is a live formula, so editing one rate updates the whole sheet',
            'Rates live on their own tab — when a vendor changes pricing you edit one cell',
            'Tells you the cheapest model for your workload and what you would save',
            'Works in Excel, Numbers and Google Sheets with no conversion',
        ],
        included=['AI_Cost_Calculator.xlsx  (Calculator, Rates, Read Me)',
                  'Opens in Excel, Numbers or Google Sheets',
                  'Rates verified July 2026 and fully editable'],
    ),
    dict(
        sku='06-volume-2-developer-setup',
        volume=2,
        pdf='Claude_Field_Guide_Volume_2_Developer_Setup.pdf',
        headline='The Developer\nSetup',
        sub='Node, Git, Docker, VS Code.',
        badges=['4 GUIDES', '26 PAGES', 'STEP BY STEP'],
        spines=['Node.js\n& npm', 'Developer\nSetup', 'Git &\nGitHub'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — install guides are developer content',
        title='Developer Setup Guide for AI Coding | Node.js Git Docker and VS Code Install Tutorial | 26 Page Beginner PDF Download',
        tags=['developer guide', 'coding for beginner', 'nodejs tutorial', 'git and github',
              'docker guide', 'vs code setup', 'programming pdf', 'digital download',
              'claude ai guide', 'learn to code', 'tech guide pdf', 'dev tools guide',
              'coding tutorial'],
        blurb='The four tools you install before you can build anything with AI — Node.js, '
              'Git, Docker and VS Code. Every step numbered, on Mac, Windows and Linux.',
        bullets=[
            'Four complete guides in one 26-page book, in the order you should install them',
            'Node.js on Mac, Windows and Linux — installer or nvm, and how to choose',
            'Git and GitHub explained for someone who has never opened a terminal',
            'Docker without the jargon, plus a working compose file for AI projects',
            'VS Code set up properly: five extensions, settings.json and the terminal',
            'Troubleshooting for the errors that actually stop people — PATH, versions, auth',
        ],
        included=['Volume 2 — Developer Setup (26 pages)',
                  'Covers: Node.js, Git & GitHub, Docker, VS Code',
                  '4 printable cheat sheets'],
    ),
    dict(
        sku='07-volume-4-automation-kit',
        volume=4,
        pdf='Claude_Field_Guide_Volume_4_Automation_Kit.pdf',
        headline='MCP Servers\n& Plugins',
        sub='Connect Claude to everything.',
        badges=['4 GUIDES', '26 PAGES', 'POWER USER'],
        spines=['MCP\nServers', 'Automation\nKit', 'Plugins\n& Skills'],
        price='$12.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — power-user tooling, not an Etsy search term',
        title='MCP Servers and Claude Plugins Guide | Build Your Own AI Skills and Connect Your Tools | 26 Page PDF Download',
        tags=['mcp server', 'claude ai guide', 'ai automation', 'claude code',
              'ai agents', 'developer guide', 'ai tools guide', 'digital download',
              'ai integrations', 'claude plugins', 'ai skills', 'tech guide pdf',
              'ai for coders'],
        blurb='How to give Claude access to your files, your repos and your apps — MCP '
              'servers, plugins, connectors, and skills you write yourself.',
        bullets=[
            'Four complete guides in one 26-page book, concept first then hands-on',
            'What MCP actually is, in plain English, with the architecture drawn out',
            'Install three real MCP servers step by step, with the full working config JSON',
            'Plugins vs MCP servers — the distinction nobody explains, plus a plan matrix',
            'Write your own Claude Skill: SKILL.md template and what makes one trigger',
            'Config file locations for Mac and Windows, and what to do after you edit them',
        ],
        included=['Volume 4 — Automation Kit (26 pages)',
                  'Covers: MCP 101, Installing MCP, Plugins, Skills',
                  '4 printable cheat sheets'],
    ),
    dict(
        sku='08-volume-5-api-automation',
        volume=5,
        pdf='Claude_Field_Guide_Volume_5_API_Automation.pdf',
        headline='The API &\nPrompting',
        sub='30 templates included.',
        badges=['3 GUIDES', '20 PAGES', '+30 TEMPLATES'],
        spines=['The Claude\nAPI', 'API &\nAutomation', 'Prompting\nMasterclass'],
        price='$9.99',
        etsy_fit='MEDIUM — the prompting masterclass carries this one on Etsy search',
        title='Claude AI API and Automation Guide | Prompt Engineering Masterclass with 30 Templates | 20 Page PDF Download',
        tags=['prompt engineering', 'claude api', 'ai automation', 'ai prompt pack',
              'developer guide', 'api tutorial', 'claude ai guide', 'digital download',
              'ai templates', 'python tutorial', 'ai for coders', 'tech guide pdf',
              'ai workflow'],
        blurb='Call Claude from your own code, schedule it to run without you, and write '
              'the prompts that make it worth doing. Ends with 30 copy-paste templates.',
        bullets=[
            'Three complete guides in one 20-page book, ending in the prompting masterclass',
            'Your first API call in curl and in Python, with the key stored safely',
            'Current model IDs and per-token pricing for every tier, side by side',
            'Error codes, rate limits and the retry pattern that handles them',
            'Scheduled and triggered automations, with a full working daily-digest example',
            '30 copy-paste prompt templates across writing, code, analysis and planning',
        ],
        included=['Volume 5 — API & Automation (20 pages)',
                  'Covers: API Basics, Automations, Prompting Masterclass',
                  '30 prompt templates · 3 printable cheat sheets'],
    ),
    dict(
        sku='09-volume-6-advanced',
        volume=6,
        pdf='Claude_Field_Guide_Volume_6_Advanced.pdf',
        headline='Advanced\nClaude AI',
        sub='Agents, evals, cost control.',
        badges=['3 GUIDES', '20 PAGES', 'ADVANCED'],
        spines=['Multi-Agent\nOrchestration', 'Advanced\nAdd-Ons', 'Cost &\nTokens'],
        price='$9.99',
        etsy_fit='LOW on Etsy, HIGH on Gumroad — this is the most technical volume in the series',
        title='Advanced Claude AI Guide | Multi Agent Orchestration Testing and Token Cost Control | 20 Page PDF Download',
        tags=['claude code', 'ai agents', 'multi agent ai', 'ai automation',
              'developer guide', 'ai testing', 'token management', 'claude ai guide',
              'digital download', 'ai orchestration', 'advanced ai guide', 'tech guide pdf',
              'ai for coders'],
        blurb='For people already running Claude every day — coordinating many agents at '
              'once, proving they actually work, and keeping the bill under control.',
        bullets=[
            'Three complete guides in one 20-page book, for people past the basics',
            'Run many agents at once: parallel, pipeline and delegate, and when each wins',
            'Five coordination patterns including adversarial verify and judge panels',
            'Build an eval loop so you can prove a change made your agent better, not worse',
            'LLM-as-judge prompts plus the four biases that quietly corrupt their scores',
            'Token billing explained, prompt caching at 90% off, and batch at 50% off',
        ],
        included=['Volume 6 — Advanced (20 pages)',
                  'Covers: Orchestration, Evaluation, Cost Management',
                  '3 printable cheat sheets'],
    ),
]


# ================================================================== IMAGE KIT

def wrap_text(draw, text, fnt, max_w):
    out = []
    for para in text.split('\n'):
        words, cur = para.split(), ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if draw.textlength(t, font=fnt) <= max_w or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def render_page(pdf_path, index, target_w):
    """Render one real PDF page to a PIL image of the given width."""
    doc = fitz.open(pdf_path)
    page = doc[min(index, doc.page_count - 1)]
    zoom = target_w / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    doc.close()
    return img


def paste_shadowed(base, img, xy, blur=26, offset=(0, 16), alpha=110):
    """Paste img with a soft drop shadow so it lifts off the cream background."""
    x, y = xy
    shadow = Image.new('RGBA', (img.width + blur * 4, img.height + blur * 4), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle(
        [blur * 2, blur * 2, blur * 2 + img.width, blur * 2 + img.height],
        fill=(40, 32, 24, alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    base.paste(shadow, (x - blur * 2 + offset[0], y - blur * 2 + offset[1]), shadow)
    base.paste(img, (x, y))


def badge_row(d, badges, cx, y, fnt):
    """Centred row of pill badges."""
    pad_x, gap, h = 34, 22, 76
    widths = [d.textlength(b, font=fnt) + pad_x * 2 for b in badges]
    total = sum(widths) + gap * (len(badges) - 1)
    x = cx - total / 2
    for b, w in zip(badges, widths):
        d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=OGC)
        d.text((x + w / 2, y + h / 2), b, font=fnt, fill=WHITE, anchor='mm')
        x += w + gap


def img_main(s, pdf_path):
    im = Image.new('RGB', (S, S), CREAM)
    d = ImageDraw.Draw(im)

    d.rectangle([0, 0, S, 26], fill=OGC)

    f_head = font(150)
    f_sub = font(62, bold=False)
    y = 130
    for line in s['headline'].split('\n'):
        d.text((S // 2, y), line, font=f_head, fill=INK, anchor='ma')
        y += 158
    d.text((S // 2, y + 14), s['sub'], font=f_sub, fill=DOGC, anchor='ma')

    badge_row(d, s['badges'], S // 2, y + 130, font(38))

    cover = render_page(pdf_path, 0, 880)
    max_h = S - (y + 250) - 190
    if cover.height > max_h:
        cover = cover.resize((int(cover.width * max_h / cover.height), max_h), Image.LANCZOS)
    paste_shadowed(im, cover, ((S - cover.width) // 2, y + 250))

    d.rectangle([0, S - 130, S, S], fill=INK)
    d.text((S // 2, S - 65), 'INSTANT DIGITAL DOWNLOAD   ·   PDF   ·   2026 EDITION',
           font=font(44), fill=CREAM, anchor='mm')
    return im


def img_inside(s, pdf_path):
    im = Image.new('RGB', (S, S), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, 26], fill=OGC)
    d.text((S // 2, 96), 'A LOOK INSIDE', font=font(96), fill=INK, anchor='ma')
    d.text((S // 2, 214), 'Real pages from the download', font=font(46, bold=False),
           fill=MUTED, anchor='ma')

    doc = fitz.open(pdf_path)
    n = doc.page_count
    doc.close()
    picks = [1, 2, 3, 4, 5, n - 1] if n > 6 else list(range(min(n, 6)))
    picks = picks[:6]

    cols, gap = 3, 46
    tile_w = (S - 200 - gap * (cols - 1)) // cols
    x0, y0 = 100, 320
    for i, p in enumerate(picks):
        page = render_page(pdf_path, p, tile_w)
        r, c = divmod(i, cols)
        paste_shadowed(im, page, (x0 + c * (tile_w + gap), y0 + r * (page.height + gap)),
                       blur=16, offset=(0, 10), alpha=90)

    d.rectangle([0, S - 130, S, S], fill=INK)
    d.text((S // 2, S - 65), s['badges'][1] + '   ·   INSTANT DOWNLOAD   ·   PDF',
           font=font(44), fill=CREAM, anchor='mm')
    return im


def img_included(s):
    im = Image.new('RGB', (S, S), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, 26], fill=OGC)
    d.text((S // 2, 110), "WHAT'S INCLUDED", font=font(96), fill=INK, anchor='ma')

    # Panel sized to its content, anchored above the footer bar.
    f_item = font(42, bold=False)
    panel_bottom = S - 130 - 40
    panel_h = 100 + len(s['included']) * 58 + 30
    panel_top = panel_bottom - panel_h

    # Bullet block, vertically centred in the space that leaves.
    f = font(50, bold=False)
    line_h, gap = 62, 22
    blocks = [wrap_text(d, b, f, S - 300) for b in s['bullets']]
    block_h = sum(len(ls) * line_h + gap for ls in blocks) - gap
    top, bottom = 290, panel_top - 70
    y = top + max(0, (bottom - top - block_h) // 2)
    for ls in blocks:
        d.ellipse([150, y + 14, 176, y + 40], fill=OGC)
        for line in ls:
            d.text((214, y), line, font=f, fill=INK)
            y += line_h
        y += gap

    d.rounded_rectangle([120, panel_top, S - 120, panel_bottom], radius=24,
                        fill=(238, 231, 220))
    d.text((160, panel_top + 38), 'FILES YOU RECEIVE', font=font(40), fill=DOGC)
    yy = panel_top + 106
    for item in s['included']:
        d.text((160, yy), '·  ' + item, font=f_item, fill=INK)
        yy += 58

    d.rectangle([0, S - 130, S, S], fill=INK)
    d.text((S // 2, S - 65), 'INSTANT DIGITAL DOWNLOAD   ·   NO SHIPPING',
           font=font(44), fill=CREAM, anchor='mm')
    return im


# ================================================================ LISTING COPY

def listing_md():
    L = ['# Etsy listing kit', '',
         'Generated by `build_etsy_kit.py`. Copy each block straight into the Etsy listing form.',
         '', 'Etsy limits: **title 140 characters**, **13 tags**, **20 characters per tag**. '
             'Every value below is validated against those limits at build time.', '',
         '## Setting up the listing', '',
         '- Type: **Digital** — "Instant download". No shipping profile needed.',
         '- Category: Paper & Party Supplies > Paper > Stationery, or Craft Supplies & Tools > '
         'Digital > Templates. Pick one and keep it consistent.',
         '- Upload the mockups from `outputs/etsy/<sku>/` in order: `01_main`, `02_inside`, '
         '`03_included`. The first image is 80% of whether anyone clicks.',
         '- Renewal: Etsy gives new listings a short visibility boost. Stagger your listings '
         'across a few days rather than posting them all at once.',
         '', '---', '']

    for s in SKUS:
        assert len(s['title']) <= 140, '%s title is %d chars' % (s['sku'], len(s['title']))
        assert len(s['tags']) == 13, '%s has %d tags' % (s['sku'], len(s['tags']))
        for t in s['tags']:
            assert len(t) <= 20, '%s tag too long: %r (%d)' % (s['sku'], t, len(t))

        L += ['## %s' % s['sku'], '',
              '**Suggested price:** %s' % s['price'], '',
              '**Etsy fit:** %s' % s['etsy_fit'], '',
              '### Title (%d/140 chars)' % len(s['title']), '', '```', s['title'], '```', '',
              '### Tags (13)', '', '```', ', '.join(s['tags']), '```', '',
              '### Description', '', '```']
        L += [s['headline'].replace('\n', ' ').upper(), '']
        L += textwrap.wrap(s['blurb'], 78)
        L += ['']
        L += ['WHAT YOU GET', '']
        for b in s['bullets']:
            L.append('* ' + b)
        L += ['', 'FILES INCLUDED', '']
        for i in s['included']:
            L.append('* ' + i)
        L += ['',
              'INSTANT DIGITAL DOWNLOAD',
              '* Files are available the moment your payment clears',
              '* Works on phone, tablet, laptop and desktop',
              '* Nothing ships — this is a digital product',
              '* Updated for 2026',
              '',
              'Part of the Claude AI Field Guide Series.',
              '',
              'Because this is an instant download, it cannot be returned. If a file will not '
              'open, message me and I will fix it.',
              '```', '', '---', '']

    L += ['## Notes on the developer SKUs', '',
          'Etsy shoppers are overwhelmingly buying planners, printables, craft and small-business '
          'material. Developers do not browse Etsy for tooling. The developer volumes '
          '(`04-claude-code-volume`, `05-config-pack`, `06-volume-2-developer-setup`, '
          '`07-volume-4-automation-kit`, `09-volume-6-advanced`) are listed for completeness and '
          'for catalogue depth, but expect them to sell on Gumroad, Reddit and X rather than '
          'through Etsy search.', '',
          'The ones worth pushing on Etsy are `01-prompt-vault`, `02-starter-volume`, '
          '`03-complete-library` and `08-volume-5-api-automation`.', '']
    return '\n'.join(L)


# ======================================================================= BUILD

def main():
    os.makedirs(ETSY, exist_ok=True)
    made = 0
    for s in SKUS:
        pdf = os.path.join(OUT, s['pdf'])
        if not os.path.exists(pdf):
            print('SKIP %s — missing %s' % (s['sku'], s['pdf']))
            continue
        folder = os.path.join(ETSY, s['sku'])
        os.makedirs(folder, exist_ok=True)
        for name, im in (('01_main', img_main(s, pdf)),
                         ('02_inside', img_inside(s, pdf)),
                         ('03_included', img_included(s))):
            p = os.path.join(folder, name + '.png')
            im.save(p, 'PNG', optimize=True)
            made += 1
        print('%-24s 3 images  %s' % (s['sku'], s['price']))

    md = os.path.join(ETSY, 'LISTINGS.md')
    with open(md, 'w', encoding='utf-8') as f:
        f.write(listing_md())
    print('%d images + LISTINGS.md -> %s' % (made, ETSY))


if __name__ == '__main__':
    main()
