from covers import catalogue, render


def test_shape_dimensions_match_the_destinations():
    assert render.SHAPES == {'square': (2000, 2000),
                             'wide': (1280, 720),
                             'pin': (1000, 1500),
                             'letter': (1700, 2200)}


def test_wide_is_landscape_so_gumroad_stops_cropping():
    img = render.render(catalogue.all_specs()['02-starter-volume'], 'wide')
    assert img.size == (1280, 720)
    assert img.width > img.height


def test_pin_is_the_pinterest_two_to_three_ratio():
    img = render.render(catalogue.all_specs()['02-starter-volume'], 'pin')
    assert img.size == (1000, 1500)
    assert round(img.width / img.height, 3) == 0.667


def test_all_three_shapes_render_for_all_21_skus():
    # Collect every offender rather than asserting inside the loop — asserting
    # inside the loop aborts on the first failure and hides the rest.
    offenders = []
    for name, spec in catalogue.all_specs().items():
        for shape in ('square', 'wide', 'pin'):
            img = render.render(spec, shape)
            if img.size != render.SHAPES[shape]:
                offenders.append((name, shape, img.size))
    assert offenders == []


def test_no_shape_renders_flat():
    offenders = []
    for shape in ('square', 'wide', 'pin'):
        img = render.render(catalogue.all_specs()['30-codex-v1'], shape)
        if len(set(img.convert('RGB').getdata())) <= 500:
            offenders.append(shape)
    assert offenders == []


def test_square_front_book_width_is_identical_within_each_kind():
    # Book WIDTH derives from the canvas alone and must never vary with a SKU's
    # title length. Height deliberately does vary — a shorter title leaves more
    # room and the books grow into it, which is the approved behaviour.
    widths = {'bundle': {}, 'single': {}}
    for name, spec in catalogue.all_specs().items():
        img = render.render(spec, 'square').convert('RGB')
        w, h = img.size
        px = img.load()
        target = spec.palette.spine_front
        best = 0
        for y in range(int(h * 0.55), int(h * 0.95), 4):
            xs = [x for x in range(0, w, 2) if px[x, y] == target]
            if xs:
                best = max(best, max(xs) - min(xs))
        assert best, '%s: front spine colour not found' % name
        widths[spec.kind][name] = best
    for kind, found in widths.items():
        distinct = set(found.values())
        assert len(distinct) == 1, '%s width varies by SKU: %s' % (kind, found)
