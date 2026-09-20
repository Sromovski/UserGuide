"""Gumroad's cover endpoint takes a public image URL and crops it -- feeding it the
square rank-1 mockup (2000x2000) crops out most of the design. etsy_cover_urls() should
prefer a landscape mockup (e.g. the 1280x720 Gumroad tile) when one exists among the
listing's images. No network calls: Etsy and etsypub.db are both faked.
"""
from __future__ import annotations

from etsypub import db as etsy_db
from etsypub.client import Etsy
from gumroadpub.publish import etsy_cover_urls


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
