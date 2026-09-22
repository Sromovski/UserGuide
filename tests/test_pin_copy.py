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


def test_etsy_url_is_empty_unless_the_row_is_active(monkeypatch):
    # Etsy listings expire after four months and --status writes that back to
    # the db, so a row can carry a stale `url` for a listing that is no
    # longer live. Only state == 'active' means it is actually there.
    monkeypatch.setattr(pc, '_edb',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://etsy/x', 'state': 'expired'})})())
    assert pc._etsy_url('02-starter-volume') == ''


def test_gumroad_url_is_empty_unless_published(monkeypatch):
    monkeypatch.setattr(pc, '_gp',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://gumroad/x', 'published': 0})})())
    assert pc._gumroad_url('02-starter-volume') == ''


def test_url_for_falls_through_an_inactive_etsy_row_to_gumroad(monkeypatch):
    monkeypatch.setattr(pc, '_edb',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://etsy/dead', 'state': 'expired'})})())
    monkeypatch.setattr(pc, '_gp',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://gumroad/live', 'published': 1})})())
    assert pc.url_for('02-starter-volume') == 'https://gumroad/live'


def test_url_for_raises_when_both_channels_are_dead(monkeypatch):
    monkeypatch.setattr(pc, '_edb',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://etsy/dead', 'state': 'expired'})})())
    monkeypatch.setattr(pc, '_gp',
                        type('M', (), {'get': staticmethod(
                            lambda s: {'url': 'https://gumroad/dead', 'published': 0})})())
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
