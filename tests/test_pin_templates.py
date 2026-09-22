# tests/test_pin_templates.py
from covers import palette
from pins import copy as pc
from pins import canvas, templates


def test_six_templates_named_exactly():
    assert set(templates.TEMPLATES) == {'product', 'listicle', 'hook',
                                        'checklist', 'comparison', 'tip'}


def test_every_template_renders_or_skips_for_every_sku():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is None:
                continue
            if img.size != (canvas.PIN_W, canvas.PIN_H):
                offenders.append('%s/%s -> %s' % (name, sku, img.size))
    assert offenders == []


def test_product_template_never_skips():
    skipped = [s for s in pc.SKUS
               if templates.TEMPLATES['product'](s, palette.get(pc.palette_key_for(s))) is None]
    assert skipped == []


def test_comparison_skips_a_sku_with_no_curated_rows():
    sku = next(s for s in pc.SKUS if s not in pc.COMPARISONS)
    assert templates.TEMPLATES['comparison'](sku, palette.get(pc.palette_key_for(sku))) is None


def test_no_template_paints_into_the_margin():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            pal = palette.get(pc.palette_key_for(sku))
            img = fn(sku, pal)
            if img is not None and canvas.overflows(img, pal):
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []


def test_comparison_budgets_two_line_rows_not_one(monkeypatch):
    # row_h used to be a single line's height even though the wrap check above
    # it allows two-line cells -- six two-line rows drew 106px per row into a
    # 53px reservation, so the block's own text ran to y~1371 against the
    # `bottom` budget of PIN_H - MARGIN - 110 = 1318 the code's own comment
    # promises ("the last row's own text always ends at `bottom`"). Force
    # every cell onto two lines and check that promise actually holds, with
    # slack only for glyph descenders -- not the finished pin, which always
    # trips footer_collision because footer() has by then stamped ink into
    # that same band.
    sku = '02-starter-volume'
    two_line_row = ('Limited usage available today', 'Limited usage available today')
    monkeypatch.setitem(pc.COMPARISONS, sku, [two_line_row] * 6)
    pal = palette.get(pc.palette_key_for(sku))
    img = templates.TEMPLATES['comparison'](sku, pal)
    assert img is not None
    assert canvas.overflows(img, pal) is False
    bottom_budget = (canvas.PIN_H - canvas.MARGIN - 110) / float(canvas.PIN_H)
    assert canvas.content_extent(img, pal) <= bottom_budget + 0.01


def test_no_pin_is_a_flat_fill():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is not None and len(set(img.convert('RGB').getdata())) < 400:
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []
