"""Derive a CoverSpec from the existing SKU catalogue.

build_etsy_kit.SKUS stays the single source of listing copy. This module reads
it; it never duplicates it.
"""
import build_etsy_kit as _kit
from covers.spec import CoverSpec

SINGLE_SKUS = {'01-prompt-vault', '05-config-pack',
               '11-cost-calculator', '12-start-here'}

# Maps a `pdf` filename prefix to its series palette. An explicit `palette`
# key on the SKU always wins. Otherwise the filename must match one of these
# prefixes -- there is no silent default. Adding a new series (ChatGPT, Grok,
# ...) means adding its prefix here; a SKU whose file does not start with any
# known prefix needs an explicit `palette` key instead (see 11-cost-calculator
# in build_etsy_kit.py).
PREFIX_PALETTE = {
    'Claude_': 'claude', 'Copilot_': 'copilot', 'Codex_': 'codex',
    'ChatGPT_': 'gpt', 'Grok_': 'grok',
}


def palette_for(sku):
    if sku.get('palette'):
        return sku['palette']
    pdf = sku.get('pdf', '')
    for prefix, key in PREFIX_PALETTE.items():
        if pdf.startswith(prefix):
            return key
    raise KeyError('cannot resolve a palette for %r -- filename matches none '
                   'of the known prefixes (%s) and the SKU has no explicit '
                   '"palette" key' % (pdf, ', '.join(sorted(PREFIX_PALETTE))))


def kind_for(sku):
    return 'single' if sku.get('sku') in SINGLE_SKUS else 'bundle'


def _badge(sku):
    if sku.get('cover_badge'):
        return sku['cover_badge']
    if sku.get('volume'):
        return 'VOL %d' % sku['volume']
    return ''


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
