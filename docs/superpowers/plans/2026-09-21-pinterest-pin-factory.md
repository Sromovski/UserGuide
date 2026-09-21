# Pinterest Pin Factory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate ~50 on-brand, factually accurate Pinterest pins across nine consumer-fit products, each with written copy and a live destination URL, so the owner can sustain daily posting for a month without repeating an image.

**Architecture:** A `pins/` package layered on the existing `covers/` render engine. Six templates render 1000×1500 images using `covers.palette`, so each pin inherits its series colour. Content comes from `build_etsy_kit.SKUS` (headline, bullets, badges) plus one small dict of hand-authored hook/tip/comparison strings. `build_pins.py` writes the images and a `PINS.csv` upload worklist. Two guards hard-fail the build: text overflow and dead destination links.

**Tech Stack:** Python 3.14, Pillow, pytest. Reuses `covers.render` (`font`, `fit_text`, `gradient`, `_width`) and `covers.palette`.

**Spec:** `docs/superpowers/specs/2026-09-21-pinterest-pin-factory-design.md`

## Global Constraints

- The nine SKUs, exactly: `40-chatgpt-v1`, `02-starter-volume`, `01-prompt-vault`, `10-cheat-sheet-pack`, `11-cost-calculator`, `12-start-here`, `03-complete-library`, `20-copilot-v1`, `30-codex-v1`.
- All pins are **1000×1500** (Pinterest 2:3).
- **No invented content.** Every claim must come from the SKU's `build_etsy_kit.SKUS` entry or from the book. Hand-authored strings live in one dict per template in `pins/copy.py` and must be traceable to the book.
- **`build_etsy_kit.SKUS` stays the single source of listing copy.** Read it; never duplicate it.
- A template that cannot render a SKU **skips it and reports the skip** — never invents filler.
- Pinterest title limit: **100 characters**. Descriptions target ~200.
- URL rule: prefer Etsy (`etsypub.db.get(sku)['url']`), fall back to Gumroad (`gumroadpub.publish.get(sku)['url']`). A SKU resolving to neither is a **build failure**.
- Boards, exactly five: `AI for Beginners`, `ChatGPT Tips`, `AI Prompts & Templates`, `Printable Cheat Sheets`, `AI Tools & Productivity`.
- Python 3.14; `%`-style formatting, single-quoted strings.
- `outputs/` is git-ignored — commit no images or CSV.
- Per-SKU loop tests **collect every offender and assert once outside the loop**. Never assert inside the loop.
- Layout must be asserted on rendered pixels where it matters, not only on image dimensions. This project has shipped four layout defects that passed a fully green suite.

---

### Task 1: Pin canvas and shared drawing helpers

**Files:**
- Create: `pins/__init__.py`
- Create: `pins/canvas.py`
- Test: `tests/test_pin_canvas.py`

**Interfaces:**
- Consumes: `covers.render.font`, `covers.render.fit_text`, `covers.render.gradient`, `covers.render._width`; `covers.palette.Palette`
- Produces:
  - `pins.canvas.PIN_W`, `pins.canvas.PIN_H` — `1000`, `1500`
  - `pins.canvas.MARGIN` — `72`
  - `pins.canvas.new_pin(pal) -> PIL.Image` — gradient background at pin size, RGB
  - `pins.canvas.wrap_lines(text, max_w, size, bold=True) -> list[str]` — greedy word wrap at a measured width
  - `pins.canvas.draw_block(img, x, y, lines, size, colour, bold=True, leading=1.30) -> int` — draws lines, returns the new y
  - `pins.canvas.fitted_heading(img, text, y, pal, max_size=96) -> int` — centred, shrink-to-fit heading, returns new y
  - `pins.canvas.footer(img, pal, text='FRANKSMARKETDESIGNS.ETSY.COM') -> None`
  - `pins.canvas.overflows(img) -> bool` — True if any non-background pixel falls inside the margin band

- [ ] **Step 1: Write the failing test**

```python
# tests/test_pin_canvas.py
from covers import palette
from pins import canvas


def test_pin_dimensions_are_pinterest_two_to_three():
    assert (canvas.PIN_W, canvas.PIN_H) == (1000, 1500)
    assert round(canvas.PIN_W / canvas.PIN_H, 3) == 0.667


def test_new_pin_uses_the_palette_gradient():
    img = canvas.new_pin(palette.get('gpt'))
    assert img.size == (1000, 1500)
    r, g, b = img.convert('RGB').getpixel((5, 5))
    assert abs(r - 250) < 12 and abs(g - 247) < 12 and abs(b - 255) < 12


def test_wrap_lines_breaks_on_words_not_characters():
    lines = canvas.wrap_lines('the quick brown fox jumps over the lazy dog', 300, 40)
    assert len(lines) > 1
    for ln in lines:
        assert not ln.startswith(' ') and not ln.endswith(' ')
    assert ' '.join(lines) == 'the quick brown fox jumps over the lazy dog'


def test_draw_block_returns_a_y_below_where_it_started():
    img = canvas.new_pin(palette.get('claude'))
    y = canvas.draw_block(img, 72, 200, ['one', 'two'], 40, (0, 0, 0))
    assert y > 200


def test_overflows_is_false_for_an_empty_pin():
    assert canvas.overflows(canvas.new_pin(palette.get('claude'))) is False


def test_overflows_is_true_when_ink_sits_in_the_margin():
    from PIL import ImageDraw
    img = canvas.new_pin(palette.get('claude'))
    ImageDraw.Draw(img).rectangle([0, 700, 40, 760], fill=(0, 0, 0))
    assert canvas.overflows(img) is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pin_canvas.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pins'`

- [ ] **Step 3: Write the implementation**

```python
# pins/__init__.py
"""Pinterest pin generation.

Pinterest rewards FRESH PINS, not new products — one image per product is about
a week of posting. These templates turn pin production from a writing problem
into a template problem, drawing their content from build_etsy_kit.SKUS so a
pin cannot claim something the product does not.
"""
```

```python
# pins/canvas.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_pin_canvas.py -v`
Expected: PASS — 6 passed

- [ ] **Step 5: Commit**

```bash
git add pins/__init__.py pins/canvas.py tests/test_pin_canvas.py
git commit -m "feat(pins): pin canvas and shared drawing helpers"
```

---

### Task 2: Pin copy — hand-authored strings, titles, descriptions, URLs, boards

**Files:**
- Create: `pins/copy.py`
- Test: `tests/test_pin_copy.py`

**Interfaces:**
- Consumes: `build_etsy_kit.SKUS`, `etsypub.db.get`, `gumroadpub.publish.get`
- Produces:
  - `pins.copy.SKUS` — the nine SKU names, in posting-priority order
  - `pins.copy.BOARDS` — the five board names
  - `pins.copy.BOARD_FOR: dict[str, str]` — sku → board
  - `pins.copy.HOOKS: dict[str, str]` — sku → one-sentence hook
  - `pins.copy.TIPS: dict[str, str]` — sku → one concrete tip
  - `pins.copy.COMPARISONS: dict[str, list[tuple[str, str]]]` — sku → rows; absent means the comparison template skips that SKU
  - `pins.copy.TITLES: dict[str, str]`, `pins.copy.DESCRIPTIONS: dict[str, str]`
  - `pins.copy.url_for(sku) -> str` — Etsy, else Gumroad; raises `KeyError` if neither
  - `pins.copy.sku_record(sku) -> dict` — the `build_etsy_kit.SKUS` entry

**Content rule:** every string in `HOOKS`, `TIPS` and `COMPARISONS` must be traceable to the book. Carry a `# page N` style comment where the source is specific, and a dated comment on anything that expires.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_pin_copy.py
import pytest

from pins import copy as pc


def test_nine_skus_in_priority_order():
    assert len(pc.SKUS) == 9
    assert pc.SKUS[0] == '12-start-here'      # free lead magnet leads


def test_five_boards_and_every_sku_maps_to_one():
    assert len(pc.BOARDS) == 5
    unmapped = [s for s in pc.SKUS if pc.BOARD_FOR.get(s) not in pc.BOARDS]
    assert unmapped == []


def test_every_sku_has_a_title_within_pinterest_limit():
    bad = ['%s: %d chars' % (s, len(pc.TITLES[s]))
           for s in pc.SKUS if len(pc.TITLES.get(s, '')) > 100]
    assert bad == []


def test_every_sku_has_a_description():
    missing = [s for s in pc.SKUS if not pc.DESCRIPTIONS.get(s)]
    assert missing == []


def test_every_sku_has_a_hook_and_a_tip():
    missing = [s for s in pc.SKUS if not pc.HOOKS.get(s) or not pc.TIPS.get(s)]
    assert missing == []


def test_url_prefers_etsy_and_falls_back_to_gumroad(monkeypatch):
    monkeypatch.setattr(pc, '_etsy_url', lambda s: 'https://etsy/x')
    monkeypatch.setattr(pc, '_gumroad_url', lambda s: 'https://gumroad/x')
    assert pc.url_for('02-starter-volume') == 'https://etsy/x'
    monkeypatch.setattr(pc, '_etsy_url', lambda s: '')
    assert pc.url_for('02-starter-volume') == 'https://gumroad/x'


def test_url_raises_when_a_sku_resolves_nowhere(monkeypatch):
    monkeypatch.setattr(pc, '_etsy_url', lambda s: '')
    monkeypatch.setattr(pc, '_gumroad_url', lambda s: '')
    with pytest.raises(KeyError, match='02-starter-volume'):
        pc.url_for('02-starter-volume')


def test_every_live_sku_resolves_to_a_real_url():
    dead = []
    for s in pc.SKUS:
        try:
            u = pc.url_for(s)
        except KeyError:
            dead.append(s)
            continue
        if not u.startswith('http'):
            dead.append('%s -> %r' % (s, u))
    assert dead == []


def test_comparison_rows_are_pairs_when_present():
    bad = [s for s, rows in pc.COMPARISONS.items()
           if any(len(r) != 2 for r in rows)]
    assert bad == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pin_copy.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pins.copy'`

- [ ] **Step 3: Write the implementation**

Use the titles and descriptions already written and validated in
`outputs/pins/PINS_wave1.csv` — they were checked against the 100-character limit and
reviewed. Read that CSV and carry the strings across verbatim rather than rewriting them.

```python
# pins/copy.py
"""The words on a pin, and where it points.

Titles lead with the SEARCH PHRASE, not the product name — Pinterest is a
search engine and nobody searches a brand they have not heard of. Descriptions
are keyword-led prose, not hashtag strings, which Pinterest has downranked for
years.

HOOKS, TIPS and COMPARISONS are the only hand-authored strings in this package.
Each must be traceable to something the book actually says.
"""
import build_etsy_kit as _kit
from etsypub import db as _edb
import gumroadpub.publish as _gp

SKUS = [
    '12-start-here',          # free: leads, because free pins get saved
    '40-chatgpt-v1',
    '01-prompt-vault',
    '10-cheat-sheet-pack',
    '02-starter-volume',
    '11-cost-calculator',
    '03-complete-library',
    '20-copilot-v1',
    '30-codex-v1',
]

BOARDS = ['AI for Beginners', 'ChatGPT Tips', 'AI Prompts & Templates',
          'Printable Cheat Sheets', 'AI Tools & Productivity']

BOARD_FOR = {
    '12-start-here': 'AI for Beginners',
    '40-chatgpt-v1': 'ChatGPT Tips',
    '01-prompt-vault': 'AI Prompts & Templates',
    '10-cheat-sheet-pack': 'Printable Cheat Sheets',
    '02-starter-volume': 'AI for Beginners',
    '11-cost-calculator': 'AI Tools & Productivity',
    '03-complete-library': 'AI for Beginners',
    '20-copilot-v1': 'AI Tools & Productivity',
    '30-codex-v1': 'AI Tools & Productivity',
}
```

Then add `TITLES` and `DESCRIPTIONS` copied from `outputs/pins/PINS_wave1.csv`, plus:

```python
# One sentence, high contrast, designed to stop a scroll. Traceable to the book.
HOOKS = {
    # EXPIRES 2026-12-11, when Custom GPTs stop running. Rewrite after that.
    '40-chatgpt-v1': 'Custom GPTs stop working\non 11 Dec 2026.',
    '12-start-here': 'Four AI tools.\nWhich one first?',
    '01-prompt-vault': 'Stop rewriting\nthe same prompt.',
    '10-cheat-sheet-pack': 'Print it once.\nStop googling it.',
    '02-starter-volume': 'You do not need\nto code to use AI.',
    '11-cost-calculator': 'What does AI\nactually cost you?',
    '03-complete-library': '23 guides.\nOne download.',
    '20-copilot-v1': 'Copilot is three\nproducts, not one.',
    '30-codex-v1': 'Codex resets every\n5 hours, not daily.',
}

# One concrete, immediately useful thing from the book.
TIPS = {
    '40-chatgpt-v1': 'Custom instructions are for who you are. Memory is for what '
                     'you are working on. Mixing them up is why ChatGPT forgets.',
    '12-start-here': 'Pick the tool that matches the job you actually have, not the '
                     'one with the loudest launch.',
    '01-prompt-vault': 'Everything you need to change is in [BRACKETS]. Swap those, '
                       'leave the rest alone.',
    '10-cheat-sheet-pack': 'Printed on a light background on purpose — a dark PDF '
                           'costs a fortune in ink.',
    '02-starter-volume': 'Free, Pro and Max differ by usage limits more than by '
                         'features. Check limits before you upgrade.',
    '11-cost-calculator': 'Cached input costs about a tenth of fresh input. Reusing '
                          'a prompt is cheaper than rewriting it.',
    '03-complete-library': 'Start at volume one even if you are technical — the '
                           'plan and pricing chapters apply to everyone.',
    '20-copilot-v1': 'Code completions are unmetered on every paid plan. Chat and '
                     'agent mode are not.',
    '30-codex-v1': 'The usage window is 5 hours rolling, so a heavy morning frees '
                   'up by mid-afternoon.',
}

# Two-column rows. A SKU absent here is SKIPPED by the comparison template —
# never padded with `included`, which is a file manifest, not a comparison.
COMPARISONS = {
    '40-chatgpt-v1': [('Free', '$0'), ('Go', '$8'), ('Plus', '$20'),
                      ('Pro', '$100 / $200')],
    '02-starter-volume': [('Free', 'Limited usage'), ('Pro', 'More usage'),
                          ('Max', 'Highest usage')],
    '20-copilot-v1': [('Completions', 'Unmetered'), ('Chat', 'Uses credits'),
                      ('Agent mode', 'Uses credits')],
}


def sku_record(sku):
    return next(s for s in _kit.SKUS if s['sku'] == sku)


def _etsy_url(sku):
    r = _edb.get(sku)
    return (r or {}).get('url') or ''


def _gumroad_url(sku):
    r = _gp.get(sku)
    return (r or {}).get('url') or ''


def url_for(sku):
    """Etsy first, Gumroad second. A pin pointing nowhere is worse than no pin."""
    u = _etsy_url(sku) or _gumroad_url(sku)
    if not u:
        raise KeyError('%s resolves to no live listing on either channel' % sku)
    return u


def palette_key_for(sku):
    """The series palette for this SKU, via the covers catalogue."""
    from covers import catalogue
    return catalogue.palette_for(sku_record(sku))
```

Add one more test to `tests/test_pin_copy.py` covering it:

```python
def test_palette_key_follows_the_series():
    assert pc.palette_key_for('40-chatgpt-v1') == 'gpt'
    assert pc.palette_key_for('20-copilot-v1') == 'copilot'
    assert pc.palette_key_for('02-starter-volume') == 'claude'
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_pin_copy.py -v`
Expected: PASS — 9 passed

- [ ] **Step 5: Commit**

```bash
git add pins/copy.py tests/test_pin_copy.py
git commit -m "feat(pins): pin copy, boards, hooks, tips and URL resolution"
```

---

### Task 3: The six templates

**Files:**
- Create: `pins/templates.py`
- Test: `tests/test_pin_templates.py`

**Interfaces:**
- Consumes: `pins.canvas` (all helpers), `pins.copy` (`sku_record`, `HOOKS`, `TIPS`, `COMPARISONS`), `covers.catalogue.all_specs`, `covers.render.render`, `covers.palette.get`
- Produces:
  - `pins.templates.TEMPLATES: dict[str, callable]` — keys exactly `product`, `listicle`, `hook`, `checklist`, `comparison`, `tip`
  - each callable has signature `fn(sku: str, pal: Palette) -> PIL.Image | None` — returns `None` to signal an honest skip

**Design notes each template must honour:**
- `product` — delegates to `covers.render.render(spec, 'pin')` for the SKU's `CoverSpec`. Never `None`.
- `listicle` — heading "WHAT'S INSIDE", then the SKU's `bullets`, numbered, each wrapped and truncated to 2 lines.
- `hook` — `HOOKS[sku]` at large size, centred vertically, plus the SKU headline small beneath. `None` if no hook.
- `checklist` — the SKU's `bullets` with a tick glyph, first 5.
- `comparison` — `COMPARISONS[sku]` as a two-column table. **`None` when absent.**
- `tip` — `TIPS[sku]` wrapped, with a small "TIP" label. `None` if no tip.

Every template calls `canvas.footer(...)` last.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_pin_templates.py
from covers import palette
from pins import copy as pc
from pins import canvas, templates


def test_six_templates_named_exactly():
    assert set(templates.TEMPLATES) == {'product', 'listicle', 'hook',
                                        'checklist', 'comparison', 'tip'}


def test_every_template_renders_or_skips_for_every_sku():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is None:
                continue
            if img.size != (canvas.PIN_W, canvas.PIN_H):
                offenders.append('%s/%s -> %s' % (name, sku, img.size))
    assert offenders == []


def test_product_template_never_skips():
    skipped = [s for s in pc.SKUS
               if templates.TEMPLATES['product'](s, palette.get(pc.palette_key_for(s))) is None]
    assert skipped == []


def test_comparison_skips_a_sku_with_no_curated_rows():
    sku = next(s for s in pc.SKUS if s not in pc.COMPARISONS)
    assert templates.TEMPLATES['comparison'](sku, palette.get(pc.palette_key_for(sku))) is None


def test_no_template_paints_into_the_margin():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is not None and canvas.overflows(img):
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []


def test_no_pin_is_a_flat_fill():
    offenders = []
    for name, fn in templates.TEMPLATES.items():
        for sku in pc.SKUS:
            img = fn(sku, palette.get(pc.palette_key_for(sku)))
            if img is not None and len(set(img.convert('RGB').getdata())) < 400:
                offenders.append('%s/%s' % (name, sku))
    assert offenders == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pin_templates.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pins.templates'`

- [ ] **Step 3: Write the implementation**

Two templates in full below — `hook` (the simplest) and `listicle` (the one with wrapping
and truncation). Write the remaining four to the same shape, using ONLY `pins.canvas`
helpers so margins stay consistent.

```python
# pins/templates.py
"""Six pin layouts.

Every template returns None rather than drawing something clipped or invented.
A skip is honest; a clipped pin is not, and a padded one is worse.
"""
from covers import catalogue, render

from pins import canvas
from pins import copy as pc


def _product(sku, pal):
    return render.render(catalogue.spec_for(pc.sku_record(sku)), 'pin')


def _hook(sku, pal):
    text = pc.HOOKS.get(sku)
    if not text:
        return None
    img = canvas.new_pin(pal)
    y = canvas.fitted_heading(img, text, 430, pal, max_size=104)
    rec = pc.sku_record(sku)
    sub = rec['headline'].replace('\n', ' ')
    lines = canvas.wrap_lines(sub, canvas.PIN_W - canvas.MARGIN * 2, 34)
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
        lines = canvas.wrap_lines(b, inner, 28)[:2]
        if len(canvas.wrap_lines(b, inner, 28)) > 2:
            lines[-1] = lines[-1].rstrip(' ,.') + '...'
        canvas.draw_block(img, canvas.MARGIN, y, ['%d' % i], 30, pal.spine_front)
        y = canvas.draw_block(img, canvas.MARGIN + 54, y, lines, 28, pal.title)
        y += 22
        if y > canvas.PIN_H - canvas.MARGIN - 90:
            break
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
```

The remaining four, to the same pattern:

- **`_checklist`** — heading `'YOUR\nCHECKLIST'`, then `rec['bullets'][:5]`, each preceded
  by a tick drawn as a small filled rounded rect in `pal.spine_front` (not a unicode glyph —
  font coverage varies). Wrap to 2 lines, truncate as `_listicle` does.
- **`_comparison`** — `rows = pc.COMPARISONS.get(sku)`; `return None` if absent. Heading from
  `rec['headline']`. Draw each row as left label at `MARGIN` and right value right-aligned
  at `PIN_W - MARGIN`, with a 1px rule in `pal.muted` between rows.
- **`_tip`** — small `'TIP'` label in `pal.spine_front`, then `pc.TIPS[sku]` wrapped at size
  36 filling the middle third. `return None` if no tip.
- **`_product`** is already complete above and never returns `None`.

Rules every one of them must follow:
- Any string longer than a word goes through `canvas.wrap_lines` before
  `canvas.draw_block`. Never draw an unwrapped string.
- If `canvas.fitted_heading` or `render.fit_text` would need to go below size 18 to fit,
  return `None` instead.
- `canvas.footer(img, pal)` is the last call before `return img`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_pin_templates.py tests/test_pin_copy.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pins/templates.py pins/copy.py tests/test_pin_templates.py tests/test_pin_copy.py
git commit -m "feat(pins): six pin templates with honest skips"
```

---

### Task 4: The build script and its guards

**Files:**
- Create: `build_pins.py`
- Test: `tests/test_build_pins.py`

**Interfaces:**
- Consumes: `pins.templates.TEMPLATES`, `pins.copy` (`SKUS`, `TITLES`, `DESCRIPTIONS`, `BOARD_FOR`, `url_for`, `palette_key_for`), `pins.canvas.overflows`
- Produces:
  - `build_pins.OUT` — `outputs/pins`
  - `build_pins.build(skus=None, templates=None) -> list[dict]` — renders, writes PNGs, returns row dicts with keys `sku`, `template`, `file`, `title`, `description`, `url`, `board`
  - `build_pins.verify_no_overflow(rows) -> None` — raises `SystemExit` naming every offender
  - `build_pins.verify_destinations(rows) -> None` — raises `SystemExit` on a missing title/description/url, a title over 100 chars, or a url not starting `http`
  - `build_pins.write_csv(rows) -> str` — writes `outputs/pins/PINS.csv`, returns the path
  - `build_pins.main()`

**Title/description per pin:** the SKU's `TITLES[sku]` and `DESCRIPTIONS[sku]`, with the
template appended to the CSV's `template` column so the owner can tell variants apart. Do
NOT generate per-template titles — one strong title per product reused across its pins is
correct for Pinterest, and inventing six variants per product is where fabricated claims
would creep in.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_build_pins.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_build_pins.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'build_pins'`

- [ ] **Step 3: Write the implementation**

`build_pins.py` renders every template for every SKU, skipping where a template returns
`None`, writes each PNG to `outputs/pins/<sku>/<template>.png`, runs both guards, writes the
CSV, and prints a per-SKU tally plus the list of skips. `main()` exits non-zero if a guard
raises.

Both guards must **collect every offender and raise once**, naming them all. A guard that
stops at the first problem makes the next run find the next one — this project lost three
rounds to exactly that pattern in the cover work.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/ -q`
Expected: PASS — the full suite

- [ ] **Step 5: Build for real and inspect**

```bash
cd /c/Projects/UserGuide
python build_pins.py
```

Report: total pins, pins per template, every skip and its reason, and the CSV path. Then
save a contact sheet of one pin per template for a human to eyeball — a suite that only
checks dimensions cannot see a pin that is ugly or unreadable.

- [ ] **Step 5: Commit**

```bash
git add build_pins.py tests/test_build_pins.py
git commit -m "feat(pins): build script, overflow and destination guards"
```

---

## Done when

- `python -m pytest tests/ -q` passes.
- `python build_pins.py` produces ≥45 pins across the nine SKUs with both guards clean.
- `outputs/pins/PINS.csv` has one row per pin with title, description, url and board.
- Every skip is reported with a reason; no pin contains invented content.
- A human has eyeballed one pin per template.
