"""Pin-sized canvas and the drawing helpers every template shares."""
from PIL import ImageDraw

from covers import render

PIN_W, PIN_H = 1000, 1500
MARGIN = 72

_BG_CACHE = {}


def new_pin(pal):
    return render.gradient((PIN_W, PIN_H), pal.grad).convert('RGB')


def _bg_for(pal):
    """The rendered background for `pal`, cached per palette key.

    overflows(), content_extent() and footer_collision() each re-rendered a
    full 1000x1500 gradient on every single call just to diff it pixel-by-
    pixel against the image under test -- that repeated render was most of
    the test suite's runtime. new_pin() itself is untouched, so templates
    that draw on top of their canvas still always get a fresh image; only
    these read-only comparisons share one render per palette key. Returns a
    copy so a caller cannot mutate the cached master.
    """
    bg = _BG_CACHE.get(pal.key)
    if bg is None:
        bg = new_pin(pal)
        _BG_CACHE[pal.key] = bg
    return bg.copy()


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


def content_extent(img, pal):
    """How far down the canvas real content reaches, as a fraction of height.

    Measured against a freshly rendered background, ignoring the footer band,
    so a pin that stacks everything at the top scores low. A pin is 2:3 because
    the vertical space is the format's advantage; leaving the bottom half empty
    throws that away.
    """
    bg = _bg_for(pal).load()
    px = img.convert('RGB').load()
    lowest = 0
    for y in range(0, PIN_H - MARGIN - 40, 4):
        for x in range(MARGIN - 4, PIN_W - MARGIN + 4, 4):
            c, r = px[x, y], bg[x, y]
            if sum(abs(c[i] - r[i]) for i in range(3)) > 90:
                lowest = y
                break
    return lowest / float(PIN_H)


def overflows(img, pal):
    """True if ink sits inside the margin band.

    Compares each margin pixel against a freshly rendered background at the
    same position. Two earlier versions were wrong in opposite directions: one
    sampled the canvas centre (which is content, so any centred pin
    false-positived), the other sampled the mirrored opposite margin (which a
    centred heading defeats, because it overflows both sides by the same amount
    in the same colour and ink got compared to ink).

    band is MARGIN - 4, not MARGIN. The slack is on the RIGHT, not the left:
    measured across all nine product renders, the closest ink to either edge
    is x=74 on the left (already inside MARGIN=72, no slack needed there) but
    x=929 on the right, 1px past PIN_W - MARGIN = 928, which a band of exactly
    MARGIN false-positives on the product template. Do not tighten this back
    toward MARGIN on the strength of the left side -- it is the right side
    that is load-bearing.
    """
    bg = _bg_for(pal).load()
    px = img.convert('RGB').load()
    band = MARGIN - 4
    for y in range(0, PIN_H, 4):
        for x in list(range(band)) + list(range(PIN_W - band, PIN_W)):
            c, r = px[x, y], bg[x, y]
            if sum(abs(c[i] - r[i]) for i in range(3)) > 90:
                return True
    return False


def footer_collision(img, pal):
    """True if content reaches the footer band or runs off the bottom.

    overflows() watches the left and right margins; without this the guard has
    no vertical axis at all, and a pin can print its last line straight over the
    footer — or off the canvas — and still be reported clean. audit_pdfs.py has
    had the equivalent footer-bar check for the PDFs since a pin-shaped version
    of this bug shipped once already.

    Call this BEFORE footer() is drawn, or the footer itself trips it.
    """
    bg = _bg_for(pal).load()
    px = img.convert('RGB').load()
    for y in range(PIN_H - MARGIN - 40, PIN_H):
        for x in range(0, PIN_W, 2):
            c, r = px[x, y], bg[x, y]
            if sum(abs(c[i] - r[i]) for i in range(3)) > 90:
                return True
    return False
