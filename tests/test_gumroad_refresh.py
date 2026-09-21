"""`push()` gates uploads behind sticky `files_done` / `covers_done` flags, so a product
created before covers went landscape-first (etsy_cover_urls, see
test_gumroad_cover_urls.py) keeps its old file and its old cropped-square cover forever.
`--refresh` clears those two flags for already-existing products and re-pushes them, so
the new PDFs and new landscape covers actually land on Gumroad.

It must never create a product -- only re-push existing ones -- and `--refresh
--dry-run` must not even construct a Gumroad client (no network at all).

All network is faked: `publish.push` and `publish.Gumroad` are monkeypatched, never the
real client.
"""
from __future__ import annotations

import sys

import build_etsy_kit
from gumroadpub import publish


FAKE_SKUS = [
    {'sku': 'aa-widget', 'price': '$9.99'},
    {'sku': 'bb-gadget', 'price': '$4.99'},
    {'sku': 'cc-gizmo', 'price': '$7.99'},
]


def _use_tmp_db(monkeypatch, tmp_path):
    db_path = str(tmp_path / 'gumroad_test.db')
    monkeypatch.setattr(publish, 'DB', db_path)
    monkeypatch.setattr(build_etsy_kit, 'SKUS', FAKE_SKUS)
    publish.init_db()
    return db_path


def _seed_existing(sku, price, **fields):
    publish.ensure(sku, price)
    base = {'product_id': 'PID-%s' % sku, 'url': 'https://sromov.gumroad.com/l/%s' % sku,
            'published': 1, 'files_done': 1, 'covers_done': 1}
    base.update(fields)
    publish.update(sku, **base)


class BoomIfConstructed:
    def __init__(self, *a, **k):
        raise AssertionError('Gumroad() must not be constructed during --refresh --dry-run')


def test_refresh_clears_flags_before_calling_push_for_each_existing_product(
        monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_existing('aa-widget', '$9.99')
    _seed_existing('bb-gadget', '$4.99')

    seen_flags_at_push_time = {}
    pushed = []

    def fake_push(g, s):
        row = publish.get(s['sku'])
        seen_flags_at_push_time[s['sku']] = (row['files_done'], row['covers_done'])
        pushed.append(s['sku'])
        return row

    monkeypatch.setattr(publish, 'push', fake_push)
    monkeypatch.setattr(publish, 'Gumroad', lambda *a, **k: object())
    monkeypatch.setattr(publish.time, 'sleep', lambda *a, **k: None)

    publish.refresh(None)

    assert sorted(pushed) == ['aa-widget', 'bb-gadget']
    offenders = [sku for sku, flags in seen_flags_at_push_time.items() if flags != (0, 0)]
    assert offenders == []


def test_refresh_dry_run_constructs_no_gumroad_client(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_existing('aa-widget', '$9.99')

    monkeypatch.setattr(publish, 'Gumroad', BoomIfConstructed)
    pushed = []
    monkeypatch.setattr(publish, 'push', lambda g, s: pushed.append(s['sku']))

    publish.refresh(None, dry_run=True)          # must not raise

    assert pushed == []


def test_refresh_never_creates_a_product_for_a_sku_with_no_product_id(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_existing('aa-widget', '$9.99')
    publish.ensure('cc-gizmo', '$7.99')           # never pushed -- no product_id at all

    pushed = []

    def fake_push(g, s):
        pushed.append(s['sku'])
        return publish.get(s['sku'])

    monkeypatch.setattr(publish, 'push', fake_push)
    monkeypatch.setattr(publish, 'Gumroad', lambda *a, **k: object())
    monkeypatch.setattr(publish.time, 'sleep', lambda *a, **k: None)

    publish.refresh(None)

    assert pushed == ['aa-widget']
    row = publish.get('cc-gizmo')
    assert row['product_id'] is None              # untouched -- refresh never creates


def test_refresh_honours_skus_and_limit(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_existing('aa-widget', '$9.99')
    _seed_existing('bb-gadget', '$4.99')
    _seed_existing('cc-gizmo', '$7.99')

    pushed = []

    def fake_push(g, s):
        pushed.append(s['sku'])
        return publish.get(s['sku'])

    monkeypatch.setattr(publish, 'push', fake_push)
    monkeypatch.setattr(publish, 'Gumroad', lambda *a, **k: object())
    monkeypatch.setattr(publish.time, 'sleep', lambda *a, **k: None)

    publish.refresh(['bb-gadget', 'cc-gizmo'], limit=1)

    assert pushed == ['bb-gadget']


def test_refresh_isolates_a_failure_in_one_sku_from_the_rest(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    _seed_existing('aa-widget', '$9.99')
    _seed_existing('bb-gadget', '$4.99')

    def fake_push(g, s):
        if s['sku'] == 'aa-widget':
            raise RuntimeError('boom')
        return publish.get(s['sku'])

    monkeypatch.setattr(publish, 'push', fake_push)
    monkeypatch.setattr(publish, 'Gumroad', lambda *a, **k: object())
    monkeypatch.setattr(publish.time, 'sleep', lambda *a, **k: None)

    publish.refresh(None)          # must not raise -- bb-gadget still gets processed

    row = publish.get('aa-widget')
    assert row['error'] and 'boom' in row['error']


def test_main_refresh_flag_invokes_refresh_with_parsed_args(monkeypatch, tmp_path):
    _use_tmp_db(monkeypatch, tmp_path)
    calls = []
    monkeypatch.setattr(publish, 'refresh',
                        lambda skus, **kw: calls.append((skus, kw)))
    monkeypatch.setattr(sys, 'argv',
                        ['publish.py', '--refresh', '--skus', 'aa-widget,bb-gadget',
                         '--limit', '1', '--dry-run'])

    publish.main()

    assert len(calls) == 1
    skus, kw = calls[0]
    assert skus == ['aa-widget', 'bb-gadget']
    assert kw.get('limit') == 1
    assert kw.get('dry_run') is True
