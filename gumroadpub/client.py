"""Gumroad API v2 client.

Auth is a plain `access_token` parameter — no OAuth consent flow, unlike Etsy.

IMPORTANT, and contrary to every public doc and forum post: **product creation via the
API works.** `POST /v2/products` is widely described as returning 404 / "dashboard only".
Tested against a live account on 2026-08-01: it returns 200 and creates the product.

**`GET /v2/products` is PAGINATED** (10 products/page, with `next_page_key` and
`next_page_url` present in the response when more remain). `products()` used to return
only the first page. That truncation caused real damage on 2026-09-20: a reconciliation
run built on the truncated list concluded 11 live products did not exist, reset their
healthy db rows to "not created", and triggered 9 create attempts Gumroad rejected with
"Custom permalink is already used by another one of your products". Nothing was
destroyed only because Gumroad refuses duplicate permalinks. `products()` now follows
`next_page_url` until it runs out, with a page cap so a malformed `next_page_url` cannot
loop forever -- and it raises rather than ever returning a partial list silently again.
Do not "simplify" this back to a single GET.

File attachment is a four-step presign flow. The API's own error message documents it:

    POST /v2/files/presign      {filename, file_size, content_type}
        -> {upload_id, key, file_url, parts:[{part_number, presigned_url}]}
    PUT each part to its presigned_url, keep the ETag response header
    POST /v2/files/complete     {upload_id, key, parts:[{part_number, etag}]}
    PUT /v2/products/:id        files[][url] = file_url

**`files` is a FULL REPLACEMENT.** Files missing from the array are removed from the
product. To keep an existing file, include an entry carrying its id. Getting this wrong
silently strips a live product's download.
"""
from __future__ import annotations

import mimetypes
import os
from typing import Any, Optional

import requests

BASE = 'https://api.gumroad.com/v2'

# Gumroad caps product CREATION at 10 per day per account, and **deleted products still
# count**. Discovered the hard way: eight throwaway probe products (all deleted straight
# away) consumed most of a day's allowance before the real catalogue was loaded. Probe
# with ONE test product and reuse it, or you lose a day.
DAILY_CREATE_LIMIT = 10

# S3 multipart minimum part size, except for the final part.
PART_SIZE = 5 * 1024 * 1024

# Prefix _req's BASE already carries. A next_page_url of "/v2/products?page_key=..."
# must have this stripped before being handed back to _req, or the request becomes
# ".../v2/v2/products?...".
_V2_PREFIX = '/v2'


class GumroadError(RuntimeError):
    pass


class Gumroad:
    # Sane cap on pages followed by products(): a malformed or cyclic next_page_url
    # must never turn into an infinite loop. Real catalogues page out in single digits.
    MAX_PRODUCT_PAGES = 50

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GUMROAD_ACCESS_TOKEN', '')
        if not self.token:
            raise GumroadError('GUMROAD_ACCESS_TOKEN is not set.')
        self.s = requests.Session()

    # ------------------------------------------------------------- low level
    def _req(self, method: str, path: str, **kw) -> Any:
        data = kw.pop('data', None) or {}
        params = kw.pop('params', None) or {}
        if method == 'GET' or params:
            params['access_token'] = self.token
        else:
            data['access_token'] = self.token
        r = self.s.request(method, BASE + path, data=data or None,
                           params=params or None, timeout=120, **kw)
        if not r.ok:
            raise GumroadError('%s %s -> %s: %s' % (method, path, r.status_code,
                                                    r.text[:400]))
        payload = r.json()
        # Gumroad returns HTTP 200 with success:false for domain errors.
        if isinstance(payload, dict) and payload.get('success') is False:
            raise GumroadError('%s %s -> %s' % (method, path,
                                                payload.get('message', payload)))
        return payload

    # ------------------------------------------------------------- discovery
    def me(self) -> dict:
        return self._req('GET', '/user').get('user', {})

    def products(self) -> list[dict]:
        """Every product, following pagination. See the module docstring -- this used
        to return only page one, and that truncation caused real damage."""
        out: list[dict] = []
        path = '/products'
        pages = 0
        while path:
            pages += 1
            if pages > self.MAX_PRODUCT_PAGES:
                raise GumroadError(
                    'products() exceeded %d pages -- next_page_url may be malformed; '
                    'refusing to return a partial list' % self.MAX_PRODUCT_PAGES)
            payload = self._req('GET', path)
            out.extend(payload.get('products', []))
            next_url = payload.get('next_page_url') or ''
            if next_url.startswith(_V2_PREFIX + '/'):
                next_url = next_url[len(_V2_PREFIX):]
            path = next_url or None
        return out

    def product(self, product_id: str) -> dict:
        return self._req('GET', '/products/%s' % product_id).get('product', {})

    # --------------------------------------------------------------- products
    def create_product(self, *, name: str, price_cents: int, description: str = '',
                       permalink: Optional[str] = None,
                       tags: Optional[list[str]] = None) -> dict:
        data = {'name': name, 'price': price_cents, 'description': description}
        if permalink:
            data['custom_permalink'] = permalink
        payload = {'data': data}
        if tags:
            # requests encodes a list under a repeated key, which is what Rails wants.
            payload['data'] = data
            r = self.s.post(BASE + '/products',
                            data=[('access_token', self.token),
                                  *[(k, v) for k, v in data.items()],
                                  *[('tags[]', t) for t in tags]],
                            timeout=60)
            if not r.ok:
                raise GumroadError('create -> %s: %s' % (r.status_code, r.text[:300]))
            out = r.json()
            if out.get('success') is False:
                raise GumroadError('create -> %s' % out.get('message'))
            return out.get('product', {})
        return self._req('POST', '/products', **payload).get('product', {})

    def update_product(self, product_id: str, **fields: Any) -> dict:
        return self._req('PUT', '/products/%s' % product_id,
                         data=fields).get('product', {})

    def delete_product(self, product_id: str) -> dict:
        return self._req('DELETE', '/products/%s' % product_id)

    def publish(self, product_id: str) -> dict:
        return self._req('PUT', '/products/%s/enable' % product_id).get('product', {})

    def unpublish(self, product_id: str) -> dict:
        return self._req('PUT', '/products/%s/disable' % product_id).get('product', {})

    # ------------------------------------------------------------ file upload
    def upload_file(self, path: str, name: Optional[str] = None) -> str:
        """Presign, upload the parts, complete. Returns the file_url to attach."""
        name = name or os.path.basename(path)
        size = os.path.getsize(path)
        ctype = mimetypes.guess_type(name)[0] or 'application/octet-stream'

        pre = self._req('POST', '/files/presign', data={
            'filename': name, 'file_size': size, 'content_type': ctype})
        upload_id, key = pre['upload_id'], pre['key']
        parts_spec = pre['parts']

        etags = []
        with open(path, 'rb') as f:
            for part in parts_spec:
                chunk = f.read(PART_SIZE)
                if not chunk:
                    break
                r = requests.put(part['presigned_url'], data=chunk, timeout=300)
                if not r.ok:
                    raise GumroadError('S3 part %s -> %s: %s'
                                       % (part['part_number'], r.status_code,
                                          r.text[:200]))
                etag = r.headers.get('ETag', '').strip('"')
                if not etag:
                    raise GumroadError('S3 part %s returned no ETag'
                                       % part['part_number'])
                etags.append((part['part_number'], etag))

        form = [('access_token', self.token), ('upload_id', upload_id), ('key', key)]
        for n, etag in etags:
            form.append(('parts[][part_number]', str(n)))
            form.append(('parts[][etag]', etag))
        r = self.s.post(BASE + '/files/complete', data=form, timeout=120)
        if not r.ok:
            raise GumroadError('files/complete -> %s: %s' % (r.status_code, r.text[:300]))
        out = r.json()
        if out.get('success') is False:
            raise GumroadError('files/complete -> %s' % out.get('message'))
        return pre['file_url']

    def set_files(self, product_id: str, files: list) -> dict:
        """Attach files. THIS REPLACES THE WHOLE LIST — anything omitted is removed.

        `files` items are either a url string, or a (url, display_name) pair.
        """
        form = [('access_token', self.token)]
        for item in files:
            url, name = item if isinstance(item, (tuple, list)) else (item, None)
            form.append(('files[][url]', url))
            if name:
                form.append(('files[][name]', name))
        r = self.s.put(BASE + '/products/%s' % product_id, data=form, timeout=120)
        if not r.ok:
            raise GumroadError('set_files -> %s: %s' % (r.status_code, r.text[:300]))
        out = r.json()
        if out.get('success') is False:
            raise GumroadError('set_files -> %s' % out.get('message'))
        return out.get('product', {})

    def set_cover(self, product_id: str, url: str) -> dict:
        """Covers take a signed_blob_id or a public URL — not a raw upload."""
        return self._req('POST', '/products/%s/covers' % product_id,
                         data={'url': url})
