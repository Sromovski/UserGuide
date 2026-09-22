#!/usr/bin/env python3
"""Build Pinterest pins for every SKU x template combination.

Renders `pins.templates.TEMPLATES` for every SKU in `pins.copy.SKUS`, writes
each PNG to `outputs/pins/<sku>/<template>.png`, runs the overflow guard and
the destination guard, and writes `outputs/pins/PINS.csv` -- the worklist the
owner uploads from.

One title and one description per SKU, reused across every template pin for
that SKU -- see pins/copy.py. The `template` column in the CSV is how the
owner tells the variants apart; it is not a second title.

A template returning None is an honest skip (see pins/templates.py), not a
build failure. A missing/short title, a missing description or a dead URL
IS a build failure -- a pin that points nowhere is worse than no pin.
"""
import csv
import os

from PIL import Image

from covers import palette
from pins import canvas
from pins import copy as pc
from pins import templates as _templates

ROOT = r'C:\Projects\UserGuide'
OUT = os.path.join(ROOT, 'outputs', 'pins')

TITLE_LIMIT = 100


def build(skus=None, templates=None):
    """Render every (sku, template) pair, write PNGs, return row dicts."""
    skus = skus if skus is not None else pc.SKUS
    names = templates if templates is not None else list(_templates.TEMPLATES)

    rows = []
    for sku in skus:
        pal = palette.get(pc.palette_key_for(sku))
        sku_dir = os.path.join(OUT, sku)
        for name in names:
            fn = _templates.TEMPLATES[name]
            img = fn(sku, pal)
            if img is None:
                continue
            os.makedirs(sku_dir, exist_ok=True)
            path = os.path.join(sku_dir, '%s.png' % name)
            img.save(path, 'PNG', optimize=True)
            rows.append({
                'sku': sku,
                'template': name,
                'file': path,
                'title': pc.TITLES.get(sku, ''),
                'description': pc.DESCRIPTIONS.get(sku, ''),
                'url': pc.url_for(sku),
                'board': pc.BOARD_FOR.get(sku, ''),
            })
    return rows


def verify_no_overflow(rows):
    """Fail the build rather than ship a pin with ink in the margin band."""
    offenders = []
    pals = {}
    for r in rows:
        sku = r['sku']
        if sku not in pals:
            pals[sku] = palette.get(pc.palette_key_for(sku))
        pal = pals[sku]
        img = Image.open(r['file']).convert('RGB')
        if canvas.overflows(img, pal):
            offenders.append('%s/%s -> %s' % (sku, r['template'], r['file']))
    if offenders:
        for o in offenders:
            print('OVERFLOW  ' + o)
        raise SystemExit('%d pin(s) overflow the margin band — %s'
                          % (len(offenders), ', '.join(offenders)))


def verify_destinations(rows):
    """Fail the build on any missing title/description/url, an over-long
    title, or a url that does not start `http`.

    Collects every offender before raising -- a guard that stops at the
    first problem makes the next run find only the next one.
    """
    offenders = []
    for r in rows:
        who = '%s/%s' % (r['sku'], r['template'])
        title = r.get('title') or ''
        description = r.get('description') or ''
        url = r.get('url') or ''
        if not title:
            offenders.append('%s: missing title' % who)
        elif len(title) > TITLE_LIMIT:
            offenders.append('%s: title is %d chars, limit %d'
                              % (who, len(title), TITLE_LIMIT))
        if not description:
            offenders.append('%s: missing description' % who)
        if not url:
            offenders.append('%s: missing url' % who)
        elif not url.startswith('http'):
            offenders.append('%s: url does not start with http -- %r'
                              % (who, url))
    if offenders:
        for o in offenders:
            print('BAD DESTINATION  ' + o)
        raise SystemExit('%d pin(s) have a bad destination — %s'
                          % (len(offenders), '; '.join(offenders)))


def write_csv(rows):
    """Write outputs/pins/PINS.csv, the owner's upload worklist."""
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'PINS.csv')
    fields = ['sku', 'template', 'file', 'title', 'description', 'url', 'board']
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return path


def main():
    rows = build()

    verify_no_overflow(rows)
    verify_destinations(rows)

    path = write_csv(rows)

    tally = {}
    for r in rows:
        tally[r['template']] = tally.get(r['template'], 0) + 1
    skips = []
    for sku in pc.SKUS:
        rendered = {r['template'] for r in rows if r['sku'] == sku}
        for name in _templates.TEMPLATES:
            if name not in rendered:
                skips.append('%s/%s' % (sku, name))

    print('%d pins across %d SKUs' % (len(rows), len(pc.SKUS)))
    for name in sorted(tally):
        print('  %-12s %d' % (name, tally[name]))
    if skips:
        print('%d skip(s) (template returned None -- no curated content):' % len(skips))
        for s in skips:
            print('  SKIP %s' % s)
    print('CSV: %s' % path)


if __name__ == '__main__':
    main()
