"""Put the Field Guide volumes on Etsy as digital instant-download listings.

    python -m etsypub.publish --dry-run     # what would happen, costs nothing, no network
    python -m etsypub.publish               # build the DRAFTS (free — nothing goes live)
    python -m etsypub.publish --status      # what Etsy actually holds right now
    python -m etsypub.publish --activate    # flip drafts live ($0.20 each, paced)
    python -m etsypub.publish --activate --limit 1 --volumes 1

Drafts are free; only activation is billed. So the safe order is: build all the drafts,
look at them in the Etsy dashboard, then activate — one first, the rest once it looks
right.

Every step is resumable. `etsy_listing_id` is written the moment the draft comes back,
before any upload, so a run that dies halfway is picked up rather than duplicated.
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time

import build_etsy_kit

from . import config, db
from .client import Etsy, EtsyError

JOB = 'etsy_publish'


# ------------------------------------------------------------------ selection

def volume_skus(volumes: list[int]) -> list[dict]:
    """The SKU records for these volumes, in volume order.

    Listing copy has exactly one source — build_etsy_kit.SKUS — so a title fixed there
    is fixed everywhere, and the character-limit asserts in that module have already run.
    """
    by_vol = {s['volume']: s for s in build_etsy_kit.SKUS if s.get('volume')}
    out = []
    for v in volumes:
        if v not in by_vol:
            raise SystemExit('No SKU defined for volume %s. Add one to build_etsy_kit.SKUS '
                             'with volume=%s.' % (v, v))
        out.append(by_vol[v])
    return out


def named_skus(names: list[str]) -> list[dict]:
    """SKU records by sku name, for products that are not part of a volume."""
    by_name = {s['sku']: s for s in build_etsy_kit.SKUS}
    out = []
    for n in names:
        if n not in by_name:
            raise SystemExit('No SKU named %r. Known: %s'
                             % (n, ', '.join(sorted(by_name))))
        out.append(by_name[n])
    return out


def deliverables(s: dict) -> list[str]:
    """The file(s) the buyer actually receives.

    Defaults to the SKU's `pdf`, but a SKU may set `files` explicitly — the cost
    calculator ships an .xlsx while its `pdf` is only a preview used for the mockups.
    Getting this wrong means shipping the sales preview instead of the product.
    """
    return list(s.get('files') or [s['pdf']])


def description_for(s: dict) -> str:
    """The listing body, rebuilt from the same fields LISTINGS.md renders."""
    L = [s['headline'].replace('\n', ' ').upper(), '', s['blurb'], '', 'WHAT YOU GET', '']
    L += ['* ' + b for b in s['bullets']]
    L += ['', 'FILES INCLUDED', '']
    L += ['* ' + i for i in s['included']]
    L += ['',
          'INSTANT DIGITAL DOWNLOAD',
          '* Files are available the moment your payment clears',
          '* Works on phone, tablet, laptop and desktop',
          '* Nothing ships — this is a digital product',
          '* Updated for 2026',
          '',
          'Part of the Claude AI Field Guide Series.',
          '',
          'Because this is an instant download, it cannot be returned. If a file will '
          'not open, message me and I will fix it.']
    return '\n'.join(L)


# ------------------------------------------------------------------- guards

def check(s: dict) -> list[str]:
    """Everything Etsy will reject, caught before we spend a call finding out.

    These are the pod-pipeline scars, ported: Etsy refuses a title starting with
    punctuation ("Title contains invalid characters"), and it will happily accept a
    product with an empty description and then never publish it.
    """
    problems = []
    title = s['title']
    if not title.strip():
        problems.append('empty title')
    elif not title[0].isalnum():
        problems.append('title starts with punctuation — Etsy rejects this')
    if len(title) > 140:
        problems.append('title is %d chars (max 140)' % len(title))
    if len(s['tags']) != 13:
        problems.append('%d tags (Etsy allows exactly 13 here)' % len(s['tags']))
    for t in s['tags']:
        if len(t) > 20:
            problems.append('tag over 20 chars: %r' % t)
    if not description_for(s).strip():
        problems.append('empty description — Etsy accepts it then never publishes')

    for f in deliverables(s):
        if not os.path.exists(os.path.join(config.OUT, f)):
            problems.append('missing deliverable: %s' % f)
    if not os.path.exists(os.path.join(config.OUT, s['pdf'])):
        problems.append('missing mockup source PDF: %s' % s['pdf'])
    for name in ('01_main', '02_inside', '03_included'):
        p = os.path.join(config.ETSY_ASSETS, s['sku'], name + '.png')
        if not os.path.exists(p):
            problems.append('missing mockup: %s/%s.png (run build_etsy_kit.py)'
                            % (s['sku'], name))
    return problems


def price_of(s: dict) -> float:
    return float(s['price'].lstrip('$'))


# ------------------------------------------------------------------ the work

def build_draft(e: Etsy, s: dict) -> dict:
    """Create-or-resume one draft: listing, then images, then the file.

    Returns the db row. Safe to call repeatedly — each stage checks what is already done.
    """
    row = db.ensure(s['sku'], s.get('volume'), s['title'], s['price'])
    listing_id = row['etsy_listing_id']

    if not listing_id:
        res = e.create_draft_listing(
            title=s['title'], description=description_for(s), price=price_of(s),
            tags=s['tags'], taxonomy_id=int(config.TAXONOMY_ID),
            quantity=config.QUANTITY, who_made=config.WHO_MADE,
            when_made=config.WHEN_MADE, is_supply=config.IS_SUPPLY,
            listing_type='download',
            return_policy_id=int(config.RETURN_POLICY_ID) if config.RETURN_POLICY_ID else None)
        listing_id = res.get('listing_id')
        if not listing_id:
            raise EtsyError('draft created but no listing_id came back: %s' % res)
        # Written before anything else, so an interrupted run resumes instead of
        # creating a second listing for the same product on the next attempt.
        db.update(s['sku'], etsy_listing_id=listing_id, state='draft', error=None,
                  url=res.get('url'))
        print('  draft #%s created' % listing_id)
    else:
        print('  draft #%s already exists' % listing_id)

    row = db.get(s['sku'])
    if not row['images_done']:
        for rank, name in enumerate(('01_main', '02_inside', '03_included'), start=1):
            path = os.path.join(config.ETSY_ASSETS, s['sku'], name + '.png')
            e.upload_image(listing_id, path, rank=rank,
                           alt_text='%s — page %d preview' % (s['title'][:120], rank))
            print('  image %d/3 uploaded' % rank)
        db.update(s['sku'], images_done=1)

    row = db.get(s['sku'])
    if not row['file_done']:
        for f in deliverables(s):
            e.upload_file(listing_id, os.path.join(config.OUT, f), name=f)
            print('  file uploaded (%s)' % f)
        db.update(s['sku'], file_done=1)

    return db.get(s['sku'])


def activate(e: Etsy, s: dict) -> None:
    row = db.get(s['sku'])
    if not row or not row['etsy_listing_id']:
        raise EtsyError('%s has no draft yet — run without --activate first' % s['sku'])
    if row['state'] == 'active':
        print('  already active')
        return
    if not row['file_done']:
        raise EtsyError('%s has no file attached — Etsy will refuse to activate it'
                        % s['sku'])
    res = e.activate(row['etsy_listing_id'])
    db.update(s['sku'], state='active', url=res.get('url'), error=None)
    print('  ACTIVE -> %s' % (res.get('url') or row['etsy_listing_id']))


# -------------------------------------------------------------------- runner

def run(volumes: list[int], *, dry_run: bool = False, do_activate: bool = False,
        limit: int | None = None, sku_names: list[str] | None = None) -> dict:
    db.init_db()
    skus = named_skus(sku_names) if sku_names else volume_skus(volumes)

    blocked = {}
    ready = []
    for s in skus:
        problems = check(s)
        if problems:
            blocked[s['sku']] = problems
        else:
            ready.append(s)

    for sku, problems in blocked.items():
        print('BLOCKED %s' % sku)
        for p in problems:
            print('    - %s' % p)

    if limit:
        ready = ready[:limit]

    if dry_run:
        print('\nDRY RUN — nothing sent to Etsy.\n')
        for s in ready:
            row = db.get(s['sku']) or {}
            state = row.get('state', 'not started')
            action = 'activate' if do_activate else 'create/complete draft'
            print('  %-6s %-28s %-9s %-8s -> %s'
                  % ('vol %s' % s['volume'] if s.get('volume') else '-',
                     s['sku'], s['price'], state, action))
        if do_activate:
            print('\n  would cost %d x $%.2f = $%.2f in Etsy listing fees'
                  % (len(ready), config.LISTING_FEE_USD,
                     len(ready) * config.LISTING_FEE_USD))
        else:
            print('\n  drafts are free — no listing fees at this stage')
        return {'ready': [s['sku'] for s in ready], 'blocked': blocked}

    missing = config.missing_credentials()
    if missing:
        print('Cannot talk to Etsy yet. Still needed:')
        for m in missing:
            print('    - %s' % m)
        return {'blocked': blocked, 'error': 'credentials'}

    e = Etsy()
    done, failed = [], []
    for i, s in enumerate(ready):
        print('\n%s%s' % ('vol %s — ' % s['volume'] if s.get('volume') else '', s['sku']))
        try:
            if do_activate:
                activate(e, s)
            else:
                build_draft(e, s)
            done.append(s['sku'])
        except Exception as exc:                          # noqa: BLE001 - per listing
            failed.append({'sku': s['sku'], 'error': str(exc)})
            db.update(s['sku'], error=str(exc))
            print('  FAILED: %s' % exc)
        if i < len(ready) - 1:
            time.sleep(random.uniform(config.JITTER_MIN, config.JITTER_MAX))

    summary = '%s: %d ok, %d failed' % ('activate' if do_activate else 'draft',
                                        len(done), len(failed))
    db.record_run(JOB, ok=not failed, summary=summary)
    print('\n' + summary)
    return {'done': done, 'failed': failed, 'blocked': blocked}


def update_file(e: Etsy, s: dict) -> str:
    """Replace the PDF on an existing listing with the current build.

    Uploads the new file BEFORE deleting the old one, so a live digital listing is never
    left without a downloadable file — Etsy deactivates those, and a buyer mid-purchase
    would hit a broken download.
    """
    row = db.get(s['sku'])
    if not row or not row['etsy_listing_id']:
        raise EtsyError('%s has no listing yet' % s['sku'])
    lid = row['etsy_listing_id']

    before = e.listing_files(lid).get('results', [])
    old_ids = [f['listing_file_id'] for f in before]

    pdf = os.path.join(config.OUT, s['pdf'])
    e.upload_file(lid, pdf, name=s['pdf'])

    after = e.listing_files(lid).get('results', [])
    if not [f for f in after if f['listing_file_id'] not in old_ids]:
        raise EtsyError('new file did not appear — leaving the old one in place')

    removed = 0
    for fid in old_ids:
        e.delete_listing_file(lid, fid)
        removed += 1
    return 'uploaded new PDF, removed %d old file(s)' % removed


IMAGE_NAMES = ('01_main.png', '02_inside.png', '03_included.png',
              '04_pin.png', '05_wide.png')


def live_skus() -> list[dict]:
    """SKU records for every row the local db has an Etsy listing id for.

    Unlike `volume_skus`, this covers every live product, not just the 6 volumes —
    images were re-rendered for all 21 live SKUs, not only the volumes. Mapped back to
    build_etsy_kit.SKUS so listing copy (e.g. the alt text) still has one source.
    """
    by_name = {s['sku']: s for s in build_etsy_kit.SKUS}
    out = []
    for row in db.all_listings():
        if row.get('etsy_listing_id') and row['sku'] in by_name:
            out.append(by_name[row['sku']])
    return out


def update_images(e: Etsy, s: dict) -> str:
    """Replace all 5 listing images on an existing listing with the current mockups.

    Uploads the 5 new images BEFORE deleting any old one, mirroring update_file's safety
    property — a live listing must never be left without gallery images.
    """
    row = db.get(s['sku'])
    if not row or not row['etsy_listing_id']:
        raise EtsyError('%s has no listing yet' % s['sku'])
    lid = row['etsy_listing_id']

    img_dir = os.path.join(config.OUT, 'etsy', s['sku'])
    missing = [n for n in IMAGE_NAMES if not os.path.exists(os.path.join(img_dir, n))]
    if missing:
        raise EtsyError('%s missing image(s): %s' % (s['sku'], ', '.join(missing)))

    before = e.listing_images(lid).get('results', [])
    old_ids = [im['listing_image_id'] for im in before]

    alt_text = s['headline'].replace('\n', ' ')
    for rank, name in enumerate(IMAGE_NAMES, start=1):
        e.upload_image(lid, os.path.join(img_dir, name), rank=rank, alt_text=alt_text)

    after = e.listing_images(lid).get('results', [])
    if not [im for im in after if im['listing_image_id'] not in old_ids]:
        raise EtsyError('new images did not appear — leaving the old ones in place')

    removed = 0
    for iid in old_ids:
        e.delete_listing_image(lid, iid)
        removed += 1
    return 'uploaded 5 images, removed %d old one(s)' % removed


def preflight() -> bool:
    """Everything checkable before the OAuth consent. Returns True if ready to go."""
    print('Etsy app')
    if not config.KEYSTRING or not config.SHARED_SECRET:
        print('   keystring/shared secret: MISSING — set both in .env')
        return False
    try:
        res = Etsy.ping()
        print('   approved and active (application_id %s)' % res.get('application_id'))
    except EtsyError as e:
        print('   NOT USABLE: %s' % e)
        print('   A 403 here usually means Etsy has not approved the app yet.')
        return False

    print('\nListing content')
    skus = volume_skus(config.VOLUMES)
    ok = True
    for s in skus:
        problems = check(s)
        if problems:
            ok = False
            print('   vol %-2s %-28s %d problem(s)' % (s['volume'], s['sku'], len(problems)))
            for p in problems:
                print('        - %s' % p)
        else:
            print('   vol %-2s %-28s %-8s ready' % (s['volume'], s['sku'], s['price']))

    print('\nAccount')
    for label, val, how in [
            ('refresh token', config.REFRESH_TOKEN, 'python -m etsypub.oauth'),
            ('shop id', config.SHOP_ID, 'python -m etsypub.oauth'),
            ('taxonomy id', config.TAXONOMY_ID,
             'python -m etsypub.taxonomy --search digital')]:
        print('   %-14s %s' % (label, val and 'set' or 'MISSING -> run: %s' % how))
        if not val:
            ok = False
    return ok


def status() -> None:
    db.init_db()
    rows = db.all_listings()
    if not rows:
        print('Nothing recorded locally yet.')
    else:
        print('%-4s %-28s %-9s %-8s %-12s %s'
              % ('VOL', 'SKU', 'PRICE', 'STATE', 'LISTING', 'URL'))
        for r in rows:
            print('%-4s %-28s %-9s %-8s %-12s %s'
                  % (r['volume'], r['sku'], r['price'] or '', r['state'],
                     r['etsy_listing_id'] or '', r['url'] or ''))

    missing = config.missing_credentials()
    if missing:
        print('\nNot connected to Etsy yet. Still needed:')
        for m in missing:
            print('    - %s' % m)
        return

    # Local state is never trusted over what the shop actually holds — and where they
    # disagree, Etsy wins. Activating from the dashboard is normal and must not leave
    # the db claiming a listing is still a draft.
    e = Etsy()
    seen = {}
    for state in ('draft', 'active', 'inactive', 'expired'):
        try:
            live = e.shop_listings(state=state)
        except Exception:                                     # noqa: BLE001
            continue
        for l in live.get('results', []):
            seen[l['listing_id']] = state

    fixed = []
    for r in rows:
        lid = r['etsy_listing_id']
        if lid and lid in seen and seen[lid] != r['state']:
            db.update(r['sku'], state=seen[lid])
            fixed.append('%s: %s -> %s' % (r['sku'], r['state'], seen[lid]))
        elif lid and lid not in seen:
            fixed.append('%s: #%s not found on Etsy (deleted?)' % (r['sku'], lid))

    if fixed:
        print('\nReconciled against Etsy:')
        for f in fixed:
            print('   %s' % f)
    else:
        print('\nLocal state matches Etsy.')

    for state in ('draft', 'active'):
        n = sum(1 for s in seen.values() if s == state)
        print('Etsy says %s: %d listing(s) in the shop' % (state, n))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--volumes', default=','.join(str(v) for v in config.VOLUMES),
                    help='comma-separated volume numbers (default: %(default)s)')
    ap.add_argument('--skus', help='comma-separated SKU names, for products that are not '
                                   'volumes (e.g. 10-cheat-sheet-pack)')
    ap.add_argument('--dry-run', action='store_true', help='no network calls at all')
    ap.add_argument('--activate', action='store_true',
                    help='flip existing drafts live — this is the step Etsy bills for')
    ap.add_argument('--limit', type=int, help='only act on the first N')
    ap.add_argument('--yes', action='store_true',
                    help='skip the activation confirmation — for unattended runs')
    ap.add_argument('--status', action='store_true', help='local state vs what Etsy holds')
    ap.add_argument('--preflight', action='store_true',
                    help='is the app approved and is everything ready to list?')
    ap.add_argument('--update-files', action='store_true',
                    help='replace the PDF on existing listings with the current build')
    a = ap.parse_args()

    if a.update_files:
        db.init_db()
        volumes = [int(v) for v in a.volumes.split(',') if v.strip()]
        skus = volume_skus(volumes)
        if a.limit:
            skus = skus[:a.limit]
        e = Etsy()
        done, failed = [], []
        for i, s in enumerate(skus):
            print('\nvol %s — %s' % (s['volume'], s['sku']))
            try:
                print('  ' + update_file(e, s))
                done.append(s['sku'])
            except Exception as exc:                      # noqa: BLE001 - per listing
                failed.append(s['sku'])
                print('  FAILED: %s' % exc)
            if i < len(skus) - 1:
                time.sleep(random.uniform(config.JITTER_MIN, config.JITTER_MAX))
        print('\nfiles updated: %d ok, %d failed' % (len(done), len(failed)))
        return

    if a.preflight:
        ok = preflight()
        print('\n%s' % ('READY — next: python -m etsypub.publish   (creates the drafts, free)'
                        if ok else 'NOT READY — see above'))
        return
    if a.status:
        status()
        return

    volumes = [int(v) for v in a.volumes.split(',') if v.strip()]
    sku_names = [s.strip() for s in a.skus.split(',')] if a.skus else None
    n = len(sku_names) if sku_names else len(volumes)
    if a.activate and not a.dry_run and not a.limit and not a.yes:
        print('Activating %d listings will cost $%.2f in Etsy fees.'
              % (n, n * config.LISTING_FEE_USD))
        if input('Type yes to continue: ').strip().lower() != 'yes':
            sys.exit('Nothing activated.')

    run(volumes, dry_run=a.dry_run, do_activate=a.activate, limit=a.limit,
        sku_names=sku_names)


if __name__ == '__main__':
    main()
