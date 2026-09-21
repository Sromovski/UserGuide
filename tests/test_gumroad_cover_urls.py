"""Gumroad's cover endpoint takes a public image URL and crops it -- feeding it the
square rank-1 mockup (2000x2000) crops out most of the design. etsy_cover_urls() should
prefer a landscape mockup (e.g. the 1280x720 Gumroad tile) when one exists among the
listing's images. No network calls: Etsy and etsypub.db are both faked.
"""
from __future__ import annotations

from etsypub import db as etsy_db
from etsypub.client import Etsy
from gumroadpub.publish import PUBLIC_COVERS, etsy_cover_urls


class FakeEtsy:
    def __init__(self, results):
        self._results = results

    def listing_images(self, listing_id):
        return {'results': self._results}


def _use(monkeypatch, results, listing_id=42):
    monkeypatch.setattr(etsy_db, 'get', lambda sku: {'etsy_listing_id': listing_id})
    monkeypatch.setattr('etsypub.client.Etsy', lambda: FakeEtsy(results))


def test_landscape_image_sorts_ahead_of_square(monkeypatch):
    square = {'listing_image_id': 1, 'url_fullxfull': 'http://img/square',
              'full_width': 2000, 'full_height': 2000}
    wide = {'listing_image_id': 2, 'url_fullxfull': 'http://img/wide',
            'full_width': 1280, 'full_height': 720}
    _use(monkeypatch, [square, wide])

    urls = etsy_cover_urls('some-sku')

    assert urls[0] == 'http://img/wide'
    assert urls[1] == 'http://img/square'


def test_stable_order_among_equally_landscape_or_equally_square(monkeypatch):
    a = {'listing_image_id': 1, 'url_fullxfull': 'http://img/a',
         'full_width': 2000, 'full_height': 2000}
    b = {'listing_image_id': 2, 'url_fullxfull': 'http://img/b',
         'full_width': 2000, 'full_height': 2000}
    c = {'listing_image_id': 3, 'url_fullxfull': 'http://img/c',
         'full_width': 1280, 'full_height': 720}
    _use(monkeypatch, [a, b, c])

    urls = etsy_cover_urls('some-sku')

    # c is the only landscape image, so it comes first; a and b keep their relative order.
    assert urls == ['http://img/c', 'http://img/a', 'http://img/b']


def test_tolerates_images_missing_dimension_keys(monkeypatch):
    no_dims = {'listing_image_id': 1, 'url_fullxfull': 'http://img/no-dims'}
    wide = {'listing_image_id': 2, 'url_fullxfull': 'http://img/wide',
            'full_width': 1280, 'full_height': 720}
    _use(monkeypatch, [no_dims, wide])

    urls = etsy_cover_urls('some-sku')

    assert urls == ['http://img/wide', 'http://img/no-dims']


# ------------------------------------------------------- PUBLIC_COVERS fallback
#
# 12-start-here is the free lead magnet -- it has no Etsy listing, because Etsy has
# no free tier -- so it would otherwise ship with zero Gumroad covers (a blank tile).
# Its covers are committed to this repo and served from raw.githubusercontent.com
# instead. The fallback must apply whenever the Etsy lookup yields nothing, whatever
# the reason: no db row, no listing id, or the lookup raising outright.

def test_public_cover_sku_with_no_etsy_row_returns_public_urls(monkeypatch):
    monkeypatch.setattr(etsy_db, 'get', lambda sku: None)

    urls = etsy_cover_urls('12-start-here')

    assert urls == PUBLIC_COVERS['12-start-here']


def test_public_cover_sku_whose_etsy_lookup_raises_returns_public_urls(monkeypatch):
    def _boom(sku):
        raise RuntimeError('db is unreachable')
    monkeypatch.setattr(etsy_db, 'get', _boom)

    urls = etsy_cover_urls('12-start-here')

    assert urls == PUBLIC_COVERS['12-start-here']


def test_etsy_listing_takes_priority_over_public_fallback(monkeypatch):
    # 12-start-here doesn't actually have a listing today, but if it ever did, real
    # listing images must win -- the fallback must not shadow them.
    wide = {'listing_image_id': 1, 'url_fullxfull': 'http://img/etsy-wide',
            'full_width': 1280, 'full_height': 720}
    _use(monkeypatch, [wide])

    urls = etsy_cover_urls('12-start-here')

    assert urls == ['http://img/etsy-wide']


def test_sku_with_neither_etsy_nor_public_cover_returns_empty_list(monkeypatch):
    monkeypatch.setattr(etsy_db, 'get', lambda sku: None)

    urls = etsy_cover_urls('some-sku-with-nothing')

    assert urls == []


def test_public_covers_are_ordered_wide_then_square():
    offenders = []
    for sku, urls in PUBLIC_COVERS.items():
        if len(urls) < 2:
            continue
        if 'wide' not in urls[0] or 'square' not in urls[1]:
            offenders.append('%s: %r' % (sku, urls))
    assert offenders == [], '\n'.join(offenders)
