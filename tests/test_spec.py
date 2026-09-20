import pytest

from covers.spec import CoverSpec


def ok(**over):
    base = dict(title_lines=('Claude AI', 'for Beginners'),
                subtitle='5 GUIDES · 32 PAGES · STEP BY STEP',
                spines=('Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'),
                badge='VOL 1', footer='INSTANT PDF DOWNLOAD',
                palette_key='claude', kind='bundle')
    base.update(over)
    return CoverSpec(**base)


def test_resolves_its_palette():
    assert ok().palette.spine_front == (226, 84, 43)


def test_rejects_more_than_two_title_lines():
    with pytest.raises(ValueError, match='title_lines'):
        ok(title_lines=('a', 'b', 'c'))


def test_rejects_no_title_lines():
    with pytest.raises(ValueError, match='1 or 2 lines'):
        ok(title_lines=())


def test_rejects_an_empty_title_line():
    with pytest.raises(ValueError, match='must not contain empty strings'):
        ok(title_lines=('Title', ''))


def test_rejects_more_than_three_spines():
    with pytest.raises(ValueError, match='spines'):
        ok(spines=('a', 'b', 'c', 'd'))


def test_single_kind_must_have_exactly_one_spine():
    with pytest.raises(ValueError, match='single'):
        ok(kind='single', spines=('a', 'b', 'c'))


def test_bundle_kind_must_have_three_spines():
    with pytest.raises(ValueError, match='bundle'):
        ok(kind='bundle', spines=('a',))


def test_rejects_unknown_kind():
    with pytest.raises(ValueError, match='kind'):
        ok(kind='boxset')


def test_rejects_unknown_palette():
    with pytest.raises(KeyError):
        ok(palette_key='gemini')
