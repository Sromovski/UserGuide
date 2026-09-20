import pytest

from covers import catalogue, render
from covers.spec import CoverSpec


def spec(**over):
    base = dict(title_lines=('Claude AI', 'for Beginners'),
                subtitle='5 GUIDES · 32 PAGES · STEP BY STEP',
                spines=('Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'),
                badge='VOL 1', footer='INSTANT PDF DOWNLOAD',
                palette_key='claude', kind='bundle')
    base.update(over)
    return CoverSpec(**base)


def test_square_render_has_the_etsy_dimensions():
    assert render.render(spec(), 'square').size == (2000, 2000)


def test_render_rejects_an_unknown_shape():
    with pytest.raises(KeyError, match='square'):
        render.render(spec(), 'billboard')


def test_background_matches_the_palette_at_the_top_edge():
    img = render.render(spec(), 'square').convert('RGB')
    r, g, b = img.getpixel((5, 5))
    assert abs(r - 255) < 12 and abs(g - 244) < 12 and abs(b - 236) < 12


def test_render_is_not_a_flat_fill():
    img = render.render(spec(), 'square').convert('RGB')
    assert len(set(img.getdata())) > 500


def test_fit_text_shrinks_a_long_string_to_fit():
    text = 'a very long product title indeed'
    f = render.fit_text(text, 300, 120)
    box = f.getbbox(text)
    # Measure the way fit_text measures — advance width, not the right edge,
    # so a non-zero left side bearing cannot make this disagree with the code.
    assert box[2] - box[0] <= 300


def test_fit_text_refuses_to_go_below_the_floor():
    with pytest.raises(ValueError, match='floor'):
        render.fit_text('x' * 400, 50, 120, floor=40)


def test_single_kind_renders_without_error():
    s = spec(kind='single', spines=('The Claude\nPrompt Vault',), badge='200')
    assert render.render(s, 'square').size == (2000, 2000)


def test_every_live_sku_renders():
    for name, s in catalogue.all_specs().items():
        assert render.render(s, 'square').size == (2000, 2000), name
