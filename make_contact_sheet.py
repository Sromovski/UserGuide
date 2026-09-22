#!/usr/bin/env python3
"""Render one pin per template into a single contact sheet for eyeballing.

The automated guards in pins/canvas.py (overflows, footer_collision,
content_extent) check CONTAINMENT and REACH -- whether ink sits in a margin
or footer band, whether it fills enough of the canvas. They cannot tell you
whether a pin is actually any good: whether the hook lands, whether the
comparison rows read cleanly at a glance, whether a palette choice looks
right next to the others. That is a human judgement call, and the only way
to make it is to look at the pins side by side.

Run this before a posting batch, not as part of `build_pins.py` -- it is a
review aid, not a guard, and it is not wired into the build.

Usage:
    python make_contact_sheet.py                  # one column per template,
                                                    # first SKU with curated
                                                    # content for that template
    python make_contact_sheet.py --sku 02-starter-volume   # that SKU only,
                                                    # templates it skips are
                                                    # left out of the sheet
"""
import argparse
import os

from PIL import Image, ImageDraw

from covers import palette
from pins import copy as pc
from pins import templates as _templates

ROOT = r'C:\Projects\UserGuide'
OUT_PATH = os.path.join(ROOT, 'outputs', 'pins', '_contact_sheet.png')

THUMB_W = 300
THUMB_H = int(THUMB_W * 1.5)          # pins are 2:3, same as PIN_W/PIN_H
LABEL_H = 34
GAP = 12
BG = (10, 10, 16)
LABEL_BG = (10, 10, 16)
LABEL_FG = (240, 240, 240)


def _first_render(name, fn):
    """The (sku, image) for the first SKU that doesn't skip this template."""
    for sku in pc.SKUS:
        pal = palette.get(pc.palette_key_for(sku))
        img = fn(sku, pal)
        if img is not None:
            return sku, img
    return None, None


def build(sku=None):
    """Render every template, return a list of (label, PIL.Image)."""
    cells = []
    for name, fn in _templates.TEMPLATES.items():
        if sku is not None:
            pal = palette.get(pc.palette_key_for(sku))
            img = fn(sku, pal)
            if img is None:
                print('SKIP  %s/%s -- template returned None for this SKU' % (name, sku))
                continue
            cells.append(('%s / %s' % (name, sku), img))
        else:
            found_sku, img = _first_render(name, fn)
            if img is None:
                print('SKIP  %s -- no SKU renders it' % name)
                continue
            cells.append(('%s / %s' % (name, found_sku), img))
    return cells


def render_sheet(cells):
    n = len(cells)
    if n == 0:
        raise SystemExit('nothing to render -- every template skipped')
    w = n * THUMB_W + (n + 1) * GAP
    h = LABEL_H + THUMB_H + GAP * 2
    sheet = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(sheet)
    x = GAP
    for label, img in cells:
        d.text((x, 8), label, fill=LABEL_FG)
        thumb = img.convert('RGB').resize((THUMB_W, THUMB_H), Image.LANCZOS)
        sheet.paste(thumb, (x, LABEL_H + GAP))
        x += THUMB_W + GAP
    return sheet


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sku', default=None,
                    help='render every template for this SKU only, instead of '
                         'the first SKU that has curated content for each')
    args = ap.parse_args()

    if args.sku is not None and args.sku not in pc.SKUS:
        raise SystemExit('unknown SKU %r -- valid: %s'
                         % (args.sku, ', '.join(pc.SKUS)))

    cells = build(args.sku)
    sheet = render_sheet(cells)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    sheet.save(OUT_PATH, 'PNG', optimize=True)
    print('%d pin(s) -> %s' % (len(cells), OUT_PATH))


if __name__ == '__main__':
    main()
