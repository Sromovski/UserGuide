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


def fitted_heading(img, text, y, pal, max_size=96, floor=18):
    d = ImageDraw.Draw(img)
    inner = PIN_W - MARGIN * 2
    lines = text.split('\n')
    fnt = render.fit_text(max(lines, key=len), inner, max_size, bold=True, floor=floor)
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


def fits(text, max_w, start, floor=18, bold=True):
    """Whether text can be drawn at `start` or smaller without going below `floor`.

    Templates must skip a pin rather than draw clipped text, so they need to ASK
    before drawing. fit_text answers by raising, which is the wrong shape for a
    caller that wants to decide.
    """
    try:
        render.fit_text(text, max_w, start, bold=bold, floor=floor)
        return True
    except ValueError:
        return False


def overflows(img, pal):
    """True if ink sits inside the margin band.

    Compares each margin pixel against a freshly rendered background at the
    same position. Two earlier versions were wrong in opposite directions: one
    sampled the canvas centre (which is content, so any centred pin
    false-positived), the other sampled the mirrored opposite margin (which a
    centred heading defeats, because it overflows both sides by the same amount
    in the same colour and ink got compared to ink).

    band is MARGIN - 4, not MARGIN: covers' own portrait layout pads to 70px and
    glyph antialiasing bleeds a pixel or two left of the pen position, so a
    band of exactly MARGIN false-positives on the product template. 4px of
    slack is far less than any real overflow.
    """
    bg = new_pin(pal).convert('RGB').load()
    px = img.convert('RGB').load()
    band = MARGIN - 4
    for y in range(0, PIN_H, 4):
        for x in list(range(band)) + list(range(PIN_W - band, PIN_W)):
            c, r = px[x, y], bg[x, y]
            if sum(abs(c[i] - r[i]) for i in range(3)) > 90:
                return True
    return False
