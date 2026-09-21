"""gumroadpub.publish.status() used to print local db state and what Gumroad holds as
two disconnected facts -- nothing ever compared them. The db drifted from reality
(products deleted or never finished on Gumroad's side) and nothing flagged it: 21 SKUs
recorded as published while Gumroad held 10 products, silently.

reconcile() fixes that: it fetches the live product list and repairs each db row from
it. These tests fake the Gumroad client entirely -- no network -- and point the db at a
tmp_path sqlite file by monkeypatching the module's DB constant.
"""
from __future__ import annotations

import sqlite3

import build_etsy_kit
from gumroadpub import publish


FAKE_SKUS = [
    {'sku': 'aa-widget', 'price': '$9.99'},
    {'sku': 'bb-gadget', 'price': '$4.99'},
    {'sku': 'cc-gizmo', 'price': '$7.99'},
    {'sku': 'dd-thing', 'price': '$1.99'},
]


class FakeGumroad:
    def __init__(self, products):
        self._products = products
        self.calls = 0

    def products(self):
        self.calls += 1
        return self._products


def _use_tmp_db(monkeypatch, tmp_path):
    db_path = str(tmp_path / 'gumroad_test.db')
    monkeypatch.setattr(publish, 'DB', db_path)
    monkeypatch.setattr(build_etsy_kit, 'SKUS', FAKE_SKUS)
    publish.init_db()
    return db_path


def _seed(sku, **fields):
    publish.ensure(sku, next(s['price'] for s in FAKE_SKUS if s['sku'] == sku))
    publish.update(sku, **fields)


def test_row_marked_published_whose_product_is_absent_gets_cleared(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed('aa-widget', product_id='OLD-ID', url='https://sromov.gumroad.com/l/widget',
         published=1)
    live = []          # nothing live at all -- including no product for any other SKU

    corrections = publish.reconcile(FakeGumroad(live))

    row = publish.get('aa-widget')
    assert row['product_id'] is None
    assert row['url'] is None
    assert row['published'] == 0
    assert row['price'] == '$9.99'          # price is not a Gumroad fact -- untouched
    assert [c[0] for c in corrections] == ['aa-widget']


def test_row_whose_product_is_present_gets_fields_set_from_api(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    live = [{'id': 'NEW-ID', 'custom_permalink': 'gadget',
             'short_url': 'https://sromov.gumroad.com/l/gadget', 'published': True}]

    corrections = publish.reconcile(FakeGumroad(live))

    row = publish.get('bb-gadget')
    assert row['product_id'] == 'NEW-ID'
    assert row['url'] == 'https://sromov.gumroad.com/l/gadget'
    assert row['published'] == 1
    assert [c[0] for c in corrections] == ['bb-gadget']


def test_reconcile_is_idempotent(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed('aa-widget', product_id='OLD-ID', published=1)
    live = [{'id': 'NEW-ID', 'custom_permalink': 'gadget',
             'short_url': 'https://sromov.gumroad.com/l/gadget', 'published': True}]

    first = publish.reconcile(FakeGumroad(live))
    second = publish.reconcile(FakeGumroad(live))

    assert first != []
    assert second == []


def test_sku_with_no_db_row_gets_one_created(monkeypatch, tmp_path):
    db_path = _use_tmp_db(monkeypatch, tmp_path)
    # 'dd-thing' has never been touched -- no row exists yet.
    assert publish.get('dd-thing') is None

    publish.reconcile(FakeGumroad([]))

    row = publish.get('dd-thing')
    assert row is not None
    assert row['price'] == '$1.99'
    assert row['product_id'] is None
    assert row['published'] == 0
    con = sqlite3.connect(db_path)
    try:
        n = con.execute('SELECT COUNT(*) FROM gumroad_listings').fetchone()[0]
    finally:
        con.close()
    assert n == len(FAKE_SKUS)


def test_matching_falls_back_to_permalink_when_custom_permalink_missing_or_empty(
        monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    live = [
        {'id': 'GIZMO-1', 'permalink': 'gizmo', 'custom_permalink': '',
         'short_url': 'https://sromov.gumroad.com/l/gizmo', 'published': False},
        {'id': 'THING-1', 'permalink': 'thing',
         'short_url': 'https://sromov.gumroad.com/l/thing', 'published': True},
    ]

    publish.reconcile(FakeGumroad(live))

    offenders = []
    expected = {'cc-gizmo': ('GIZMO-1', 0), 'dd-thing': ('THING-1', 1)}
    for sku, (pid, published) in expected.items():
        row = publish.get(sku)
        if row['product_id'] != pid or row['published'] != published:
            offenders.append('%s: got product_id=%r published=%r'
                             % (sku, row['product_id'], row['published']))
    assert offenders == []
