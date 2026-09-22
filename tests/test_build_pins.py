import pytest

import build_pins
from pins import copy as pc


def test_build_returns_a_row_per_rendered_pin(tmp_path, monkeypatch):
    monkeypatch.setattr(build_pins, 'OUT', str(tmp_path))
    rows = build_pins.build(skus=['12-start-here'])
    assert rows
    for r in rows:
        assert set(r) == {'sku', 'template', 'file', 'title', 'description',
                          'url', 'board'}


def test_build_skips_rather_than_inventing(tmp_path, monkeypatch):
    monkeypatch.setattr(build_pins, 'OUT', str(tmp_path))
    rows = build_pins.build(skus=['12-start-here'], templates=['comparison'])
    assert rows == []          # no curated comparison rows for this SKU


def test_verify_destinations_rejects_an_over_long_title():
    rows = [{'sku': 'x', 'template': 't', 'file': 'f', 'title': 'x' * 101,
             'description': 'd', 'url': 'https://e', 'board': 'b'}]
    with pytest.raises(SystemExit, match='101'):
        build_pins.verify_destinations(rows)


def test_verify_destinations_rejects_a_dead_url():
    rows = [{'sku': 'x', 'template': 't', 'file': 'f', 'title': 'ok',
             'description': 'd', 'url': '', 'board': 'b'}]
    with pytest.raises(SystemExit, match='url'):
        build_pins.verify_destinations(rows)


def test_verify_destinations_reports_every_offender_not_just_the_first():
    rows = [{'sku': 'a', 'template': 't', 'file': 'f', 'title': '',
             'description': 'd', 'url': 'https://e', 'board': 'b'},
            {'sku': 'b', 'template': 't', 'file': 'f', 'title': 'ok',
             'description': '', 'url': 'https://e', 'board': 'b'}]
    with pytest.raises(SystemExit) as e:
        build_pins.verify_destinations(rows)
    assert 'a' in str(e.value) and 'b' in str(e.value)


def test_write_csv_has_a_header_and_one_row_per_pin(tmp_path, monkeypatch):
    monkeypatch.setattr(build_pins, 'OUT', str(tmp_path))
    rows = build_pins.build(skus=['12-start-here'])
    path = build_pins.write_csv(rows)
    lines = open(path, encoding='utf-8').read().strip().splitlines()
    assert lines[0].startswith('sku,template,file,title,description,url,board')
    assert len(lines) == len(rows) + 1


def test_no_canvas_template_leaves_the_bottom_half_empty():
    # A 2:3 pin exists for its vertical space. Anything that stacks content in
    # the top third reads as unfinished in a feed. `product` is exempt: it is
    # the approved cover art, rendered by covers/.
    from covers import palette
    from pins import copy as pc, templates, canvas
    thin = []
    for name, fn in templates.TEMPLATES.items():
        if name == 'product':
            continue
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is None:
                continue
            e = canvas.content_extent(img, palette.get(pc.palette_key_for(sku)))
            if e < 0.70:
                thin.append('%s/%s -> %.2f' % (name, sku, e))
    assert thin == [], '\n'.join(thin)
