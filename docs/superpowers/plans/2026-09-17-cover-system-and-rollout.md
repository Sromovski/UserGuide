# Cover System & Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single `covers/` package that renders the approved "direction C" cover from existing SKU metadata, then splice that cover onto page 1 of all 21 live product PDFs and regenerate the listing images — without touching any PDF interior.

**Architecture:** One Pillow renderer is the only thing that knows what a cover looks like. It reads a `CoverSpec` derived from `build_etsy_kit.SKUS` (no second catalogue) and emits three shapes: square 2000×2000 for Etsy, wide 1280×720 for Gumroad, pin 1000×1500 for Pinterest. The PDF cover page is the square render placed full-bleed at 200 DPI, so the listing image and the PDF cover cannot drift apart. Rollout is a splice: back up, delete page 0, insert the new page 0, verify page count and audit cleanliness. Interiors are never regenerated.

**Tech Stack:** Python 3.14, Pillow (rendering), PyMuPDF/`fitz` 1.28 (splice), reportlab 5.0 (one-page cover PDF), pytest 9.0.3 (tests).

**Spec:** `docs/superpowers/specs/2026-09-17-cover-system-and-distribution-design.md`

## Global Constraints

- Output root is `C:\Projects\UserGuide\outputs\` — Windows local paths, never `/mnt/`.
- `build_etsy_kit.SKUS` remains the single source of listing copy. Do not create a second catalogue.
- The 23 shipped Claude build scripts are **not** retrofitted onto `fieldguide/`. Standing decision in `CLAUDE.md`.
- PDF interiors are out of scope. Only page 0 is replaced.
- All five palettes are **light**. The dark `#0F0F1A` house style applies to interiors only.
- No vendor logos, wordmarks or icons. Palette only.
- Cover PDF page: square render, full-bleed on US Letter (612×792 pt), 200 DPI, JPEG q92.
- `audit_pdfs.py` runs over the whole catalogue as a release check (Task 7 Step 9) and its output is reviewed before the work is called done. It is deliberately **not** a per-file gate inside `rebuild_covers.py` — it encodes the volume geometry, and four SKUs are not volumes. The per-file gate is page-0-scoped.
- Fonts come from `C:\Windows\Fonts` with the fallback chain already used by `build_etsy_kit.font()`: bold `seguibl.ttf` → `arialbd.ttf` → `segoeuib.ttf`; regular `segoeui.ttf` → `arial.ttf`.
- Spine order is always back-left, back-right, front-centre (front drawn last).
- Rotations are fixed: back-left `-8°`, front-centre `-2°`, back-right `+6°`, badge `+6°`. Single-kind covers use one spine at `-3°`.

---

### Task 0: Initialize version control

**Files:**
- Create: `.gitignore`

**Interfaces:**
- Consumes: nothing
- Produces: a git repository, so every later task's commit step works

> **Requires the owner's go-ahead.** `C:\Projects\UserGuide` is not currently a git repository. If the owner declines, treat every "Commit" step in this plan as a checkpoint — stop, confirm tests pass, and move on without committing.

- [ ] **Step 1: Create the ignore file**

```gitignore
# LIVE CREDENTIALS — Etsy keystring, shared secret, refresh token, Gumroad
# access token. The GitHub repo is public. This line is load-bearing.
.env

__pycache__/
*.pyc
outputs/
logs/
etsy.db
.superpowers/
~$*
```

`.env.example` stays tracked — it is the template and holds no values.

- [ ] **Step 2: Initialize and connect to the existing GitHub repo**

The remote `Sromovski/UserGuide` already exists and is **public**.

```bash
cd /c/Projects/UserGuide
git init -b main
git remote add origin https://github.com/Sromovski/UserGuide.git
```

- [ ] **Step 3: Prove `.env` is ignored BEFORE staging anything**

```bash
cd /c/Projects/UserGuide
git check-ignore -v .env
git status --short | grep -E "^\?\? \.env$" && echo "DANGER: .env is not ignored" || echo "safe"
```

Expected: `check-ignore` prints the `.gitignore` line that matches, and the second command
prints `safe`. **If it prints DANGER, stop.** Do not stage, do not commit, do not push.

- [ ] **Step 4: Stage, review the file list, then commit**

```bash
cd /c/Projects/UserGuide
git add -A
git status --short | sort
```

Read that list before committing. It must not contain `.env`, `etsy.db`, anything under
`outputs/`, `logs/` or `.superpowers/`.

```bash
git commit -m "chore: initialize repository"
```

- [ ] **Step 5: Verify the tree is clean, then push**

```bash
cd /c/Projects/UserGuide
git ls-files | grep -E "^\.env$|^etsy\.db$|^outputs/|^logs/" && echo "DANGER: secret or artifact tracked" || echo "clean"
```

Expected: `clean`. Only then:

```bash
git push -u origin main
```

---

### Task 1: Palette registry

**Files:**
- Create: `covers/__init__.py`
- Create: `covers/palette.py`
- Create: `tests/__init__.py`
- Test: `tests/test_palette.py`

**Interfaces:**
- Consumes: nothing
- Produces:
  - `covers.palette.Palette` — frozen dataclass with fields `key: str`, `grad: tuple[RGB, RGB, RGB]`, `title: RGB`, `muted: RGB`, `spine_back_left: RGB`, `spine_front: RGB`, `spine_back_right: RGB`, `badge_bg: RGB`, `badge_fg: RGB`, `shadow: RGB` where `RGB = tuple[int, int, int]`
  - `covers.palette.PALETTES: dict[str, Palette]` — keys exactly `claude`, `copilot`, `codex`, `gpt`, `grok`
  - `covers.palette.get(key: str) -> Palette` — raises `KeyError` with the list of valid keys on miss

- [ ] **Step 1: Write the failing test**

```python
# tests/test_palette.py
import pytest

from covers import palette


def test_all_five_series_have_a_palette():
    assert set(palette.PALETTES) == {'claude', 'copilot', 'codex', 'gpt', 'grok'}


def test_every_palette_is_light():
    # Cover art is deliberately light so it holds an edge against Etsy's white
    # search grid. Guard the decision: the top gradient stop must be bright.
    for key, p in palette.PALETTES.items():
        assert min(p.grad[0]) > 200, '%s top stop is too dark' % key


def test_title_ink_is_dark_enough_to_read():
    for key, p in palette.PALETTES.items():
        assert max(p.title) < 90, '%s title ink is too light' % key


def test_get_rejects_unknown_key_and_names_the_valid_ones():
    with pytest.raises(KeyError) as e:
        palette.get('gemini')
    assert 'claude' in str(e.value)


def test_get_returns_the_named_palette():
    assert palette.get('gpt').key == 'gpt'
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_palette.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'covers'`

- [ ] **Step 3: Write minimal implementation**

```python
# covers/__init__.py
"""Cover art for every Field Guide product.

The only place in the project that knows what a cover looks like. One Pillow
renderer draws both the PDF cover page and the listing images, so they cannot
drift apart.
"""
```

```python
# tests/__init__.py
```

```python
# covers/palette.py
"""The five series palettes.

All five are deliberately LIGHT. This reverses the dark house style for cover
art only: a light cover holds its edges against Etsy's white search grid and
Gumroad's white cards at thumbnail size, a dark one sinks into them. Interiors
stay dark.

No vendor logos, wordmarks or icons anywhere — palette only.
"""
from dataclasses import dataclass

RGB = tuple


@dataclass(frozen=True)
class Palette:
    key: str
    grad: tuple              # three stops, top -> bottom
    title: RGB
    muted: RGB
    spine_back_left: RGB
    spine_front: RGB         # the accent colour
    spine_back_right: RGB
    badge_bg: RGB
    badge_fg: RGB
    shadow: RGB


PALETTES = {
    'claude': Palette(
        key='claude',
        grad=((255, 244, 236), (251, 226, 211), (243, 203, 182)),
        title=(32, 26, 22), muted=(138, 106, 87),
        spine_back_left=(35, 32, 46), spine_front=(226, 84, 43),
        spine_back_right=(20, 18, 28),
        badge_bg=(20, 18, 28), badge_fg=(255, 255, 255),
        shadow=(80, 40, 20)),
    'copilot': Palette(
        key='copilot',
        grad=((242, 244, 255), (226, 230, 251), (205, 211, 245)),
        title=(23, 26, 46), muted=(94, 100, 134),
        spine_back_left=(43, 48, 80), spine_front=(79, 70, 229),
        spine_back_right=(18, 20, 42),
        badge_bg=(23, 26, 46), badge_fg=(255, 255, 255),
        shadow=(30, 35, 90)),
    'codex': Palette(
        key='codex',
        grad=((238, 247, 244), (220, 238, 232), (195, 226, 216)),
        title=(14, 31, 26), muted=(78, 114, 104),
        spine_back_left=(29, 58, 51), spine_front=(15, 157, 116),
        spine_back_right=(11, 26, 22),
        badge_bg=(14, 31, 26), badge_fg=(255, 255, 255),
        shadow=(15, 60, 48)),
    'gpt': Palette(
        key='gpt',
        grad=((240, 250, 246), (221, 243, 234), (194, 233, 216)),
        title=(12, 31, 24), muted=(74, 117, 102),
        spine_back_left=(24, 73, 58), spine_front=(16, 163, 127),
        spine_back_right=(10, 23, 18),
        badge_bg=(12, 31, 24), badge_fg=(255, 255, 255),
        shadow=(12, 70, 52)),
    'grok': Palette(
        key='grok',
        grad=((244, 245, 247), (228, 231, 236), (203, 210, 218)),
        title=(11, 13, 16), muted=(91, 100, 111),
        spine_back_left=(35, 42, 51), spine_front=(11, 13, 16),
        spine_back_right=(0, 184, 217),
        badge_bg=(11, 13, 16), badge_fg=(255, 255, 255),
        shadow=(20, 28, 40)),
}


def get(key):
    """Return the named palette, or raise KeyError listing the valid keys."""
    try:
        return PALETTES[key]
    except KeyError:
        raise KeyError('unknown palette %r — valid keys: %s'
                       % (key, ', '.join(sorted(PALETTES)))) from None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_palette.py -v`
Expected: PASS — 5 passed

- [ ] **Step 5: Commit**

```bash
git add covers/__init__.py covers/palette.py tests/__init__.py tests/test_palette.py
git commit -m "feat(covers): add the five series palettes"
```

---

### Task 2: CoverSpec

**Files:**
- Create: `covers/spec.py`
- Test: `tests/test_spec.py`

**Interfaces:**
- Consumes: `covers.palette.get`
- Produces:
  - `covers.spec.CoverSpec` — frozen dataclass with fields `title_lines: tuple[str, ...]` (1–2 entries), `subtitle: str`, `spines: tuple[str, ...]` (1–3 entries, each may contain one `\n`), `badge: str`, `footer: str`, `palette_key: str`, `kind: str` (`'bundle'` or `'single'`)
  - `CoverSpec.palette` — property returning the resolved `Palette`
  - `CoverSpec.validate()` — raises `ValueError` on any violation; called from `__post_init__`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_spec.py
import pytest

from covers.spec import CoverSpec


def ok(**over):
    base = dict(title_lines=('Claude AI', 'for Beginners'),
                subtitle='5 GUIDES · 32 PAGES · STEP BY STEP',
                spines=('Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'),
                badge='VOL 1', footer='INSTANT PDF DOWNLOAD',
                palette_key='claude', kind='bundle')
    base.update(over)
    return CoverSpec(**base)


def test_resolves_its_palette():
    assert ok().palette.spine_front == (226, 84, 43)


def test_rejects_more_than_two_title_lines():
    with pytest.raises(ValueError, match='title_lines'):
        ok(title_lines=('a', 'b', 'c'))


def test_rejects_empty_title():
    with pytest.raises(ValueError, match='title_lines'):
        ok(title_lines=())


def test_rejects_more_than_three_spines():
    with pytest.raises(ValueError, match='spines'):
        ok(spines=('a', 'b', 'c', 'd'))


def test_single_kind_must_have_exactly_one_spine():
    with pytest.raises(ValueError, match='single'):
        ok(kind='single', spines=('a', 'b', 'c'))


def test_bundle_kind_must_have_three_spines():
    with pytest.raises(ValueError, match='bundle'):
        ok(kind='bundle', spines=('a',))


def test_rejects_unknown_kind():
    with pytest.raises(ValueError, match='kind'):
        ok(kind='boxset')


def test_rejects_unknown_palette():
    with pytest.raises(KeyError):
        ok(palette_key='gemini')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_spec.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'covers.spec'`

- [ ] **Step 3: Write minimal implementation**

```python
# covers/spec.py
"""What a single cover says. Rendering-agnostic."""
from dataclasses import dataclass

from covers import palette as _palette

KINDS = ('bundle', 'single')


@dataclass(frozen=True)
class CoverSpec:
    title_lines: tuple
    subtitle: str
    spines: tuple
    badge: str
    footer: str
    palette_key: str
    kind: str

    def __post_init__(self):
        self.validate()

    @property
    def palette(self):
        return _palette.get(self.palette_key)

    def validate(self):
        if not 1 <= len(self.title_lines) <= 2:
            raise ValueError('title_lines must hold 1 or 2 lines, got %d'
                             % len(self.title_lines))
        if not all(self.title_lines):
            raise ValueError('title_lines must not contain empty strings')
        if not 1 <= len(self.spines) <= 3:
            raise ValueError('spines must hold 1 to 3 entries, got %d'
                             % len(self.spines))
        if self.kind not in KINDS:
            raise ValueError('kind must be one of %s, got %r'
                             % (', '.join(KINDS), self.kind))
        if self.kind == 'single' and len(self.spines) != 1:
            raise ValueError('kind "single" needs exactly 1 spine, got %d'
                             % len(self.spines))
        if self.kind == 'bundle' and len(self.spines) != 3:
            raise ValueError('kind "bundle" needs exactly 3 spines, got %d'
                             % len(self.spines))
        _palette.get(self.palette_key)     # raises KeyError if unknown
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_spec.py -v`
Expected: PASS — 8 passed

- [ ] **Step 5: Commit**

```bash
git add covers/spec.py tests/test_spec.py
git commit -m "feat(covers): add CoverSpec with validation"
```

---

### Task 3: Derive specs from the SKU catalogue

**Files:**
- Create: `covers/catalogue.py`
- Modify: `build_etsy_kit.py` — add a `spines` key (and where needed `cover_badge`) to each of the 21 entries in `SKUS`
- Test: `tests/test_catalogue.py`

**Interfaces:**
- Consumes: `covers.spec.CoverSpec`
- Produces:
  - `covers.catalogue.palette_for(sku: dict) -> str`
  - `covers.catalogue.kind_for(sku: dict) -> str`
  - `covers.catalogue.spec_for(sku: dict) -> CoverSpec`
  - `covers.catalogue.all_specs() -> dict[str, CoverSpec]` — keyed by `sku['sku']`

**Derivation rules (implement exactly):**
- palette: `pdf` filename starts `Copilot_` → `copilot`; starts `Codex_` → `codex`; otherwise `claude`. (`gpt` and `grok` arrive with their own series later and are set by an explicit `palette` key.) An explicit `palette` key on the SKU always wins.
- kind: `single` for `01-prompt-vault`, `05-config-pack`, `11-cost-calculator`, `12-start-here`; `bundle` otherwise.
- title_lines: `headline.split('\n')`.
- subtitle: `' · '.join(badges)`.
- spines: the SKU's `spines` key. Required — no silent fallback, because a wrong spine label is invisible in a thumbnail but wrong on a product page.
- badge: the SKU's `cover_badge` if present, else `'VOL %d' % volume` if `volume` is set, else the first badge entry.
- footer: `'FREE DOWNLOAD'` for `12-start-here`, else `'INSTANT PDF DOWNLOAD'`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_catalogue.py
import pytest

import build_etsy_kit as kit
from covers import catalogue


def by_sku(name):
    return next(s for s in kit.SKUS if s['sku'] == name)


def test_every_live_sku_produces_a_valid_spec():
    specs = catalogue.all_specs()
    assert len(specs) == len(kit.SKUS) == 21


def test_palette_follows_the_pdf_prefix():
    assert catalogue.palette_for(by_sku('20-copilot-v1')) == 'copilot'
    assert catalogue.palette_for(by_sku('30-codex-v1')) == 'codex'
    assert catalogue.palette_for(by_sku('02-starter-volume')) == 'claude'


def test_explicit_palette_key_wins():
    assert catalogue.palette_for({'pdf': 'Anything.pdf', 'palette': 'grok'}) == 'grok'


def test_the_four_single_products_are_single_kind():
    for name in ('01-prompt-vault', '05-config-pack',
                 '11-cost-calculator', '12-start-here'):
        assert catalogue.kind_for(by_sku(name)) == 'single', name


def test_volumes_are_bundles():
    assert catalogue.kind_for(by_sku('02-starter-volume')) == 'bundle'


def test_subtitle_is_the_badges_joined():
    spec = catalogue.spec_for(by_sku('02-starter-volume'))
    assert spec.subtitle == '5 GUIDES · 32 PAGES · STEP BY STEP'


def test_badge_uses_the_volume_number_when_present():
    assert catalogue.spec_for(by_sku('02-starter-volume')).badge == 'VOL 1'


def test_start_here_footer_says_free():
    assert catalogue.spec_for(by_sku('12-start-here')).footer == 'FREE DOWNLOAD'


def test_missing_spines_is_a_hard_error():
    with pytest.raises(KeyError, match='spines'):
        catalogue.spec_for({'sku': 'x', 'pdf': 'x.pdf', 'headline': 'A\nB',
                            'badges': ['ONE']})


def test_every_sku_declares_spines():
    missing = [s['sku'] for s in kit.SKUS if not s.get('spines')]
    assert missing == []


def test_spine_labels_are_short_enough_to_read_on_a_spine():
    # Check each spine's own lines. Joining the spines first would invent lines
    # that span two labels and fail on correct data.
    for s in kit.SKUS:
        for spine in s['spines']:
            for line in spine.split('\n'):
                assert len(line) <= 18, (s['sku'], line)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_catalogue.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'covers.catalogue'`

- [ ] **Step 3: Write the catalogue module**

```python
# covers/catalogue.py
"""Derive a CoverSpec from the existing SKU catalogue.

build_etsy_kit.SKUS stays the single source of listing copy. This module reads
it; it never duplicates it.
"""
import build_etsy_kit as _kit
from covers.spec import CoverSpec

SINGLE_SKUS = {'01-prompt-vault', '05-config-pack',
               '11-cost-calculator', '12-start-here'}


def palette_for(sku):
    if sku.get('palette'):
        return sku['palette']
    pdf = sku.get('pdf', '')
    if pdf.startswith('Copilot_'):
        return 'copilot'
    if pdf.startswith('Codex_'):
        return 'codex'
    return 'claude'


def kind_for(sku):
    return 'single' if sku.get('sku') in SINGLE_SKUS else 'bundle'


def _badge(sku):
    if sku.get('cover_badge'):
        return sku['cover_badge']
    if sku.get('volume'):
        return 'VOL %d' % sku['volume']
    return sku['badges'][0]


def spec_for(sku):
    if not sku.get('spines'):
        raise KeyError('SKU %r has no "spines" key' % sku.get('sku'))
    return CoverSpec(
        title_lines=tuple(sku['headline'].split('\n')),
        subtitle=' · '.join(sku['badges']),
        spines=tuple(sku['spines']),
        badge=_badge(sku),
        footer=('FREE DOWNLOAD' if sku.get('sku') == '12-start-here'
                else 'INSTANT PDF DOWNLOAD'),
        palette_key=palette_for(sku),
        kind=kind_for(sku),
    )


def all_specs():
    return {s['sku']: spec_for(s) for s in _kit.SKUS}
```

- [ ] **Step 4: Add `spines` to every SKU in `build_etsy_kit.py`**

Add a `spines=[...]` entry to each of the 21 dicts in `SKUS`, immediately after the existing `badges=[...]` line. Bundles take exactly three, singles exactly one. Order is back-left, front-centre, back-right — the front-centre entry is the one people read, so it carries the product's own name.

```python
# 01-prompt-vault      (single)
spines=['The Claude\nPrompt Vault'],
# 02-starter-volume
spines=['Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'],
# 03-complete-library
spines=['Volumes\n1 – 2', 'The Complete\nLibrary', 'Volumes\n5 – 6'],
# 04-claude-code-volume
spines=['Claude Code\nin VS Code', 'Claude Code\n& Agents', 'Hooks &\nSubagents'],
# 05-config-pack       (single)
spines=['Claude Code\nConfig Pack'],
# 06-volume-2-developer-setup
spines=['Node.js\n& npm', 'Developer\nSetup', 'Git &\nGitHub'],
# 07-volume-4-automation-kit
spines=['MCP\nServers', 'Automation\nKit', 'Plugins\n& Skills'],
# 08-volume-5-api-automation
spines=['The Claude\nAPI', 'API &\nAutomation', 'Prompting\nMasterclass'],
# 09-volume-6-advanced
spines=['Multi-Agent\nOrchestration', 'Advanced\nAdd-Ons', 'Cost &\nTokens'],
# 10-cheat-sheet-pack
spines=['Claude Code\nCommands', 'Cheat Sheet\nPack', 'MCP &\nHooks'],
# 11-cost-calculator   (single)
spines=['AI Cost\nCalculator'],
# 12-start-here        (single)
spines=['Start Here'],
# 20-copilot-v1
spines=['The Editors', 'Getting\nStarted', 'Credits\n& Plans'],
# 21-copilot-v2
spines=['Ask, Edit,\nAgent', 'Chat &\nAgent Mode', 'Slash\nCommands'],
# 22-copilot-v3
spines=['The CLI', 'CLI & Coding\nAgent', 'Pull\nRequests'],
# 23-copilot-v4
spines=['Instruction\nFiles', 'Customisation', 'MCP &\nHooks'],
# 24-copilot-v5
spines=['Credits\nExplained', 'Cost &\nTeams', 'Budgets\n& Pools'],
# 30-codex-v1
spines=['Install\n& Setup', 'Getting\nStarted', 'Plans &\nLimits'],
# 31-codex-v2
spines=['Commands', 'The Codex\nCLI', 'Permissions\n& Sandbox'],
# 32-codex-v3
spines=['AGENTS.md', 'Subagents\n& MCP', 'MCP\nServers'],
# 33-codex-v4
spines=['Delegation', 'Review\n& Cost', 'Usage\nLimits'],
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_catalogue.py -v`
Expected: PASS — 11 passed

- [ ] **Step 6: Commit**

```bash
git add covers/catalogue.py build_etsy_kit.py tests/test_catalogue.py
git commit -m "feat(covers): derive CoverSpec from the SKU catalogue"
```

---

### Task 4: The renderer — square shape

**Files:**
- Create: `covers/render.py`
- Test: `tests/test_render.py`

**Interfaces:**
- Consumes: `covers.spec.CoverSpec`, `covers.palette.Palette`
- Produces:
  - `covers.render.font(size: int, bold: bool = True) -> ImageFont`
  - `covers.render.fit_text(text: str, max_w: int, start: int, bold: bool = True, floor: int = 8) -> ImageFont` — shrinks until the text measures within `max_w`; raises `ValueError` if it would have to go below `floor`
  - `covers.render.gradient(size: tuple[int, int], stops: tuple) -> Image` — three-stop diagonal
  - `covers.render.render(spec: CoverSpec, shape: str = 'square') -> Image` — `shape` in `('square', 'wide', 'pin')`
  - `covers.render.SHAPES: dict[str, tuple[int, int]]` — `{'square': (2000, 2000), 'wide': (1280, 720), 'pin': (1000, 1500)}`

**Why `fit_text` exists:** `CLAUDE.md` logs four separate cover-text overflow bugs caused by hardcoded widths. Measuring before drawing makes that class of bug impossible.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_render.py
import pytest

from covers import catalogue, render
from covers.spec import CoverSpec


def spec(**over):
    base = dict(title_lines=('Claude AI', 'for Beginners'),
                subtitle='5 GUIDES · 32 PAGES · STEP BY STEP',
                spines=('Claude on\nthe Web', 'Getting\nInto Claude', 'Claude in\nChrome'),
                badge='VOL 1', footer='INSTANT PDF DOWNLOAD',
                palette_key='claude', kind='bundle')
    base.update(over)
    return CoverSpec(**base)


def test_square_render_has_the_etsy_dimensions():
    assert render.render(spec(), 'square').size == (2000, 2000)


def test_render_rejects_an_unknown_shape():
    with pytest.raises(KeyError, match='square'):
        render.render(spec(), 'billboard')


def test_background_matches_the_palette_at_the_top_edge():
    img = render.render(spec(), 'square').convert('RGB')
    r, g, b = img.getpixel((5, 5))
    assert abs(r - 255) < 12 and abs(g - 244) < 12 and abs(b - 236) < 12


def test_render_is_not_a_flat_fill():
    img = render.render(spec(), 'square').convert('RGB')
    assert len(set(img.getdata())) > 500


def test_fit_text_shrinks_a_long_string_to_fit():
    text = 'a very long product title indeed'
    f = render.fit_text(text, 300, 120)
    box = f.getbbox(text)
    # Measure the way fit_text measures — advance width, not the right edge,
    # so a non-zero left side bearing cannot make this disagree with the code.
    assert box[2] - box[0] <= 300


def test_fit_text_refuses_to_go_below_the_floor():
    with pytest.raises(ValueError, match='floor'):
        render.fit_text('x' * 400, 50, 120, floor=40)


def test_single_kind_renders_without_error():
    s = spec(kind='single', spines=('The Claude\nPrompt Vault',), badge='200')
    assert render.render(s, 'square').size == (2000, 2000)


def test_every_live_sku_renders():
    for name, s in catalogue.all_specs().items():
        assert render.render(s, 'square').size == (2000, 2000), name
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_render.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'covers.render'`

- [ ] **Step 3: Write the renderer**

```python
# covers/render.py
"""Direction C — the angled 3D stack.

One renderer draws every shape, so the PDF cover page and the listing images
cannot drift apart. Visual reference: outputs/design/cover-system.html
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = r'C:\Windows\Fonts'
BOLD = ['seguibl.ttf', 'arialbd.ttf', 'segoeuib.ttf']
REG = ['segoeui.ttf', 'arial.ttf']

SHAPES = {'square': (2000, 2000), 'wide': (1280, 720), 'pin': (1000, 1500)}

# rotation, in degrees, of each element. Fixed by the approved design.
ROT_BACK_LEFT, ROT_FRONT, ROT_BACK_RIGHT = -8, -2, 6
ROT_SINGLE, ROT_BADGE = -3, 6


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


def _spine(size, colour, label, pal):
    """One book spine, unrotated, with its dark left edge and white rule."""
    w, h = size
    img = Image.new('RGBA', (w, h), colour + (255,))
    d = ImageDraw.Draw(img)
    edge = max(3, int(w * 0.035))
    for x in range(edge):
        t = x / float(edge)
        d.line([(x, 0), (x, h)], fill=(0, 0, 0, int(115 * (1 - t))))
    pad = int(w * 0.10)
    fnt = fit_text(max(label.split('\n'), key=len), w - pad * 2,
                   max(9, int(w * 0.105)))
    y = int(h * 0.13)
    for line in label.split('\n'):
        d.text((pad, y), line, font=fnt, fill=(255, 255, 255, 255))
        y += int(fnt.size * 1.25)
    d.rectangle([pad, y + int(h * 0.02), pad + int(w * 0.34),
                 y + int(h * 0.02) + max(2, int(h * 0.007))],
                fill=(255, 255, 255, 140))
    return img


def _paste_rotated(base, img, centre, angle, pal, shadow=True):
    rot = img.rotate(angle, expand=True, resample=Image.BICUBIC)
    x = int(centre[0] - rot.width / 2)
    y = int(centre[1] - rot.height / 2)
    if shadow:
        sh = Image.new('RGBA', rot.size, (0, 0, 0, 0))
        sh.paste(pal.shadow + (120,), (0, 0), rot)
        sh = sh.filter(ImageFilter.GaussianBlur(int(base.width * 0.014)))
        base.alpha_composite(sh, (x - int(base.width * 0.006),
                                  y + int(base.width * 0.012)))
    base.alpha_composite(rot, (x, y))


def _badge(base, text, centre, pal, scale):
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
    _paste_rotated(base, chip, centre, ROT_BADGE, pal, shadow=False)


def _centred(d, text, fnt, cx, y, fill):
    d.text((cx - _width(text, fnt) / 2, y), text, font=fnt, fill=fill)


def _stack(base, spec, box, pal):
    """Draw the spine stack inside box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    if spec.kind == 'single':
        sw, sh = int(bw * 0.46), int(bh * 0.88)
        img = _spine((sw, sh), pal.spine_front, spec.spines[0], pal)
        _paste_rotated(base, img, (x0 + bw * 0.50, y0 + bh * 0.50),
                       ROT_SINGLE, pal)
        return
    back, front, right = spec.spines
    sw, sh = int(bw * 0.40), int(bh * 0.82)
    _paste_rotated(base, _spine((sw, sh), pal.spine_back_left, back, pal),
                   (x0 + bw * 0.27, y0 + bh * 0.51), ROT_BACK_LEFT, pal)
    _paste_rotated(base, _spine((int(bw * 0.42), int(bh * 0.86)),
                                pal.spine_back_right, right, pal),
                   (x0 + bw * 0.73, y0 + bh * 0.51), ROT_BACK_RIGHT, pal)
    _paste_rotated(base, _spine((sw, sh), pal.spine_front, front, pal),
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
    _badge(base, spec.badge, (w - pad - int(w * 0.035), y + int(h * 0.01)),
           pal, w)

    spaced = '  '.join(spec.footer)
    ff = fit_text(spaced, inner, int(w * 0.019))
    _centred(d, spaced, ff, w / 2, foot_y, pal.muted + (255,))
    return base.convert('RGB')


def _render_wide(spec, size):
    """Gumroad's grid is landscape: title block left, stack right."""
    w, h = size
    pal = spec.palette
    base = gradient(size, pal.grad).convert('RGBA')
    d = ImageDraw.Draw(base)
    pad = int(w * 0.06)
    col = int(w * 0.46)

    y = int(h * 0.26)
    tf = fit_text(max(spec.title_lines, key=len), col, int(h * 0.145))
    for line in spec.title_lines:
        d.text((pad, y), line, font=tf, fill=pal.title + (255,))
        y += int(tf.size * 1.04)
    y += int(h * 0.030)
    sf = fit_text(spec.subtitle, col, int(h * 0.040))
    d.text((pad, y), spec.subtitle, font=sf, fill=pal.muted + (255,))

    sx0 = w - pad - int(h * 0.80)
    _stack(base, spec, (sx0, int(h * 0.10), w - pad, int(h * 0.90)), pal)
    return base.convert('RGB')


def render(spec, shape='square'):
    if shape not in SHAPES:
        raise KeyError('unknown shape %r — valid: %s'
                       % (shape, ', '.join(sorted(SHAPES))))
    size = SHAPES[shape]
    return _render_wide(spec, size) if shape == 'wide' else _render_portrait(spec, size)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_render.py -v`
Expected: PASS — 8 passed

- [ ] **Step 5: Eyeball one render before trusting the suite**

```bash
cd /c/Projects/UserGuide
python -c "from covers import catalogue, render; render.render(catalogue.all_specs()['02-starter-volume'],'square').save(r'outputs\design\_check_square.png')"
start outputs\design\_check_square.png
```

Compare against `outputs/design/cover-system.html`. The suite proves it renders; only your eye proves it renders *right*.

- [ ] **Step 6: Commit**

```bash
git add covers/render.py tests/test_render.py
git commit -m "feat(covers): render the direction C square cover"
```

---

### Task 5: Wide and pin shapes

**Files:**
- Modify: `covers/render.py` — already contains `_render_wide`; this task proves both non-square shapes
- Test: `tests/test_shapes.py`

**Interfaces:**
- Consumes: `covers.render.render`, `covers.render.SHAPES`
- Produces: no new names — this task locks the contract that all three shapes render for all 21 SKUs

- [ ] **Step 1: Write the failing test**

```python
# tests/test_shapes.py
from covers import catalogue, render


def test_shape_dimensions_match_the_destinations():
    assert render.SHAPES == {'square': (2000, 2000),
                             'wide': (1280, 720),
                             'pin': (1000, 1500)}


def test_wide_is_landscape_so_gumroad_stops_cropping():
    img = render.render(catalogue.all_specs()['02-starter-volume'], 'wide')
    assert img.size == (1280, 720)
    assert img.width > img.height


def test_pin_is_the_pinterest_two_to_three_ratio():
    img = render.render(catalogue.all_specs()['02-starter-volume'], 'pin')
    assert img.size == (1000, 1500)
    assert round(img.width / img.height, 3) == 0.667


def test_all_three_shapes_render_for_all_21_skus():
    for name, spec in catalogue.all_specs().items():
        for shape in ('square', 'wide', 'pin'):
            img = render.render(spec, shape)
            assert img.size == render.SHAPES[shape], (name, shape)


def test_no_shape_renders_flat():
    for shape in ('square', 'wide', 'pin'):
        img = render.render(catalogue.all_specs()['30-codex-v1'], shape)
        assert len(set(img.convert('RGB').getdata())) > 500, shape
```

- [ ] **Step 2: Run test to verify it fails or passes for the right reason**

Run: `python -m pytest tests/test_shapes.py -v`
Expected: the 21×3 test is the one that matters. If any SKU raises `ValueError` from `fit_text`, that is a real defect — shorten that SKU's `spines` entry in `build_etsy_kit.py` rather than lowering the floor.

- [ ] **Step 3: Fix any SKU that fails to fit**

No code change should be needed in `render.py`. If a spine label cannot fit, edit its `spines` entry in `build_etsy_kit.SKUS` to a shorter phrase and re-run.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/ -v`
Expected: PASS — all tests across all files

- [ ] **Step 5: Eyeball the wide and pin shapes**

```bash
cd /c/Projects/UserGuide
python -c "from covers import catalogue, render; s=catalogue.all_specs()['02-starter-volume']; render.render(s,'wide').save(r'outputs\design\_check_wide.png'); render.render(s,'pin').save(r'outputs\design\_check_pin.png')"
start outputs\design\_check_wide.png
```

- [ ] **Step 6: Commit**

```bash
git add covers/render.py tests/test_shapes.py build_etsy_kit.py
git commit -m "test(covers): lock all three shapes across all 21 SKUs"
```

---

### Task 6: The one-page cover PDF

**Files:**
- Create: `covers/pdfpage.py`
- Test: `tests/test_pdfpage.py`

**Interfaces:**
- Consumes: `covers.render.render`, `covers.spec.CoverSpec`
- Produces:
  - `covers.pdfpage.PAGE_W`, `covers.pdfpage.PAGE_H` — `612.0`, `792.0`
  - `covers.pdfpage.cover_pdf_bytes(spec: CoverSpec) -> bytes` — a one-page US Letter PDF whose single page is the square render, cropped to letter aspect and placed full-bleed

**Note on aspect:** the square render is 1:1 and the page is 0.773:1. Crop the square vertically about its centre to the page aspect rather than distorting it — the design has breathing room top and bottom for exactly this.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_pdfpage.py
import io

import fitz

from covers import catalogue, pdfpage


def test_produces_a_single_letter_page():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    assert doc.page_count == 1
    r = doc[0].rect
    assert round(r.width) == 612 and round(r.height) == 792
    doc.close()


def test_the_page_carries_a_full_bleed_image():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    info = doc[0].get_image_info()
    assert len(info) == 1
    bbox = fitz.Rect(info[0]['bbox'])
    assert bbox.width >= 611 and bbox.height >= 791
    doc.close()


def test_the_page_has_no_text_spans_so_the_audit_cannot_flag_it():
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    doc = fitz.open(stream=data, filetype='pdf')
    assert doc[0].get_text().strip() == ''
    doc.close()


def test_every_sku_produces_a_valid_cover_pdf():
    for name, spec in catalogue.all_specs().items():
        data = pdfpage.cover_pdf_bytes(spec)
        doc = fitz.open(stream=data, filetype='pdf')
        assert doc.page_count == 1, name
        doc.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pdfpage.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'covers.pdfpage'`

- [ ] **Step 3: Write the implementation**

```python
# covers/pdfpage.py
"""Turn a rendered cover into a one-page US Letter PDF.

The cover is rasterised deliberately. One engine draws both the listing image
and the PDF cover page, so they cannot drift; and because the page carries no
text spans, audit_pdfs.py cannot flag it for the overflow bugs that have hit
cover pages four times in this project's history.
"""
import io

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from covers import render

PAGE_W, PAGE_H = 612.0, 792.0
DPI = 200
JPEG_QUALITY = 92


def _letter_crop(img):
    """Centre-crop the square render to the page aspect. Never distort."""
    target = PAGE_W / PAGE_H
    w, h = img.size
    new_h = int(round(w / target))
    if new_h > h:                      # too tall for the source: crop width
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def cover_pdf_bytes(spec):
    img = _letter_crop(render.render(spec, 'square'))
    target_px = (int(PAGE_W / 72.0 * DPI), int(PAGE_H / 72.0 * DPI))
    img = img.resize(target_px, Image.LANCZOS)

    raw = io.BytesIO()
    img.save(raw, format='JPEG', quality=JPEG_QUALITY, optimize=True)
    raw.seek(0)

    out = io.BytesIO()
    c = canvas.Canvas(out, pagesize=(PAGE_W, PAGE_H))
    c.drawImage(ImageReader(raw), 0, 0, width=PAGE_W, height=PAGE_H)
    c.showPage()
    c.save()
    return out.getvalue()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_pdfpage.py -v`
Expected: PASS — 4 passed

- [ ] **Step 5: Commit**

```bash
git add covers/pdfpage.py tests/test_pdfpage.py
git commit -m "feat(covers): render the cover as a one-page letter PDF"
```

---

### Task 7: Splice the new cover into the 21 live PDFs

**Files:**
- Create: `rebuild_covers.py`
- Modify: `audit_pdfs.py:58-60` — a page with no text is only blank if it also has no images
- Modify: the 21 build scripts — one comment marking the superseded `cover()` / `volume_cover()`
- Test: `tests/test_rebuild_covers.py`
- Test: `tests/test_audit_blank.py`

**Interfaces:**
- Consumes: `covers.catalogue.all_specs`, `covers.pdfpage.cover_pdf_bytes`, `audit_pdfs.audit`
- Produces:
  - `rebuild_covers.BACKUP_DIR` — `outputs/_pre_cover_backup`
  - `rebuild_covers.backup_once(pdf_name: str) -> str` — copies the original exactly once; returns the backup path
  - `rebuild_covers.splice(pdf_path: str, cover_bytes: bytes) -> None` — replaces page 0 atomically
  - `rebuild_covers.rebuild(sku_filter: list[str] | None = None, dry_run: bool = False) -> list[tuple[str, str]]` — returns `(sku, status)` pairs
  - `rebuild_covers.main()` — CLI entry, `--skus a,b`, `--dry-run`

**The backup rule that matters:** `backup_once` must never overwrite an existing backup. A second run would otherwise replace the pristine original with an already-modified file, and the true original would be gone forever.

- [ ] **Step 1: Teach the audit that an image-only page is not blank**

`audit_pdfs.spans()` collects **text** spans only, so `audit()` files any page with no
text under `blank`. The new cover page is a single full-bleed image with zero text spans,
so without this change every one of the 21 rebuilds fails its own verify guard.

Write the failing test first:

```python
# tests/test_audit_blank.py
import fitz

import audit_pdfs
from covers import catalogue, pdfpage


def test_a_truly_empty_page_is_still_blank(tmp_path):
    p = tmp_path / 'empty.pdf'
    doc = fitz.open()
    doc.new_page(width=612, height=792)
    doc.save(str(p))
    doc.close()
    _n, _meta, issues = audit_pdfs.audit(str(p))
    assert issues['blank'] == [1]


def test_an_image_only_page_is_not_blank(tmp_path):
    p = tmp_path / 'cover.pdf'
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    p.write_bytes(data)
    _n, _meta, issues = audit_pdfs.audit(str(p))
    assert 'blank' not in issues
```

Run: `python -m pytest tests/test_audit_blank.py -v`
Expected: FAIL — the image-only page is reported blank

Then change `audit()` in `audit_pdfs.py`. Replace:

```python
        sp = spans(page)
        if not sp:
            issues['blank'].append(pno + 1)
            continue
```

with:

```python
        sp = spans(page)
        if not sp:
            # A full-bleed cover carries no text spans but is not blank.
            if not page.get_image_info():
                issues['blank'].append(pno + 1)
            continue
```

Run: `python -m pytest tests/test_audit_blank.py -v`
Expected: PASS — 2 passed

- [ ] **Step 2: Write the failing test**

```python
# tests/test_rebuild_covers.py
import os
import shutil

import fitz
import pytest

import rebuild_covers
from covers import catalogue, pdfpage


@pytest.fixture
def sample(tmp_path):
    p = tmp_path / 'sample.pdf'
    doc = fitz.open()
    for i in range(4):
        page = doc.new_page(width=612, height=792)
        page.insert_text((80, 120), 'original page %d' % i)
    doc.save(str(p))
    doc.close()
    return str(p)


def test_splice_keeps_the_page_count(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert doc.page_count == 4
    doc.close()


def test_splice_replaces_page_zero_and_leaves_the_interior_alone(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert 'original page 0' not in doc[0].get_text()
    assert 'original page 1' in doc[1].get_text()
    assert 'original page 3' in doc[3].get_text()
    doc.close()


def test_spliced_page_zero_is_not_blank(sample):
    data = pdfpage.cover_pdf_bytes(catalogue.all_specs()['02-starter-volume'])
    rebuild_covers.splice(sample, data)
    doc = fitz.open(sample)
    assert len(doc[0].get_image_info()) == 1
    doc.close()


def test_backup_once_never_overwrites_the_pristine_original(tmp_path, monkeypatch):
    out = tmp_path / 'outputs'
    out.mkdir()
    (out / 'thing.pdf').write_bytes(b'ORIGINAL')
    monkeypatch.setattr(rebuild_covers, 'OUT', str(out))
    monkeypatch.setattr(rebuild_covers, 'BACKUP_DIR', str(out / '_pre_cover_backup'))

    rebuild_covers.backup_once('thing.pdf')
    (out / 'thing.pdf').write_bytes(b'MODIFIED')
    rebuild_covers.backup_once('thing.pdf')

    kept = (out / '_pre_cover_backup' / 'thing.pdf').read_bytes()
    assert kept == b'ORIGINAL'


def test_dry_run_writes_nothing(tmp_path, monkeypatch):
    out = tmp_path / 'outputs'
    out.mkdir()
    monkeypatch.setattr(rebuild_covers, 'OUT', str(out))
    results = rebuild_covers.rebuild(dry_run=True)
    assert results
    assert not os.path.exists(out / '_pre_cover_backup')
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python -m pytest tests/test_rebuild_covers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'rebuild_covers'`

- [ ] **Step 4: Write the implementation**

```python
#!/usr/bin/env python3
"""Replace page 1 of every live product PDF with the new direction C cover.

Approach A from the design doc: render centrally, splice into the shipped PDFs.
Interiors are NEVER regenerated, so nothing that is currently audit-clean can
regress.

Run:
    python rebuild_covers.py --dry-run
    python rebuild_covers.py
    python rebuild_covers.py --skus 02-starter-volume,30-codex-v1
"""
import argparse
import os
import shutil
import sys

import fitz

import audit_pdfs
import build_etsy_kit as kit
from covers import catalogue, pdfpage

ROOT = r'C:\Projects\UserGuide'
OUT = os.path.join(ROOT, 'outputs')
BACKUP_DIR = os.path.join(OUT, '_pre_cover_backup')


def backup_once(pdf_name):
    """Copy the original aside exactly once. Never overwrite a backup."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dst = os.path.join(BACKUP_DIR, pdf_name)
    if not os.path.exists(dst):
        shutil.copy2(os.path.join(OUT, pdf_name), dst)
    return dst


def splice(pdf_path, cover_bytes):
    """Replace page 0 with the cover. Atomic: temp file, then replace."""
    doc = fitz.open(pdf_path)
    before = doc.page_count
    cover = fitz.open(stream=cover_bytes, filetype='pdf')
    doc.delete_page(0)
    doc.insert_pdf(cover, from_page=0, to_page=0, start_at=0)
    if doc.page_count != before:
        doc.close()
        cover.close()
        raise AssertionError('page count changed %d -> %d in %s'
                             % (before, doc.page_count, pdf_path))
    tmp = pdf_path + '.tmp'
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    cover.close()
    os.replace(tmp, pdf_path)


def _verify(pdf_path):
    """Check page 0 — the only page this script touches.

    Deliberately NOT a whole-document audit. audit_pdfs.py encodes the volume
    geometry (MX 46.8pt, 22pt footer), but four SKUs are not volumes: the Cheat
    Sheet Pack is a light single-wide-column printable, and the Cost Calculator
    preview, Prompt Vault and Start Here each have their own layout. Gating on a
    whole-document audit would let a pre-existing interior quirk in one of them
    abort a rollout that only ever replaced page 1. The full audit still runs as
    a release check over the whole catalogue — see the run instructions.
    """
    doc = fitz.open(pdf_path)
    try:
        page = doc[0]
        if len(page.get_image_info()) != 1:
            raise AssertionError('page 1 of %s is not a single full-bleed image'
                                 % os.path.basename(pdf_path))
        if page.get_text().strip():
            raise AssertionError('page 1 of %s still carries text'
                                 % os.path.basename(pdf_path))
    finally:
        doc.close()


def rebuild(sku_filter=None, dry_run=False):
    specs = catalogue.all_specs()
    results = []
    for s in kit.SKUS:
        name = s['sku']
        if sku_filter and name not in sku_filter:
            continue
        pdf_name = s['pdf']
        path = os.path.join(OUT, pdf_name)
        if not os.path.exists(path):
            results.append((name, 'MISSING %s' % pdf_name))
            continue
        if dry_run:
            results.append((name, 'would rebuild %s' % pdf_name))
            continue
        backup_once(pdf_name)
        splice(path, pdfpage.cover_pdf_bytes(specs[name]))
        _verify(path)
        results.append((name, 'ok'))
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skus', help='comma-separated SKU names')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    filt = a.skus.split(',') if a.skus else None
    failed = 0
    for name, status in rebuild(filt, a.dry_run):
        if status != 'ok' and not a.dry_run:
            failed += 1
        print('%-30s %s' % (name, status))
    print('\n%s' % ('DRY RUN — nothing written' if a.dry_run
                    else '%d problem(s)' % failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_rebuild_covers.py -v`
Expected: PASS — 5 passed

- [ ] **Step 6: Dry run against the real catalogue**

Run: `python rebuild_covers.py --dry-run`
Expected: 21 lines, each "would rebuild ...", and "DRY RUN — nothing written"

- [ ] **Step 7: Rebuild one SKU and look at it**

```bash
cd /c/Projects/UserGuide
python rebuild_covers.py --skus 02-starter-volume
start outputs\Claude_Field_Guide_Volume_1_Getting_Started.pdf
```

Confirm page 1 is the new cover, page 2 onward is untouched, and the page count still reads 32.

- [ ] **Step 8: Rebuild all 21**

Run: `python rebuild_covers.py`
Expected: 21 × "ok", then "0 problem(s)"

- [ ] **Step 9: Full audit**

Run: `python audit_pdfs.py`
Expected: CLEAN for every file, or only the known cover-tagline false positive documented in `CLAUDE.md`

- [ ] **Step 10: Mark the superseded cover functions**

The `cover()` / `volume_cover()` function in each build script no longer produces what
ships. Leave the code in place — deleting it would silently change what a from-source
rebuild produces — but add this comment directly above each one so the next person
understands why page 1 of the PDF does not match the code that claims to draw it:

```python
# SUPERSEDED 2026-09-17 — page 1 of the shipped PDF is now rendered by covers/
# and spliced in by rebuild_covers.py. This function is retained so a from-source
# rebuild still produces a complete document; run rebuild_covers.py afterwards.
```

Apply to the cover function in: `build_guide01.py` … `build_guide23.py` (the `cover()`
in each), `build_volumes.py` (`volume_cover()`), `build_copilot_v1.py` … `v5`,
`build_codex_v1.py` … `v4`, `build_prompt_vault.py`, `build_config_pack.py`,
`build_cheatsheets.py`, `build_start_here.py`, `build_cost_calculator.py`.

Verify none were missed:

```bash
cd /c/Projects/UserGuide
grep -L "SUPERSEDED 2026-09-17" $(grep -rl "^def cover\|^def volume_cover" build_*.py)
```

Expected: no output — every file that defines a cover function carries the note.

- [ ] **Step 11: Commit**

```bash
git add rebuild_covers.py audit_pdfs.py tests/test_rebuild_covers.py tests/test_audit_blank.py build_*.py
git commit -m "feat: splice the new cover into all 21 live PDFs"
```

---

### Task 8: Regenerate listing images and wire up the channels

**Files:**
- Modify: `build_etsy_kit.py` — replace the body of `img_main`, add `img_pin`, add both to `main()`
- Test: `tests/test_listing_images.py`

**Interfaces:**
- Consumes: `covers.catalogue.spec_for`, `covers.render.render`
- Produces:
  - `build_etsy_kit.img_main(s, pdf_path) -> Image` — now returns the direction C square render
  - `build_etsy_kit.img_pin(s) -> Image` — the 1000×1500 Pinterest render
  - `build_etsy_kit.img_wide(s) -> Image` — the 1280×720 Gumroad render
  - files `outputs/etsy/<sku>/01_main.png`, `04_pin.png`, `05_wide.png`

`02_inside.png` and `03_included.png` are **not** touched. They composite real rendered pages, which is honest and satisfies Etsy's three-image minimum.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_listing_images.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_listing_images.py -v`
Expected: FAIL — `img_main` still composites a page, and `img_pin` does not exist

- [ ] **Step 3: Replace `img_main` and add the two new renderers**

Replace the whole body of `img_main` (currently at line 678) and add the two new functions beside it.

**Import `covers` inside the functions, not at module top.** `covers/catalogue.py` imports
`build_etsy_kit`, so a module-level import here would form a cycle. It would happen to
resolve today — neither module touches the other's attributes at import time — but that is
an accident, not a design, and the next person to add a module-level constant breaks it.

```python
def _cover_render(s, shape):
    """Render this SKU's cover. Imported lazily: covers.catalogue imports this
    module, and a module-level import here would make that a cycle."""
    from covers import catalogue, render
    return render.render(catalogue.spec_for(s), shape)


def img_main(s, pdf_path=None):
    """The Etsy main image — direction C, generated not composited.

    pdf_path is accepted and ignored; kept so existing callers still work.
    """
    return _cover_render(s, 'square')


def img_pin(s):
    """1000x1500 for Pinterest."""
    return _cover_render(s, 'pin')


def img_wide(s):
    """1280x720 for the Gumroad storefront grid, which is landscape."""
    return _cover_render(s, 'wide')
```

- [ ] **Step 4: Write the new files in `main()`**

In `build_etsy_kit.main()` (line 840), alongside the existing `01_main.png` save, add:

```python
        img_pin(s).save(os.path.join(d, '04_pin.png'))
        img_wide(s).save(os.path.join(d, '05_wide.png'))
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/ -v`
Expected: PASS — every test file

- [ ] **Step 6: Regenerate the whole kit and look at it**

```bash
cd /c/Projects/UserGuide
python build_etsy_kit.py
start outputs\etsy\02-starter-volume\01_main.png
```

Confirm `01_main.png`, `04_pin.png` and `05_wide.png` exist for all 21 SKUs and that `02_inside.png` / `03_included.png` are unchanged.

- [ ] **Step 7: Push the new files and images to both channels**

```bash
cd /c/Projects/UserGuide
python -m etsypub.publish --update-files
python -m etsypub.publish --status
```

`--update-files` uploads the new PDF **before** deleting the old one — Etsy deactivates a digital listing left with no file. Gumroad covers are pulled from the Etsy listing images, so upload `05_wide.png` to each Etsy listing first, then re-run the Gumroad cover step so the storefront stops side-cropping.

- [ ] **Step 8: Commit**

```bash
git add build_etsy_kit.py tests/test_listing_images.py
git commit -m "feat: regenerate listing images from the cover system"
```

---

## Done when

- `python -m pytest tests/ -v` passes.
- `python rebuild_covers.py` reports 21 × ok, 0 problems.
- `python audit_pdfs.py` is clean.
- Every SKU has `01_main.png`, `04_pin.png`, `05_wide.png`.
- `outputs/_pre_cover_backup/` holds 21 pristine originals.
- Both channels serve the new files, and Gumroad covers are landscape.
