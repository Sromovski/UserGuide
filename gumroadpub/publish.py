"""Put the Field Guide catalogue on Gumroad.

    python -m gumroadpub.publish --dry-run     # what would happen, no network
    python -m gumroadpub.publish               # create + upload, leaves them UNPUBLISHED
    python -m gumroadpub.publish --publish     # flip them live (Gumroad charges nothing)
    python -m gumroadpub.publish --status      # local state vs what Gumroad holds
    python -m gumroadpub.publish --skus 01-prompt-vault

Listing content comes from `build_etsy_kit.SKUS` — the same single source Etsy uses, so
the two channels cannot drift on title, price or copy.

Gumroad charges no listing fee, so unlike Etsy there is no cost reason to split create
from publish. It is still split, because publishing is the irreversible-ish step and you
should look at the products first.

Covers: Gumroad's cover endpoint takes a public image URL, and refuses the S3 URL its own
presign flow returns. The mockups are already publicly hosted on the Etsy listings, so
covers are pulled from there. A SKU with no Etsy listing gets no cover — reported, not
silently skipped.
"""
from __future__ import annotations

import argparse
import os
import random
import sqlite3
import time

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, '.env'))

import build_etsy_kit                                              # noqa: E402
from etsypub import config as etsy_config                          # noqa: E402
from gumroadpub.client import Gumroad, GumroadError                # noqa: E402

DB = etsy_config.DB_PATH
# Gentle. Creating products back to back is what tips a daily-cap refusal into a 429.
JITTER = (5, 12)

SCHEMA = """
CREATE TABLE IF NOT EXISTS gumroad_listings (
    sku         TEXT PRIMARY KEY,
    product_id  TEXT,
    permalink   TEXT,
    url         TEXT,
    price       TEXT,
    published   INTEGER NOT NULL DEFAULT 0,
    files_done  INTEGER NOT NULL DEFAULT 0,
    covers_done INTEGER NOT NULL DEFAULT 0,
    error       TEXT,
    updated_at  TEXT
);
"""


def _con():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with _con() as con:
        con.executescript(SCHEMA)


def get(sku):
    with _con() as con:
        r = con.execute('SELECT * FROM gumroad_listings WHERE sku=?', (sku,)).fetchone()
    return dict(r) if r else None


def ensure(sku, price):
    if get(sku):
        return get(sku)
    with _con() as con:
        con.execute('INSERT INTO gumroad_listings (sku, price) VALUES (?,?)', (sku, price))
    return get(sku)


def update(sku, **f):
    if not f:
        return
    cols = ', '.join('%s=?' % k for k in f)
    with _con() as con:
        con.execute('UPDATE gumroad_listings SET %s WHERE sku=?' % cols,
                    (*f.values(), sku))


def all_rows():
    with _con() as con:
        return [dict(r) for r in
                con.execute('SELECT * FROM gumroad_listings ORDER BY sku').fetchall()]


def ensure_all():
    """A row for every catalogue SKU, so a SKU added to build_etsy_kit.SKUS is never
    invisible to --status or the creation path just because nothing has pushed it yet."""
    init_db()
    for s in build_etsy_kit.SKUS:
        ensure(s['sku'], s['price'])


# ------------------------------------------------------------------- content

def gumroad_name(s):
    """Etsy titles are keyword-stuffed to 140 chars for its search engine. That reads as
    spam on a personal Gumroad storefront, where the buyer arrives from a link rather
    than a search grid. Take the first segment before the pipe — clean, and still derived
    from the single source so the two channels cannot drift on wording."""
    return s['title'].split('|')[0].strip()


def permalink_for(s):
    return s['sku'].split('-', 1)[1].replace('_', '-')[:60]


def price_cents(s):
    return int(round(float(s['price'].lstrip('$')) * 100))


def deliverables(s):
    return list(s.get('files') or [s['pdf']])


def description_html(s):
    """Gumroad descriptions are HTML."""
    parts = ['<p>%s</p>' % s['blurb'], '<h3>What you get</h3>', '<ul>']
    parts += ['<li>%s</li>' % b for b in s['bullets']]
    parts += ['</ul>', '<h3>Files included</h3>', '<ul>']
    parts += ['<li>%s</li>' % i for i in s['included']]
    parts += ['</ul>',
              '<p><strong>Instant download.</strong> Works on phone, tablet, laptop and '
              'desktop. Nothing ships.</p>',
              '<p><em>Unofficial and independent. Not affiliated with, endorsed by, or '
              'sponsored by Anthropic.</em></p>']
    return ''.join(parts)


def _is_landscape(im):
    """True only when both dimensions are known and width exceeds height. Missing or
    zero dimension keys are treated as not-landscape rather than raising."""
    w = im.get('full_width') or 0
    h = im.get('full_height') or 0
    return w > h


def etsy_cover_urls(sku):
    """Public mockup URLs from the matching Etsy listing, if there is one.

    Gumroad's cover endpoint crops to the image it's given, so a landscape mockup
    (e.g. the 1280x720 Gumroad tile) is put ahead of the square 2000x2000 ones rather
    than always handing Gumroad the square rank-1 image. Sort is stable, so relative
    order is otherwise unchanged.
    """
    try:
        from etsypub import db as etsy_db
        from etsypub.client import Etsy
        row = etsy_db.get(sku)
        if not row or not row.get('etsy_listing_id'):
            return []
        ims = Etsy().listing_images(row['etsy_listing_id']).get('results', [])
        ims = sorted(ims, key=lambda im: not _is_landscape(im))
        return [i['url_fullxfull'] for i in ims if i.get('url_fullxfull')]
    except Exception:                                              # noqa: BLE001
        return []


def check(s):
    problems = []
    for f in deliverables(s):
        if not os.path.exists(os.path.join(etsy_config.OUT, f)):
            problems.append('missing deliverable: %s' % f)
    if not s.get('blurb') or not s.get('bullets'):
        problems.append('missing description content')
    return problems


# ---------------------------------------------------------------------- work

def push(g, s):
    """Create-or-resume one Gumroad product. Safe to re-run."""
    row = ensure(s['sku'], s['price'])
    pid = row['product_id']

    if not pid:
        p = g.create_product(
            name=gumroad_name(s),
            price_cents=price_cents(s),
            description=description_html(s),
            permalink=permalink_for(s),
            tags=s['tags'][:10],
        )
        pid = p.get('id')
        if not pid:
            raise GumroadError('created but no id came back: %s' % p)
        # Recorded before anything else, so a retry resumes instead of duplicating.
        update(s['sku'], product_id=pid, permalink=p.get('custom_permalink'),
               url=p.get('short_url'), error=None)
        print('  created %s' % p.get('short_url'))
    else:
        print('  product exists (%s)' % row['url'])

    row = get(s['sku'])
    if not row['files_done']:
        urls = []
        for f in deliverables(s):
            u = g.upload_file(os.path.join(etsy_config.OUT, f), name=f)
            urls.append((u, f))
            print('  uploaded %s' % f)
        # set_files REPLACES the whole list — send them all at once.
        g.set_files(pid, urls)
        update(s['sku'], files_done=1)

    row = get(s['sku'])
    if not row['covers_done']:
        covers = etsy_cover_urls(s['sku'])
        if covers:
            for u in covers[:3]:
                g.set_cover(pid, u)
            update(s['sku'], covers_done=1)
            print('  %d cover(s) set from the Etsy listing' % len(covers[:3]))
        else:
            print('  NO COVERS — no Etsy listing to source public image URLs from')
    return get(s['sku'])


def refresh(skus, *, dry_run=False, limit=None):
    """Re-push already-existing products: clear `files_done` / `covers_done` and call
    `push()` again, so the rebuilt PDFs and the now-landscape-first covers
    (`etsy_cover_urls`) actually reach Gumroad instead of staying stuck on whatever was
    uploaded the first time.

    Never creates a product -- a SKU with no `product_id` yet is reported and skipped,
    not pushed. `--dry-run` makes no network call at all: it does not even construct a
    `Gumroad()` client.
    """
    ensure_all()
    by_name = {s['sku']: s for s in build_etsy_kit.SKUS}
    chosen = [by_name[n] for n in skus] if skus else list(build_etsy_kit.SKUS)
    if limit:
        chosen = chosen[:limit]

    targets, skipped = [], []
    for s in chosen:
        row = get(s['sku'])
        if row and row.get('product_id'):
            targets.append(s)
        else:
            skipped.append(s['sku'])

    if skipped:
        print('SKIPPED (not created yet -- --refresh never creates):')
        for sku in skipped:
            print('    - %s' % sku)

    if dry_run:
        print('\nDRY RUN -- nothing sent to Gumroad.\n')
        for s in targets:
            r = get(s['sku']) or {}
            print('  %-28s %-8s -> clear files_done/covers_done, re-push (%s)'
                  % (s['sku'], s['price'], r.get('url', '')))
        return

    if not targets:
        print('\nNothing to refresh.')
        return

    g = Gumroad()
    done, failed = [], []
    for i, s in enumerate(targets):
        print('\n%s' % s['sku'])
        try:
            update(s['sku'], files_done=0, covers_done=0)
            push(g, s)
            done.append(s['sku'])
            print('  refreshed (files + covers re-uploaded)')
        except Exception as exc:                                   # noqa: BLE001
            failed.append(s['sku'])
            update(s['sku'], error=str(exc))
            print('  FAILED: %s' % exc)
        if i < len(targets) - 1:
            time.sleep(random.uniform(*JITTER))

    print('\nrefresh: %d ok, %d failed' % (len(done), len(failed)))


def run(skus, *, dry_run=False, do_publish=False, limit=None):
    ensure_all()
    by_name = {s['sku']: s for s in build_etsy_kit.SKUS}
    chosen = [by_name[n] for n in skus] if skus else list(build_etsy_kit.SKUS)
    if limit:
        chosen = chosen[:limit]

    ready, blocked = [], {}
    for s in chosen:
        probs = check(s)
        (blocked.setdefault(s['sku'], probs) if probs else ready.append(s))

    for sku, probs in blocked.items():
        print('BLOCKED %s' % sku)
        for p in probs:
            print('    - %s' % p)

    if dry_run:
        print('\nDRY RUN — nothing sent to Gumroad.\n')
        for s in ready:
            r = get(s['sku']) or {}
            print('  %-28s %-8s %-12s -> %s'
                  % (s['sku'], s['price'],
                     'exists' if r.get('product_id') else 'new',
                     'publish' if do_publish else 'create + upload'))
        print('\n  Gumroad charges no listing fee.')
        return

    g = Gumroad()
    done, failed = [], []
    for i, s in enumerate(ready):
        print('\n%s' % s['sku'])
        try:
            if do_publish:
                row = get(s['sku'])
                if not row or not row['product_id']:
                    raise GumroadError('not created yet — run without --publish first')
                g.publish(row['product_id'])
                update(s['sku'], published=1)
                print('  PUBLISHED -> %s' % row['url'])
            else:
                push(g, s)
            done.append(s['sku'])
        except Exception as exc:                                   # noqa: BLE001
            failed.append(s['sku'])
            update(s['sku'], error=str(exc))
            print('  FAILED: %s' % exc)
            # STOP THE WHOLE PASS on a quota or rate-limit wall. Continuing means
            # hammering the API with calls that cannot succeed — which is how a
            # daily cap turned into 429s. The next scheduled run retries cleanly.
            msg = str(exc).lower()
            if 'per day' in msg or '429' in msg or 'retry later' in msg:
                remaining = len(ready) - i - 1
                print('\n  STOPPING THIS PASS — Gumroad is refusing further creates.')
                print('  %d SKU(s) not attempted. The next scheduled run picks them up.'
                      % remaining)
                break
        if i < len(ready) - 1:
            time.sleep(random.uniform(*JITTER))

    print('\n%s: %d ok, %d failed' % ('publish' if do_publish else 'create',
                                      len(done), len(failed)))


def verify(g, sku):
    """Is this product actually fit to go public? Returns a list of problems."""
    row = get(sku)
    if not row or not row['product_id']:
        return ['not created']
    try:
        p = g.product(row['product_id'])
    except GumroadError as e:
        return ['cannot read from Gumroad: %s' % e]
    problems = []
    if not p.get('files'):
        problems.append('NO FILE ATTACHED — buyers would get nothing')
    if not (p.get('description') or '').strip():
        problems.append('empty description')
    if not p.get('name'):
        problems.append('no name')
    # A zero price is a defect UNLESS the SKU is deliberately free — the Start Here
    # lead magnet is $0.00 on purpose, and a blanket check would keep it a draft forever.
    intended = {s['sku']: s['price'] for s in build_etsy_kit.SKUS}.get(sku, '')
    deliberately_free = intended.strip() in ('$0', '$0.00', '0')
    if p.get('price') in (None, 0) and not deliberately_free:
        problems.append('price is zero')
    return problems


def finish():
    """Create whatever is left, verify everything, then publish what passes.

    Written for an unattended run: the 10-per-day creation cap means the catalogue is
    loaded across two days, and this is the second half. Nothing goes public without a
    file attached — a published Gumroad product with no download is worse than no product.
    """
    init_db()
    g = Gumroad()

    print('=== STEP 1: create anything still missing ===')
    run(None)

    print('\n=== STEP 2: verify ===')
    ok, bad = [], {}
    for s in build_etsy_kit.SKUS:
        problems = verify(g, s['sku'])
        if problems:
            bad[s['sku']] = problems
            print('  FAIL %-28s %s' % (s['sku'], '; '.join(problems)))
        else:
            ok.append(s['sku'])
            print('  ok   %s' % s['sku'])

    if bad:
        print('\n%d product(s) not fit to publish — leaving them as drafts.' % len(bad))
    if not ok:
        print('Nothing to publish.')
        return

    print('\n=== STEP 3: publish %d verified product(s) ===' % len(ok))
    run(ok, do_publish=True)

    print('\n=== RESULT ===')
    status()


def _live_permalink(p):
    """A live product's stable identifier: custom_permalink, falling back to the
    auto-assigned permalink when custom_permalink is absent or empty."""
    return p.get('custom_permalink') or p.get('permalink')


def reconcile(g=None, live=None):
    """Repair local db rows against what Gumroad actually holds.

    The db has drifted before: a product created and recorded, then deleted (or never
    finished) on Gumroad's side, leaves the row claiming product_id/url/published that
    no longer correspond to anything live. Trust the API, not the row.

    Matches each catalogue SKU to a live product on permalink (see _live_permalink),
    since that is the stable value chosen at creation time (permalink_for). A SKU with
    no live match has product_id/url/published cleared so the creation path picks it
    up again -- price is left untouched, it is not a Gumroad fact. A SKU with a live
    match has product_id/url/published set from the API response.

    Every catalogue SKU gets a db row first (ensure_all) so a SKU with no row yet --
    e.g. one just added to build_etsy_kit.SKUS -- is not silently skipped.

    Returns a list of (sku, before, after) for every row actually changed. Idempotent:
    a second call against the same live state makes no changes and returns [].
    """
    ensure_all()
    g = g or Gumroad()
    if live is None:
        live = g.products()

    by_permalink = {}
    for p in live:
        pl = _live_permalink(p)
        if pl:
            by_permalink[pl] = p

    corrections = []
    for s in build_etsy_kit.SKUS:
        sku = s['sku']
        before = get(sku)
        p = by_permalink.get(permalink_for(s))
        if p:
            fields = {'product_id': p.get('id'), 'url': p.get('short_url'),
                     'published': 1 if p.get('published') else 0}
        else:
            fields = {'product_id': None, 'url': None, 'published': 0}

        if any(before.get(k) != fields.get(k) for k in fields):
            update(sku, **fields)
            corrections.append((sku, before, get(sku)))

    return corrections


def status():
    try:
        g = Gumroad()
        live = g.products()
    except GumroadError as e:
        # No live data to reconcile against -- fall back to printing local state as-is.
        ensure_all()
        print('%-28s %-9s %-10s %s' % ('SKU', 'PRICE', 'STATE', 'URL'))
        for r in all_rows():
            print('%-28s %-9s %-10s %s'
                  % (r['sku'], r['price'] or '',
                     'published' if r['published'] else 'draft', r['url'] or ''))
        print('\nCannot reach Gumroad: %s' % e)
        return

    # Deliberately reconciled BEFORE the table is printed, not after: the table is what
    # a human skimming --status actually reads, and showing a stale "published" for a
    # product reconcile already knows is gone is the exact bug this module exists to
    # catch, just moved into the display layer. Do not reorder this to match
    # etsypub.publish.status() (which reconciles after printing) -- that's a separate,
    # already-proven-against-live-listings tool; this ordering is deliberate here.
    corrections = reconcile(g, live)

    rows = all_rows()
    print('%-28s %-9s %-10s %s' % ('SKU', 'PRICE', 'STATE', 'URL'))
    for r in rows:
        print('%-28s %-9s %-10s %s'
              % (r['sku'], r['price'] or '',
                 'published' if r['published'] else 'draft', r['url'] or ''))

    if corrections:
        print('\nReconciled against Gumroad:')
        for sku, before, after in corrections:
            if after['product_id']:
                print('   %s: matched a live product -> product_id=%s published=%s'
                      % (sku, after['product_id'], 'yes' if after['published'] else 'no'))
            else:
                print('   %s: NOT ON GUMROAD (db said published=%s) -- reset to '
                     'not-created, the next create pass will pick it up'
                     % (sku, 'yes' if before['published'] else 'no'))
    else:
        print('\nLocal state matches Gumroad.')

    print('\nGumroad holds %d product(s):' % len(live))
    for p in live:
        print('   %-9s %-10s %s' % (p.get('formatted_price'),
                                    'published' if p.get('published') else 'draft',
                                    p.get('name', '')[:70]))

    published_local = sum(1 for r in all_rows() if r['published'])
    if published_local != len(live):
        print('\n*** WARNING: db marks %d SKU(s) published, but Gumroad holds only '
             '%d product(s) total -- see the reconciliation above ***'
             % (published_local, len(live)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skus', help='comma-separated SKU names (default: all)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--publish', action='store_true', help='flip created products live')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--finish', action='store_true',
                    help='create whatever is left, verify, then publish what passes')
    ap.add_argument('--refresh', action='store_true',
                    help='re-push files + covers for already-existing products; '
                         'never creates')
    ap.add_argument('--limit', type=int)
    a = ap.parse_args()

    if a.status:
        status()
        return
    if a.finish:
        finish()
        return
    skus = [s.strip() for s in a.skus.split(',')] if a.skus else None
    if a.refresh:
        refresh(skus, dry_run=a.dry_run, limit=a.limit)
        return
    run(skus, dry_run=a.dry_run, do_publish=a.publish, limit=a.limit)


if __name__ == '__main__':
    main()
