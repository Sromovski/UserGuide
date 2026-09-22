import pytest

from pins import copy as pc


def test_nine_skus_in_priority_order():
    assert len(pc.SKUS) == 9
    assert pc.SKUS[0] == '12-start-here'      # free lead magnet leads


def test_five_boards_and_every_sku_maps_to_one():
    assert len(pc.BOARDS) == 5
    unmapped = [s for s in pc.SKUS if pc.BOARD_FOR.get(s) not in pc.BOARDS]
    assert unmapped == []


def test_every_sku_has_a_title_within_pinterest_limit():
    bad = ['%s: %d chars' % (s, len(pc.TITLES[s]))
           for s in pc.SKUS if len(pc.TITLES.get(s, '')) > 100]
    assert bad == []


def test_every_sku_has_a_description():
    missing = [s for s in pc.SKUS if not pc.DESCRIPTIONS.get(s)]
    assert missing == []


def test_every_sku_has_a_hook_and_a_tip():
    missing = [s for s in pc.SKUS if not pc.HOOKS.get(s) or not pc.TIPS.get(s)]
    assert missing == []


def test_url_prefers_etsy_and_falls_back_to_gumroad(monkeypatch):
    monkeypatch.setattr(pc, '_etsy_url', lambda s: 'https://etsy/x')
    monkeypatch.setattr(pc, '_gumroad_url', lambda s: 'https://gumroad/x')
    assert pc.url_for('02-starter-volume') == 'https://etsy/x'
    monkeypatch.setattr(pc, '_etsy_url', lambda s: '')
    assert pc.url_for('02-starter-volume') == 'https://gumroad/x'


def test_url_raises_when_a_sku_resolves_nowhere(monkeypatch):
    monkeypatch.setattr(pc, '_etsy_url', lambda s: '')
    monkeypatch.setattr(pc, '_gumroad_url', lambda s: '')
    with pytest.raises(KeyError, match='02-starter-volume'):
        pc.url_for('02-starter-volume')


def test_every_live_sku_resolves_to_a_real_url():
    dead = []
    for s in pc.SKUS:
        try:
            u = pc.url_for(s)
        except KeyError:
            dead.append(s)
            continue
        if not u.startswith('http'):
            dead.append('%s -> %r' % (s, u))
    assert dead == []


def test_comparison_rows_are_pairs_when_present():
    bad = [s for s, rows in pc.COMPARISONS.items()
           if any(len(r) != 2 for r in rows)]
    assert bad == []


def test_palette_key_follows_the_series():
    assert pc.palette_key_for('40-chatgpt-v1') == 'gpt'
    assert pc.palette_key_for('20-copilot-v1') == 'copilot'
    assert pc.palette_key_for('02-starter-volume') == 'claude'
