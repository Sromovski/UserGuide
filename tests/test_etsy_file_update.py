"""--update-files: replace the PDF on existing listings, without leaving a listing
file-less, and without duplicating --update-images' own (already-tested) driver logic.

Also covers the two `build_draft` / `check()` gaps found alongside it: a new draft only
ever uploaded 3 of the 5 mockups, and the pre-flight check never caught that a 4th or 5th
was missing.

No network calls anywhere in this file. Etsy is a small fake that records an ordered
call log, matching the style of tests/test_etsy_update_images.py.
"""
from __future__ import annotations

import os
import sys

import pytest

import build_etsy_kit as kit
from etsypub import config, db
from etsypub.client import EtsyError
import etsypub.publish as publish
from etsypub.publish import (build_draft, check, deliverables, live_named_skus,
                             live_skus, run_over_live, update_file)

IMAGE_NAMES = publish.IMAGE_NAMES


def sku(name):
    return next(s for s in kit.SKUS if s['sku'] == name)


SKU = sku('02-starter-volume')                       # has a volume key
NON_VOLUME_SKU = next(s for s in kit.SKUS if not s.get('volume'))


def _write_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(b'fake')


def _write_all_mockups(base, sku_name, skip=()):
    d = os.path.join(base, 'etsy', sku_name)
    for n in IMAGE_NAMES:
        if n not in skip:
            _write_file(os.path.join(d, n))


def _write_all_deliverables(base, s):
    for f in deliverables(s):
        _write_file(os.path.join(base, f))
    _write_file(os.path.join(base, s['pdf']))


def _row(listing_id=555, **extra):
    row = {'sku': SKU['sku'], 'etsy_listing_id': listing_id}
    row.update(extra)
    return row


class FakeEtsyFiles:
    """Records every call in order. `files` is the live file-list state."""

    def __init__(self, files, appear_on_upload=True):
        self.files = list(files)
        self.calls = []
        self.appear_on_upload = appear_on_upload
        self._next_id = max([f['listing_file_id'] for f in files], default=0) + 1

    def listing_files(self, lid):
        self.calls.append(('list', lid))
        return {'results': list(self.files)}

    def upload_file(self, listing_id, path, name):
        self.calls.append(('upload', path, name))
        if self.appear_on_upload:
            new_id = self._next_id
            self._next_id += 1
            self.files.append({'listing_file_id': new_id})
        return {}

    def delete_listing_file(self, listing_id, file_id):
        self.calls.append(('delete', file_id))
        self.files = [f for f in self.files if f['listing_file_id'] != file_id]
        return {}


OLD_FILES = [{'listing_file_id': 1}]


# --------------------------------------------------------------- selection (Fix 1)

def test_update_files_with_no_skus_selects_every_live_listing_not_just_volumes(
        monkeypatch, capsys):
    # This is the actual bug: the old --update-files block called volume_skus(), which
    # can never return a SKU with no `volume` key at all, no matter what the db says.
    monkeypatch.setattr(db, 'init_db', lambda: None)
    monkeypatch.setattr(db, 'all_listings', lambda: [
        {'sku': SKU['sku'], 'etsy_listing_id': 111},
        {'sku': NON_VOLUME_SKU['sku'], 'etsy_listing_id': 222},
    ])
    monkeypatch.setattr(publish, 'Etsy',
                        lambda: (_ for _ in ()).throw(AssertionError('no network')))
    monkeypatch.setattr(sys, 'argv', ['publish', '--update-files', '--dry-run'])

    publish.main()

    out = capsys.readouterr().out
    assert SKU['sku'] in out
    assert NON_VOLUME_SKU['sku'] in out, (
        'a non-volume live SKU was dropped -- --update-files is still selecting via '
        'volume_skus() instead of live_skus()')


def test_update_files_dry_run_constructs_no_etsy(monkeypatch, capsys):
    monkeypatch.setattr(db, 'init_db', lambda: None)
    monkeypatch.setattr(db, 'all_listings', lambda: [
        {'sku': SKU['sku'], 'etsy_listing_id': 111}])

    def boom():
        raise AssertionError('Etsy() must not be constructed on --update-files --dry-run')
    monkeypatch.setattr(publish, 'Etsy', boom)
    monkeypatch.setattr(sys, 'argv', ['publish', '--update-files', '--dry-run'])

    publish.main()  # would raise via boom() if Etsy() were ever constructed

    out = capsys.readouterr().out
    assert 'DRY RUN' in out
    assert 'nothing sent' in out.lower()


def test_update_files_skus_unknown_name_raises(monkeypatch):
    monkeypatch.setattr(db, 'init_db', lambda: None)
    monkeypatch.setattr(db, 'all_listings', lambda: [])
    monkeypatch.setattr(sys, 'argv',
                        ['publish', '--update-files', '--dry-run',
                         '--skus', 'totally-not-a-real-sku'])

    with pytest.raises(SystemExit) as exc:
        publish.main()

    assert 'No SKU named' in str(exc.value)
    assert 'totally-not-a-real-sku' in str(exc.value)


def test_update_files_skus_known_but_unlisted_raises_distinct_message(monkeypatch):
    real_names = [s['sku'] for s in kit.SKUS]
    listed, unlisted = real_names[0], real_names[1]
    monkeypatch.setattr(db, 'init_db', lambda: None)
    monkeypatch.setattr(db, 'all_listings',
                        lambda: [{'sku': listed, 'etsy_listing_id': 111}])
    monkeypatch.setattr(sys, 'argv',
                        ['publish', '--update-files', '--dry-run', '--skus', unlisted])

    with pytest.raises(SystemExit) as exc:
        publish.main()

    msg = str(exc.value)
    assert unlisted in msg
    # Must be distinguishable from the "unknown name" message -- the fix here is
    # "publish it first", not "check your spelling". Matches --update-images' behaviour.
    assert 'No SKU named' not in msg


# ----------------------------------------------------------------- shared driver

def test_run_over_live_runs_the_given_action_per_sku(monkeypatch):
    calls = []

    def fake_action(e, s):
        calls.append(s['sku'])
        return 'did it for %s' % s['sku']

    fake_e = object()
    monkeypatch.setattr(publish, 'Etsy', lambda: fake_e)

    result = run_over_live([SKU], fake_action, 'widgets')

    assert calls == [SKU['sku']]
    assert result == {'done': [SKU['sku']], 'failed': []}


def test_run_over_live_uses_update_file_for_the_files_flag(monkeypatch):
    calls = []

    def fake_update_file(e, s):
        calls.append(('update_file', s['sku']))
        return 'ok'

    monkeypatch.setattr(publish, 'update_file', fake_update_file)
    monkeypatch.setattr(publish, 'Etsy', lambda: object())

    run_over_live([SKU], publish.update_file, 'files')

    assert calls == [('update_file', SKU['sku'])]


def test_run_over_live_dry_run_previews_with_the_given_verb_and_makes_no_calls(
        monkeypatch, capsys):
    monkeypatch.setattr(publish, 'Etsy',
                        lambda: (_ for _ in ()).throw(AssertionError('no network')))

    result = run_over_live([SKU], lambda e, s: 'unused', 'files', dry_run=True)

    out = capsys.readouterr().out
    assert 'would update files' in out
    assert result == {'ready': [SKU['sku']]}


def test_run_over_live_respects_limit(monkeypatch):
    monkeypatch.setattr(publish, 'Etsy',
                        lambda: (_ for _ in ()).throw(AssertionError('no network')))
    other = next(s for s in kit.SKUS if s['sku'] != SKU['sku'])

    result = run_over_live([SKU, other], lambda e, s: 'unused', 'files',
                           dry_run=True, limit=1)

    assert result['ready'] == [SKU['sku']]


# ----------------------------------------------------------------- update_file (unchanged logic, sanity)

def test_update_file_uploads_before_deleting(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    _write_file(os.path.join(str(tmp_path), SKU['pdf']))
    monkeypatch.setattr(db, 'get', lambda s: _row())

    fake = FakeEtsyFiles(OLD_FILES)
    update_file(fake, SKU)

    upload_idx = [i for i, c in enumerate(fake.calls) if c[0] == 'upload']
    delete_idx = [i for i, c in enumerate(fake.calls) if c[0] == 'delete']
    assert upload_idx and delete_idx
    assert max(upload_idx) < min(delete_idx)


# ----------------------------------------------------------------------- Fix 2

def test_build_draft_uploads_five_images_at_ranks_1_to_5_in_order(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'ETSY_ASSETS', os.path.join(str(tmp_path), 'etsy'))
    _write_all_mockups(str(tmp_path), SKU['sku'])

    state = {}

    def fake_ensure(sku_name, volume, title, price):
        state.setdefault(sku_name, {'sku': sku_name, 'etsy_listing_id': None,
                                    'images_done': 0, 'file_done': 0})
        return state[sku_name]

    monkeypatch.setattr(db, 'ensure', fake_ensure)
    monkeypatch.setattr(db, 'get', lambda sku_name: state[sku_name])
    monkeypatch.setattr(db, 'update', lambda sku_name, **f: state[sku_name].update(f))

    class FakeEtsyDraft:
        def __init__(self):
            self.calls = []

        def create_draft_listing(self, **kw):
            return {'listing_id': 999, 'url': 'http://etsy/999'}

        def upload_image(self, listing_id, path, rank, alt_text=''):
            self.calls.append(('image', path, rank))
            return {'listing_image_id': rank}

        def upload_file(self, listing_id, path, name):
            self.calls.append(('file', path, name))
            return {}

    fake = FakeEtsyDraft()
    build_draft(fake, SKU)

    uploads = [c for c in fake.calls if c[0] == 'image']
    assert len(uploads) == 5
    for (_, path, rank), expected_rank, expected_name in zip(
            uploads, range(1, 6), IMAGE_NAMES):
        assert rank == expected_rank
        assert os.path.basename(path) == expected_name


def test_check_reports_missing_04_pin_as_a_problem(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    monkeypatch.setattr(config, 'ETSY_ASSETS', os.path.join(str(tmp_path), 'etsy'))
    _write_all_deliverables(str(tmp_path), SKU)
    _write_all_mockups(str(tmp_path), SKU['sku'], skip=('04_pin.png',))

    problems = check(SKU)

    assert any('04_pin' in p for p in problems), problems


def test_check_reports_missing_05_wide_as_a_problem(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    monkeypatch.setattr(config, 'ETSY_ASSETS', os.path.join(str(tmp_path), 'etsy'))
    _write_all_deliverables(str(tmp_path), SKU)
    _write_all_mockups(str(tmp_path), SKU['sku'], skip=('05_wide.png',))

    problems = check(SKU)

    assert any('05_wide' in p for p in problems), problems


def test_check_passes_with_all_five_mockups_present(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'OUT', str(tmp_path))
    monkeypatch.setattr(config, 'ETSY_ASSETS', os.path.join(str(tmp_path), 'etsy'))
    _write_all_deliverables(str(tmp_path), SKU)
    _write_all_mockups(str(tmp_path), SKU['sku'])

    assert check(SKU) == []
