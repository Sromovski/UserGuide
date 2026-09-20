# COPILOT & CODEX FIELD GUIDE SERIES — BUILD PLAN
# Companion series to the Claude AI Field Guide
# Drafted 2026-08-01

---

## THE ONE LESSON TO CARRY OVER

The Claude series was built as 23 six-page guides, then repackaged into 6 volumes when it
became clear the individual guides were not saleable — buyers scan page count first, and a
6-page PDF loses to a 100-page competitor bundle. Roughly a month of work produced inputs,
not SKUs.

**Do not repeat that. Write at volume scale from the first line.** The unit of work is a
20–32 page volume, not a 6-page guide. Chapters inside a volume replace "guides"; there is
no standalone-chapter product and no per-chapter cover page.

Second lesson, from `outputs/etsy/LISTINGS.md`: the asset products (Prompt Vault, Config
Pack) are where willingness-to-pay actually is. Prose explains; templates get bought.
Plan the asset product **alongside** each series, not as an afterthought.

---

## THE UNCOMFORTABLE PART — READ BEFORE COMMITTING

Both of these are **developer products**. The Claude listing kit already grades its own
developer volumes as *"LOW on Etsy, HIGH on Gumroad — developers do not browse Etsy for
tooling."* Copilot and Codex are 100% that category; there is no "Claude on your phone"
equivalent to pull in a non-technical Etsy buyer.

So: building 9 more volumes aimed at Etsy would likely underperform the Claude series,
which itself leans on Volumes 1 and 5 for its Etsy appeal.

**Recommendation: build these with Gumroad as the primary channel and Etsy as secondary.**
That changes what to optimise — Gumroad rewards depth, bundles and developer credibility;
Etsy rewards a scannable first image and a beginner promise. Same PDFs, different framing
and different price points ($19–39 works on Gumroad where $9.99 is the Etsy ceiling).

If Etsy has to be primary, cut the scope hard: one beginner volume per brand plus the
asset pack, and see whether either sells before building the rest.

---

## TRADEMARK & POSITIONING (settle this before writing)

Naming a product your guide is about is normally fine; implying endorsement is not.

- **No logos, no Octocat, no OpenAI marks, no GitHub/Microsoft/OpenAI branding.** The
  Claude series already avoids screenshots for the same reason — keep that rule.
- **Do not use "GitHub Copilot" or "OpenAI Codex" as the leading words of the product
  name.** Prefer *"The Unofficial Field Guide to GitHub Copilot"*.
- **Put a disclaimer on the cover and in every Etsy/Gumroad description:**
  *"Unofficial and independent. Not affiliated with, endorsed by, or sponsored by GitHub,
  Microsoft or OpenAI."*
- Etsy's Aug-2026 original-artwork rule already applies to this shop — the design system
  is original, keep it that way.

---

## DESIGN SYSTEM — SHARED SKELETON, DISTINCT SKIN

Reuse the entire layout engine from the Claude series verbatim: Letter page, `MX` margins,
`step_card` / `info_panel` / `tip_box` / `warn_box` / `code_block` / `tbl`, the volume
cover budget (`BAR_H` / `VALUE_GAP` / `VALUE_H` / `PANEL_GAP`), `build_volumes.py`,
`build_etsy_kit.py`, `audit_pdfs.py`, and `etsypub/`.

Only the palette changes, so the three series read as one family of products from one
publisher while remaining visibly distinct on a search grid.

```
CLAUDE   (shipped)   BG #0F0F1A   accent #E07A38 orange
COPILOT  (proposed)  BG #0D1117   accent #58A6FF blue     (GitHub-dark inspired, original)
CODEX    (proposed)  BG #0B0F0E   accent #10A37F teal
```

Everything else — CREAM/LGR/MGR text, PNL/PNL2 panels, GRN success, AMB warning, CODE_BG —
stays identical. Refactor the shared helpers into `fieldguide/theme.py` + `fieldguide/
draw.py` on first use rather than copy-pasting a third time; three copies is where the
Claude scripts' hardcoded-badge-width bug would have been fixed once instead of 23 times.

---

## SERIES 1 — GITHUB COPILOT (5 volumes, ~130 pages)

| Vol | Title | ~pp | Chapters |
|-----|-------|-----|----------|
| C1 | Getting Started with Copilot | 28 | What it is · plans & the 2026 usage-based billing model · install in VS Code / JetBrains / Visual Studio / Neovim · completions & Next Edit Suggestions · your first hour |
| C2 | Chat & Agent Mode | 28 | Copilot Chat · agent mode · slash commands · `#file` / `@workspace` context · reviewing and accepting multi-file edits |
| C3 | Copilot CLI & the Coding Agent | 26 | Terminal workflows · assigning an issue to the coding agent · the PR it opens · automated code review |
| C4 | Customisation | 26 | `copilot-instructions.md` · prompt files · custom agents · MCP servers in Copilot · extensions |
| C5 | Credits, Cost & Teams | 22 | AI credits and what consumes them · budgets & overage · Business vs Enterprise · org policy & content exclusion |

**Volatile facts — must be re-verified at build time, they moved twice in 2026:**
usage-based billing went live 1 June 2026; completions/NES stay unmetered while chat,
agent mode, code review and CLI draw on a monthly credit pool; tiers seen as Free / Pro
$10 (~$15 credits) / Pro+ $39 (~$70) / Max $100 (~$200) / Business $19 seat / Enterprise
$39 seat. **Do not hardcode these into prose without a fresh check** — put every price in
one table on one page so a reprint is a single edit.

---

## SERIES 2 — OPENAI CODEX (4 volumes, ~100 pages)

| Vol | Title | ~pp | Chapters |
|-----|-------|-----|----------|
| X1 | Getting Started with Codex | 26 | What Codex is · where it runs (web · VS Code extension · CLI · iOS) · plans Go/Plus/Pro 5x/Pro 20x · first task end to end |
| X2 | The Codex CLI | 28 | Install & auth · approval modes and the sandbox · `AGENTS.md` · MCP servers · local vs cloud execution |
| X3 | Cloud Tasks & Delegation | 24 | Background agents · parallel task execution · the PR workflow · automated code review · Slack integration |
| X4 | Advanced & Cost | 22 | API vs subscription billing · Bedrock · prompting patterns for autonomous agents · guardrails and review discipline |

**Volatile facts:** Pro tiers were renamed in April 2026 (old $200 Pro → "Pro 20x";
$100 "Pro 5x" added); Go at ~$8; cloud delegation starts at Plus; Bedrock availability
landed June 2026. Same rule — one pricing table, one page.

---

## ASSET PRODUCTS (build these first if forced to choose)

| Product | Contents | Price |
|---------|----------|-------|
| **Copilot Instructions Pack** | 8–10 `copilot-instructions.md` templates by stack, prompt-file library, custom-agent definitions, MCP configs | $14.99 |
| **AGENTS.md Pack** | 8–10 `AGENTS.md` templates by stack, sandbox/approval recipes, review checklists, MCP configs | $14.99 |
| **AI Coding Prompt Vault** | 200 prompts that work across Copilot, Codex *and* Claude — the cross-series SKU | $12.99 |

The Prompt Vault is the strongest commercial idea here: it is tool-agnostic, so it sells
to all three audiences, and prompt packs are the one thing in this category that Etsy
buyers already reach for. `prompt_vault_data.py` gives a proven single-source pattern —
copy it, keep `verify_no_overflow()`.

---

## PHASING

1. **Refactor shared code** into `fieldguide/` — theme, draw helpers, volume builder,
   etsy kit, audit. One day, and it stops the third copy-paste of the design system.
2. **AI Coding Prompt Vault.** Cross-tool, sells against all three series, no dependency
   on volatile pricing facts. Ship and measure.
3. **Copilot C1 + Copilot Instructions Pack.** Copilot has the larger and less technical
   audience of the two; C1 is the volume with any chance on Etsy.
4. **Measure before continuing.** If C1 and the packs move, build C2–C5 then the Codex
   series. If they do not, stop at the packs and put the effort into the Claude Complete
   Library, which is already built and still unlisted.

Do not build all 9 volumes before the first one has sold anything. That is precisely the
mistake the Claude series made at 23-guide scale.

---

## REUSABLE INFRASTRUCTURE — WHAT ALREADY WORKS

- `build_volumes.py` — monkeypatches each chapter module's `ftr()` for continuous page
  numbering and renders onto one canvas. Works unchanged; add a `VOLUMES` entry.
- `build_etsy_kit.py` — mockups composited from real PDF pages, with Etsy's limits
  (140-char title, exactly 13 tags, ≤20 chars each) asserted at build time.
- `audit_pdfs.py` — catches right/left margin overflow, text colliding with the footer,
  overlapping spans, blank pages. It found 33 real defects in the Claude volumes. **Run it
  before every reprint.**
- `etsypub/` — Etsy Open API v3 publisher. Drafts are free, activation is billed; state is
  reconciled against Etsy rather than trusted locally. Needs a per-brand SKU registry
  (currently reads `build_etsy_kit.SKUS` directly) — small change, worth doing at the
  refactor.
- **Gumroad has no equivalent yet.** If Gumroad becomes the primary channel, a
  `gumroadpub/` sibling is a new build — their API is simpler than Etsy's, no OAuth
  consent dance, but it is still real work. Budget for it.
