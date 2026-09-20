# etsypub — Field Guide volumes → Etsy

Publishes the six volume PDFs as Etsy **digital instant-download** listings via the
Etsy Open API v3.

## Why not the TShirt1 mechanism verbatim

`C:\Projects\TShirt1\pod-pipeline` reaches Etsy *through Printify* — its own notes say
"Etsy and TikTok have no equivalent client here, only Printify." Printify only knows
physical print-on-demand products, so it cannot carry a PDF. The transport had to change.

What was copied is the shape, and specifically the parts that were learned the hard way:

| pod-pipeline lesson | how it lands here |
|---|---|
| 44 ghost Shopify products from re-runs | `etsy_listing_id` is written the instant the draft returns, before any upload |
| local state drifted from the channel | `--status` asks Etsy what it actually holds instead of trusting `etsy.db` |
| Etsy refuses titles starting with punctuation | `check()` rejects them before a call is spent |
| Etsy accepts an empty description then silently never publishes | `check()` treats an empty body as fatal |
| whole-catalogue pushes get young shops reviewed | paced batches, `--limit`, jitter between listings |
| one channel failing shouldn't stop the others | each volume is caught independently and left resumable |

## One-time setup

```
copy .env.example .env
```

0. `python -m etsypub.publish --preflight` at any point answers "is this set up
   properly?" — it pings Etsy (no OAuth needed) to prove the app is approved and the key
   active, validates all six listings, and names anything still missing.

1. Register an app at <https://www.etsy.com/developers/register>. Put **both** the
   **keystring** and the **shared secret** in `.env` — Etsy wants them joined as
   `keystring:shared_secret` in the `x-api-key` header, and the keystring alone returns
   `403 Shared secret is required in x-api-key header`. Register the callback exactly as
   `https://localhost:3003/oauth/redirect`.

   Etsy's form rejects `http://`. Nothing is actually served on that https address —
   after you click Allow the browser shows a connection error, which is expected, and
   the `?code=...` you need is sitting in the address bar. `oauth.py` detects the https
   scheme and asks you to paste that URL back instead of listening for it. PKCE is what
   makes that safe: the code is useless without the verifier held in the running process.
   (Set `ETSY_REDIRECT_URI` to an `http://` URL and it goes back to catching the redirect
   automatically — but Etsy will not let you register one.)
2. `python -m etsypub.oauth` — opens the consent page, takes the pasted redirect, writes
   `ETSY_REFRESH_TOKEN` and `ETSY_SHOP_ID` back into `.env`.
3. `python -m etsypub.taxonomy --search digital` — pick a category id, put it in `.env`
   as `ETSY_TAXONOMY_ID`. Keep every listing on the same one.

## Running

```
python -m etsypub.publish --dry-run          # no network at all; shows what would happen
python -m etsypub.publish                    # create the 6 DRAFTS — free, nothing goes live
python -m etsypub.publish --status           # local state next to what Etsy actually holds
python -m etsypub.publish --activate --limit 1   # take ONE live ($0.20), check it
python -m etsypub.publish --activate         # the rest, paced (prompts to confirm)
```

Drafts cost nothing — only activation is billed, at $0.20 per listing ($1.20 for all
six). That split is deliberate: build everything, look at it in the Etsy dashboard, then
go live one at a time.

Every command is safe to re-run. Each stage checks what is already done, so an
interrupted run resumes rather than duplicating.

## Where the listing copy comes from

`build_etsy_kit.SKUS` — one source for titles, 13 tags, descriptions, prices and the
three 2000×2000 mockups, with Etsy's character limits asserted at build time. Change a
title there and `python build_etsy_kit.py` regenerates `outputs/etsy/LISTINGS.md` and the
images; `etsypub` reads the same records. Do not retype listing copy here.
