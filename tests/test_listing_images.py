import os

import build_etsy_kit as kit


def sku(name):
    return next(s for s in kit.SKUS if s['sku'] == name)


def test_main_image_is_the_new_square_render():
    img = kit.img_main(sku('02-starter-volume'), None)
    assert img.size == (2000, 2000)


def test_pin_image_is_two_to_three():
    assert kit.img_pin(sku('02-starter-volume')).size == (1000, 1500)


def test_wide_image_is_landscape_for_gumroad():
    img = kit.img_wide(sku('02-starter-volume'))
    assert img.size == (1280, 720)


def test_main_image_no_longer_needs_the_pdf():
    # The cover is generated, not composited, so a missing PDF must not break it.
    assert kit.img_main(sku('30-codex-v1'), '/does/not/exist.pdf').size == (2000, 2000)
