# CLAUDE AI FIELD GUIDE — MASTER BUILD PLAN
# PDF Series for Etsy/Gumroad Digital Product Sales
# Last updated: June 26, 2026 — ALL 20 GUIDES COMPLETE

---

## PROJECT OVERVIEW

A series of 20 beginner-to-advanced PDF field guides covering every way to access and
use Claude AI. Each guide is a standalone Etsy/Gumroad digital product. Together they
form a complete "Claude AI Learning Library" bundle.

**Target audience:** Complete beginners → developers → power users → automation builders
**Format:** Dark-themed PDF (matching Guide 01 visual style)
**Price range:** $7–$15 per guide / $49–$99 for full bundle
**Platforms:** Etsy (primary), Gumroad (secondary)

---

## DESIGN SYSTEM (apply to every guide)

```
COLORS:
  BG      = #0F0F1A   (page background)
  OG      = #E07A38   (primary accent, headings)
  OGL     = #F5A66B   (secondary accent)
  CREAM   = #F5F0E8   (title text)
  LGR     = #D4CFC7   (body text)
  MGR     = #9B9690   (captions, footnotes)
  PNL     = #1C1C2E   (info panels, cards)
  PNL2    = #161625   (alternating table rows, secondary panels)
  GRN     = #5CB85C   (checkmarks, success, tips)
  AMB     = #F59E0B   (warning boxes)
  PUR     = #8B5CF6   (Max plan, advanced content)
  DOG     = #C86820   (darker orange — decorative circles on cover)
  DDOG    = #B85C18   (darkest orange — badge background)
  DBGRN   = #0D2B0D   (tip box background)
  DBAMB   = #2B1A00   (warning box background)
  CODE_BG = #0A0A15   (code block background)
  WHT     = #FFFFFF

TYPOGRAPHY:
  Title:    Helvetica-Bold 22–28pt Orange
  H2:       Helvetica-Bold 15pt OGL
  H3:       Helvetica-Bold 12pt Cream
  Body:     Helvetica 10–11pt LGR, leading 15–17
  Caption:  Helvetica 9pt MGR
  Code:     Courier 9pt (comments in MGR, code in GRN)

LAYOUT:
  Page:    Letter (8.5 x 11 in / 612 x 792 pt)
  Margins: MX = 0.65in  →  CW = W - 2*MX = 518.4pt
  Footer:  22pt dark panel bar — page number right, guide title left
  Header:  6pt orange accent bar across top of every content page

COVER PAGE ELEMENTS:
  - Full dark background
  - Orange top block (130pt tall) with decorative DOG/DDOG circles
  - Guide number badge ("GUIDE XX OF 20") in DDOG rounded rect
  - Series name: CLAUDE AI FIELD GUIDE SERIES (8pt WHT)
  - Guide title (26–28pt CREAM Helvetica-Bold)
  - Subtitle / tagline (14pt OGL)
  - "What's Inside" bullet box (PNL panel, OG left border, 6 bullets)
  - Bottom orange bar (36pt) with series tagline in WHT

CONTENT PAGES:
  - Step cards   — card_h = 48 + len(lines)*15  (orange badge, PNL background)
  - Info panels  — ph = len(lines)*16 + pad*2 + 22  (pad=12)
  - Tip boxes    — bh = len(lines)*15 + pad*2 + 20  (pad=10, GRN left border)
  - Warning boxes — same formula as tip, AMB/DBAMB
  - Code blocks  — lh=13, CODE_BG background, OG 0.5pt border, Courier 9pt
  - Tables       — OG header row, alternating PNL2/PNL rows, rh=22
```

---

## BUILD RULES (follow every time)

1. Run `python build_guideXX.py` to generate — never edit PDFs manually
2. All output goes to `C:\Projects\UserGuide\outputs\`
3. File naming: `Claude_Field_Guide_XX_[ShortTitle].pdf`
4. Each guide: 6 pages (cover + 5 content pages) — established pattern
5. Every guide must include:
   - Cover page with "What's Inside" box (6 bullets)
   - Page 2: What/Why intro or first major topic
   - Pages 3–5: Step-by-step content (step cards, tables, code blocks)
   - Page 6: Quick reference cheat sheet + troubleshooting table + "Next in series" CTA
6. Verify current facts (pricing, features) via web search before writing
7. Keep screenshots described in text — no actual screenshots in PDF (copyright risk)
8. End every guide with: "Next in the series: [Guide N+1 title]" (Guide 20 uses series-end CTA)
9. Use `simpleSplit` from `reportlab.lib.utils` for all body text wrapping
10. Use `canvas` API (not Platypus) — full layout control required for design system

---

## TECHNICAL IMPLEMENTATION

### Environment
- Python 3.14.4
- reportlab 5.0.0 (`pip install reportlab`)
- Windows 10 Pro, PowerShell

### Helper Function Signatures (copy into every build script)

```python
def pg_bg(c):           # fill page with BG color
def hdr(c):             # 6pt OG bar at top of page
def ftr(c, n):          # 22pt PNL footer — guide title left, page num right
def step_card(c, x, y, num, title, lines, w):   # returns new y after card
def tip_box(c, x, y, heading, lines, w):         # returns new y
def warn_box(c, x, y, heading, lines, w):        # returns new y
def info_panel(c, x, y, heading, lines, w):      # returns new y
def code_block(c, x, y, lines, w):              # returns new y
def tbl(c, x, y, headers, rows, col_w):         # returns new y after table
def wrap(text, size, width, font='Helvetica'):   # simpleSplit wrapper
```

### Key Formula Notes
- Card height: `card_h = 48 + len(lines) * 15`
- Info panel height: `ph = len(lines) * 16 + pad*2 + 22` (pad=12)
- Tip/warn height: `bh = len(lines) * 15 + pad*2 + 20` (pad=10)
- Code block height: `bh = len(lines) * 13 + pad*2` (pad=10, lh=13)
- Table row height: `rh = 22` (header row + each data row)
- Origin: bottom-left (reportlab default) — y decreases as you go down the page
- Content start: `y = H - 30` after header, first element at `y - 20`

### Build Command
```
cd C:\Projects\UserGuide
python build_guideXX.py
```

---

## SERIES STRUCTURE

### VOLUME 1: Getting Into Claude (No coding required)
Target: Complete beginners. Sell individually or as a "Starter Pack" bundle.

| # | File | Title | Status |
|---|------|-------|--------|
| 01 | build_guide01.py | Claude on the Web (claude.ai) | ✅ DONE |
| 02 | build_guide02.py | Claude Mobile App (iOS & Android) | ✅ DONE |
| 03 | build_guide03.py | Claude Desktop App (Mac & Windows) | ✅ DONE |
| 04 | build_guide04.py | Claude in Chrome (Browser Extension) | ✅ DONE |
| 05 | build_guide05.py | Claude Integrations (Slack, Excel, PowerPoint, Cowork) | ✅ DONE |

### VOLUME 2: Developer Setup (First coding tools)
Target: Beginners who want to go deeper. "Dev Starter Kit" bundle.

| # | File | Title | Status |
|---|------|-------|--------|
| 06 | build_guide06.py | Installing Node.js | ✅ DONE |
| 07 | build_guide07.py | Git & GitHub for Claude Users | ✅ DONE |
| 08 | build_guide08.py | Docker Basics for AI Projects | ✅ DONE |
| 09 | build_guide09.py | VS Code Setup for Claude | ✅ DONE |

### VOLUME 3: Claude Code & Agentic Workflows
Target: Developers. "Claude Code Mastery" bundle.

| # | File | Title | Status |
|---|------|-------|--------|
| 10 | build_guide10.py | Claude Code in VS Code | ✅ DONE |
| 11 | build_guide11.py | CLAUDE.md Files — Build Plans That Work | ✅ DONE |
| 12 | build_guide12.py | Subagents & Hooks in Claude Code | ✅ DONE |
| 13 | build_guide13.py | How Agentic Loops Work | ✅ DONE |

### VOLUME 4: MCP Servers, Plugins & Skills
Target: Power users. "Claude Automation Kit" bundle.

| # | File | Title | Status |
|---|------|-------|--------|
| 14 | build_guide14.py | MCP Servers 101 | ✅ DONE |
| 15 | build_guide15.py | Installing & Using MCP Servers | ✅ DONE |
| 16 | build_guide16.py | Claude Plugins Guide | ✅ DONE |
| 17 | build_guide17.py | Claude Skills — Create Your Own | ✅ DONE |

### VOLUME 5: Automation & API
Target: Advanced users and developers.

| # | File | Title | Status |
|---|------|-------|--------|
| 18 | build_guide18.py | Claude API Basics | ✅ DONE |
| 19 | build_guide19.py | Building Automations with Claude | ✅ DONE |
| 20 | build_guide20.py | Prompting Masterclass | ✅ DONE |

### VOLUME 6: Advanced Add-Ons (post-20 expansion)
Target: Claude Code power users. Sold individually or as an "Advanced Pack".

| # | File | Title | Status |
|---|------|-------|--------|
| 21 | build_guide21.py | Multi-Agent Orchestration | ✅ DONE |
| 22 | build_guide22.py | Evaluating & Testing Claude Agents | ✅ DONE |
| 23 | build_guide23.py | Claude Cost & Token Management | ✅ DONE |
| 24 | build_guide24.py | Security & Safety for Claude Workflows | 🔲 PLANNED |
| 25 | build_guide25.py | Context Engineering & Memory | 🔲 PLANNED |

---

## SALEABLE PRODUCTS (built — these are what actually get listed)

Individual 6-page guides are NOT competitive as standalone paid products (buyers
scan page count first). They are inputs. These compiled products are the SKUs.

### Volume compilations — `python build_volumes.py`
Imports each `build_guideXX.py`, monkeypatches its module-level `ftr()` for continuous
page numbering, and renders all pages onto one canvas behind a new volume cover + TOC.
Source guides are never modified. Add a volume by appending to `VOLUMES` in that file.

| File | Guides | Pages | Price |
|------|--------|-------|-------|
| `Claude_Field_Guide_Volume_1_Getting_Started.pdf` | 01–05 | 32 | $9.99 |
| `Claude_Field_Guide_Volume_2_Developer_Setup.pdf` | 06–09 | 26 | $9.99 |
| `Claude_Field_Guide_Volume_3_Claude_Code.pdf` | 10–13 | 26 | $12.99 |
| `Claude_Field_Guide_Volume_4_Automation_Kit.pdf` | 14–17 | 26 | $12.99 |
| `Claude_Field_Guide_Volume_5_API_Automation.pdf` | 18–20 | 20 | $9.99 |
| `Claude_Field_Guide_Volume_6_Advanced.pdf` | 21–23 | 20 | $9.99 |
| `Claude_Field_Guide_COMPLETE_LIBRARY.pdf` | 01–23 | 140 | $29.99 |

### Asset products (not prose — this is where willingness-to-pay is)
| Product | Build script | Output |
|---------|--------------|--------|
| The Claude Prompt Vault | `build_prompt_vault.py` | 29pp PDF + `.md` + `.txt`, 200 prompts / 10 categories |
| Claude Code Config Pack | `build_config_pack.py` | 32-file tree + `.zip` + 6pp install guide PDF |
| Etsy listing kit | `build_etsy_kit.py` | 27 mockup PNGs (2000×2000) + `LISTINGS.md` |
| Etsy publisher | `etsypub/` (package) | Pushes the 6 volumes live via Etsy Open API v3 |
| FREE lead magnet | `build_start_here.py` | 2pp Start Here |

- Prompt Vault content lives in `prompt_vault_data.py` (single source → PDF, md, txt).
  `build_prompt_vault.py` runs `verify_no_overflow()` and hard-fails the build on any
  line that would run past the right margin — do not remove that guard.
- Config Pack file contents are string literals in `build_config_pack.py`. Every hook,
  permission and MCP fact in it was verified against code.claude.com/docs, July 2026.
- Etsy mockups composite REAL pages rendered from the product PDFs via PyMuPDF. Cream
  (#F7F2EA) background, not white — white blends into Etsy's search grid.
  Title ≤140 chars, exactly 13 tags, ≤20 chars per tag are asserted at build time.

---

## CONTENT OUTLINE PER GUIDE

Each guide follows this template:

```
COVER PAGE
  - Badge: "Guide XX of 20 — Claude AI Field Guide Series"
  - Title (26-28pt)
  - Tagline (14pt OGL)
  - What's Inside box (6 bullet points, GRN checkmarks)

PAGE 2: INTRO / FIRST MAJOR TOPIC
  - What you'll learn
  - Who this is for
  - Prerequisites or first concept explained

PAGES 3–5: STEP-BY-STEP CONTENT
  - Numbered step cards (orange badge + dark panel)
  - Info panels for context and definitions
  - Tip boxes for pro advice (green border)
  - Warning boxes for common mistakes (amber border)
  - Code blocks for commands/configs (CODE_BG, OG border)
  - Comparison tables (OG header, alternating rows)

PAGE 6: QUICK REFERENCE CHEAT SHEET
  - Two-column reference panels (key commands/facts)
  - Common troubleshooting table (Problem | Fix)
  - "Next in the series" CTA panel (OG border)
  - Guide 20 only: Series-end CTA (OG full-width panel)
```

---

## INDIVIDUAL GUIDE NOTES (what was actually built)

### Guide 01 — Claude on the Web ✅
- File: `Claude_Field_Guide_01_Web.pdf` | 6 pages
- Key content: claude.ai tour, account setup, Free/Pro/Max/Team/Enterprise plan comparison
  table, 10 things to try today, keyboard shortcuts, pro tips
- Unique: Plan comparison table with per-plan feature matrix

### Guide 02 — Claude Mobile App ✅
- File: `Claude_Field_Guide_02_Mobile.pdf` | 6 pages
- Key content: iOS App Store + Android Google Play download, account login, voice conversation
  mode walkthrough, camera/image input, on-the-go use cases (commute, travel, meetings)
- Unique: Voice mode step-by-step, mobile-specific tips panel

### Guide 03 — Claude Desktop App ✅
- File: `Claude_Field_Guide_03_Desktop.pdf` | 6 pages
- Key content: Download from claude.ai/download (Mac Apple Silicon/Intel + Windows),
  differences from web version, Projects setup, local file drag & drop,
  keyboard shortcuts table (Cmd/Ctrl+K new chat, Cmd+, settings, etc.)
- Unique: Shortcuts reference table, Projects workflow

### Guide 04 — Claude in Chrome ✅
- File: `Claude_Field_Guide_04_Chrome.pdf` | 6 pages
- Key content: Chrome Web Store install, extension activation, browsing agent mode,
  page summarization, form-filling assistance, privacy controls
- Note: Extension described as beta as of mid-2026; feature set verified via web search

### Guide 05 — Claude Integrations ✅
- File: `Claude_Field_Guide_05_Integrations.pdf` | 6 pages
- Key content: Claude for Slack (slash commands /claude, workspace setup, Team plan required),
  Claude in Excel (MS365 add-in, formula help, data analysis), Claude in PowerPoint
  (slide generation), Cowork (collaborative AI workspace)
- Note: MS365 integration requires Microsoft 365 subscription; Slack requires Team/Enterprise

### Guide 06 — Installing Node.js ✅
- File: `Claude_Field_Guide_06_NodeJS.pdf` | 6 pages
- Key content: Node.js LTS 22.x explained in plain English, nvm vs direct installer,
  Mac (Homebrew + nvm), Windows (installer + nvm-windows), Linux (apt + nvm),
  verify with `node -v` and `npm -v`, PATH troubleshooting, version conflict fixes
- Unique: Three-platform install paths in one guide; common errors section

### Guide 07 — Git & GitHub ✅
- File: `Claude_Field_Guide_07_Git.pdf` | 6 pages
- Key content: Version control explained for non-coders, Git install (Mac/Windows/Linux),
  configure name + email, create GitHub account, clone a repo, core commands
  (init/add/commit/push/pull/status/log), plain-English glossary (repo/branch/commit/PR/fork)
- Unique: Glossary panel; framed for someone who has never used a terminal

### Guide 08 — Docker Basics ✅
- File: `Claude_Field_Guide_08_Docker.pdf` | 6 pages
- Key content: Docker Desktop licensing (free for personal/education/small business
  <250 employees AND <$10M revenue; Pro $9/month annual), container vs VM comparison,
  "lunchbox" analogy, essential commands (pull/run/ps/stop/build/logs),
  docker-compose.yml example with ANTHROPIC_API_KEY env var
- Unique: Lunchbox framing; real compose example for AI projects

### Guide 09 — VS Code Setup ✅
- File: `Claude_Field_Guide_09_VSCode.pdf` | 6 pages
- Key content: VS Code 1.98+ download, UI tour (Explorer/Editor/Terminal/Extensions),
  5 key extensions (Claude Code by Anthropic, GitLens, ESLint, Prettier, Error Lens),
  settings.json (formatOnSave, defaultFormatter, tabSize, wordWrap),
  integrated terminal, Claude Code extension features (file context, inline diffs)
- Unique: Settings.json code block; extension feature comparison

### Guide 10 — Claude Code in VS Code ✅
- File: `Claude_Field_Guide_10_ClaudeCode.pdf` | 6 pages
- Key content: `npm install -g @anthropic-ai/claude-code`, paid plan required
  (Pro/Max/Team/Enterprise) or API key, browser-based auth flow, trust dialog,
  diff review workflow, slash commands (/help /clear /compact /status /doctor
  /terminal-setup /plugins /cost), Escape to cancel mid-run
- Unique: Slash command reference table; trust dialog explained

### Guide 11 — CLAUDE.md Files ✅
- File: `Claude_Field_Guide_11_CLAUDEmd.pdf` | 6 pages
- Key content: Plain markdown auto-loaded every session, keep under 200 lines,
  6 essential sections (Tech Stack / Commands / Architecture / Conventions /
  Boundaries / Build Rules), progressive disclosure (link to detail files),
  CLAUDE.md advisory (~70-90%) vs Hooks deterministic, three locations
  (~/CLAUDE.md global, ./CLAUDE.md project, subdirectory overrides)
- Unique: Copy-paste template CLAUDE.md; meta guide — teaches the skill used to build this series

### Guide 12 — Subagents & Hooks ✅
- File: `Claude_Field_Guide_12_Hooks.pdf` | 6 pages
- Key content: Subagents = parallel Claude instances for subtasks, 8 hook events
  (SessionStart / SessionEnd / UserPromptSubmit / PreToolUse / PostToolUse /
  Stop / StopFailure / Notification), config in .claude/settings.json (shared)
  or .claude/settings.local.json (personal), matcher field for targeted hooks,
  real examples (ESLint PostToolUse, guard PreToolUse, Stop desktop notification)
- Unique: Hook event reference table; annotated settings.json example

### Guide 13 — Agentic Loops ✅
- File: `Claude_Field_Guide_13_AgenticLoops.pdf` | 6 pages
- Key content: 4-step loop (Receive → Evaluate → Tool Call → Decide to continue/stop),
  available tools (Read/Write/Edit/Bash/Grep/Glob/Agent/WebFetch), stopping conditions
  (task complete / --max-turns / max_budget_usd / hook exit 1 / Escape),
  context growth (50K+ tokens by iteration 20), /compact for 60-80% reduction,
  cost management (/status, explicit criteria, --max-turns, max_budget_usd)
- Unique: Loop diagram walkthrough; cost control reference panel

### Guide 14 — MCP Servers 101 ✅
- File: `Claude_Field_Guide_14_MCP101.pdf` | 6 pages
- Key content: MCP = Model Context Protocol, open standard by Anthropic (Nov 2024),
  USB-hub analogy, three-layer architecture (Host/Client/Server), three primitives
  (Tools=actions / Resources=read-only data / Prompts=templates), JSON-RPC 2.0,
  "mcpServers" config key, 16,000+ servers available, mcp.so and modelcontextprotocol.io
- Unique: Architecture diagram in text; primitive comparison table

### Guide 15 — Installing MCP Servers ✅
- File: `Claude_Field_Guide_15_MCPInstall.pdf` | 6 pages
- Key content: Config file locations (Mac: ~/Library/Application Support/Claude/
  claude_desktop_config.json; Windows: %APPDATA%\Claude\claude_desktop_config.json),
  step-by-step for 3 MCPs: Filesystem (@modelcontextprotocol/server-filesystem, no key),
  GitHub (@modelcontextprotocol/server-github, PAT with repo/read:org/read:user scopes),
  Brave Search (@modelcontextprotocol/server-brave-search, free 2000 queries/month),
  complete 3-server config JSON shown; restart required after editing
- Unique: Full working config.json with all 3 servers; PAT scope list

### Guide 16 — Claude Plugins ✅
- File: `Claude_Field_Guide_16_Plugins.pdf` | 6 pages
- Key content: claude.com/plugins, Plugins vs MCP servers distinction clearly drawn,
  Web Search (all plans, real-time citations), Code Execution (Pro+ only, Python sandbox),
  Chat Artifacts (all plans, up to 20MB, can call APIs + MCP connections),
  Claude Code Artifacts (beta June 18 2026, Team/Enterprise only, single HTML page),
  Connectors (managed MCP — Gmail/Drive/Slack/GitHub/Notion/Stripe/Zapier), plan matrix
- Unique: Plugins vs MCP comparison; plan availability matrix table

### Guide 17 — Claude Skills ✅
- File: `Claude_Field_Guide_17_Skills.pdf` | 6 pages
- Key content: Skills = folders at ~/.claude/skills/skill-name/ with SKILL.md,
  YAML frontmatter (name / description / allowed-tools / disable-model-invocation),
  description field is the trigger — must be specific, Skill Creator tool
  (prompt "create a new skill"), official skills at github.com/anthropics/skills,
  community 330+ skills at github.com/alirezarezvani/claude-skills,
  /skills and /skill skill-name commands, keep body concise (tokens per turn)
- Unique: Copy-paste SKILL.md template; trigger specificity guidance

### Guide 18 — Claude API Basics ✅
- File: `Claude_Field_Guide_18_API.pdf` | 6 pages
- Key content: console.anthropic.com, pay-as-you-go (separate from claude.ai subscription),
  ANTHROPIC_API_KEY env var, curl example + Python SDK (pip install anthropic),
  model IDs + pricing: Haiku 4.5 (claude-haiku-4-5-20251001) $1/$5 per M tokens,
  Sonnet 4.6 (claude-sonnet-4-6) $3/$15, Opus 4.8 (claude-opus-4-8) $5/$25,
  cache hit 10%, Message Batches 50% off, error codes (401/429/529/400),
  retry with exponential backoff pattern
- Unique: Pricing table with all 3 tiers; error code reference

### Guide 19 — Building Automations ✅
- File: `Claude_Field_Guide_19_Automations.pdf` | 6 pages
- Key content: Claude Code Routines (launched April 14, 2026, research preview),
  Routine = config + prompt + repos + connectors + trigger, three trigger types:
  Scheduled (hourly/daily/weekday/weekly), API (POST to endpoint with bearer token —
  api.anthropic.com/v1/claude_code/routines/{id}/fire), GitHub (push/PR/issues/CI events),
  cloud execution on Anthropic infrastructure, daily digest Python pipeline example,
  scheduling options (Routines / cron / Task Scheduler / GitHub Actions / Zapier)
- Unique: End-to-end daily digest code example; alert-response pipeline flow diagram

### Guide 20 — Prompting Masterclass ✅
- File: `Claude_Field_Guide_20_Prompting.pdf` | 6 pages
- Key content: 5-part prompt anatomy (Role/Task/Context/Constraints/Output Format),
  system prompt "contract" format, XML tags as best structuring method
  (<instructions> <context> <example> <thinking> <answer> <format>),
  chain-of-thought (+19 point boost on MMLU-Pro, skip for reasoning models),
  7 techniques (few-shot / role / CoT / XML / output schema / negatives / iterative),
  optimal prompt length 150-300 words, 30 copy-paste templates across 5 categories
  (Writing / Code / Analysis / Productivity / Creative), before/after examples
- Unique: 30 templates; before/after weak vs strong prompt comparison; series capstone

---

## EXECUTION WORKFLOW

When rebuilding or adding a guide, follow this process:

1. **Check this file** — confirm which guide is next (find first status that isn't ✅ DONE)
2. **Research** — web search for current facts on that topic (pricing, versions, features)
3. **Write `build_guideXX.py`** — use reportlab canvas API, match design system exactly
4. **Build PDF** — `python build_guideXX.py` from `C:\Projects\UserGuide\`
5. **Output file** — `C:\Projects\UserGuide\outputs\Claude_Field_Guide_XX_[Title].pdf`
6. **Update status** — mark ✅ DONE in the series table above
7. **Report** — confirm PDF exists and page count is correct

---

## ETSY LISTING TEMPLATE

**Title format:** `[Topic] for Beginners | Complete Claude AI Guide [Volume X] | Digital PDF | [Year]`

**Tags (use all 13):**
claude ai, claude tutorial, ai guide pdf, ai for beginners, claude pro, anthropic,
ai tools 2026, digital download, claude code, ai automation, prompt engineering,
ai tutorial pdf, claude field guide

**Description template:**
```
🤖 GUIDE [XX] OF 20 — CLAUDE AI FIELD GUIDE SERIES

Everything you need to know about [topic] — explained in plain English.
No tech background required.

✅ [Bullet 1 from What's Inside]
✅ [Bullet 2]
✅ [Bullet 3]
✅ [Bullet 4]
✅ [Bullet 5]
✅ [Bullet 6]

---
📥 INSTANT DIGITAL DOWNLOAD
• PDF format — works on phone, tablet, or computer
• 6 pages of clear, step-by-step guidance
• Updated for 2026

Part of the Claude AI Field Guide Series — 20 guides covering every way to use Claude AI.
```

---

## NOTES & DECISIONS LOG

- 2026-09-22: **PINTEREST PIN FACTORY — `pins/` package, 48 pins, `build_pins.py`.**
  Distribution work, not more catalogue. Pinterest rewards FRESH PINS, not new
  products, so one image per product is about a week of posting. Six templates x nine
  consumer-fit SKUs turns pin production from a writing problem into a template one.
  `pins/canvas.py` (pin-sized canvas + shared drawing) · `pins/copy.py` (titles,
  descriptions, boards, hooks, tips, comparisons, URL resolution) · `pins/templates.py`
  (product · listicle · hook · checklist · comparison · tip) · `build_pins.py` ->
  `outputs/pins/<sku>/<template>.png` + `PINS.csv`. Built on `covers/`, so a pin
  inherits its series palette. 167 tests. Spec + plan in `docs/superpowers/`.
  - **Scoped to NINE consumer-fit SKUs** (40-chatgpt-v1, 02, 01, 10, 11, 12, 03, 20, 30).
    The deep developer volumes are excluded: their audience is not on Pinterest, and
    low-engagement pins drag a young account's signal when it matters most.
  - 48 render, 6 skip. **A template that cannot render returns None and the build says
    so** — `comparison` skips the six SKUs with no curated rows. Padding it with the
    SKU's `included` list (a file manifest) is explicitly forbidden.
  - **One title per product, reused across its pins.** Inventing six per-template
    variants is where fabricated claims creep in. Titles/descriptions are byte-identical
    to `outputs/pins/PINS_wave1.csv`, which is already live on Pinterest.
  - Posting is MANUAL — no Pinterest API, no credentials in this project.

  **`canvas.overflows()` WAS WRONG THREE TIMES. Read this before touching a guard.**
  It stops a pin shipping with clipped text, and each wrong version passed review:
  1. Compared margin pixels to the canvas CENTRE — but the centre is CONTENT, so any
     centred pin false-positived. Survived because every test drew on an EMPTY pin.
  2. Compared to the MIRRORED opposite margin — defeated by centred text, which
     overflows both sides by the same amount in the same colour, so ink was compared
     to ink. Reproduced with two rectangles at x 0-40 and x 959-999.
  3. Correct: compare against a FRESHLY RENDERED background. Deterministic, and no
     symmetry can game it. **It assumes every template paints the standard gradient** —
     a future full-bleed template would make the whole canvas read as overflow.
  **And the real hole was an axis nobody checked:** both guards looked sideways only.
  Text at y=1420 (straight over the footer) or y=1480 (off the canvas) passed clean.
  `footer_collision()` closes it. `audit_pdfs.py` has had the equivalent footer-bar
  check for the PDFs since the same bug shipped there. **Three properties matter:
  containment, reach, collision.** A guard that checks two of three looks green.
  - `content_extent()` requires content to reach >= 0.70 down the canvas. Proved
    non-vacuous by measuring the PRE-FIX templates: 0.30-0.54, all under the floor.
    `product` is exempt — it renders the approved cover art via `covers/`.
  - **`make_contact_sheet.py` is committed and should be run before a posting batch.**
    The guards prove a pin is contained and full; only eyes tell you it is worth
    pinning. A human looking at rendered pins is what caught BOTH real design defects
    on this branch — half-empty canvases, and `checklist` being `listicle` with a
    different glyph — neither of which any passing test could see.
  - **FIXED IN `covers/palette.py`: grok had `title` and `spine_front` IDENTICAL**
    `(11,13,16)`. Every accent — listicle numerals, checklist ticks, the comparison's
    whole right column, the TIP label — would have rendered as body text the moment
    the Grok series started. A test now asserts `title != spine_front` for all five.
  - `url_for` gates on Etsy `state == 'active'` and Gumroad `published`. **Etsy
    listings expire after four months**, so this is a decaying guarantee — rebuild
    before a posting batch rather than trusting an old CSV.

- 2026-09-20: **ETSY FULLY REPUBLISHED — 21 products, new covers, matching PDFs.**
  `--update-images` pushed 5 images to all 20 existing listings (20 ok / 0 failed), then
  `--update-files` pushed the rebuilt PDFs (20 ok / 1 benign fail). **ChatGPT Volume 1 is
  LIVE** — listing 4579194466, $9.99, activated for $0.20. Catalogue is now 21 Etsy SKUs.
  Verified after the fact: every listing holds exactly ONE file and the remote byte sizes
  match the local builds.
  - The one `--update-files` failure was `40-chatgpt-v1`: *"File ... is already attached to
    this listing"*. **Etsy dedupes by content** — that listing got the identical PDF at
    draft creation an hour earlier, so the re-upload was refused. Benign. It also proved
    per-SKU error isolation works: one failure did not abort the other twenty.
  - **`--status` lagging is normal.** Immediately after activation Etsy still reported the
    listing as `draft`; it reconciled to `active` minutes later. Do not "fix" a mismatch
    seen seconds after an activation — re-check first.
  - **Listing GETs are listing-scoped, not shop-scoped.** `GET /shops/{s}/listings/{id}`
    404s; `GET /listings/{id}` works. Same asymmetry already logged for images, now
    confirmed for the listing itself.
  - **The shop holds 74 active listings but only 21 are ours** — the other 53 are POD
    t-shirts from `TShirt1` sharing the shop. Checked and classified: **zero** are digital
    or AI products, so nothing competes with the guides. Expect this gap in `--status`.

- 2026-09-20: **etsypub gaps closed** (branches merged to main; 94 tests).
  - `--update-images` ADDED — there was previously NO way to replace listing images on an
    already-published listing; `build_draft` gates image upload behind a sticky
    `images_done` flag. Without it the shop would have shown old thumbnails over new PDFs.
  - `--update-files` previously covered only the 6 volume SKUs, ignored `--skus`, and
    **ignored `--dry-run` entirely** — typing it would have silently mutated 6 live
    listings. It now covers every live listing and short-circuits before `Etsy()` is even
    constructed. Both flags share one driver (`run_over_live`).
  - `build_draft` uploaded only 3 images; now 5, and `check()` validates all five
    pre-flight. The missing one was `05_wide.png`, which `gumroadpub.etsy_cover_urls`
    needs — without it Gumroad keeps cropping the square cover.
  - `gumroadpub.etsy_cover_urls` now PREFERS LANDSCAPE (`full_width > full_height`).
    Etsy must keep the square at rank 1, so sorting at the Gumroad end is the only way
    both channels get the right shape.
  - `--skus` on these flags now RAISES on an unknown name, and raises a *different*
    message for a known-but-unlisted SKU ("publish it first"). A publishing tool that
    silently does nothing looks like success.

- 2026-09-20: **ChatGPT Volume 1 built** — `build_chatgpt_v1.py`, 27pp, audit clean, 66%
  fill. Violet accent `#B45CFF`, NOT OpenAI green: `CODEX` already owns `#10A37F`, and at
  thumbnail size two OpenAI products in the same green merge into one another on the shop
  page. Cover palette `gpt` was changed to match after a side-by-side shelf comparison.
  - **Ch 4 was swapped before writing.** The approved outline said "Custom GPTs — build
    one". OpenAI is RETIRING them: migration opened 17 Sep 2026, new creation ends
    **25 Sep 2026**, they stop running **11 Dec 2026**. Teaching a buyer to build one would
    have been the Brave-Search-free-tier mistake again. Ch 4 is now Plugins & Connected
    Apps, and the retirement table is the volume's differentiator — competing guides still
    teach building GPTs. **This content decays: after 11 Dec it needs rewriting.**
  - Also verified and printed: Pro $200 **new sign-ups are PAUSED** (since 10 Sep 2026);
    existing subs and Pro $100 unaffected. Plans are Free / Go $8 / Plus $20 / Pro $100
    (5x) / Pro $200 (20x). All pricing is on ONE page so a reprint is one edit.
  - Ch 5 limits are NOT printed as fact — OpenAI does not publish image-generation
    numbers. The book says so. Codex V4 precedent: an acknowledged gap beats an invented
    figure.
  - **`Theme.series_display` replaces `theme.series.title()`.** `.title()` turned
    'CHATGPT ...' into '**Chatgpt** ...' on all 27 pages AND in the PDF author metadata.
    Build was clean, audit was clean, 80 tests passed — nothing checks what a footer SAYS.
    Caught only by reading the PDF. Note `'CLAUDE AI ...'.title()` gives 'Claude **Ai**',
    which is also wrong but ships on live products; pinned in a test, deliberately unfixed.

- 2026-09-20: **COVER SYSTEM REBUILT — all 21 live products, new art, `covers/` package.**
  Owner feedback: nothing on Gumroad sold; covers must look like a 2026 digital product.
  New `covers/` package is the ONLY thing that knows what a cover looks like:
  `palette.py` (5 series palettes) + `spec.py` (`CoverSpec`, validates in `__post_init__`)
  + `catalogue.py` (derives specs from `build_etsy_kit.SKUS` — no second catalogue)
  + `render.py` (one Pillow renderer) + `pdfpage.py` (one-page Letter PDF).
  Four shapes: `square` 2000x2000 (Etsy), `wide` 1280x720 (Gumroad — its grid is
  LANDSCAPE and was side-cropping every square image), `pin` 1000x1500 (Pinterest),
  `letter` 1700x2200 (the PDF cover page, exactly 8.5x11in at 200 DPI).
  Design is "direction C": angled 3-book stack on a light gradient. **Covers are LIGHT
  even though interiors stay dark #0F0F1A** — a dark thumbnail sinks into Etsy's white
  search grid. Rolled out by `rebuild_covers.py`, which splices page 0 only; interiors
  are never regenerated. Pristine originals in `outputs/_pre_cover_backup/`.
  Spec + plan in `docs/superpowers/`. 65 tests.

  **FOUR BUGS THAT PASSED A FULLY GREEN SUITE** — all invisible to assertions that
  check image dimensions rather than layout. This is the lesson:
  - **Pillow `Image.rotate(+N)` is COUNTER-clockwise; CSS `rotate(+Ndeg)` is CLOCKWISE.**
    Angles transcribed from the CSS mockup made the whole stack fan backwards.
    Negate at the Pillow boundary; keep the constants matching the design reference.
  - **A badge ran off-canvas on 10 of 21 SKUs.** Pillow SILENTLY CLIPS a paste box past
    the edge — no exception, image dimensions unchanged. Same hardcoded-width bug class
    already logged four times in this file. `fit_text` measures before drawing; `_badge`
    bypassed it. Now clamped, with a test scanning the right edge for badge ink.
  - **`_letter_crop` amputated the badge on all 20 badged covers and clipped 6 titles**,
    including the $29.99 flagship, which shipped reading "Claude AI Library" / "BEST VALU".
    Cause: a square render centre-cropped to Letter drops 227px per side, exactly the band
    the layout uses for its right margin. NEVER crop a composed layout to a new aspect —
    render natively at that aspect. `_render_portrait` is parametric on (w, h); adding
    `'letter'` to SHAPES was the whole fix. Per-task review could not see this: one task
    verified the layout, another verified the crop arithmetic, nobody composed them.
  - **Book proportions distorted in `wide` and `pin`** because spine WIDTH came from box
    width and HEIGHT from box height, so any box that was not the square's aspect stretched
    them. Two attempted fixes each regressed 4 SKUs (3 of them live) because the stack box
    height varies per SKU with the title block. Settled by restoring the original formulas
    and clamping BOOK ASPECT at 1.55 — never fires in square (max observed 1.47), fires
    only in wide/pin. **Verify a layout change against EVERY SKU, not the one you looked at.**

  **The cover page is deliberately a rasterised image with zero text spans.** One renderer
  draws both the PDF cover and the listing image, so they cannot drift, and the four
  cover-text-overflow bugs in this log become structurally impossible. `audit_pdfs.py`
  was changed accordingly: a page with no text is only blank if it also has no images.
  - `covers/catalogue.py` `PREFIX_PALETTE` FAILS CLOSED on an unknown filename prefix.
    `ChatGPT_` -> gpt and `Grok_` -> grok are pre-registered; without this a new series
    would have rendered silently in Claude orange.
  - **NOT DONE — blocks publishing, not merging:** `etsypub` can update a listing's PDF
    (`--update-files`) but has NO path to replace listing IMAGES on an already-published
    listing (upload is gated behind a sticky `images_done` flag). Nothing consumes
    `05_wide.png` yet either. Publishing as-is would ship new covers inside the PDFs
    behind the OLD thumbnails. Needs `--update-images` first.
  - **Also open:** `rebuild_covers.splice()` writes via `os.replace` BEFORE `_verify` runs,
    so a failing SKU leaves a spliced-but-unverified file with no rollback to the backup.

- 2026-06-25: Series planned, Guide 01 (Web) completed
- 2026-06-25: CLAUDE.md created, 20-guide series mapped
- 2026-06-25: Guides 01–07 completed (Volumes 1–2 partial)
- 2026-06-25: Guides 08–18 completed (Volumes 2–4 complete, Volume 5 partial)
- 2026-06-26: Guides 19–20 completed — ALL 20 GUIDES DONE
- 2026-07-14: Guide 21 (Multi-Agent Orchestration) added — first Volume 6 advanced add-on.
  Builds on Guide 12 (Subagents) + 13 (Agentic Loops). Covers subagents vs Agent Teams vs
  Workflows, parallel/pipeline/delegate primitives, coordination patterns (adversarial verify,
  judge panel, loop-until-dry, multi-modal sweep, completeness critic), custom agent
  frontmatter, Dynamic Workflows (June 2026), worktree isolation. Facts web-verified.
  CTA points to planned Guide 22. Note: header badge widened to 150pt for "GUIDE 21 — ADVANCED ADD-ON".
- 2026-07-14: Guide 22 (Evaluating & Testing Claude Agents) built. Covers eval loop
  (Collect/Run/Grade/Compare), 3 quality axes (task completion/tool use/planning), gold sets,
  grading methods (exact/code/LLM-judge/human), judge prompt + biases (position/verbosity/
  self-preference/rubric-drift), validate judge vs gold set, Console Evals/Promptfoo/DeepEval,
  CI thresholds, promptfooconfig.yaml example. Facts web-verified. CTA -> planned Guide 23.
- 2026-07-14: FREE lead magnet built — build_start_here.py -> Claude_Field_Guide_00_Start_Here.pdf
  (2 pages). Page 1 = "Choose Your Path" (4 color-coded pathways). Page 2 = full 22-guide library
  map (6 volumes, two columns) + bundles table. Use as free Etsy/Gumroad listing to drive bundle
  sales. Uses vol_block() helper (not in the standard helper set). Model IDs current as of build.
- 2026-07-14: Guide 23 (Claude Cost & Token Management) built. Covers token billing (input/output),
  2026 price table (Haiku 4.5 $1/$5, Sonnet 4.6 $3/$15, Opus 4.8 $5/$25, cache hit ~10%, Batch 50%),
  4 cost drivers, prompt caching (cache_control ephemeral, 90% off), Batch API, model routing,
  context growth table + /compact, budgeting (/cost, /status, --max-turns, count_tokens, Console
  limits), cost-estimate table. Pricing web-verified July 2026. CTA -> planned Guide 24.
  NOTE: watch drawString overflow on long caption lines — split the price-table footnote onto
  two lines (a single line ran off the right margin on first build).
- 2026-07-14: Start Here roadmap updated to 23 guides (Volume 6 now lists 21/22/23).
- 2026-07-28: PACKAGING PASS. Built `build_volumes.py` (7 compiled volume PDFs incl. a
  140-page Complete Library), `build_prompt_vault.py` + `prompt_vault_data.py` (200
  prompts, PDF+md+txt), `build_config_pack.py` (32 template files + zip + guide),
  `build_etsy_kit.py` (15 mockups + listing copy). Reason: 6-page PDFs at $7–15 lose to
  100+ page competitor bundles, and the individual guides duplicate free Anthropic docs.
  Templates and prompt packs are what this category actually pays for.
- 2026-07-28: BUG FIXED in `build_guide01.py` `page2()` — `drawString(MX, y - 44, line)`
  inside a loop that also did `y -= 17` left `y` 44pt above the last baseline, so the
  "What You'll Learn" heading overlapped the intro paragraph. Now `y -= 44` before the
  loop, `drawString(MX, y, line)` inside it. Grepped every build script; this was the
  only occurrence. NEVER offset the baseline inside a wrap loop that also moves `y`.

- 2026-07-30: VOLUME COVER LAYOUT FIXED in `build_volumes.py` `volume_cover()`. The cover
  was top-anchored — every block flowed down from `y = H - 210` and the "What's Inside"
  panel was sized to its content (`ph = rows*lh + 44`), so whatever was left over fell to
  the bottom as bare background. On the 3-guide volumes (5 and 6) that was ~300pt, about a
  third of the cover, and the first thing an Etsy thumbnail shows. Now there is an explicit
  bottom-up budget (`BAR_H` / `VALUE_GAP` / `VALUE_H` / `PANEL_GAP`) and the panel absorbs
  the slack, so a 3-guide and a 23-guide volume both reach the bottom. Added: guide entries
  in the non-compact (<=8) path are row cards that divide the panel evenly and carry their
  `BLURB` line; a value strip above the bottom bar. The compact (>8) two-column path was
  already filling and only got even distribution. NEVER size that panel to its content —
  that is what caused this.
- 2026-07-30: ETSY PUBLISHING. Built `etsypub/` — publishes the six volume PDFs to Etsy as
  digital instant-download listings via the **Etsy Open API v3**. Asked to reuse the
  TShirt1 mechanism; it could not be reused verbatim, because `TShirt1\pod-pipeline`
  reaches Etsy *through Printify* and Printify has no concept of a digital download.
  The architecture was ported instead: SQLite state per SKU, remote id recorded before
  any upload (the fix for that project's 44 ghost listings), `--status` reconciling
  against what Etsy actually holds rather than local state, pre-flight guards for the
  two Etsy quirks it learned the hard way (no title starting with punctuation; an empty
  description is accepted and then silently never published), and paced batches.
  KEY PROPERTY: **drafts are free, only activation is billed** ($0.20/listing), so
  `publish` builds drafts and `publish --activate` is a separate, confirmed step.
  Listing copy has one source — `build_etsy_kit.SKUS`, now carrying a `volume` key on
  the six volume SKUs. Added SKUs 06–09 for Volumes 2, 4, 5, 6 (1 and 3 already existed).
  Requires `requests` (installed) and a registered Etsy app — see `etsypub/README.md`.
  NOTE: **Etsy's app registration form rejects an `http://` callback** — it demands
  `https://`. There is no TLS cert on localhost and a self-signed one only trades the
  problem for a browser warning, so `oauth.py` switches on the scheme: `http` = catch the
  redirect on a local listener, `https` = print instructions and take the redirect URL
  pasted back. Safe because PKCE keeps the code useless without the in-process verifier.
  Default `ETSY_REDIRECT_URI` is now `https://localhost:3003/oauth/redirect`.
- 2026-07-31: Etsy app approved (application_id 1503425050780). Two things learned by
  testing rather than reading: **the `x-api-key` header must be `keystring:shared_secret`,
  not the bare keystring** (which returns 403 "Shared secret is required in x-api-key
  header"), so the shared secret IS required despite PKCE; and `GET /openapi-ping` needs
  only that header, no OAuth, which makes it the cheapest way to tell "app not approved
  yet" apart from "OAuth flow is wrong". Added `config.api_key()`,
  `Etsy.ping()` and `python -m etsypub.publish --preflight`.

### KNOWN FACTUAL ERRORS — ALL FIXED 2026-07-30 (re-verified vs code.claude.com/docs)
- ~~Guides 12 & 13 say a hook blocks on exit 1~~ → now **exit 2**. Confirmed against the
  docs: 0 = success, 2 = blocking (stderr fed back to Claude), any other code including 1
  = NON-blocking, execution continues. Guide 12 now lists exit 1 as its own row.
- ~~Guide 12's "8 hook events" presented as the complete list~~ → docs list **30 events**.
  Reframed as "The 8 Core Hook Lifecycle Events" with the page subtitle stating 30+ exist.
  `StopFailure` corrected: it fires when the turn ends from an **API error**, nothing more.
- ~~Guide 12's ESLint hook used `${file}`~~ → hooks get JSON on **stdin**; now uses
  `jq -r '.tool_input.file_path' | xargs`. There is no `$CLAUDE_FILE_PATHS`;
  `CLAUDE_PROJECT_DIR` does exist.
- ~~Guide 15 teaches `@modelcontextprotocol/server-github` / `-brave-search`~~ → both
  deprecated and archived. GitHub moved to `ghcr.io/github/github-mcp-server`
  (repo `github/github-mcp-server`, hosted endpoint api.githubcopilot.com/mcp/);
  Brave moved to `@brave/brave-search-mcp-server`. `server-filesystem` is still current.
- ~~Guide 15 promises a Brave free tier of 2,000 queries/month~~ → **the free tier was
  retired 12 Feb 2026**. All plans are metered (~$5/1,000 queries) with a $5/month credit
  only if you attribute Brave Search. This one would have actively misled a buyer.
- ~~"GUIDE XX OF 20" badges~~ → all now "OF 23", plus cover footers and CTAs.
  Guide 20's "SERIES FINALE" removed (21–23 follow it).

- 2026-08-01: **SHOP URL CTA FIX.** Every guide's page-6 "Next in the Series" panel and
  cover bar read "Available at claude.ai" — Anthropic's site, where these guides are NOT
  sold. It was inaccurate and pointed paying customers away from the shop. Swept 5 exact
  seller-CTA strings (43 instances across all 23 build scripts) to
  `etsy.com/shop/FranksMarketDesigns`. **Shop name verified via the API first — it ends in
  "s"**; the requested spelling omitted it and would have baked a dead URL into every PDF.
  CRITICAL: the ~50 OTHER `claude.ai` references are teaching content about Anthropic's
  product ("Navigate to claude.ai", "claude.ai/pricing", "claude.ai/download") and must
  NEVER be swept — only replace the 5 exact CTA strings.
  Rebuilt all guides + volumes, audit clean (0 issues), then pushed the corrected PDFs to
  the 6 live listings with `python -m etsypub.publish --update-files`.
- 2026-08-01: Volumes 1–6 ACTIVE on Etsy (FranksMarketDesigns, shop 36996679). Listing ids
  4548067194 / 4548053179 / 4548053233 / 4548053309 / 4548053363 / 4548067558.
  `--update-files` uploads the new PDF BEFORE deleting the old one — Etsy deactivates a
  digital listing left with no file, and a buyer mid-purchase would hit a broken download.
  `--status` now reconciles local state against Etsy (activating from the dashboard used
  to leave the db claiming "draft" forever).
- **DECIDED: the 23 individual guides will NOT be listed separately.** They are inputs,
  not SKUs (see the 2026-07-28 packaging note). The in-guide "Next in the Series" pointers
  are not dead ends — they resolve to content inside the next VOLUME, so they work as
  cross-sell. Still unlisted and built: Complete Library ($29.99, the SKU that actually
  delivers the advertised 23 guides), Prompt Vault ($8.99), Config Pack ($14.99).

- 2026-08-01: **TWO NEW PRODUCTS, LIVE.** See `IDEAS.md` for the full backlog.
  - `build_cheatsheets.py` + `cheatsheet_data.py` -> `Claude_Cheat_Sheet_Pack.pdf`
    (13pp, $6.99, listing 4548222295). **Deliberately a LIGHT theme** — the house dark
    #0F0F1A is the wrong choice for something meant to be printed. Single wide column,
    not two: two columns squeezed the value field to ~34 chars, which would have meant
    gutting content to fit the layout. Two guards hard-fail the build —
    `verify_no_overflow()` and `verify_fits_one_page()`. One sheet per page IS the promise.
  - `build_cost_calculator.py` -> `AI_Cost_Calculator.xlsx` (3 sheets, $7.99, listing
    4548222363) + `AI_Cost_Calculator_Preview.pdf` (mockup source only). Every figure is
    a LIVE FORMULA referencing the editable Rates tab, so the product does not rot when
    vendors move pricing. openpyxl writes formulas but never evaluates them — the maths
    was re-implemented independently in Python and cross-checked before shipping.
- 2026-08-01: `etsypub` extended for non-volume products: `--skus <name,...>` selector,
  and a `files` key on a SKU separating **what the buyer downloads** from the `pdf` used
  as the mockup source. The calculator would otherwise have shipped its sales preview
  instead of the spreadsheet. `upload_file` now sets MIME by extension.
  Fixed: `db.ensure` assumed a `volume` key; `listing_images` GET is listing-scoped, not
  shop-scoped (uploads are shop-scoped — the two paths differ).
- 2026-08-01: **Gumroad CAN create products via API — the docs are wrong.** Public docs
  and community posts all say `POST /v2/products` returns 404 / "creation is
  dashboard-only". Tested against this account: it returns **200 and creates the product**
  (test artifact deleted immediately; store verified back to 0). A full `gumroadpub`
  publisher mirroring `etsypub` is therefore possible. Account: Thomas Sromovski,
  sromov.gumroad.com. Auth is a simple `access_token` query param — no OAuth dance.
  LESSON, third time this session: verify against the live API, never trust the docs.
  (The other two: `x-api-key` needs `keystring:shared_secret`, and Etsy's listing-images
  GET is listing-scoped while the upload is shop-scoped.)
- 2026-08-01: `fieldguide/` package created — `theme.py` (CLAUDE / COPILOT / CODEX
  palettes) + `draw.py` (`Painter`, same geometry as the shipped design system). Smoke
  tested in all three themes. **The 23 shipped Claude guide scripts are deliberately NOT
  retrofitted onto it** — they are correct, audited and selling; rewriting them risks live
  products to buy nothing. This exists so Copilot/Codex are not a third copy-paste.
- 2026-08-01: Complete Library LIVE on Etsy — $29.99, listing 4548260666.
- 2026-08-01: `gumroadpub/` built. The full file-attach contract, which no public doc
  covers, came out of the API's own error message:
      POST /v2/files/presign {filename, file_size, content_type}
        -> {upload_id, key, file_url, parts:[{part_number, presigned_url}]}
      PUT each part to its presigned_url, keep the ETag header
      POST /v2/files/complete {upload_id, key, parts:[{part_number, etag}]}
      PUT /v2/products/:id  files[][url] (+ optional files[][name])
  **`files` is a FULL REPLACEMENT** — anything omitted is removed from the product.
  **Covers take a PUBLIC image url**, and reject the S3 url the presign flow returns.
  Solution: pull the mockup urls from the matching Etsy listing (`url_fullxfull`), which
  are already publicly hosted. A SKU with no Etsy listing gets no cover.
  Gumroad names use the Etsy title's first segment — the 140-char keyword-stuffed Etsy
  title reads as spam on a personal storefront.
- 2026-08-01: **GUMROAD CAPS PRODUCT CREATION AT 10/DAY, AND DELETED PRODUCTS STILL
  COUNT.** Eight throwaway probe products (all deleted immediately) ate most of the
  day's allowance, so only 2 of 11 real products were created — the other 9 hit
  "you can only create 10 products per day". Probe with ONE product and reuse it.
  `gumroadpub.publish` is resumable: re-running skips anything with a product_id, so
  the remaining 9 need only `python -m gumroadpub.publish` tomorrow.
- 2026-08-01: **SCHEDULED — Windows Task "Gumroad Finish Load", 2026-08-02 10:00**, runs
  `scripts\gumroad_finish.bat` -> `python -m gumroadpub.publish --finish`, logging to
  `logs\gumroad.log`. `--finish` is three gated steps: create whatever is missing ->
  verify every product -> publish only those that pass. **A product with no file attached
  is never published** — a live Gumroad product that delivers nothing is worse than no
  product. Safe to re-run: creation skips anything already made, publishing an already
  published product is a no-op. Delete with
  `schtasks /Delete /TN "Gumroad Finish Load" /F`.

- 2026-08-02: **COPILOT VOLUME 1 BUILT** — `build_copilot_v1.py` ->
  `Copilot_Field_Guide_Volume_1_Getting_Started.pdf`, 24pp, audit clean. First product on
  the `fieldguide/` engine, and written at VOLUME scale (5 chapters in one document, no
  per-chapter covers) — the whole point of the refactor.
  Added `fieldguide/volume.py`: `Volume` handles cover, contents, running footers and page
  numbering, so Codex gets all of it free. Cover panel STRETCHES to the value strip rather
  than sizing to content — the fix already learned on the Claude covers.
  Facts verified against docs.github.com 2026-08-02: 1 AI Credit = $0.01; Free = 2,000
  completions + 50 chat requests; Pro $10 = 1,000 base + 500 flex = 1,500 credits;
  Pro+ $39 = 7,000; Max $100 = 20,000. **Completions and Next Edit Suggestions are NEVER
  metered on paid plans**; chat, agent mode, CLI, cloud agent, Spaces, Spark and code
  review all draw on credits. Overage is opt-in against a self-set budget.
  A web search claimed "Pro includes $15 in credits" — half right, and only resolvable at
  the source: 1,000 base + 500 flex happens to equal $15. ALL pricing is confined to ONE
  table on ONE page so a reprint is a single edit.
- 2026-08-02: **PAGE-FILL IS NOW A MEASURED STANDARD.** First Copilot build averaged 57%
  vertical fill against the shipped Claude volumes' 68-73% — every page was visibly airy.
  Measure with the fill script (max text y / 760) rather than eyeballing; content was
  added, not pages merged, because page count is what the product is sold on. Now 69%
  average, 60% minimum. **Check fill on every new volume before shipping.**
  Also generalised `audit_pdfs.py`: `_is_bar_content` matched series-specific PHRASES and
  flagged all 23 Copilot footers as errors. Now structural — left-aligned at MX, or
  right-aligned "Page N", or centred in a cover bar. Takes a path argument now too.

- 2026-08-02: **COPILOT VOLUME 2 BUILT** — `build_copilot_v2.py` ->
  `Copilot_Field_Guide_Volume_2_Chat_and_Agents.pdf`, 26pp, audit clean, 68% fill.
  Chapters: the three modes (ask/edit/agent) · slash commands, participants and #
  references · agent mode · reviewing multi-file changes · getting good results.
  Facts verified against code.visualstudio.com/docs/copilot 2026-08-02. Current surface
  is much larger than older write-ups suggest: participants are `@github` `@terminal`
  `@vscode`; context is namespaced (`#read/` `#search/` `#edit/` `#execute/` `#web`
  `#browser` `#agent` `#todos`) plus `#selection` `#changes` `#session` `#<file>`;
  shortcuts Ctrl+Alt+I chat, Ctrl+I inline, Ctrl+Shift+I agents, Ctrl+Shift+Alt+L quick,
  Ctrl+N new session. `/yolo` and `/autoApprove` enable GLOBAL tool auto-approval
  (`/disableYolo` reverses it) — treated as a safety topic, not a convenience feature,
  because it auto-approves shell commands.
  **Both Copilot volumes came in at ~56% fill on the first build and needed content added
  to reach house standard.** That is now a predictable step, not a surprise: write the
  chapters, measure fill, then add a real block to every page under 60%. Do not merge
  pages to fix it — page count is what the product is sold on.
- 2026-08-02: Gumroad "10 per day" is a **ROLLING 24-HOUR WINDOW, not a calendar-day
  reset** — the 10:00 run still hit the cap from the previous evening's creations. Task
  changed from once-daily to **every 4 hours** (`schtasks /Change /RI 240`), so it catches
  the window whenever it clears and no-ops once everything exists. The 2 existing products
  did publish: prompt-vault and cheat-sheet-pack are LIVE on sromov.gumroad.com.

- 2026-08-02: **START HERE LEAD MAGNET FIXED**, queued for Gumroad at $0.00 (SKU
  `12-start-here`; Gumroad-only — Etsy has no free listing tier). It had two defects that
  made it actively harmful: the CTA said "grab your first guide today" and **named no
  shop at all**, and the bundle table advertised a **"$79 Complete Library, Guides 01-20"
  that has never existed** — the real product is $29.99 and covers 23 guides. It also said
  guides were "sold separately", which was decided against. Table rebuilt from live
  prices, shop URL added, hardcoded badge width fixed (same bug class as guide 20).
  **Check the prices in this file whenever a product price changes** — it is the one
  document that quotes the whole catalogue.
- 2026-08-02: `gumroadpub.verify` rejected any zero-price product, which would have kept
  the free lead magnet a draft forever. Now a zero price is only a defect when the SKU is
  not deliberately free (`price` of `$0.00` in `build_etsy_kit.SKUS`).
- 2026-08-02: `audit_pdfs.py` bottom-bar check now tests the LINE box, not the span box.
  PyMuPDF splits a line into spans at font changes, so a trailing glyph (the `→` on Start
  Here page 1) was its own span sitting right of centre and got flagged even though its
  line was centred in the bar.

- 2026-08-02: **COPILOT VOLUME 3 BUILT** — `build_copilot_v3.py` ->
  `Copilot_Field_Guide_Volume_3_CLI_and_Coding_Agent.pdf`, 26pp, audit clean, 67% fill.
  Chapters: the CLI · the cloud coding agent · handing it work · the pull request ·
  review and guardrails.
  Facts verified against docs.github.com/copilot 2026-08-02 — the cloud agent's documented
  HARD limits are load-bearing content: **59 minutes maximum, one repository per session,
  one branch, one pull request, GitHub-hosted repos only**, and **its PRs require human
  approval before any CI/CD runs**. Available on all paid plans; admin must enable on
  Business/Enterprise. Started five ways (assign an issue · agents panel · VS Code ·
  `@copilot` in a PR comment · automated workflows). Steer mid-run by mentioning
  `@copilot` in a comment. Rulesets can block it — Copilot can be added as a bypass actor.
  The volume's spine is the FIVE ISSUE HEADINGS (problem / expected / where / how to
  verify / out of scope), because the issue IS the prompt and nobody is watching.
- 2026-08-02: **PAGE FILL: all three Copilot volumes came in at 56-57% on first build.**
  This is now established, not a coincidence — the design system is airier than a
  per-page content estimate suggests, by roughly 20%. Plan for the fill pass as part of
  building a volume, not as a fix. Sequence: write chapters -> measure -> add a real
  block to every page under 60% -> re-measure. Never merge pages.

- 2026-08-02: **COPILOT VOLUME 4 BUILT** — `build_copilot_v4.py` ->
  `Copilot_Field_Guide_Volume_4_Customisation.pdf`, 26pp, audit clean, 66% fill.
  Chapters: instruction files · prompt files · custom agents & skills · MCP & hooks ·
  rolling it out.
  Facts verified against code.visualstudio.com/docs/copilot/customization 2026-08-02.
  Seven customisation types with exact conventions: `.github/copilot-instructions.md`
  (always-on) · `*.instructions.md` in `.github/instructions/` with frontmatter
  `applyTo` / `name` / `description` · `AGENTS.md` at root · `*.prompt.md` (becomes a
  slash command) · `*.agent.md` (role with its own tools and model) · `SKILL.md` ·
  MCP servers · hooks · agent plugins (preview).
  **Precedence: personal > repository > organization** — all are supplied, higher wins a
  conflict. Worth knowing before debugging why a teammate gets different suggestions.
  **CROSS-SERIES: VS Code Copilot also reads `CLAUDE.md`** (using `paths` rather than
  `applyTo`), so a repo configured for Claude Code is partly configured for Copilot. Good
  hook for a future cross-tool product — see IDEAS.md 2b and 3.
  V4 came in at 60% first pass rather than the usual 56-57%, because the content is
  table-heavy. Still needed a fill pass on ten pages.
- 2026-08-02 14:00: Gumroad retry #2 — still capped. Rolling window from the 2026-08-01
  probe products has not cleared. Task continues every 4 hours; nothing to fix.

- 2026-08-02: **COPILOT SERIES COMPLETE — 5 VOLUMES, 128 PAGES, ALL AUDIT CLEAN.**
  V1 Getting Started 24pp/69% · V2 Chat & Agent Mode 26pp/68% · V3 CLI & Coding Agent
  26pp/67% · V4 Customisation 26pp/66% · V5 Credits, Cost & Teams 26pp/67%.
  All built on `fieldguide/` (theme + Painter + Volume). Nothing was copy-pasted from the
  Claude scripts, which was the entire point of the refactor.
  V5 facts verified against docs.github.com billing docs 2026-08-02:
  **org credits are POOLED at the billing entity level** (do not police individuals —
  watch the pool); Business 1,900/user/month and Enterprise 3,900, with a **promotional
  3,000 / 7,000 that ENDS 1 SEPT 2026** — a ~40% cliff worth warning buyers about;
  **unused credits do NOT carry over**; **additional usage is ENABLED BY DEFAULT for
  organizations** (opt-in for individuals — the asymmetry that surprises people);
  budgets exist at four levels (user · cost centre · organization · enterprise).
  **GitHub does NOT publish Business/Enterprise per-seat prices** on the public plans
  page — V5 deliberately prints the documented credit allocations instead of a
  widely-quoted seat price that could not be verified. Do not add one on reprint.
## UNATTENDED PUBLISHING — READ THIS FIRST (set up 2026-08-02, owner away until 08-08)

`publish_all.py` drives BOTH channels to a complete, published catalogue, and is
scheduled as Windows Task **"Publish All Products"** — every 4 hours for 7 days
(`PT4H` / `P7D`), running `scripts\publish_all.bat`, logging to `logs\publish_all.log`.

It exists because **Gumroad caps product creation at 10 per ROLLING 24 hours**, so the
catalogue physically cannot be loaded in one sitting. The job converges instead of
needing a person to retry it. Every stage is idempotent, resumable and gated: anything
already live is skipped, a failed stage does not block the other channel, and **nothing
is published without its file attached**.

- `python publish_all.py --dry-run` — what it would do, no network, no cost
- `python publish_all.py --etsy-only` / `--gumroad-only`
- Etsy costs $0.20 per activated listing. Gumroad costs nothing.
- `12-start-here` is excluded from Etsy — it is free and Etsy has no free tier.

**CRITICAL FIX 2026-08-02 16:10 — the create loop now STOPS on the first quota or
rate-limit refusal** instead of walking the whole SKU list. It was attempting all 21
products every pass; ~19 of those calls could not possibly succeed, and that turned a
polite "only 10 per day" into hard **429: Retry later** responses. Unattended for a week
that would have hammered the API six times a day for nothing. A blocked pass is now 2
calls, not 21. Jitter between creates raised to 5-12s for the same reason.
**Rule: when an API says you are over a limit, stop the pass — do not iterate into it.**

**GOTCHA THAT COST TIME: .bat files need CRLF line endings.** Written with LF only,
cmd.exe misparses every `REM` and emits "'M' is not recognized". The script still ran, so
the failure was invisible in the log. If a scheduled batch behaves oddly, check the line
endings first.

- 2026-08-02: **ETSY IS COMPLETE — 16 products live.** Added 01-prompt-vault and
  05-config-pack (which also fixes their missing Gumroad covers, since covers are pulled
  from the Etsy listing images) plus all five Copilot volumes. $1.40 in listing fees.
- Copilot SKUs 20-24 added to `build_etsy_kit.SKUS`. Product names deliberately do NOT
  lead with "GitHub Copilot" and every description carries the not-affiliated line.
- 2026-08-02: **CODEX SERIES COMPLETE — 4 VOLUMES, 104 PAGES, ALL AUDIT CLEAN, ALL LIVE
  ON ETSY.** V1 Getting Started 26pp/62% · V2 The CLI 26pp/65% · V3 AGENTS.md, Subagents
  & MCP 26pp/64% · V4 Delegation, Review & Cost 26pp/63%. SKUs 30-33.
  Facts verified against learn.chatgpt.com/docs 2026-08-02: install via
  chatgpt.com/codex/install.sh · `/permissions` `/init` `/status` `/model` `/review` ·
  `codex resume` `codex exec` `codex mcp` · **usage limits are a 5-HOUR ROLLING WINDOW**
  (not daily/monthly — the thing people from other tools get wrong first) ·
  per-message pricing retired 2 Apr 2026, now token-based credits · Pro 5x added
  9 Apr 2026, old $200 Pro renamed Pro 20x · **cloud delegation starts at PLUS**, Go is
  local-only. AGENTS.md is plain markdown, hierarchical, CLOSEST FILE WINS, explicit
  prompt overrides all. Subagents are TOML in `~/.codex/agents/` or `.codex/agents/`,
  required `name` / `description` / `developer_instructions`, USER-TRIGGERED, and they
  INHERIT the parent sandbox and permission mode.
  **DELIBERATE GAP IN V4:** OpenAI's cloud-task doc pages were not publicly fetchable, so
  V4 states no specifics about the remote environment, PR-opening behaviour or runtime
  limits. Do not add them on reprint without a verified source — an invented limit is
  worse than an acknowledged gap, and the volume says so to the reader.
- **ETSY NOW 20 PRODUCTS.** Claude (6 volumes + library + vault + config pack + cheat
  sheets + calculator), Copilot (5), Codex (4).
- Anything added to `build_etsy_kit.SKUS` is picked up by the scheduled job
  automatically — adding a SKU is the same as scheduling its publication.

- **NEXT FOR COPILOT:** a volume compilation if the five should also sell as one book
  (`build_volumes.py` already handles that pattern).

### PDF AUDIT (`audit_pdfs.py` in the project root — rerun before any reprint)
Checks the mechanical faults an eye misses over 140 pages: text past the right/left
margin, text colliding with the 22pt footer bar, overlapping spans, blank pages. Found
**33 real issues** on 2026-07-30; all fixed. The only remaining hits are the cover
tagline inside the orange bottom bar on page 1 of each volume — a false positive.
Fixes applied:
- `build_guide06.py` page3 — the Homebrew curl one-liner ran ~50pt past the right margin
  and off the paper (now split on a `\` continuation); the "Then restart Terminal"
  caption sat on the code block's bottom border (gap 6 -> 16); the tip box ran under the
  footer (gaps tightened, card text trimmed).
- `build_guide12.py` page4 — Example 1 carried a full settings.json wrapper the other two
  examples omit, pushing the tip box off the page. Now a fragment like the others.
- `build_guide20.py` page3 — **the caller ignored `tbl()`'s return value** and hardcoded
  an offset 36pt taller than the table, which was most of a ~120pt overrun. Use the
  return value. Descriptions and code blocks also trimmed.
- `build_guide20.py` page5 — 5 categories x 6 templates at 18pt/28pt came to exactly the
  full 710pt content height, so the last row landed under the footer. Now 17pt/24pt.
  (All 30 templates verified to fit on one line — `page5` silently drops any wrapped
  remainder, so a longer template would be truncated mid-sentence with no error.)
- **Cover badge width was hardcoded (`bw, bh2 = 114, 22`) while the label was drawn
  CENTRED on it** — any longer label spilled out both sides, which is why guide 20's
  badge started 28pt left of the page margin. All 23 now derive `bw` from
  `c.stringWidth(...) + 24`. Never hardcode that width again.

- Design system locked to dark/orange aesthetic from Guide 01
- Decided NOT to include actual screenshots (copyright risk) — describe UI in text
- Output path is `C:\Projects\UserGuide\outputs\` (Windows local, not /mnt/)
- All guides are 6 pages (cover + 5 content) — consistent page count across series
- reportlab canvas API used (not Platypus) for full layout control
- simpleSplit used for all body text wrapping — never drawString raw long text
- Code block lh=13 (established from Guide 12 onward); earlier guides used lh=14
- roundRect() requires radius= keyword arg in reportlab 5.0 — always pass it explicitly
- Web search run before every guide to verify pricing, model IDs, feature availability
