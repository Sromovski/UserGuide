"""gumroadpub.client.Gumroad.products() used to return only the first page of
`GET /v2/products`, which is paginated (10 products/page, `next_page_key` +
`next_page_url` present when more remain). That truncation caused real damage: a
reconciliation run built on the truncated list concluded 11 live products did not
exist, reset their db rows to "not created", and triggered 9 create attempts Gumroad
rejected as duplicate permalinks. Nothing was destroyed only because Gumroad refuses
duplicate permalinks.

These tests fake `Gumroad._req` directly (no network) and drive `products()` through
multi-page, single-page, and pathological (never-ending) response sequences.
"""
from __future__ import annotations

import pytest

from gumroadpub.client import Gumroad, GumroadError


def _client():
    return Gumroad(token='fake-token')


def test_products_follows_pagination_across_three_pages():
    g = _client()
    pages = {
        '/products': {
            'success': True,
            'products': [{'id': '1'}, {'id': '2'}],
            'next_page_key': 'key-a',
            'next_page_url': '/v2/products?page_key=key-a',
        },
        '/products?page_key=key-a': {
            'success': True,
            'products': [{'id': '3'}, {'id': '4'}],
            'next_page_key': 'key-b',
            'next_page_url': '/v2/products?page_key=key-b',
        },
        '/products?page_key=key-b': {
            'success': True,
            'products': [{'id': '5'}],
        },
    }
    calls = []

    def fake_req(method, path, **kw):
        calls.append((method, path))
        return pages[path]

    g._req = fake_req

    out = g.products()

    assert [p['id'] for p in out] == ['1', '2', '3', '4', '5']
    assert calls == [
        ('GET', '/products'),
        ('GET', '/products?page_key=key-a'),
        ('GET', '/products?page_key=key-b'),
    ]


def test_products_stops_on_a_final_page_with_no_next_page_url():
    g = _client()

    def fake_req(method, path, **kw):
        assert path == '/products'
        return {'success': True, 'products': [{'id': 'only'}]}

    g._req = fake_req

    out = g.products()

    assert [p['id'] for p in out] == ['only']


def test_products_never_doubles_the_v2_prefix_when_following_next_page_url():
    g = _client()
    pages = {
        '/products': {
            'success': True,
            'products': [{'id': '1'}],
            'next_page_url': '/v2/products?page_key=key-a',
        },
        '/products?page_key=key-a': {
            'success': True,
            'products': [{'id': '2'}],
        },
    }
    calls = []

    def fake_req(method, path, **kw):
        calls.append(path)
        return pages[path]

    g._req = fake_req

    g.products()

    offenders = [p for p in calls if '/v2/v2' in p or p.startswith('/v2/products')]
    assert offenders == []


def test_products_raises_rather_than_returning_a_partial_list_at_the_page_cap():
    g = _client()
    g.MAX_PRODUCT_PAGES = 3          # keep the test fast; behaviour is cap-size agnostic
    seen = []

    def fake_req(method, path, **kw):
        n = len(seen)
        seen.append(path)
        # Never-ending: every page claims there is another one after it.
        return {
            'success': True,
            'products': [{'id': str(n)}],
            'next_page_url': '/v2/products?page_key=page-%d' % (n + 1),
        }

    g._req = fake_req

    with pytest.raises(GumroadError):
        g.products()

    # It must have actually tried pages, not failed some other way immediately.
    assert len(seen) >= g.MAX_PRODUCT_PAGES
