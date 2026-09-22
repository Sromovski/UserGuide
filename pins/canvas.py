"""Pin-sized canvas and the drawing helpers every template shares."""
from PIL import Image, ImageDraw

from covers import render

PIN_W, PIN_H = 1000, 1500
MARGIN = 72


def new_pin(pal):
    return render.gradient((PIN_W, PIN_H), pal.grad).convert('RGB')


def wrap_lines(text, max_w, size, bold=True):
    """Greedy word wrap at a MEASURED width, never a character count."""
    fnt = render.font(size, bold)
    words, lines, cur = text.split(), [], ''
    for w in words:
        trial = ('%s %s' % (cur, w)).strip()
        if cur and render._width(trial, fnt) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def draw_block(img, x, y, lines, size, colour, bold=True, leading=1.30):
    d = ImageDraw.Draw(img)
    fnt = render.font(size, bold)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=colour)
        y += int(size * leading)
    return y


def fitted_heading(img, text, y, pal, max_size=96):
    d = ImageDraw.Draw(img)
    inner = PIN_W - MARGIN * 2
    lines = text.split('\n')
    fnt = render.fit_text(max(lines, key=len), inner, max_size)
    for ln in lines:
        d.text(((PIN_W - render._width(ln, fnt)) / 2, y), ln, font=fnt,
               fill=pal.title)
        y += int(fnt.size * 1.06)
    return y


def footer(img, pal, text='FRANKSMARKETDESIGNS.ETSY.COM'):
    d = ImageDraw.Draw(img)
    spaced = '  '.join(text)
    fnt = render.fit_text(spaced, PIN_W - MARGIN * 2, 22)
    d.text(((PIN_W - render._width(spaced, fnt)) / 2, PIN_H - MARGIN - fnt.size),
           spaced, font=fnt, fill=pal.muted)


def overflows(img):
    """True if ink sits inside the margin band.

    The background is a gradient, so 'ink' means a pixel that differs markedly
    from the background pixel at the same height on the opposite side of the
    canvas. Cheap, and it catches the failure that matters: text running off.
    """
    px = img.convert('RGB').load()
    band = MARGIN - 8
    for y in range(0, PIN_H, 4):
        ref = px[PIN_W // 2, y]
        for x in list(range(band)) + list(range(PIN_W - band, PIN_W)):
            c = px[x, y]
            if sum(abs(c[i] - ref[i]) for i in range(3)) > 90:
                return True
    return False
