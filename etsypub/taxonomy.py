"""Find the numeric taxonomy id for the category these listings go in.

    python -m etsypub.taxonomy --search digital
    python -m etsypub.taxonomy --search "paper party"
    python -m etsypub.taxonomy --top            # just the top-level categories

The seller taxonomy is PUBLIC — it needs only the x-api-key header, no OAuth token. So
this runs before the consent step, not after it.

Etsy's category tree changes, so this reads it live rather than hardcoding an id that
quietly rots. Pick one, put it in .env as ETSY_TAXONOMY_ID, and keep every listing on it
— a shop whose products sit in one coherent category ranks better than one scattered
across five.
"""
from __future__ import annotations

import argparse

import requests

from . import config
from .client import BASE, EtsyError


def fetch_nodes() -> list[dict]:
    r = requests.get(BASE + '/seller-taxonomy/nodes',
                     headers={'x-api-key': config.api_key()}, timeout=60)
    if not r.ok:
        raise EtsyError('seller-taxonomy/nodes -> %s: %s' % (r.status_code, r.text[:300]))
    return r.json().get('results', [])


def walk(nodes: list[dict], trail: tuple[str, ...] = ()):
    """Yield (node, 'A > B > C') for every node, depth first."""
    for n in nodes:
        path = trail + (n.get('name', ''),)
        yield n, ' > '.join(path)
        yield from walk(n.get('children') or [], path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--search', default='digital',
                    help='case-insensitive substring matched against the full path')
    ap.add_argument('--top', action='store_true', help='list top-level categories only')
    ap.add_argument('--limit', type=int, default=40)
    a = ap.parse_args()

    if not config.KEYSTRING or not config.SHARED_SECRET:
        raise SystemExit('Set ETSY_KEYSTRING and ETSY_SHARED_SECRET in .env first.')

    tree = fetch_nodes()

    if a.top:
        print('%-10s %s' % ('ID', 'CATEGORY'))
        for n in tree:
            print('%-10s %s' % (n['id'], n.get('name', '')))
        return

    needle = a.search.lower()
    hits = [(n['id'], path) for n, path in walk(tree) if needle in path.lower()]
    if not hits:
        print('Nothing matched %r. Try --top to see the top-level categories.' % a.search)
        return

    print('%-10s %s' % ('ID', 'CATEGORY'))
    for tid, path in hits[:a.limit]:
        print('%-10s %s' % (tid, path))
    if len(hits) > a.limit:
        print('... %d more (raise --limit)' % (len(hits) - a.limit))
    print('\nPut your pick in .env as  ETSY_TAXONOMY_ID=<id>')


if __name__ == '__main__':
    main()
