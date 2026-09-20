"""Settings for the Etsy publisher. Reads .env, falls back to sane defaults.

Nothing secret lives in this file — ETSY_KEYSTRING, ETSY_SHARED_SECRET and the tokens
all come from .env, which is gitignored.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, '.env'))

OUT = os.path.join(ROOT, 'outputs')
ETSY_ASSETS = os.path.join(OUT, 'etsy')
DB_PATH = os.getenv('ETSY_DB_PATH', os.path.join(ROOT, 'etsy.db'))

# ---------------------------------------------------------------- credentials
KEYSTRING = os.getenv('ETSY_KEYSTRING', '')          # the app's "keystring" / client id
SHARED_SECRET = os.getenv('ETSY_SHARED_SECRET', '')  # required — see api_key() below


def api_key() -> str:
    """The x-api-key header value.

    Etsy wants "<keystring>:<shared_secret>" here, NOT the bare keystring — sending the
    keystring alone returns 403 "Shared secret is required in x-api-key header." The
    keystring on its own is still what goes in `client_id` for the OAuth calls.
    """
    return '%s:%s' % (KEYSTRING, SHARED_SECRET) if SHARED_SECRET else KEYSTRING
SHOP_ID = os.getenv('ETSY_SHOP_ID', '')              # numeric; oauth.py fills this in
REFRESH_TOKEN = os.getenv('ETSY_REFRESH_TOKEN', '')

# Must match the app registration EXACTLY, including scheme and port. Etsy's form only
# accepts https://, and on https oauth.py asks you to paste the redirect back instead of
# listening for it — there is no TLS cert on localhost. See etsypub/README.md.
REDIRECT_URI = os.getenv('ETSY_REDIRECT_URI', 'https://localhost:3003/oauth/redirect')
SCOPES = os.getenv('ETSY_SCOPES', 'listings_r listings_w shops_r').split()

# ------------------------------------------------------------------- listings
# Which volumes go up. The publisher pulls titles/tags/descriptions/mockups for these
# out of build_etsy_kit.SKUS, so listing copy has exactly one source.
VOLUMES = [int(v) for v in os.getenv('ETSY_VOLUMES', '1,2,3,4,5,6').split(',')]

QUANTITY = int(os.getenv('ETSY_QUANTITY', '999'))
WHO_MADE = os.getenv('ETSY_WHO_MADE', 'i_did')
# Etsy's recent-years bucket rolls forward. If the API 400s on this, the error body
# lists the currently valid enum values — copy the newest one into .env.
WHEN_MADE = os.getenv('ETSY_WHEN_MADE', '2020_2026')
IS_SUPPLY = os.getenv('ETSY_IS_SUPPLY', 'false').lower() == 'true'

# Numeric seller-taxonomy node. There is no safe default — run
# `python -m etsypub.taxonomy --search "digital prints"` against the live API and put
# the id you pick in .env, so the category is chosen deliberately and stays consistent.
TAXONOMY_ID = os.getenv('ETSY_TAXONOMY_ID', '')

RETURN_POLICY_ID = os.getenv('ETSY_RETURN_POLICY_ID', '')  # optional

# Pacing. A young shop that posts its whole catalogue in one sitting is the pattern
# that gets reviewed — same reason pod-pipeline drips Etsy in daily instalments.
PER_RUN = int(os.getenv('ETSY_PER_RUN', '2'))
JITTER_MIN = float(os.getenv('ETSY_JITTER_MIN', '3'))
JITTER_MAX = float(os.getenv('ETSY_JITTER_MAX', '8'))

LISTING_FEE_USD = 0.20


def missing_credentials() -> list[str]:
    """What still has to be filled in before anything can talk to Etsy."""
    out = []
    if not KEYSTRING:
        out.append('ETSY_KEYSTRING (from etsy.com/developers — your app keystring)')
    if not SHARED_SECRET:
        out.append('ETSY_SHARED_SECRET (same page as the keystring — the x-api-key '
                   'header needs both)')
    if not REFRESH_TOKEN:
        out.append('ETSY_REFRESH_TOKEN (run: python -m etsypub.oauth)')
    if not SHOP_ID:
        out.append('ETSY_SHOP_ID (run: python -m etsypub.oauth, it prints this)')
    if not TAXONOMY_ID:
        out.append('ETSY_TAXONOMY_ID (run: python -m etsypub.taxonomy --search digital)')
    return out
