#!/usr/bin/env python3
"""Replace page 1 of every live product PDF with the new direction C cover.

Approach A from the design doc: render centrally, splice into the shipped PDFs.
Interiors are NEVER regenerated, so nothing that is currently audit-clean can
regress.

Run:
    python rebuild_covers.py --dry-run
    python rebuild_covers.py
    python rebuild_covers.py --skus 02-starter-volume,30-codex-v1
"""
import argparse
import os
import shutil
import sys

import fitz

import audit_pdfs
import build_etsy_kit as kit
from covers import catalogue, pdfpage

ROOT = r'C:\Projects\UserGuide'
OUT = os.path.join(ROOT, 'outputs')
BACKUP_DIR = os.path.join(OUT, '_pre_cover_backup')


def backup_once(pdf_name):
    """Copy the original aside exactly once. Never overwrite a backup."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dst = os.path.join(BACKUP_DIR, pdf_name)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(OUT, pdf_name), dst)
    return dst


def splice(pdf_path, cover_bytes):
    """Replace page 0 with the cover. Atomic: temp file, then replace."""
    doc = fitz.open(pdf_path)
    before = doc.page_count
    cover = fitz.open(stream=cover_bytes, filetype='pdf')
    doc.delete_page(0)
    doc.insert_pdf(cover, from_page=0, to_page=0, start_at=0)
    if doc.page_count != before:
        doc.close()
        cover.close()
        raise AssertionError('page count changed %d -> %d in %s'
                             % (before, doc.page_count, pdf_path))
    tmp = pdf_path + '.tmp'
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    cover.close()
    os.replace(tmp, pdf_path)


def _verify(pdf_path):
    """Check page 0 — the only page this script touches.

    Deliberately NOT a whole-document audit. audit_pdfs.py encodes the volume
    geometry (MX 46.8pt, 22pt footer), but four SKUs are not volumes: the Cheat
    Sheet Pack is a light single-wide-column printable, and the Cost Calculator
    preview, Prompt Vault and Start Here each have their own layout. Gating on a
    whole-document audit would let a pre-existing interior quirk in one of them
    abort a rollout that only ever replaced page 1. The full audit still runs as
    a release check over the whole catalogue — see the run instructions.
    """
    doc = fitz.open(pdf_path)
    try:
        page = doc[0]
        if len(page.get_image_info()) != 1:
            raise AssertionError('page 1 of %s is not a single full-bleed image'
                                 % os.path.basename(pdf_path))
        if page.get_text().strip():
            raise AssertionError('page 1 of %s still carries text'
                                 % os.path.basename(pdf_path))
    finally:
        doc.close()


def rebuild(sku_filter=None, dry_run=False):
    specs = catalogue.all_specs()
    results = []
    for s in kit.SKUS:
        name = s['sku']
        if sku_filter and name not in sku_filter:
            continue
        pdf_name = s['pdf']
        path = os.path.join(OUT, pdf_name)
        if not os.path.exists(path):
            results.append((name, 'MISSING %s' % pdf_name))
            continue
        if dry_run:
            results.append((name, 'would rebuild %s' % pdf_name))
            continue
        try:
            backup_once(pdf_name)
            splice(path, pdfpage.cover_pdf_bytes(specs[name]))
            _verify(path)
        except AssertionError as e:
            results.append((name, 'FAILED: %s' % e))
            continue
        results.append((name, 'ok'))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skus', help='comma-separated SKU names')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    filt = a.skus.split(',') if a.skus else None
    failed = 0
    for name, status in rebuild(filt, a.dry_run):
        if status != 'ok' and not a.dry_run:
            failed += 1
        print('%-30s %s' % (name, status))
    print('\n%s' % ('DRY RUN — nothing written' if a.dry_run
                    else '%d problem(s)' % failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
