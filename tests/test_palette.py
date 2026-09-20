import pytest

from covers import palette


def test_all_five_series_have_a_palette():
    assert set(palette.PALETTES) == {'claude', 'copilot', 'codex', 'gpt', 'grok'}


def test_every_palette_is_light():
    # Cover art is deliberately light so it holds an edge against Etsy's white
    # search grid. Guard the decision: the top gradient stop must be bright.
    for key, p in palette.PALETTES.items():
        assert min(p.grad[0]) > 200, '%s top stop is too dark' % key


def test_title_ink_is_dark_enough_to_read():
    for key, p in palette.PALETTES.items():
        assert max(p.title) < 90, '%s title ink is too light' % key


def test_get_rejects_unknown_key_and_names_the_valid_ones():
    with pytest.raises(KeyError) as e:
        palette.get('gemini')
    assert 'claude' in str(e.value)


def test_get_returns_the_named_palette():
    assert palette.get('gpt').key == 'gpt'
