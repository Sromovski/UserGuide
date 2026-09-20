import pytest

import build_etsy_kit as kit
from covers import catalogue


def by_sku(name):
    return next(s for s in kit.SKUS if s['sku'] == name)


def test_every_live_sku_produces_a_valid_spec():
    specs = catalogue.all_specs()
    assert len(specs) == len(kit.SKUS) == 21


def test_palette_follows_the_pdf_prefix():
    assert catalogue.palette_for(by_sku('20-copilot-v1')) == 'copilot'
    assert catalogue.palette_for(by_sku('30-codex-v1')) == 'codex'
    assert catalogue.palette_for(by_sku('02-starter-volume')) == 'claude'


def test_explicit_palette_key_wins():
    assert catalogue.palette_for({'pdf': 'Anything.pdf', 'palette': 'grok'}) == 'grok'


def test_the_four_single_products_are_single_kind():
    for name in ('01-prompt-vault', '05-config-pack',
                 '11-cost-calculator', '12-start-here'):
        assert catalogue.kind_for(by_sku(name)) == 'single', name


def test_volumes_are_bundles():
    assert catalogue.kind_for(by_sku('02-starter-volume')) == 'bundle'


def test_subtitle_is_the_badges_joined():
    spec = catalogue.spec_for(by_sku('02-starter-volume'))
    assert spec.subtitle == '5 GUIDES · 32 PAGES · STEP BY STEP'


def test_badge_uses_the_volume_number_when_present():
    assert catalogue.spec_for(by_sku('02-starter-volume')).badge == 'VOL 1'


def test_start_here_footer_says_free():
    assert catalogue.spec_for(by_sku('12-start-here')).footer == 'FREE DOWNLOAD'


def test_missing_spines_is_a_hard_error():
    with pytest.raises(KeyError, match='spines'):
        catalogue.spec_for({'sku': 'x', 'pdf': 'x.pdf', 'headline': 'A\nB',
                            'badges': ['ONE']})


def test_every_sku_declares_spines():
    missing = [s['sku'] for s in kit.SKUS if not s.get('spines')]
    assert missing == []


def test_spine_labels_are_short_enough_to_read_on_a_spine():
    # Check each spine's own lines. Joining the spines first would invent lines
    # that span two labels and fail on correct data.
    for s in kit.SKUS:
        for spine in s['spines']:
            for line in spine.split('\n'):
                assert len(line) <= 18, (s['sku'], line)
