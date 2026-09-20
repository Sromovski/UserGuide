"""Minimal Etsy Open API v3 client.

Docs:  https://developers.etsy.com/documentation/
Auth:  every request needs BOTH headers —
           x-api-key:     <keystring>:<shared_secret>   (NOT the bare keystring —
                          that returns 403 "Shared secret is required in x-api-key")
           Authorization: Bearer <access token>
       An access token lasts 1 hour; the refresh token lasts 90 days. This client
       exchanges the refresh token for an access token on first use and re-exchanges
       automatically on a 401, so nothing above it has to think about expiry.

The digital instant-download flow:
    1. create_draft_listing(type='download')  -> a free, unpublished draft
    2. upload_image()  x3                     -> the mockups, rank 1..3
    3. upload_file()                          -> the PDF buyers receive
    4. activate()                             -> goes live, and Etsy bills $0.20

Steps 1-3 cost nothing, which is why publish.py does them for every volume first and
keeps activation behind a separate explicit flag.
"""
from __future__ import annotations

import os
import time
from typing import Any, Optional

import requests

from . import config

BASE = 'https://api.etsy.com/v3/application'
TOKEN_URL = 'https://api.etsy.com/v3/public/oauth/token'


class EtsyError(RuntimeError):
    pass


class Etsy:
    def __init__(self, keystring: Optional[str] = None,
                 refresh_token: Optional[str] = None,
                 shop_id: Optional[str] = None):
        self.keystring = keystring or config.KEYSTRING
        self.refresh_token = refresh_token or config.REFRESH_TOKEN
        self.shop_id = shop_id or config.SHOP_ID
        if not self.keystring:
            raise EtsyError('ETSY_KEYSTRING is not set.')
        if not self.refresh_token:
            raise EtsyError('ETSY_REFRESH_TOKEN is not set — run: python -m etsypub.oauth')
        self.access_token: Optional[str] = None
        self.s = requests.Session()
        self.s.headers.update({'x-api-key': config.api_key(),
                               'User-Agent': 'userguide-etsypub/0.1'})

    # ------------------------------------------------------------------ auth
    def refresh(self) -> str:
        r = requests.post(TOKEN_URL, timeout=30, data={
            'grant_type': 'refresh_token',
            'client_id': self.keystring,
            'refresh_token': self.refresh_token,
        })
        if not r.ok:
            raise EtsyError('token refresh failed -> %s: %s' % (r.status_code, r.text[:400]))
        payload = r.json()
        self.access_token = payload['access_token']
        # Etsy rotates the refresh token on each exchange. Losing the new one means
        # re-doing the browser consent, so surface it for .env.
        new_refresh = payload.get('refresh_token')
        if new_refresh and new_refresh != self.refresh_token:
            self.refresh_token = new_refresh
            _persist_refresh_token(new_refresh)
        self.s.headers['Authorization'] = 'Bearer ' + self.access_token
        return self.access_token

    # ------------------------------------------------------------- low level
    def _req(self, method: str, path: str, *, retry_auth: bool = True, **kw) -> Any:
        if not self.access_token:
            self.refresh()
        r = self.s.request(method, BASE + path, timeout=90, **kw)
        if r.status_code == 401 and retry_auth:
            self.refresh()
            return self._req(method, path, retry_auth=False, **kw)
        if r.status_code == 429:
            # Etsy's per-second cap. One backoff, then let it fail loudly.
            time.sleep(5)
            r = self.s.request(method, BASE + path, timeout=90, **kw)
        if not r.ok:
            raise EtsyError('%s %s -> %s: %s' % (method, path, r.status_code, r.text[:600]))
        return r.json() if r.text else {}

    # ------------------------------------------------------------- discovery
    @staticmethod
    def ping() -> dict:
        """Is the app approved and the key active? Needs no OAuth token.

        Returns {'application_id': ...} on success. This is the cheapest way to tell
        'Etsy has not approved the app yet' apart from 'the OAuth flow is wrong'.
        """
        r = requests.get(BASE + '/openapi-ping',
                         headers={'x-api-key': config.api_key()}, timeout=30)
        if not r.ok:
            raise EtsyError('ping -> %s: %s' % (r.status_code, r.text[:300]))
        return r.json()

    def me(self) -> dict:
        return self._req('GET', '/users/me')

    def get_shop(self, shop_id: Optional[str] = None) -> dict:
        return self._req('GET', '/shops/%s' % (shop_id or self.shop_id))

    def taxonomy_nodes(self) -> dict:
        return self._req('GET', '/seller-taxonomy/nodes')

    def shop_listings(self, state: str = 'active', limit: int = 100) -> dict:
        """What the shop actually holds. Local state is never trusted over this."""
        return self._req('GET', '/shops/%s/listings' % self.shop_id,
                         params={'state': state, 'limit': limit})

    def get_listing(self, listing_id: int) -> dict:
        return self._req('GET', '/listings/%s' % listing_id)

    # ------------------------------------------------------------------ core
    def create_draft_listing(self, *, title: str, description: str, price: float,
                             tags: list[str], taxonomy_id: int, quantity: int,
                             who_made: str, when_made: str, is_supply: bool,
                             listing_type: str = 'download',
                             return_policy_id: Optional[int] = None) -> dict:
        """Create a free, unpublished DRAFT. No shipping profile — digital listings
        do not take one, and digital listings cannot have processing profiles."""
        body = {
            'quantity': quantity,
            'title': title,
            'description': description,
            'price': price,
            'who_made': who_made,
            'when_made': when_made,
            'taxonomy_id': taxonomy_id,
            'type': listing_type,
            'is_supply': is_supply,
            'tags': ','.join(tags),
        }
        if return_policy_id:
            body['return_policy_id'] = return_policy_id
        # This endpoint takes form-encoded, not JSON.
        return self._req('POST', '/shops/%s/listings' % self.shop_id, data=body)

    def upload_image(self, listing_id: int, path: str, rank: int,
                     alt_text: str = '') -> dict:
        with open(path, 'rb') as f:
            files = {'image': (os.path.basename(path), f, 'image/png')}
            data = {'rank': rank}
            if alt_text:
                data['alt_text'] = alt_text[:250]
            return self._req('POST',
                             '/shops/%s/listings/%s/images' % (self.shop_id, listing_id),
                             files=files, data=data)

    MIME = {
        '.pdf':  'application/pdf',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.zip':  'application/zip',
        '.md':   'text/markdown',
        '.txt':  'text/plain',
        '.csv':  'text/csv',
    }

    def upload_file(self, listing_id: int, path: str, name: str, rank: int = 1) -> dict:
        mime = self.MIME.get(os.path.splitext(name)[1].lower(),
                             'application/octet-stream')
        with open(path, 'rb') as f:
            files = {'file': (name, f, mime)}
            return self._req('POST',
                             '/shops/%s/listings/%s/files' % (self.shop_id, listing_id),
                             files=files, data={'name': name, 'rank': rank})

    def listing_files(self, listing_id: int) -> dict:
        return self._req('GET',
                         '/shops/%s/listings/%s/files' % (self.shop_id, listing_id))

    def delete_listing_file(self, listing_id: int, file_id: int) -> dict:
        return self._req('DELETE', '/shops/%s/listings/%s/files/%s'
                         % (self.shop_id, listing_id, file_id))

    def listing_images(self, listing_id: int) -> dict:
        # Uploads are shop-scoped, reads are not — the shop-scoped GET 404s.
        return self._req('GET', '/listings/%s/images' % listing_id)

    def update_listing(self, listing_id: int, **fields: Any) -> dict:
        return self._req('PATCH',
                         '/shops/%s/listings/%s' % (self.shop_id, listing_id),
                         data=fields)

    def activate(self, listing_id: int) -> dict:
        """Flip a draft live. Etsy bills the $0.20 listing fee here, not at draft time.

        Etsy 400s this if the digital listing has no downloadable file attached — which
        is the correct failure, and the reason publish.py uploads the file first.
        """
        return self.update_listing(listing_id, state='active')


def _persist_refresh_token(token: str) -> None:
    """Rewrite ETSY_REFRESH_TOKEN in .env in place, leaving everything else alone."""
    env = os.path.join(config.ROOT, '.env')
    line = 'ETSY_REFRESH_TOKEN=%s\n' % token
    if not os.path.exists(env):
        with open(env, 'a', encoding='utf-8') as f:
            f.write(line)
        return
    with open(env, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if l.startswith('ETSY_REFRESH_TOKEN='):
            lines[i] = line
            break
    else:
        lines.append(line)
    with open(env, 'w', encoding='utf-8') as f:
        f.writelines(lines)
