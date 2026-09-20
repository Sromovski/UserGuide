"""Direction C — the angled 3D stack.

One renderer draws every shape, so the PDF cover page and the listing images
cannot drift apart. Visual reference: outputs/design/cover-system.html
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from covers import palette

FONT_DIR = r'C:\Windows\Fonts'
BOLD = ['seguibl.ttf', 'arialbd.ttf', 'segoeuib.ttf']
REG = ['segoeui.ttf', 'arial.ttf']

SHAPES = {'square': (2000, 2000), 'wide': (1280, 720), 'pin': (1000, 1500),
         'letter': (1700, 2200)}

# rotation, in degrees, of each element. Fixed by the approved design.
ROT_BACK_LEFT, ROT_FRONT, ROT_BACK_RIGHT = -8, -2, 6
ROT_SINGLE, ROT_BADGE = -3, 6

# A book may not be more than this many times taller than it is wide. Every
# observed square-shape aspect across the catalogue is well under this, so
# it never fires in `square`; wide and pin are taller-than-wide boxes whose
# unclamped aspect would run past it, which is exactly what this catches.
MAX_BOOK_H_OVER_W = 1.55


def font(size, bold=True):
    for name in (BOLD if bold else REG):
        p = os.path.join(FONT_DIR, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _width(text, fnt):
    box = fnt.getbbox(text)
    return box[2] - box[0]


def fit_text(text, max_w, start, bold=True, floor=8):
    """Largest font at or below `start` whose `text` fits inside `max_w`."""
    size = start
    while size >= floor:
        fnt = font(size, bold)
        if _width(text, fnt) <= max_w:
            return fnt
        size -= 1
    raise ValueError('%r cannot fit in %dpx without dropping below floor %d'
                     % (text[:40], max_w, floor))


def gradient(size, stops):
    """Three-stop diagonal gradient, matching the 165deg CSS reference."""
    w, h = size
    small = Image.new('RGB', (64, 64))
    px = small.load()
    a, b, c = stops
    for y in range(64):
        for x in range(64):
            t = (0.26 * (x / 63.0) + 0.97 * (y / 63.0)) / 1.23
            t = 0.0 if t < 0 else (1.0 if t > 1 else t)
            if t < 0.5:
                u, lo, hi = t * 2, a, b
            else:
                u, lo, hi = (t - 0.5) * 2, b, c
            px[x, y] = tuple(int(lo[i] + (hi[i] - lo[i]) * u) for i in range(3))
    return small.resize((w, h), Image.BICUBIC)


def _spine(size, colour, label, text_w=None, align='left'):
    """One book spine, unrotated, with its dark left edge and white rule."""
    w, h = size
    img = Image.new('RGBA', (w, h), colour + (255,))
    d = ImageDraw.Draw(img)
    edge = max(3, int(w * 0.035))
    for x in range(edge):
        t = x / float(edge)
        d.line([(x, 0), (x, h)], fill=(0, 0, 0, int(115 * (1 - t))))
    pad = int(w * 0.10)
    if text_w is None:
        text_w = w - pad * 2
    fnt = fit_text(max(label.split('\n'), key=len), text_w,
                   max(9, int(w * 0.068)))
    y = int(h * 0.13)
    bar_w = int(w * 0.34)
    for line in label.split('\n'):
        x = pad if align == 'left' else w - pad - _width(line, fnt)
        d.text((x, y), line, font=fnt, fill=(255, 255, 255, 255))
        y += int(fnt.size * 1.25)
    bar_x = pad if align == 'left' else w - pad - bar_w
    d.rectangle([bar_x, y + int(h * 0.02), bar_x + bar_w,
                 y + int(h * 0.02) + max(2, int(h * 0.007))],
                fill=(255, 255, 255, 140))
    return img


def _paste_rotated(base, img, centre, angle, pal, shadow=True, clamp=False):
    rot = img.rotate(-angle, expand=True, resample=Image.BICUBIC)
    x = int(centre[0] - rot.width / 2)
    y = int(centre[1] - rot.height / 2)
    if clamp:
        m = int(base.width * 0.02)
        x = max(m, min(x, base.width - rot.width - m))
        y = max(m, min(y, base.height - rot.height - m))
    if shadow:
        sh = Image.new('RGBA', rot.size, (0, 0, 0, 0))
        sh.paste(pal.shadow + (120,), (0, 0), rot)
        sh = sh.filter(ImageFilter.GaussianBlur(int(base.width * 0.014)))
        base.alpha_composite(sh, (x - int(base.width * 0.006),
                                  y + int(base.width * 0.012)))
    base.alpha_composite(rot, (x, y))


def _badge(base, text, right_x, top_y, pal, scale):
    fnt = font(max(9, int(scale * 0.030)), True)
    tw = _width(text, fnt)
    th = fnt.getbbox(text)[3]
    padx, pady = int(scale * 0.020), int(scale * 0.014)
    w, h = tw + padx * 2, th + pady * 2
    chip = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(chip)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2,
                        fill=pal.badge_bg + (255,))
    d.text((padx, pady - fnt.getbbox(text)[1]), text, font=fnt,
           fill=pal.badge_fg + (255,))
    rot = chip.rotate(-ROT_BADGE, expand=True, resample=Image.BICUBIC)
    cx = right_x - rot.width / 2
    cy = top_y + rot.height / 2 + int(scale * 0.012)
    _paste_rotated(base, chip, (cx, cy), ROT_BADGE, pal, shadow=False, clamp=True)


def _centred(d, text, fnt, cx, y, fill):
    d.text((cx - _width(text, fnt) / 2, y), text, font=fnt, fill=fill)


def _stack(base, spec, box, pal):
    """Draw the spine stack inside box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if spec.kind == 'single':
        # Sizes and centre are exactly a72e720's approved square art. Height
        # is meant to track bh (a shorter title leaves more room and the
        # book grows into it) — only the ASPECT is clamped, and only so it
        # cannot run away in the non-square shapes (see MAX_BOOK_H_OVER_W).
        sw, sh = int(bw * 0.36), int(bh * 0.88)
        if sh > sw * MAX_BOOK_H_OVER_W:
            sh = int(sw * MAX_BOOK_H_OVER_W)
        img = _spine((sw, sh), pal.spine_front, spec.spines[0])
        _paste_rotated(base, img, (x0 + bw * 0.50, y0 + bh * 0.50),
                       ROT_SINGLE, pal)
        return
    back, front, right = spec.spines
    # Sizes and centres are exactly a72e720's approved square art. Height
    # is meant to track bh (a shorter title leaves more room and the books
    # grow into it) — only the ASPECT is clamped, and only so it cannot run
    # away in the non-square shapes (see MAX_BOOK_H_OVER_W). Every observed
    # square aspect across the catalogue is well under the clamp, so it
    # never fires there.
    sw, sh = int(bw * 0.40), int(bh * 0.82)
    rw, rh = int(bw * 0.42), int(bh * 0.86)
    if sh > sw * MAX_BOOK_H_OVER_W:
        sh = int(sw * MAX_BOOK_H_OVER_W)
    if rh > rw * MAX_BOOK_H_OVER_W:
        rh = int(rw * MAX_BOOK_H_OVER_W)
    _paste_rotated(base, _spine((sw, sh), pal.spine_back_left, back,
                                text_w=int(sw * 0.55)),
                   (x0 + bw * 0.27, y0 + bh * 0.51), ROT_BACK_LEFT, pal)
    _paste_rotated(base, _spine((rw, rh), pal.spine_back_right, right,
                                text_w=int(bw * 0.42 * 0.55), align='right'),
                   (x0 + bw * 0.73, y0 + bh * 0.51), ROT_BACK_RIGHT, pal)
    _paste_rotated(base, _spine((sw, sh), pal.spine_front, front),
                   (x0 + bw * 0.50, y0 + bh * 0.46), ROT_FRONT, pal)


def _render_portrait(spec, size):
    """Square and pin share a layout: title top, stack middle, footer bottom."""
    w, h = size
    pal = spec.palette
    base = gradient(size, pal.grad).convert('RGBA')
    d = ImageDraw.Draw(base)
    pad = int(w * 0.07)
    inner = w - pad * 2

    y = int(h * 0.085)
    tf = fit_text(max(spec.title_lines, key=len), inner, int(w * 0.105))
    for line in spec.title_lines:
        _centred(d, line, tf, w / 2, y, pal.title + (255,))
        y += int(tf.size * 1.04)

    y += int(h * 0.012)
    sf = fit_text(spec.subtitle, inner, int(w * 0.026))
    _centred(d, spec.subtitle, sf, w / 2, y, pal.muted + (255,))
    y += int(sf.size * 2.0)

    foot_f = font(int(w * 0.019), True)
    foot_y = h - pad - foot_f.size
    _stack(base, spec, (pad, y, w - pad, foot_y - int(h * 0.035)), pal)
    if spec.badge:
        _badge(base, spec.badge, w - pad, y, pal, w)

    spaced = '  '.join(spec.footer)
    ff = fit_text(spaced, inner, int(w * 0.019))
    _centred(d, spaced, ff, w / 2, foot_y, pal.muted + (255,))
    return base.convert('RGB')


def _render_wide(spec, size):
    """Gumroad's grid is landscape: title block left, stack right.

    Draws the badge (VOL n / EDITABLE RATES / FREE etc.) top-right when the
    spec carries one -- it is the product's differentiator on a storefront
    tile (12-start-here is free and that needs to be visible at a glance,
    every volume loses its "VOL n" without it). Deliberately does NOT draw
    the portrait layout's footer strip: "INSTANT PDF DOWNLOAD" is redundant
    on a 1280x720 tile that Gumroad's own listing chrome already marks as a
    digital download.
    """
    w, h = size
    pal = spec.palette
    base = gradient(size, pal.grad).convert('RGBA')
    d = ImageDraw.Draw(base)
    pad = int(w * 0.06)
    sx0 = w - pad - int(h * 0.80)
    col = sx0 - pad - int(w * 0.03)

    y = int(h * 0.26)
    tf = fit_text(max(spec.title_lines, key=len), col, int(h * 0.145))
    for line in spec.title_lines:
        d.text((pad, y), line, font=tf, fill=pal.title + (255,))
        y += int(tf.size * 1.04)
    y += int(h * 0.030)
    sf = fit_text(spec.subtitle, col, int(h * 0.040))
    d.text((pad, y), spec.subtitle, font=sf, fill=pal.muted + (255,))

    _stack(base, spec, (sx0, int(h * 0.10), w - pad, int(h * 0.90)), pal)
    if spec.badge:
        _badge(base, spec.badge, w - pad, int(h * 0.08), pal, h)
    return base.convert('RGB')


def render(spec, shape='square'):
    if shape not in SHAPES:
        raise KeyError('unknown shape %r — valid: %s'
                       % (shape, ', '.join(sorted(SHAPES))))
    size = SHAPES[shape]
    return _render_wide(spec, size) if shape == 'wide' else _render_portrait(spec, size)
