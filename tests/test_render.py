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


def test_no_sku_renders_its_badge_off_canvas():
    # Pillow silently clips a paste box past the canvas edge, so a badge that
    # runs off the right side is invisible to a size assertion. 10 of 21 SKUs
    # did exactly that before the clamp. Collect every offender — asserting
    # inside the loop would report only the first and hide the rest.
    offenders = []
    for name, spec in catalogue.all_specs().items():
        img = render.render(spec, 'square').convert('RGB')
        pal = spec.palette
        w, h = img.size
        px = img.load()
        # the badge is the only element painted in badge_bg; scan the right edge
        edge_hits = [y for y in range(h) if px[w - 2, y] == pal.badge_bg]
        if edge_hits:
            offenders.append('%s paints badge colour on the right edge' % name)
    assert offenders == [], '\n'.join(offenders)


def test_rotation_matches_the_css_direction():
    # CSS rotate(+N) is clockwise; PIL rotate(+N) is counter-clockwise. The
    # constants come from the CSS, so the renderer must negate on the way in.
    # A tall red bar rotated CLOCKWISE puts its top edge to the RIGHT of centre.
    from PIL import Image
    bar = Image.new('RGBA', (40, 400), (255, 0, 0, 255))
    base = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
    render._paste_rotated(base, bar, (300, 300), 30, render.palette.get('claude'),
                          shadow=False)
    px = base.load()
    top_xs = [x for x in range(600) if px[x, 180][3] > 0]
    assert top_xs, 'nothing drawn'
    assert sum(top_xs) / len(top_xs) > 300, 'rotation is mirrored vs the CSS'
