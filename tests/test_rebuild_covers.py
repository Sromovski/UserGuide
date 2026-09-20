import os
import shutil

import fitz
import pytest

import rebuild_covers
from covers import catalogue, pdfpage


@pytest.fixture
def sample(tmp_path):
    p = tmp_path / 'sample.pdf'
    doc = fitz.open()
    for i in range(4):
        page = doc.new_page(width=612, height=792)
        page.insert_text((80, 120), 'original page %d' % i)
    doc.save(str(p))
    doc.close()
    return str(p)


def test_splice_keeps_the_page_count(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert doc.page_count == 4
    doc.close()


def test_splice_replaces_page_zero_and_leaves_the_interior_alone(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert 'original page 0' not in doc[0].get_text()
    assert 'original page 1' in doc[1].get_text()
    assert 'original page 3' in doc[3].get_text()
    doc.close()


def test_spliced_page_zero_is_not_blank(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert len(doc[0].get_image_info()) == 1
    doc.close()


def test_backup_once_never_overwrites_the_pristine_original(tmp_path, monkeypatch):
    out = tmp_path / 'outputs'
    out.mkdir()
    (out / 'thing.pdf').write_bytes(b'ORIGINAL')
    monkeypatch.setattr(rebuild_covers, 'OUT', str(out))
    monkeypatch.setattr(rebuild_covers, 'BACKUP_DIR', str(out / '_pre_cover_backup'))

    rebuild_covers.backup_once('thing.pdf')
    (out / 'thing.pdf').write_bytes(b'MODIFIED')
    rebuild_covers.backup_once('thing.pdf')

    kept = (out / '_pre_cover_backup' / 'thing.pdf').read_bytes()
    assert kept == b'ORIGINAL'


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    out = tmp_path / 'outputs'
    out.mkdir()
    monkeypatch.setattr(rebuild_covers, 'OUT', str(out))
    results = rebuild_covers.rebuild(dry_run=True)
    assert results
    assert not os.path.exists(out / '_pre_cover_backup')


def test_verify_rejects_a_page_that_is_not_full_bleed(tmp_path):
    # A 1x1 image tucked in the corner passes "exactly one image, no text"
    # but is obviously not the cover. The bbox check must catch it.
    p = tmp_path / 'tiny.pdf'
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)
    pix = fitz.Pixmap(fitz.csRGB, (0, 0, 1, 1), False)
    pix.set_rect(pix.irect, (255, 0, 0))
    page.insert_image(fitz.Rect(0, 0, 10, 10), pixmap=pix)
    doc.save(str(p))
    doc.close()

    with pytest.raises(AssertionError, match='full-bleed'):
        rebuild_covers._verify(str(p))


def test_a_failing_verify_does_not_stop_later_skus(tmp_path, monkeypatch):
    # One bad product must not hide the other twenty. _verify raising used to
    # propagate straight out of rebuild(), aborting the whole batch.
    import build_etsy_kit as kit

    out = tmp_path / 'outputs'
    out.mkdir()
    monkeypatch.setattr(rebuild_covers, 'OUT', str(out))
    monkeypatch.setattr(rebuild_covers, 'BACKUP_DIR', str(out / '_pre_cover_backup'))

    bad, good = kit.SKUS[0], kit.SKUS[1]
    for s in (bad, good):
        p = out / s['pdf']
        doc = fitz.open()
        doc.new_page(width=612, height=792)
        doc.save(str(p))
        doc.close()

    def fake_verify(path):
        if bad['pdf'] in path:
            raise AssertionError('simulated verify failure')

    monkeypatch.setattr(rebuild_covers, '_verify', fake_verify)

    results = dict(rebuild_covers.rebuild(sku_filter=[bad['sku'], good['sku']]))
    assert results[bad['sku']].startswith('FAILED')
    assert results[good['sku']] == 'ok'
