"""One-time OAuth 2.0 + PKCE consent, so everything after it runs unattended.

Two ways to run it. The split form is the reliable one — it survives a closed terminal,
a mistyped paste, and anything that cannot supply interactive stdin:

    python -m etsypub.oauth --start
        Prints the Etsy consent URL and remembers the PKCE verifier on disk.

    python -m etsypub.oauth --finish "<the URL your browser landed on>"
        Exchanges the code and writes ETSY_REFRESH_TOKEN + ETSY_SHOP_ID into .env.

    python -m etsypub.oauth
        Interactive: does both, opening the browser and prompting for the paste.

Etsy's registration form only accepts an https:// callback, and nothing is served on
localhost over TLS — so after you click Allow the browser shows a connection error. That
is expected. The ?code=... in the address bar is the whole point; PKCE is what makes it
safe to move by hand, because the code is useless without the verifier.

Authorization codes expire quickly. Run --finish promptly after clicking Allow; if it
fails with an invalid_grant, just run --start again.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import urllib.parse
import webbrowser

import requests

from . import client, config

AUTH_URL = 'https://www.etsy.com/oauth/connect'
PENDING = os.path.join(config.ROOT, '.etsy_oauth_pending.json')


def _pkce() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip('=')
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
    return verifier, challenge


def _persist(key: str, value: str) -> None:
    env = os.path.join(config.ROOT, '.env')
    line = '%s=%s\n' % (key, value)
    lines = []
    if os.path.exists(env):
        with open(env, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    for i, l in enumerate(lines):
        if l.startswith(key + '='):
            lines[i] = line
            break
    else:
        lines.append(line)
    with open(env, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def start(*, open_browser: bool = True) -> str:
    if not config.KEYSTRING:
        raise SystemExit('Set ETSY_KEYSTRING in .env first.')

    verifier, challenge = _pkce()
    state = secrets.token_urlsafe(16)
    with open(PENDING, 'w', encoding='utf-8') as f:
        json.dump({'verifier': verifier, 'state': state,
                   'redirect_uri': config.REDIRECT_URI}, f)

    url = AUTH_URL + '?' + urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': config.KEYSTRING,
        'redirect_uri': config.REDIRECT_URI,
        'scope': ' '.join(config.SCOPES),
        'state': state,
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
    })
    print('Open this and click Allow:\n')
    print(url + '\n')
    print('Your browser will then land on %s and show a connection error.'
          % config.REDIRECT_URI)
    print('That is expected. Copy the FULL address from the address bar and run:\n')
    print('    python -m etsypub.oauth --finish "<that URL>"\n')
    if open_browser:
        webbrowser.open(url)
    return url


def finish(pasted: str) -> None:
    if not os.path.exists(PENDING):
        raise SystemExit('No pending consent found — run: python -m etsypub.oauth --start')
    with open(PENDING, encoding='utf-8') as f:
        pending = json.load(f)

    raw = pasted.strip().strip('"').strip("'")
    if '?' in raw:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
        res = {k: v[0] for k, v in q.items()}
    else:
        res = {'code': raw}

    if 'code' not in res:
        raise SystemExit('No ?code= in what you pasted. Etsy returned: %s' % res)
    if 'state' in res and res['state'] != pending['state']:
        raise SystemExit('State mismatch — aborting rather than trusting this redirect.')

    r = requests.post(client.TOKEN_URL, timeout=30, data={
        'grant_type': 'authorization_code',
        'client_id': config.KEYSTRING,
        'redirect_uri': pending['redirect_uri'],
        'code': res['code'],
        'code_verifier': pending['verifier'],
    })
    if not r.ok:
        raise SystemExit('Token exchange failed -> %s: %s\n'
                         'Codes expire fast — run --start again and retry promptly.'
                         % (r.status_code, r.text[:400]))
    tok = r.json()
    _persist('ETSY_REFRESH_TOKEN', tok['refresh_token'])
    print('Refresh token saved to .env.')

    # The access token is "<user_id>.<random>", so the user id is free. The SHOP id is a
    # different number and has to be asked for.
    e = client.Etsy(refresh_token=tok['refresh_token'])
    e.access_token = tok['access_token']
    e.s.headers['Authorization'] = 'Bearer ' + tok['access_token']
    user_id = str(tok['access_token']).split('.')[0]
    try:
        shops = e._req('GET', '/users/%s/shops' % user_id)
        shop = shops if 'shop_id' in shops else (shops.get('results') or [{}])[0]
    except Exception as exc:                                  # noqa: BLE001
        print('Could not read the shop id automatically: %s' % exc)
        shop = {}
    if shop.get('shop_id'):
        _persist('ETSY_SHOP_ID', str(shop['shop_id']))
        print('Shop: %s (id %s) — saved to .env.'
              % (shop.get('shop_name'), shop['shop_id']))
    else:
        print('Set ETSY_SHOP_ID in .env by hand — find it in your Etsy shop URL.')

    os.remove(PENDING)
    print('\nNext: python -m etsypub.publish --preflight')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--start', action='store_true', help='print the consent URL')
    ap.add_argument('--finish', metavar='URL', help='exchange the code from that URL')
    ap.add_argument('--no-browser', action='store_true')
    a = ap.parse_args()

    if a.finish:
        finish(a.finish)
    elif a.start:
        start(open_browser=not a.no_browser)
    else:
        start(open_browser=not a.no_browser)
        finish(input('Pasted URL: '))


if __name__ == '__main__':
    main()
