# Pinterest Pin Factory — Design

Date: 2026-09-21
Status: approved (brainstorm complete, ready for implementation plan)

---

## Problem

The catalogue is finished and consistent: 21 products on Etsy, 22 on Gumroad, all carrying
new covers and current files. None of that sells anything by itself. The August 2026
channel review concluded that distribution is the constraint, and nothing has been done
about it since.

Pinterest was chosen as one of two channels the owner will actually work. It is the right
pick for this catalogue: it is image-driven, it suits digital products, and unlike a social
post a pin keeps returning traffic for months.

**The specific problem this solves is volume.** Pinterest rewards *fresh pins*, not new
products. One pin per product is 22 pins — roughly a week of posting at a useful cadence,
after which there is nothing left to post. Manually authoring hundreds of pins is not a
thing the owner will sustain, and the catalogue already contains everything a good pin
needs to say.

So: turn pin production from a writing problem into a template problem.

## Goal

A repeatable generator producing enough on-brand, factually accurate pins to sustain daily
posting for months, each pointing at a live listing, with the copy written and ready.

## Constraints

- **Manual upload.** The owner uploads and schedules pins in Pinterest's own scheduler.
  No Pinterest API, no third-party scheduler, no credentials in this project. Decided
  2026-09-21 — API access needs a business account and app review, which does not gate
  the useful work.
- **Nine consumer-fit SKUs only** for the first wave: `40-chatgpt-v1`, `02-starter-volume`,
  `01-prompt-vault`, `10-cheat-sheet-pack`, `11-cost-calculator`, `12-start-here`,
  `03-complete-library`, `20-copilot-v1`, `30-codex-v1`. The deeper developer volumes (MCP
  servers, AGENTS.md, CLI internals) are excluded: their audience is not on Pinterest, and
  low-engagement pins drag a young account's signal at the point it matters most. They get
  pins only if the first wave shows traction.
- **No invented content.** Every claim on a pin must come from that SKU's existing
  `build_etsy_kit.SKUS` entry or from the book itself. This catalogue has already been
  burned once by a fact that went stale (the Brave Search free tier).
- **`build_etsy_kit.SKUS` stays the single source.** The pin generator reads it; it never
  duplicates listing copy.
- Python 3.14, Pillow. `%`-style formatting, single-quoted strings. `outputs/` is
  git-ignored.

---

## Design

### `pins/templates.py` — six layouts

All 1000×1500 (Pinterest's 2:3), all rendered with `covers.palette` so a pin inherits its
series colour and a ChatGPT pin is visibly violet against a Claude pin's ember.

| Template | What it shows | Source |
|----------|---------------|--------|
| `product` | The angled cover stack, as `04_pin.png` already renders | `covers.render` |
| `listicle` | "What's inside", numbered | SKU `bullets` |
| `hook` | One large statement, high contrast | curated per SKU (see below) |
| `checklist` | Ticked items, designed to be saved | SKU `bullets` |
| `comparison` | A small two-column table | curated row list, per SKU |
| `tip` | A single concrete, useful tip | curated per SKU |

`hook`, `tip` and `comparison` need copy that does not exist in the SKU record. These are
the only hand-authored strings in the system, they live in one dict per template in
`pins/copy.py`, and each must be traceable to something the book actually says. Example for
`40-chatgpt-v1`: *"Custom GPTs stop working on 11 Dec 2026."* — that is page 19 of the book.
`comparison` takes a list of `(left, right)` rows; a SKU with no curated rows is skipped,
never filled with `included` entries, which are file manifests rather than comparisons.

A template that cannot render a SKU (no comparison data, say) **skips that SKU rather than
inventing filler**, and the build reports the skip. Fewer honest pins beat padded ones.

### `pins/copy.py` — the words

Per pin: a Pinterest **title** (≤100 characters), a **description** (~200 characters,
keyword-led prose rather than hashtag soup — Pinterest is a search engine), and a
**destination URL**.

**URL rule:** prefer the Etsy listing from `etsypub.db`; fall back to Gumroad from
`gumroadpub.publish.get`. `12-start-here` has no Etsy listing — it is free and Etsy has no
free tier — so it resolves to Gumroad. A SKU that resolves to neither is a build failure,
not a warning: a pin pointing nowhere is worse than no pin.

**Boards** — five, assigned per pin so the upload worklist is unambiguous:
`AI for Beginners` · `ChatGPT Tips` · `AI Prompts & Templates` ·
`Printable Cheat Sheets` · `AI Tools & Productivity`

### `build_pins.py` — the build

Writes `outputs/pins/<sku>/<template>.png`, and `outputs/pins/PINS.csv` with one row per
pin: `file`, `title`, `description`, `url`, `board`, `sku`, `template`.

That CSV is the owner's upload worklist — sort by board, work down it.

Expected first wave: 6 templates × 9 SKUs = **up to 54 pins**, minus honest skips.

### Guards — both hard-fail the build

Following the precedent of `build_prompt_vault.verify_no_overflow()` and
`build_cheatsheets.verify_fits_one_page()`:

1. **`verify_no_overflow()`** — no text runs past a pin's margins. Text is measured before
   drawing, as `covers.render.fit_text` does.
2. **`verify_destinations()`** — every CSV row has a non-empty title, description and URL,
   every title is ≤100 characters, and every URL resolves to a listing the local db records
   as live.

### Testing

- all six templates render for all nine SKUs, or record an explicit skip
- every rendered pin is exactly 1000×1500 and not a flat fill
- no pin paints text outside its margins
- every CSV row has title, description, URL, board
- titles are within Pinterest's 100-character limit
- the URL rule prefers Etsy and falls back to Gumroad — proven on `12-start-here`, which
  has only Gumroad
- a SKU resolving to no URL fails the build

Per house convention, per-SKU loop tests collect every offender and assert once outside the
loop. Layout is asserted on rendered pixels where it matters, not only on image dimensions
— this project has already shipped four layout defects that passed a fully green suite.

---

## Out of scope

- Posting to Pinterest. Manual upload, by decision.
- The 13 developer-heavy SKUs, pending first-wave traction.
- Etsy Ads and the Reddit/X work — separate efforts.
- Pin analytics. Pinterest's own dashboard covers it, and there is no data yet to analyse.

## Success criteria

- ≥45 pins generated across the nine SKUs, each on-brand for its series.
- `PINS.csv` is directly workable: sort by board, upload, schedule.
- Both guards pass; no pin has clipped text or a dead link.
- Enough material for roughly a month of daily posting without repeating an image.

## Risks

- **A generated pin set can look mechanical.** Six templates across nine products is
  visibly systematic if the layouts are too similar. Mitigation: the templates differ in
  structure, not just content — a hook pin is mostly one sentence, a checklist is mostly
  list. Review a sample by eye before bulk upload.
- **Pin copy decays with the product.** The ChatGPT hook pin cites dates that expire on
  11 Dec 2026. `pins/copy.py` must carry a comment saying so, next to the string.
