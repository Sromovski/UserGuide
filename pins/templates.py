# pins/templates.py
"""Six pin layouts.

Every template returns None rather than drawing something clipped or invented.
A skip is honest; a clipped pin is not, and a padded one is worse.
"""
from PIL import ImageDraw

from covers import catalogue, render

from pins import canvas
from pins import copy as pc


def _safe_heading_size(text, inner, start, floor=18):
    """The largest size at which EVERY line of a multi-line heading fits.

    `canvas.fitted_heading` sizes off `max(lines, key=len)` -- the line with
    the most CHARACTERS, not the most PIXELS. Two lines can tie on character
    count and still differ in rendered width (digits and commas are narrower
    than some letters), so the line fitted_heading did not measure can run
    past the margin at the size it picked. This checks every line at once and
    returns the size fitted_heading should be capped to, or None if no size
    down to `floor` fits them all.
    """
    lines = text.split('\n')
    size = start
    while size >= floor:
        fnt = render.font(size, True)
        if all(render._width(ln, fnt) <= inner for ln in lines):
            return size
        size -= 1
    return None


def _ellipsize(line, max_w, size):
    """Shrink `line` until `line + '...'` measures within `max_w` at `size`.

    A flat `rstrip(...) + '...'` on an already-width-fitted line can push it
    past `max_w`, because the appended dots were never accounted for in the
    original wrap. This re-measures after every trim so the truncated line
    is guaranteed to fit, not just assumed to.
    """
    fnt = render.font(size, True)
    base = line.rstrip(' ,.')
    text = base + '...'
    while render._width(text, fnt) > max_w and base:
        base = base[:-1].rstrip(' ,.')
        text = base + '...'
    return text


def _draw_right_aligned(img, right_x, y, lines, size, colour, leading=1.30):
    """Like canvas.draw_block, but each line's right edge lands at `right_x`."""
    d = ImageDraw.Draw(img)
    fnt = render.font(size, True)
    for ln in lines:
        w = render._width(ln, fnt)
        d.text((right_x - w, y), ln, font=fnt, fill=colour)
        y += int(size * leading)
    return y


def _card_fill(pal):
    """A light panel colour a few shades off the page background.

    Lightens the gradient's middle stop toward white rather than hardcoding a
    colour, so the card stays legible against all five series palettes.
    """
    r, g, b = pal.grad[1]
    return (min(255, int(r + (255 - r) * 0.55)),
            min(255, int(g + (255 - g) * 0.55)),
            min(255, int(b + (255 - b) * 0.55)))


def _product(sku, pal):
    return render.render(catalogue.spec_for(pc.sku_record(sku)), 'pin')


def _hook(sku, pal):
    text = pc.HOOKS.get(sku)
    if not text:
        return None
    inner = canvas.PIN_W - canvas.MARGIN * 2
    size = _safe_heading_size(text, inner, 104)
    if size is None:
        return None
    img = canvas.new_pin(pal)
    # Heading starts well below centre and the subtitle gets real separation
    # and a bigger, more generously leaded font, so the block reaches past
    # 70% of the canvas instead of stopping under half.
    y = canvas.fitted_heading(img, text, 580, pal, max_size=size)
    rec = pc.sku_record(sku)
    sub = rec['headline'].replace('\n', ' ')
    lines = canvas.wrap_lines(sub, inner, 42)
    y = canvas.draw_block(img, canvas.MARGIN, y + 90, lines, 42, pal.muted,
                          leading=1.42)

    # A thick accent bar anchored low on the canvas. A short hook plus a
    # one-line product name naturally stops around 55-60%, even with the
    # extra separation above -- this is what closes the rest of the gap
    # without inventing more copy. Anchored to whichever is lower: the
    # natural end of the subtitle, or a fixed point past 70% of the canvas.
    d = ImageDraw.Draw(img)
    bar_y = max(y + 60, canvas.PIN_H - canvas.MARGIN - 260)
    d.rounded_rectangle([canvas.MARGIN, bar_y, canvas.MARGIN + 140, bar_y + 14],
                        radius=7, fill=pal.spine_front)
    canvas.footer(img, pal)
    return img


def _listicle(sku, pal):
    rec = pc.sku_record(sku)
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, "WHAT'S\nINSIDE", 110, pal, max_size=86)
    top = y + 60
    bottom = canvas.PIN_H - canvas.MARGIN - 120
    inner = canvas.PIN_W - canvas.MARGIN * 2 - 54
    bullets = rec['bullets'][:6]
    items = []
    for b in bullets:
        wrapped = canvas.wrap_lines(b, inner, 28)
        lines = wrapped[:2]
        if len(wrapped) > 2:
            lines[-1] = _ellipsize(lines[-1], inner, 28)
        items.append(lines)

    # Spread the items across the FULL usable height rather than bunching
    # them under the heading -- the slot is computed from the space actually
    # available and the item count, so 3 bullets and 6 bullets both reach the
    # bottom of the canvas instead of stopping wherever the last one lands.
    n = max(len(items), 1)
    slot = (bottom - top) // n
    y = top
    for i, lines in enumerate(items, start=1):
        canvas.draw_block(img, canvas.MARGIN, y, ['%d' % i], 32, pal.spine_front)
        canvas.draw_block(img, canvas.MARGIN + 54, y, lines, 28, pal.title,
                          leading=1.34)
        y += slot
    canvas.footer(img, pal)
    return img


def _checklist(sku, pal):
    """A printable to-do card -- distinct STRUCTURE from `_listicle`, not
    just a different glyph: a light rounded card, outlined (not filled) tick
    boxes, and a lower item cap so the density visibly differs.
    """
    rec = pc.sku_record(sku)
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, 'YOUR\nCHECKLIST', 110, pal, max_size=86)

    card_x0 = canvas.MARGIN
    card_x1 = canvas.PIN_W - canvas.MARGIN
    card_y0 = y + 50
    card_y1 = canvas.PIN_H - canvas.MARGIN - 90

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=28,
                        fill=_card_fill(pal), outline=pal.muted, width=2)

    pad = 36
    tick = 36
    size = 27
    inner = (card_x1 - card_x0) - pad * 2 - tick - 24
    bullets = rec['bullets'][:5]
    items = []
    for b in bullets:
        wrapped = canvas.wrap_lines(b, inner, size)
        lines = wrapped[:2]
        if len(wrapped) > 2:
            lines[-1] = _ellipsize(lines[-1], inner, size)
        items.append(lines)

    n = max(len(items), 1)
    inner_top = card_y0 + pad
    inner_bottom = card_y1 - pad
    slot = (inner_bottom - inner_top) // n
    box_x = card_x0 + pad
    text_x = box_x + tick + 24
    yy = inner_top
    for lines in items:
        d.rounded_rectangle([box_x, yy + 2, box_x + tick, yy + 2 + tick],
                            radius=8, outline=pal.spine_front, width=4)
        canvas.draw_block(img, text_x, yy, lines, size, pal.title, leading=1.34)
        yy += slot

    canvas.footer(img, pal)
    return img


def _comparison(sku, pal):
    rows = pc.COMPARISONS.get(sku)
    if not rows:
        return None
    rec = pc.sku_record(sku)
    inner = canvas.PIN_W - canvas.MARGIN * 2
    heading = rec['headline'].replace('\n', ' ')
    if not canvas.fits(heading, inner, 64):
        return None

    # Each cell gets half the inner width minus a gutter between columns, and
    # is wrapped -- 'Agent mode' / 'Uses credits' / 'Limited usage' are all
    # multi-word and unwrapped text can overlap mid-canvas, which the
    # margin-only overflow guard cannot see. A cell that still needs more
    # than 2 lines at that width means the row cannot be drawn without
    # overlap, so the whole pin is skipped rather than risking that overlap.
    gutter = 40
    col_w = (inner - gutter) // 2
    wrapped_rows = []
    for left, right in rows:
        left_lines = canvas.wrap_lines(left, col_w, 40)
        right_lines = canvas.wrap_lines(right, col_w, 40)
        if len(left_lines) > 2 or len(right_lines) > 2:
            return None
        wrapped_rows.append((left_lines, right_lines))

    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, heading, 150, pal, max_size=64)

    # Space-between, not evenly-sliced-and-left-top-anchored: a fixed number
    # of even slots starting from the top leaves a large trailing gap after
    # the LAST row whenever there are few rows (3 rows x a big slot each
    # leaves most of that slot blank under the last one). Instead the gap
    # BETWEEN rows is computed from the actual text height and row count so
    # the last row's own text always ends at `bottom`, whether there are 3
    # rows or 6.
    row_h = int(40 * 1.34)
    top = y + 70
    bottom = canvas.PIN_H - canvas.MARGIN - 110
    n = len(wrapped_rows)
    total_text = n * row_h
    gap = (bottom - top - total_text) / max(n - 1, 1) if n > 1 else 0

    d = ImageDraw.Draw(img)
    yy = float(top)
    for i, (left_lines, right_lines) in enumerate(wrapped_rows):
        iy = int(yy)
        canvas.draw_block(img, canvas.MARGIN, iy, left_lines, 40, pal.title,
                          leading=1.34)
        _draw_right_aligned(img, canvas.PIN_W - canvas.MARGIN, iy, right_lines,
                            40, pal.spine_front, leading=1.34)
        if i < n - 1:
            rule_y = iy + row_h + int(gap / 2)
            d.line([(canvas.MARGIN, rule_y), (canvas.PIN_W - canvas.MARGIN, rule_y)],
                  fill=pal.muted, width=2)
        yy += row_h + gap
    canvas.footer(img, pal)
    return img


def _tip(sku, pal):
    """A quote card: one sentence, set large, wrapped across the middle of
    the canvas and centred within a band that is itself biased toward the
    lower two-thirds -- a short tip still has to reach past 70% of the
    canvas, not just sit wherever a true geometric centre would put it.
    """
    text = pc.TIPS.get(sku)
    if not text:
        return None
    inner = canvas.PIN_W - canvas.MARGIN * 2
    if not canvas.fits(text.split()[0], inner, 40):
        return None

    size = 60
    lines = canvas.wrap_lines(text, inner, size)
    while size > 34 and len(lines) > 7:
        size -= 4
        lines = canvas.wrap_lines(text, inner, size)

    leading = 1.42
    block_h = len(lines) * int(size * leading)

    img = canvas.new_pin(pal)
    canvas.draw_block(img, canvas.MARGIN, 150, ['TIP'], 28, pal.spine_front)

    band_top, band_bottom = 620, 1350
    band = band_bottom - band_top
    y = band_top + max(0, (band - block_h) // 2)
    canvas.draw_block(img, canvas.MARGIN, y, lines, size, pal.title,
                      leading=leading)

    d = ImageDraw.Draw(img)
    rule_y = min(y + block_h + 50, canvas.PIN_H - canvas.MARGIN - 130)
    d.line([(canvas.MARGIN, rule_y), (canvas.MARGIN + 90, rule_y)],
          fill=pal.spine_front, width=6)

    canvas.footer(img, pal)
    return img


TEMPLATES = {
    'product': _product,
    'listicle': _listicle,
    'hook': _hook,
    'checklist': _checklist,
    'comparison': _comparison,
    'tip': _tip,
}
