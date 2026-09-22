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
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is not None and canvas.overflows(img):
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []


def test_no_pin_is_a_flat_fill():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is not None and len(set(img.convert('RGB').getdata())) < 400:
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []
