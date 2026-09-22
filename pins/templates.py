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
    y = canvas.fitted_heading(img, text, 430, pal, max_size=size)
    rec = pc.sku_record(sku)
    sub = rec['headline'].replace('\n', ' ')
    lines = canvas.wrap_lines(sub, inner, 34)
    canvas.draw_block(img, canvas.MARGIN, y + 46, lines, 34, pal.muted)
    canvas.footer(img, pal)
    return img


def _listicle(sku, pal):
    rec = pc.sku_record(sku)
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, "WHAT'S\nINSIDE", 120, pal, max_size=86)
    y += 40
    inner = canvas.PIN_W - canvas.MARGIN * 2 - 54
    for i, b in enumerate(rec['bullets'][:6], start=1):
        wrapped = canvas.wrap_lines(b, inner, 28)
        lines = wrapped[:2]
        if len(wrapped) > 2:
            lines[-1] = _ellipsize(lines[-1], inner, 28)
        canvas.draw_block(img, canvas.MARGIN, y, ['%d' % i], 30, pal.spine_front)
        y = canvas.draw_block(img, canvas.MARGIN + 54, y, lines, 28, pal.title)
        y += 22
        if y > canvas.PIN_H - canvas.MARGIN - 90:
            break
    canvas.footer(img, pal)
    return img


def _checklist(sku, pal):
    rec = pc.sku_record(sku)
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, 'YOUR\nCHECKLIST', 120, pal, max_size=86)
    y += 40
    tick = 26
    inner = canvas.PIN_W - canvas.MARGIN * 2 - tick - 30
    d = ImageDraw.Draw(img)
    for b in rec['bullets'][:5]:
        wrapped = canvas.wrap_lines(b, inner, 28)
        lines = wrapped[:2]
        if len(wrapped) > 2:
            lines[-1] = _ellipsize(lines[-1], inner, 28)
        d.rounded_rectangle(
            [canvas.MARGIN, y + 6, canvas.MARGIN + tick, y + 6 + tick],
            radius=6, fill=pal.spine_front)
        y = canvas.draw_block(img, canvas.MARGIN + tick + 30, y, lines, 28,
                              pal.title)
        y += 22
        if y > canvas.PIN_H - canvas.MARGIN - 90:
            break
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
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, heading, 130, pal, max_size=64)
    y += 60
    d = ImageDraw.Draw(img)
    row_h = 90
    for left, right in rows:
        canvas.draw_block(img, canvas.MARGIN, y, [left], 34, pal.title)
        rfnt = render.font(34, True)
        rw = render._width(right, rfnt)
        canvas.draw_block(img, canvas.PIN_W - canvas.MARGIN - rw, y, [right],
                          34, pal.spine_front)
        rule_y = y + row_h - 24
        d.line([(canvas.MARGIN, rule_y), (canvas.PIN_W - canvas.MARGIN, rule_y)],
              fill=pal.muted, width=1)
        y += row_h
        if y > canvas.PIN_H - canvas.MARGIN - 90:
            break
    canvas.footer(img, pal)
    return img


def _tip(sku, pal):
    text = pc.TIPS.get(sku)
    if not text:
        return None
    inner = canvas.PIN_W - canvas.MARGIN * 2
    if not canvas.fits(text.split()[0], inner, 36):
        return None
    img = canvas.new_pin(pal)
    canvas.draw_block(img, canvas.MARGIN, canvas.PIN_H // 3 - 80, ['TIP'], 26,
                      pal.spine_front)
    lines = canvas.wrap_lines(text, inner, 36)
    canvas.draw_block(img, canvas.MARGIN, canvas.PIN_H // 3, lines, 36,
                      pal.title)
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
