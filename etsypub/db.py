"""SQLite state for what is on Etsy.

One row per SKU. The row exists so a second run never creates a second listing for a
product that already has one — the exact bug that put 44 ghost products on Shopify in
the pod-pipeline project. `etsy_listing_id` is written the moment the draft comes back,
before any image or file upload, so an interrupted run is resumable rather than orphaned.
"""
from __future__ import annotations

import datetime
import sqlite3
from typing import Any, Optional

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS listings (
    sku              TEXT PRIMARY KEY,
    volume           INTEGER,
    etsy_listing_id  INTEGER,
    state            TEXT NOT NULL DEFAULT 'pending',
    images_done      INTEGER NOT NULL DEFAULT 0,
    file_done        INTEGER NOT NULL DEFAULT 0,
    price            TEXT,
    title            TEXT,
    url              TEXT,
    error            TEXT,
    created_at       TEXT,
    updated_at       TEXT
);
CREATE TABLE IF NOT EXISTS runs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    job        TEXT,
    ok         INTEGER,
    summary    TEXT,
    created_at TEXT
);
"""


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec='seconds')


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(config.DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    with connect() as con:
        con.executescript(SCHEMA)


def get(sku: str) -> Optional[dict]:
    with connect() as con:
        r = con.execute('SELECT * FROM listings WHERE sku = ?', (sku,)).fetchone()
    return dict(r) if r else None


def all_listings() -> list[dict]:
    with connect() as con:
        rows = con.execute('SELECT * FROM listings ORDER BY volume').fetchall()
    return [dict(r) for r in rows]


def ensure(sku: str, volume: int, title: str, price: str) -> dict:
    row = get(sku)
    if row:
        return row
    with connect() as con:
        con.execute(
            'INSERT INTO listings (sku, volume, title, price, created_at, updated_at) '
            'VALUES (?,?,?,?,?,?)',
            (sku, volume, title, price, _now(), _now()))
    return get(sku)


def update(sku: str, **fields: Any) -> None:
    if not fields:
        return
    fields['updated_at'] = _now()
    cols = ', '.join('%s = ?' % k for k in fields)
    with connect() as con:
        con.execute('UPDATE listings SET %s WHERE sku = ?' % cols,
                    (*fields.values(), sku))


def record_run(job: str, *, ok: bool, summary: str) -> None:
    with connect() as con:
        con.execute('INSERT INTO runs (job, ok, summary, created_at) VALUES (?,?,?,?)',
                    (job, 1 if ok else 0, summary, _now()))
