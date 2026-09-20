"""--update-images: replace listing gallery images without ever leaving a listing
image-less, and without touching --update-files' own (already-live) selection logic.

No network calls anywhere in this file. Etsy is a small fake that records an ordered
call log so upload-before-delete ordering is assertable, not just call counts.
"""
from __future__ import annotations

import os

import pytest

import build_etsy_kit as kit
from etsypub import config, db
from etsypub.client import EtsyError
import etsypub.publish as publish
from etsypub.publish import live_named_skus, live_skus, run_update_images, update_images

IMAGE_NAMES = ('01_main.png', '02_inside.png', '03_included.png',
              '04_pin.png', '05_wide.png')


def sku(name):
    return next(s for s in kit.SKUS if s['sku'] == name)


SKU = sku('02-starter-volume')


class FakeEtsy:
    """Records every call in order. `images` is the live gallery state."""

    def __init__(self, images, appear_on_upload=True):
        self.images = list(images)
        self.calls = []
        self.appear_on_upload = appear_on_upload
        self._next_id = max([im['listing_image_id'] for im in images], default=0) + 1

    def listing_images(self, lid):
        self.calls.append(('list', lid))
        return {'results': list(self.images)}

    def upload_image(self, listing_id, path, rank, alt_text=''):
        self.calls.append(('upload', path, rank))
        if self.appear_on_upload:
            new_id = self._next_id
            self._next_id += 1
            self.images.append({'listing_image_id': new_id,
                                'url_fullxfull': 'http://img/%d' % new_id})
            return {'listing_image_id': new_id}
        return {'listing_image_id': None}

    def delete_listing_image(self, listing_id, image_id):
        self.calls.append(('delete', image_id))
        self.images = [im for im in self.images if im['listing_image_id'] != image_id]
        return {}


OLD_IMAGES = [
    {'listing_image_id': 1, 'url_fullxfull': 'http://img/1'},
    {'listing_image_id': 2, 'url_fullxfull': 'http://img/2'},
    {'listing_image_id': 3, 'url_fullxfull': 'http://img/3'},
]


def _write_images(base, sku_name, names=IMAGE_NAMES):
    d = os.path.join(base, 'etsy', sku_name)
    os.makedirs(d, exist_ok=True)
    for n in names:
        with open(os.path.join(d, n), 'wb') as f:
            f.write(b'fake-png')
    return d


def _row(listing_id=555):
    return {'sku': SKU['sku'], 'etsy_listing_id': listing_id}


# --------------------------------------------------------------- update_images

def test_uploads_all_five_before_any_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_images(str(tmp_path), SKU['sku'])
    monkeypatch.setattr(db, 'get', lambda s: _row())

    fake = FakeEtsy(OLD_IMAGES)
    update_images(fake, SKU)

    upload_idx = [i for i, c in enumerate(fake.calls) if c[0] == 'upload']
    delete_idx = [i for i, c in enumerate(fake.calls) if c[0] == 'delete']
    assert upload_idx, 'expected upload calls'
    assert delete_idx, 'expected delete calls'
    assert max(upload_idx) < min(delete_idx), (
        'a delete happened before all uploads finished: %s' % fake.calls)


def test_uploads_five_files_at_ranks_1_to_5_in_order(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_images(str(tmp_path), SKU['sku'])
    monkeypatch.setattr(db, 'get', lambda s: _row())

    fake = FakeEtsy(OLD_IMAGES)
    update_images(fake, SKU)

    uploads = [c for c in fake.calls if c[0] == 'upload']
    assert len(uploads) == 5
    for (_, path, rank), expected_rank, expected_name in zip(
            uploads, range(1, 6), IMAGE_NAMES):
        assert rank == expected_rank
        assert os.path.basename(path) == expected_name


def test_missing_image_file_raises_before_any_upload(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    # Only write 4 of the 5 required files.
    _write_images(str(tmp_path), SKU['sku'], names=IMAGE_NAMES[:4])
    monkeypatch.setattr(db, 'get', lambda s: _row())

    fake = FakeEtsy(OLD_IMAGES)
    with pytest.raises(EtsyError):
        update_images(fake, SKU)

    assert not [c for c in fake.calls if c[0] == 'upload'], (
        'an upload happened despite a missing source file: %s' % fake.calls)


def test_no_delete_when_new_images_do_not_appear(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_images(str(tmp_path), SKU['sku'])
    monkeypatch.setattr(db, 'get', lambda s: _row())

    # listing_images always reports only the old set, as if the uploads never landed.
    fake = FakeEtsy(OLD_IMAGES, appear_on_upload=False)
    with pytest.raises(EtsyError):
        update_images(fake, SKU)

    assert not [c for c in fake.calls if c[0] == 'delete'], (
        'deleted the old images despite the new ones never appearing: %s' % fake.calls)


def test_old_image_ids_all_deleted_on_success(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_images(str(tmp_path), SKU['sku'])
    monkeypatch.setattr(db, 'get', lambda s: _row())

    fake = FakeEtsy(OLD_IMAGES)
    update_images(fake, SKU)

    deleted = {c[1] for c in fake.calls if c[0] == 'delete'}
    assert deleted == {im['listing_image_id'] for im in OLD_IMAGES}


def test_sku_with_no_listing_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_images(str(tmp_path), SKU['sku'])
    monkeypatch.setattr(db, 'get', lambda s: None)

    fake = FakeEtsy(OLD_IMAGES)
    with pytest.raises(EtsyError):
        update_images(fake, SKU)
    assert fake.calls == []


# ------------------------------------------------------------------- live_skus

def test_live_skus_only_returns_rows_with_a_listing_id(monkeypatch):
    real_names = [s['sku'] for s in kit.SKUS]
    a, b = real_names[0], real_names[1]
    fake_rows = [
        {'sku': a, 'etsy_listing_id': 111},
        {'sku': b, 'etsy_listing_id': None},
        {'sku': 'not-a-real-catalogue-sku', 'etsy_listing_id': 222},
    ]
    monkeypatch.setattr(db, 'all_listings', lambda: fake_rows)

    result = live_skus()

    assert [s['sku'] for s in result] == [a]
    assert result[0] is sku(a)


# --------------------------------------------------------------- run_update_images

def test_dry_run_makes_no_network_calls(monkeypatch):
    def boom():
        raise AssertionError('Etsy() must not be constructed on --dry-run')
    monkeypatch.setattr(publish, 'Etsy', boom)

    result = run_update_images([SKU], dry_run=True)

    assert result['ready'] == [SKU['sku']]


def test_dry_run_respects_limit(monkeypatch):
    monkeypatch.setattr(publish, 'Etsy', lambda: (_ for _ in ()).throw(
        AssertionError('must not construct Etsy()')))
    other = sku([s['sku'] for s in kit.SKUS if s['sku'] != SKU['sku']][0])

    result = run_update_images([SKU, other], dry_run=True, limit=1)

    assert result['ready'] == [SKU['sku']]


# ---------------------------------------------------------------- live_named_skus

def test_live_named_skus_narrows_a_valid_subset(monkeypatch):
    real_names = [s['sku'] for s in kit.SKUS]
    a, b = real_names[0], real_names[1]
    monkeypatch.setattr(db, 'all_listings', lambda: [
        {'sku': a, 'etsy_listing_id': 111},
        {'sku': b, 'etsy_listing_id': 222},
    ])

    result = live_named_skus([a])

    assert [s['sku'] for s in result] == [a]
    assert result[0] is sku(a)


def test_live_named_skus_raises_on_unknown_name(monkeypatch):
    monkeypatch.setattr(db, 'all_listings', lambda: [])

    with pytest.raises(SystemExit) as exc:
        live_named_skus(['totally-not-a-real-sku'])

    msg = str(exc.value)
    assert 'totally-not-a-real-sku' in msg
    assert 'No SKU named' in msg


def test_live_named_skus_raises_distinctly_for_known_but_unlisted_sku(monkeypatch):
    real_names = [s['sku'] for s in kit.SKUS]
    listed, unlisted = real_names[0], real_names[1]
    # `unlisted` is a real catalogue SKU, but the db has no listing id for it --
    # never published, or a row that predates any Etsy draft.
    monkeypatch.setattr(db, 'all_listings', lambda: [
        {'sku': listed, 'etsy_listing_id': 111},
    ])

    with pytest.raises(SystemExit) as exc:
        live_named_skus([unlisted])

    msg = str(exc.value)
    assert unlisted in msg
    # Must be distinguishable from the "unknown name" message -- the fix here is
    # "publish it first", not "check your spelling".
    assert 'No SKU named' not in msg
