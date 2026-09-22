from covers import palette
from pins import canvas


def test_pin_dimensions_are_pinterest_two_to_three():
    assert (canvas.PIN_W, canvas.PIN_H) == (1000, 1500)
    assert round(canvas.PIN_W / canvas.PIN_H, 3) == 0.667


def test_new_pin_uses_the_palette_gradient():
    img = canvas.new_pin(palette.get('gpt'))
    assert img.size == (1000, 1500)
    r, g, b = img.convert('RGB').getpixel((5, 5))
    assert abs(r - 250) < 12 and abs(g - 247) < 12 and abs(b - 255) < 12


def test_wrap_lines_breaks_on_words_not_characters():
    lines = canvas.wrap_lines('the quick brown fox jumps over the lazy dog', 300, 40)
    assert len(lines) > 1
    for ln in lines:
        assert not ln.startswith(' ') and not ln.endswith(' ')
    assert ' '.join(lines) == 'the quick brown fox jumps over the lazy dog'


def test_draw_block_returns_a_y_below_where_it_started():
    img = canvas.new_pin(palette.get('claude'))
    y = canvas.draw_block(img, 72, 200, ['one', 'two'], 40, (0, 0, 0))
    assert y > 200


def test_overflows_is_false_for_an_empty_pin():
    assert canvas.overflows(canvas.new_pin(palette.get('claude'))) is False


def test_overflows_is_true_when_ink_sits_in_the_margin():
    from PIL import ImageDraw
    img = canvas.new_pin(palette.get('claude'))
    ImageDraw.Draw(img).rectangle([0, 700, 40, 760], fill=(0, 0, 0))
    assert canvas.overflows(img) is True
