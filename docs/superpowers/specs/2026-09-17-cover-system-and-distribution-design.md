# Cover System, New Series & Distribution — Design

Date: 2026-09-17
Status: approved (brainstorm complete, ready for implementation plan)

---

## Problem

Twenty-one products are live on Gumroad and twenty on Etsy. None have sold.

The August 2026 channel review in `IDEAS.md` concluded that the catalogue is not the
constraint — distribution is. That conclusion still holds, and this design is shaped by it:
the covers and the marketing plan come first, and the two new series launch into a fixed
storefront rather than a broken one.

Three specific defects in what is live today:

1. **The cover art reads as a 2019 template.** A flat drop-shadow rectangle on flat colour.
2. **Orange-on-navy is the least differentiated palette in the AI category**, and the dark
   `#0F0F1A` house background — correct inside the PDF — sinks into Etsy's white search grid
   and Gumroad's white cards at thumbnail size.
3. **Every listing image is square.** Gumroad's storefront grid is landscape, so it is
   side-cropping all twenty-one covers today.

Beyond the art, the catalogue is almost entirely developer material (Claude Code, MCP, hooks,
CLI, API) sold into marketplaces whose shoppers are not developers. The new series and the
new product ideas below are chosen to correct that mismatch, not merely to add SKUs.

## Goal

One sale per week.

Stated plainly so it is not judged early: from a standing start, on organic traffic plus an
ad budget under $50/month, this is a **2–3 month** build, not a two-week one.

## Constraints

- Ad budget: **under $50/month** while unproven.
- Channels the owner will actually work: **Pinterest** and **Reddit / X**. Not TikTok.
- Rebuild scope: **listing images + PDF cover page**. Interiors are out of scope.
- The 23 shipped Claude build scripts are **not** retrofitted onto `fieldguide/`. This is a
  standing decision recorded in `CLAUDE.md` — those scripts are correct, audited and live, and
  rewriting them risks selling products to buy nothing. Covers are not a reason to overturn it.
- Everything continues to run through `build_etsy_kit.SKUS` as the single source of listing
  copy, and through `audit_pdfs.py` before any reprint.

---

## Section 1 — The `covers/` package

A new package that is the only thing in the project which knows what a cover looks like.

| Module | Responsibility |
|--------|----------------|
| `covers/palette.py` | The five palettes: gradient stops, title ink, muted text, three spine colours, badge fg/bg. |
| `covers/spec.py` | `CoverSpec` dataclass — title lines, subtitle, up to three spine labels, badge text, footer, palette key, `kind`. |
| `covers/catalogue.py` | Derives a `CoverSpec` from each entry in `build_etsy_kit.SKUS`. |
| `covers/render.py` | One Pillow renderer producing three shapes from a `CoverSpec`. |

### Visual specification — direction C

Approved from `outputs/design/cover-system.html`, which is the visual reference for
implementation.

```
Soft vertical gradient background (three stops, light/warm per palette)
  centred title, 2 lines, ~800 weight, tight tracking (-0.03em)
  centred subtitle line: "5 guides · 32 pages · instant download"
  stage:
    three angled book spines, rotated -8deg / -2deg / +6deg,
    z-order back-left, back-right, front-centre
    each spine: solid palette colour, dark gradient strip down the left edge,
    white title text, one short white rule
    real gaussian drop shadow, offset down-left
    badge: rounded pill, rotated +6deg, top-right of the stage
  centred footer strip: "INSTANT PDF DOWNLOAD", letterspaced, uppercase
```

`kind` controls the stack only:

- `bundle` — three spines. Signals quantity. Used by volumes, the Complete Library, packs.
- `single` — one spine, centred, rotated -3deg. Used by the Prompt Vault, Cost Calculator,
  Config Pack, Start Here.

Nothing else in the layout changes between the two.

### Palettes

| Key | Background | Accent spine | Used by |
|-----|-----------|--------------|---------|
| `claude` | warm cream | ember `#E2542B` | Claude volumes, library, vault, config pack, cheat sheets, calculator, start here |
| `copilot` | cool grey | indigo `#4F46E5` | Copilot V1–V5 |
| `codex` | sea glass | jade `#0F9D74` | Codex V1–V4 |
| `gpt` | mint | signal green `#10A37F` | ChatGPT series (new) |
| `grok` | steel | cyan `#00B8D9` | Grok series (new) |

All five are **light**. This is deliberate and is a reversal of the house dark style for
cover art only: a light cover holds its edges against Etsy's white grid, a dark one does not.
The interiors stay dark.

No vendor logos, wordmarks or icons are used — palette only. Every listing keeps its existing
not-affiliated line.

### Output shapes

| Shape | Size | Destination |
|-------|------|-------------|
| square | 2000 × 2000 | Etsy `01_main.png` |
| wide | 1280 × 720 | Gumroad storefront cover |
| pin | 1000 × 1500 | Pinterest `04_pin.png` |

The wide shape is a different composition, not a crop: title block left, stack right.

### Decision — the cover is rasterised

The PDF cover page is the rendered image placed full-bleed at 200 DPI, embedded as JPEG q92.

Rationale:

- The listing image and the PDF cover are then guaranteed identical, because one engine draws
  both. A vector reportlab cover and a Pillow listing image would drift.
- `CLAUDE.md` records four separate cover-page text-overflow bugs (hardcoded badge width
  across all 23 guides, guide 20's badge, the Start Here badge, guide 06's caption). Pillow
  measures text before drawing, so the class of bug disappears.
- Page 1 becomes trivially clean under `audit_pdfs.py`, which checks text spans.

Accepted cost: cover text is not selectable or searchable in the PDF. Acceptable for a cover.
Expected size impact ≈ 400–700 KB per document.

---

## Section 2 — Rollout to the 21 live SKUs

`rebuild_covers.py`. Approach A: render centrally, splice into the existing PDFs. Interiors
are never touched.

1. **Back up first.** Copy every current product PDF to `outputs/_pre_cover_backup/` before
   anything is written. Skipped if the backup already exists, so the script stays re-runnable
   without overwriting the pristine originals with already-modified files.
2. **Per SKU:** build `CoverSpec` → render square → write a one-page letter PDF containing
   that image → open the product with PyMuPDF → delete page 0 → insert the new page 0 → write
   to a temp file → atomic replace.
3. **Guards, each hard-failing the run:**
   - page count unchanged before and after
   - new page 0 is non-blank
   - `audit_pdfs.py` reports clean for the rebuilt file
4. Non-PDF deliverables (the Cost Calculator `.xlsx`, the Config Pack `.zip`) are untouched;
   their associated preview/guide PDFs get covers like any other.

The superseded `cover()` / `volume_cover()` functions in the 21 build scripts are **left in
place with a comment** marking them superseded and pointing at `covers/`. Deleting them would
silently change what a from-source rebuild produces.

---

## Section 3 — Listing images

- `01_main.png` — replaced by the new square render.
- `02_inside.png`, `03_included.png` — **kept as they are.** They composite real rendered pages,
  which is honest and is what Etsy's 3-image minimum is for.
- `04_pin.png` — new, 1000 × 1500, for Pinterest.
- Gumroad cover — continues to use the documented "upload to Etsy, reuse the public
  `url_fullxfull`" route, because Gumroad's cover endpoint requires a public URL and rejects
  the S3 URL its own presign flow returns. It now receives the **wide** render.

---

## Section 4 — ChatGPT series, then Grok

`build_chatgpt_v1.py`, on the existing `fieldguide/` engine with the `gpt` palette. Volume
scale: 5 chapters, ~26pp, one document, no per-chapter covers.

Chapters:

1. Getting started — free vs Plus vs Pro, the interface
2. Prompting that actually works, with copy-paste templates
3. Projects, memory and custom instructions
4. Custom GPTs — using them, then building one
5. Voice, images, files and data analysis

Build requirements:

- Every fact web-verified at build time. ChatGPT's pricing and model lineup move faster than
  anything else in the catalogue.
- **All pricing confined to one table on one page**, so a reprint is a single edit. Same rule
  applied to Copilot V5.
- Plan for the fill pass as part of the build, not as a fix: every volume so far has landed at
  56–57% vertical fill on first build against a house standard of 60% minimum, 66–69% typical.
  Write chapters → measure → add a real block to every page under 60% → re-measure. Never merge
  pages; page count is what the product is sold on.
- Where a fact cannot be verified from a public source, state the gap rather than inventing a
  figure — the precedent is Codex V4's acknowledged gap on cloud-task limits.

Grok V1 follows the same shape once ChatGPT is live and listed.

---

## Section 5 — New products, ranked for these channels

1. **Niche prompt packs.** "300 ChatGPT Prompts for Small Business Owners", then teachers,
   realtors, Etsy sellers. **Ranked above the Grok series.** Prompt packs are the best-selling
   digital category on Etsy; they are Pinterest-native in a way a developer guide is not; and
   the build cost is near zero because `prompt_vault_data.py` and its `verify_no_overflow()`
   guard already exist. This is the product the chosen channels are actually shaped for.
2. **ChatGPT printable cheat-sheet pack.** Printables are the one format confirmed to fit Etsy
   buyers. Light theme, one sheet per page, reusing `build_cheatsheets.py` and its two guards.
3. **Cross-tool comparison guide** — IDEAS.md item 3. The one thing no vendor will publish, and
   it cross-sells every existing series.
4. **Notion prompt library** — IDEAS.md item 6. Repackaging of an asset that already ships as
   Markdown.

---

## Section 6 — Distribution

### Pinterest — the compounding channel
Five boards. 3–5 pins/day. Pinterest rewards **fresh pins, not new products**, so pin variants
are generated automatically from existing SKUs — 40+ from the current catalogue — rather than
requiring new inventory. `covers/render.py` already produces the 2:3 shape this needs.

### Reddit / X — where the developer volumes' audience is
Value first. Give away the free Start Here PDF; never cold-link a paid product. Both platforms
punish selling, and a burned account is not recoverable.

### Etsy Ads — a measurement instrument, not a growth channel
$1.50/day against **three** listings only: Cheat Sheet Pack, Cost Calculator, and ChatGPT once
live. Spreading ~$40/month across twenty listings produces no interpretable data about any of
them. The question being answered is narrow and worth answering either way: *do these listings
convert when someone actually sees them?* If they do not convert with traffic, the problem is
the listing or the product, not the channel.

### Listing SEO
One pass across all twenty listings, retitling for search intent. Existing build-time
assertions hold: title ≤140 chars, exactly 13 tags, ≤20 chars per tag.

### Email
Route the free lead magnet into an owned list. It is the only channel here that neither
marketplace can take away.

---

## Sequencing

| When | Work |
|------|------|
| Week 1 | `covers/` package · rollout to all 21 · pin images |
| Week 2 | Pinterest live · listing SEO pass · Etsy Ads on three listings |
| Weeks 2–3 | ChatGPT Volume 1 |
| Week 4 | First niche prompt pack |
| Weeks 5–6 | Grok Volume 1 |

## Implementation decomposition

This design is too large for a single implementation plan. It becomes three, executed in
order, each independently shippable:

1. **Plan 1 — cover system and rollout.** Sections 1–3. Ends with all 21 products carrying the
   new cover on both channels, audit clean.
2. **Plan 2 — distribution.** Section 6. Can start as soon as Plan 1's images exist; does not
   depend on Plan 3.
3. **Plan 3 — ChatGPT Volume 1.** Section 4, then the first niche prompt pack from Section 5.
   Grok follows on its own plan once ChatGPT is live.

## Success criteria

- All 21 live products carry the new cover, on both channels, with `audit_pdfs.py` clean.
- Every SKU has square, wide and pin renders.
- Gumroad covers are landscape and no longer side-cropped.
- ChatGPT Volume 1 live on both channels, ≥60% fill, audit clean, facts verified.
- Pinterest running daily with automatically generated pins.
- Etsy Ads data on three listings sufficient to answer the conversion question.

## Out of scope

- PDF interiors and the dark house theme.
- Retrofitting the 23 Claude build scripts onto `fieldguide/`.
- TikTok Shop.
- Listing the 23 individual guides separately — settled 2026-07-28, reaffirmed twice.
