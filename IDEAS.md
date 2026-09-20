# PRODUCT IDEAS — BACKLOG
# Digital products adjacent to the Field Guide series
# Started 2026-08-01

Ranked by return on effort **given assets that already exist**. Status is honest: most of
these are unbuilt, and a few duplicate work already sitting in `outputs/`.

---

## SHIPPED

### 1. Claude AI Cheat Sheet Pack — printables ✅ LIVE
13 pages (cover + 12 sheets), $6.99. Etsy listing 4548222295. On Gumroad as
`sromov.gumroad.com/l/cheat-sheet-pack`.

**The insight: 23 printable cheat sheets already existed and were not being sold.** Every
guide ends with a one-page reference; the cover copy even advertised it. Printables are
the strongest-selling digital category on Etsy, and unlike the guides it is a format Etsy
buyers actively search for.

**Critical design note:** the house style is dark (#0F0F1A) — which is *wrong* for a
printable. Nobody prints a full-bleed dark page, so this is a purpose-built light,
ink-frugal document rather than an extract of page 6. Also single-column: two columns
squeezed the value field to ~34 characters, which would have meant gutting content to fit
the layout.

### 2. AI Cost Calculator — spreadsheet ✅ LIVE
3 sheets, $7.99. Etsy listing 4548222363. Enter monthly token usage, get cost across every
current model with cache-hit and batch discounts applied. Every figure is a **live
formula** reading an editable Rates tab, so the product does not rot when vendors move
pricing. Sidesteps the "this duplicates the vendor docs" problem that undermines prose.

---

## AGREED, BLOCKED ON THE VOLUMES

### 2b. Combined "AI Coding Cheat Sheet Pack" — ~26 sheets, $12.99
**Decided 2026-08-01. Build AFTER the Copilot and Codex volumes exist**, when the research
is already done and extraction is nearly free — exactly how the Claude pack came about.

Rejected alternative: a separate cheat sheet pack per tool. That is overkill. The Claude
pack was cheap only because 23 guides of researched content already existed; for Copilot
and Codex nothing exists yet, so building sheets first means researching twice. And the
reference surface is smaller — Claude earns 12 sheets, Copilot and Codex realistically
~6 each. Two thin 6-sheet packs at $6.99 compete with each other and read as a weaker
catalogue than one strong product.

Composition: 12 Claude + ~6 Copilot + ~6 Codex + **2–3 side-by-side comparison sheets**.
The comparison sheets are what make the whole worth more than the parts — commands, config
files (`CLAUDE.md` / `copilot-instructions.md` / `AGENTS.md`) and billing models next to
each other. No vendor will ever publish that, because no vendor compares itself to two
competitors.

Gives a clean ladder: $6.99 Claude pack as entry, $12.99 combined pack as upsell — the
same shape as Volume 1 → Complete Library.

**Caveat, stated honestly:** this is contingent on the volumes actually being built. If
Copilot/Codex stall after V1 there is no combined pack. It is a consequence of that
decision, not an independent bet.

---

## HIGH VALUE, NOT STARTED

### 3. Cross-tool decision guide
"Claude Code vs Copilot vs Codex — which tool for which job." The one thing no vendor will
ever publish. Cross-sells all three series and becomes the natural anchor for a
three-series bundle. Build **after** the Copilot and Codex volumes exist.

Shares its research with the comparison sheets in **2b** — do them in the same pass, not
as two separate efforts.

### 4. Merch crossover — use the POD pipeline that already runs
`C:\Projects\TShirt1\pod-pipeline` has 48 live listings and a debugged Printify → Etsy
pipeline. The AI-developer audience these guides attract is the same audience that buys
developer-humour shirts ("exit 2 blocks the hook", "it works on my agent"). **Two
businesses that currently don't know about each other** — fulfilment infrastructure is
already built, so the marginal cost is design work only.

### 5. AI-ready repo starter template
Extend the Config Pack into a complete template repo: `CLAUDE.md` + `AGENTS.md` +
`copilot-instructions.md`, hooks, CI workflow, MCP configs — all three tools configured
together. Higher price point ($19–29), strong Gumroad fit, weak Etsy fit.

### 6. Notion / Obsidian prompt system
`Claude_Prompt_Vault.md` already ships Markdown. A structured Notion database version
(prompt library with categories, tags, favourites) is mostly repackaging into a large and
proven template category.

---

## WORTH CONSIDERING

### 7. Localised editions
Etsy is global and the volumes are mostly plain English. Spanish, German and Portuguese
editions of Volume 1 are a translation pass over an asset that is already built and
already selling. Watch for text overflow — the layout is width-constrained and German
in particular will break lines that fit in English. `audit_pdfs.py` will catch it.

### 8. Email course as a funnel asset
A 7-day "Getting started with AI coding" email sequence. Not a product — a lead magnet
that sells the bundle. Pairs with the existing free `Start Here` PDF.

### 9. Video walkthroughs
Higher perceived value, different medium, much higher production cost. Only worth it once
a written product proves the audience exists.

### 10. Resume / portfolio assets for AI engineers
Adjacent audience, unproven overlap. Parked.

---

## DECIDED AGAINST

- **Listing the 23 individual guides separately.** They are inputs, not SKUs — buyers scan
  page count first and a 6-page PDF loses to a 100-page competitor bundle. Settled
  2026-07-28, reaffirmed 2026-08-01.
- **A separate cheat sheet pack per tool.** Overkill — see 2b. One combined pack instead.
- ~~A symmetrical Gumroad publisher~~ — **WRONG, retracted 2026-08-01.** Every public doc
  says `POST /v2/products` returns 404 and creation is dashboard-only. Tested live: it
  returns 200 and creates the product. `gumroadpub/` is built and working.

---

## STILL UNLISTED, ALREADY BUILT

No build work required, only listing:

| Product | Where it stands | Price |
|---------|-----------------|-------|
| The Claude Prompt Vault | Gumroad draft (no cover — not on Etsy) · **not on Etsy** | $8.99 |
| Claude Code Config Pack | **Neither channel yet** — queued for Gumroad 08-02 | $14.99 |
| FREE lead magnet — Start Here | **Neither channel** | $0 |

**Covers gap:** Gumroad's cover endpoint needs a PUBLIC image url and rejects the S3 url
its own upload flow returns, so covers are pulled from the matching Etsy listing. Prompt
Vault and Config Pack are not on Etsy, so they will publish to Gumroad **without listing
images**, which hurts conversion. Fix is either listing those two on Etsy ($0.40, which
also gets them covers automatically) or dragging the mockups in by hand from
`outputs/etsy/01-prompt-vault/` and `outputs/etsy/05-config-pack/`.

**Start Here — FIXED AND QUEUED 2026-08-02.** It had two real defects that made it worse
than useless as a lead magnet: the CTA said "grab your first guide today" and **never said
where**, and the bundle table advertised a **"$79 Complete Library, Guides 01-20"** that
has never existed at that price or that scope (it is $29.99 and covers 23). It also
claimed guides were "sold separately", which was decided against. All corrected against
live prices, shop URL added to the CTA, hardcoded badge width fixed. Queued for Gumroad at
$0.00 — Etsy has no free tier, so it is Gumroad-only.

---

## ⚠ CHANNEL REALITY CHECK — 2026-08-02 (owner feedback)

**No hits on Etsy at all for the guides. Very little for the t-shirts.** Owner wants to
tackle ADVERTISING and TIKTOK SHOP on return (~08-08).

This is the concern raised before the Copilot/Codex series was commissioned, now
confirmed by data rather than argument: *"Etsy shoppers are overwhelmingly buying
planners, printables, craft and small-business material. Developers do not browse Etsy
for tooling."* Sixteen products are live and organic Etsy search is not delivering an
audience for any of them.

**Do not respond by building more products.** The catalogue is not the constraint —
distribution is. Before another volume is written, the open questions are:

1. **Etsy Ads** — the only lever inside Etsy. Cheap to test, and it tells you within a
   week whether the listings convert when someone actually sees them. If they do not
   convert with traffic, the problem is the listing or the product, not the channel.
2. **TikTok Shop** — owner's stated priority. Note the POD pipeline already has a
   TikTok channel wired up (`pod-pipeline` `DEFAULT_CHANNELS`, TikTok opt-in), so the
   t-shirt side has a head start the guides do not.
3. **Off-platform** — the developer volumes were always predicted to sell on Gumroad,
   Reddit and X rather than Etsy search. Gumroad is now loaded; nothing has been done
   to drive traffic to it.
4. **The printables are the exception worth watching.** The Cheat Sheet Pack and Cost
   Calculator are the two products that fit what Etsy buyers actually search for. If
   ANYTHING moves organically, expect it to be those — and that would tell you the
   format matters more than the topic.

**Honest read:** the guides are good products in a marketplace whose shoppers are not
looking for them. That is a distribution problem with three possible answers — pay for
traffic, change channel, or change what is being sold — and it should be settled before
more volumes are commissioned.

---

## LIVE NOW (for reference)

Etsy — 9 products: Volumes 1–6, Complete Library ($29.99, 4548260666), Cheat Sheet Pack,
Cost Calculator. Gumroad — 2 created as drafts, remaining 9 scheduled 2026-08-02 10:00
via the "Gumroad Finish Load" task.

The Complete Library is the one the live volumes already advertise ("23-Guide Field Guide
Series") without it being purchasable.
