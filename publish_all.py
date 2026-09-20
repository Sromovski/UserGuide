#!/usr/bin/env python3
"""Get every product onto Etsy and Gumroad, unattended.

    python publish_all.py            # do it
    python publish_all.py --dry-run  # what it would do, no network

Written to run from Task Scheduler with nobody watching, so every stage is:

  * IDEMPOTENT   — anything already live is skipped, never duplicated
  * RESUMABLE    — a failed stage does not block the others, and the next run retries
  * GATED        — nothing is published without its file attached
  * LOGGED       — the log is the only thing anyone will read afterwards

The reason it exists: Gumroad caps product creation at 10 per day on a ROLLING 24-hour
window, so the catalogue cannot be loaded in one sitting. This runs repeatedly and
converges, rather than needing a person to retry it.

Etsy charges $0.20 per activated listing. Gumroad charges nothing.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from dotenv import load_dotenv                                     # noqa: E402

load_dotenv(os.path.join(ROOT, '.env'))

import build_etsy_kit                                              # noqa: E402

# 12-start-here is free and Etsy has no free listing tier, so it is Gumroad-only.
ETSY_EXCLUDE = {'12-start-here'}


def log(msg=''):
    print(msg, flush=True)


def stamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# ------------------------------------------------------------------------ ETSY

def etsy_stage(dry_run):
    from etsypub import config as ecfg
    from etsypub import db as edb
    from etsypub.client import Etsy
    from etsypub.publish import check, run as etsy_run

    log('\n' + '=' * 70)
    log('ETSY')
    log('=' * 70)

    missing = ecfg.missing_credentials()
    if missing:
        log('SKIPPED — credentials missing:')
        for m in missing:
            log('   %s' % m)
        return

    edb.init_db()
    wanted = [s for s in build_etsy_kit.SKUS if s['sku'] not in ETSY_EXCLUDE]

    # Reconcile first: Etsy is the source of truth about what is actually live.
    try:
        e = Etsy()
        live = {}
        for state in ('draft', 'active', 'inactive', 'expired'):
            try:
                for l in e.shop_listings(state=state).get('results', []):
                    live[l['listing_id']] = state
            except Exception:                                      # noqa: BLE001
                continue
        for r in edb.all_listings():
            lid = r['etsy_listing_id']
            if lid and lid in live and live[lid] != r['state']:
                edb.update(r['sku'], state=live[lid])
                log('   reconciled %s -> %s' % (r['sku'], live[lid]))
    except Exception as exc:                                       # noqa: BLE001
        log('   could not reconcile: %s' % exc)

    todo_create, todo_activate, blocked = [], [], []
    for s in wanted:
        problems = check(s)
        if problems:
            blocked.append((s['sku'], problems))
            continue
        row = edb.get(s['sku'])
        if not row or not row['etsy_listing_id']:
            todo_create.append(s['sku'])
        elif row['state'] != 'active':
            todo_activate.append(s['sku'])

    for sku, problems in blocked:
        log('BLOCKED %s' % sku)
        for p in problems:
            log('     - %s' % p)

    log('to create:   %s' % (', '.join(todo_create) or 'nothing'))
    log('to activate: %s' % (', '.join(todo_activate) or 'nothing'))
    if dry_run:
        cost = (len(todo_create) + len(todo_activate)) * ecfg.LISTING_FEE_USD
        log('would cost $%.2f in Etsy listing fees' % cost)
        return

    if todo_create:
        log('\n--- creating drafts (free) ---')
        etsy_run([], sku_names=todo_create)
    # Re-read: anything just created is now a draft awaiting activation.
    to_go = [s['sku'] for s in wanted
             if (edb.get(s['sku']) or {}).get('etsy_listing_id')
             and (edb.get(s['sku']) or {}).get('state') != 'active']
    if to_go:
        log('\n--- activating ($%.2f) ---' % (len(to_go) * ecfg.LISTING_FEE_USD))
        etsy_run([], do_activate=True, sku_names=to_go)


# --------------------------------------------------------------------- GUMROAD

def gumroad_stage(dry_run):
    log('\n' + '=' * 70)
    log('GUMROAD')
    log('=' * 70)

    if not os.getenv('GUMROAD_ACCESS_TOKEN'):
        log('SKIPPED — GUMROAD_ACCESS_TOKEN not set')
        return

    from gumroadpub.publish import finish, init_db, run as g_run

    init_db()
    if dry_run:
        g_run(None, dry_run=True)
        return
    # finish() = create what is missing, verify everything, publish what passes.
    finish()


# ------------------------------------------------------------------------ MAIN

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--etsy-only', action='store_true')
    ap.add_argument('--gumroad-only', action='store_true')
    a = ap.parse_args()

    log('#' * 70)
    log('# PUBLISH ALL   %s' % stamp())
    log('#' * 70)

    failed = []
    if not a.gumroad_only:
        try:
            etsy_stage(a.dry_run)
        except Exception:                                          # noqa: BLE001
            failed.append('etsy')
            log('ETSY STAGE FAILED:\n%s' % traceback.format_exc())
    if not a.etsy_only:
        try:
            gumroad_stage(a.dry_run)
        except Exception:                                          # noqa: BLE001
            failed.append('gumroad')
            log('GUMROAD STAGE FAILED:\n%s' % traceback.format_exc())

    log('\n' + '#' * 70)
    log('# DONE %s  %s' % (stamp(),
                           ('FAILURES: ' + ', '.join(failed)) if failed else 'no errors'))
    log('#' * 70)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
