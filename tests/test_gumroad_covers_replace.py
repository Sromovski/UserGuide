"""`client.set_cover()` POSTs to `/products/{id}/covers`, which APPENDS a cover -- it
never replaces one. `publish.push()` used to call it in a loop with no clearing step
first, so every `--refresh` grew the cover list instead of replacing it. Observed live
on `02-starter-volume`: a single `--refresh` took it from 3 covers to 6, and because
Gumroad's storefront thumbnail is whichever cover is `main_cover_id` (effectively the
first one), the three stale square covers stayed in front and the new landscape image
-- the whole point of which is to stop Gumroad cropping the cover -- landed at
position 4.

`DELETE /v2/products/{product_id}/covers/{cover_id}` is undocumented but verified
working (2026-09-20). `client.clear_covers()` fetches the product and deletes every
cover it reports; `publish.push()` now calls it before re-adding covers, so the result
is exactly the intended set with the landscape image (etsy_cover_urls sorts
landscape-first) first -- which Gumroad then makes `main_cover_id` automatically.

All network is faked: the client tests fake `Gumroad._req` directly, and the push()
tests fake the whole client plus `etsy_cover_urls`. No real Gumroad or Etsy call is
ever made.
"""
from __future__ import annotations

import build_etsy_kit
from gumroadpub import publish
from gumroadpub.client import Gumroad


# --------------------------------------------------------------- client.clear_covers

def _client():
    return Gumroad(token='fake-token')


def test_clear_covers_deletes_every_cover_the_product_reports_and_returns_the_count():
    g = _client()
    covers = [{'id': 'c1'}, {'id': 'c2'}, {'id': 'c3'}]
    calls = []

    def fake_req(method, path, **kw):
        calls.append((method, path))
        if method == 'GET':
            return {'success': True, 'product': {'covers': covers}}
        return {'success': True, 'covers': [], 'main_cover_id': None}

    g._req = fake_req

    n = g.clear_covers('PID')

    assert n == 3
    delete_calls = [c for c in calls if c[0] == 'DELETE']
    assert delete_calls == [
        ('DELETE', '/products/PID/covers/c1'),
        ('DELETE', '/products/PID/covers/c2'),
        ('DELETE', '/products/PID/covers/c3'),
    ]


def test_clear_covers_on_a_product_with_no_covers_deletes_nothing_and_returns_zero():
    g = _client()

    def fake_req(method, path, **kw):
        if method == 'GET':
            return {'success': True, 'product': {'covers': []}}
        raise AssertionError('DELETE must not be called when there are no covers')

    g._req = fake_req

    n = g.clear_covers('PID')

    assert n == 0


def test_clear_covers_raises_but_reports_how_many_it_removed_before_failing():
    """A mid-loop DELETE failure must not lose the partial progress: the exception it
    raises carries how many covers were actually removed, so a caller (push()) can log
    the true partial state instead of implying the clear either fully succeeded or did
    nothing at all."""
    g = _client()
    covers = [{'id': 'c1'}, {'id': 'c2'}, {'id': 'c3'}, {'id': 'c4'}]
    calls = []

    def fake_req(method, path, **kw):
        calls.append((method, path))
        if method == 'GET':
            return {'success': True, 'product': {'covers': covers}}
        if path.endswith('/c3'):
            raise RuntimeError('S3/API hiccup deleting c3')
        return {'success': True, 'covers': [], 'main_cover_id': None}

    g._req = fake_req

    try:
        g.clear_covers('PID')
        raise AssertionError('expected clear_covers to raise')
    except RuntimeError as exc:
        assert getattr(exc, 'covers_removed', None) == 2

    delete_calls = [c for c in calls if c[0] == 'DELETE']
    assert delete_calls == [
        ('DELETE', '/products/PID/covers/c1'),
        ('DELETE', '/products/PID/covers/c2'),
        ('DELETE', '/products/PID/covers/c3'),
    ]


# ---------------------------------------------------------------------- publish.push

FAKE_SKUS = [
    {'sku': 'aa-widget', 'price': '$9.99'},
    {'sku': 'bb-gadget', 'price': '$4.99'},
]


class FakeGumroadClient:
    """Records every call in order, so ordering (not just counts) can be asserted."""

    def __init__(self):
        self.calls = []

    def create_product(self, **kw):
        self.calls.append(('create_product',))
        return {'id': 'PID', 'custom_permalink': 'widget',
                'short_url': 'https://sromov.gumroad.com/l/widget'}

    def upload_file(self, path, name=None):
        self.calls.append(('upload_file', name))
        return 'https://files.example/%s' % name

    def set_files(self, product_id, urls):
        self.calls.append(('set_files', product_id))

    def clear_covers(self, product_id):
        self.calls.append(('clear_covers', product_id))
        return 2

    def set_cover(self, product_id, url):
        self.calls.append(('set_cover', product_id, url))


def _use_tmp_db(monkeypatch, tmp_path):
    db_path = str(tmp_path / 'gumroad_test.db')
    monkeypatch.setattr(publish, 'DB', db_path)
    monkeypatch.setattr(build_etsy_kit, 'SKUS', FAKE_SKUS)
    publish.init_db()
    return db_path


def _seed_ready_for_covers(sku, price, product_id='PID'):
    """A product that already exists and already has its file uploaded -- only the
    cover step is untouched (covers_done=0), which isolates the behaviour under test."""
    publish.ensure(sku, price)
    publish.update(sku, product_id=product_id,
                   url='https://sromov.gumroad.com/l/%s' % sku,
                   files_done=1, covers_done=0)


def test_push_clears_covers_before_setting_any_of_them(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls',
                        lambda sku: ['http://img/wide', 'http://img/sq1',
                                     'http://img/sq2'])

    g = FakeGumroadClient()
    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})

    cover_calls = [c for c in g.calls if c[0] in ('clear_covers', 'set_cover')]
    assert cover_calls[0] == ('clear_covers', 'PID')
    assert all(c[0] == 'set_cover' for c in cover_calls[1:])


def test_push_still_caps_covers_at_three_and_sets_covers_done(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls',
                        lambda sku: ['http://img/1', 'http://img/2', 'http://img/3',
                                     'http://img/4', 'http://img/5'])

    g = FakeGumroadClient()
    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})

    set_cover_urls = [c[2] for c in g.calls if c[0] == 'set_cover']
    assert set_cover_urls == ['http://img/1', 'http://img/2', 'http://img/3']
    row = publish.get('aa-widget')
    assert row['covers_done'] == 1


def test_push_sets_the_landscape_url_first_since_etsy_cover_urls_sorts_it_first(
        monkeypatch, tmp_path):
    """etsy_cover_urls() sorts landscape-first (see test_gumroad_cover_urls.py) so
    that the landscape image becomes Gumroad's main_cover_id -- the storefront
    thumbnail -- once the old covers are cleared. This is the property that makes the
    whole fix matter: a first set_cover call that isn't the landscape image would
    leave the storefront thumbnail wrong even with clearing in place."""
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls',
                        lambda sku: ['http://img/landscape', 'http://img/square'])

    g = FakeGumroadClient()
    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})

    set_cover_calls = [c for c in g.calls if c[0] == 'set_cover']
    assert set_cover_calls[0][2] == 'http://img/landscape'


def test_push_clear_covers_runs_before_every_set_cover_call_ordered_call_log(
        monkeypatch, tmp_path):
    """A test that only counted calls would pass on the broken (append-only) code, so
    this asserts on the full ordered call log instead."""
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls',
                        lambda sku: ['http://img/a', 'http://img/b'])

    g = FakeGumroadClient()
    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})

    assert g.calls == [
        ('clear_covers', 'PID'),
        ('set_cover', 'PID', 'http://img/a'),
        ('set_cover', 'PID', 'http://img/b'),
    ]


def test_push_with_no_etsy_covers_never_calls_clear_covers(monkeypatch, tmp_path):
    """No point clearing a cover list we have nothing to replace it with."""
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls', lambda sku: [])

    g = FakeGumroadClient()
    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})

    assert g.calls == []
    row = publish.get('aa-widget')
    assert row['covers_done'] == 0


class FakeGumroadClientCoverDeleteFailsPartway(FakeGumroadClient):
    """Mirrors the real client.clear_covers() shape: deletes existing covers one at a
    time, and the failing delete raises an exception carrying `.covers_removed` --
    exactly like the real client -- rather than silently losing how far it got.
    """

    def __init__(self, existing_cover_ids, fail_at_index):
        super().__init__()
        self._existing = existing_cover_ids
        self._fail_at = fail_at_index

    def clear_covers(self, product_id):
        removed = 0
        for i, cover_id in enumerate(self._existing):
            self.calls.append(('delete_cover', product_id, cover_id))
            if i == self._fail_at:
                exc = RuntimeError('boom deleting cover %s' % cover_id)
                exc.covers_removed = removed
                raise exc
            removed += 1
        return removed


def test_push_still_sets_every_new_cover_when_clear_covers_fails_partway(
        monkeypatch, tmp_path):
    """A mid-loop DELETE failure must not leave the product with zero covers. push()
    must catch the clear_covers() failure, report it, and still run the full
    set_cover loop -- worst case is a few stale covers lingering alongside the correct
    ones, never a product with no cover image at all.
    """
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls',
                        lambda sku: ['http://img/a', 'http://img/b', 'http://img/c'])

    g = FakeGumroadClientCoverDeleteFailsPartway(
        existing_cover_ids=['old1', 'old2', 'old3', 'old4', 'old5'], fail_at_index=2)

    publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})          # must not raise

    assert g.calls == [
        ('delete_cover', 'PID', 'old1'),
        ('delete_cover', 'PID', 'old2'),
        ('delete_cover', 'PID', 'old3'),
        ('set_cover', 'PID', 'http://img/a'),
        ('set_cover', 'PID', 'http://img/b'),
        ('set_cover', 'PID', 'http://img/c'),
    ]
    row = publish.get('aa-widget')
    assert row['covers_done'] == 1


def test_push_still_raises_when_set_cover_itself_fails(monkeypatch, tmp_path):
    """clear_covers() failures are swallowed (see above), but a set_cover() failure is
    not -- there is nothing further push() can do for that product at that point, and
    the per-SKU handler in refresh()/run() must still see and record the error."""
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_ready_for_covers('aa-widget', '$9.99')
    monkeypatch.setattr(publish, 'etsy_cover_urls', lambda sku: ['http://img/a'])

    class FailingSetCoverClient(FakeGumroadClient):
        def set_cover(self, product_id, url):
            raise RuntimeError('set_cover boom')

    g = FailingSetCoverClient()
    try:
        publish.push(g, {'sku': 'aa-widget', 'price': '$9.99'})
        raise AssertionError('expected push() to propagate the set_cover failure')
    except RuntimeError as exc:
        assert 'set_cover boom' in str(exc)
