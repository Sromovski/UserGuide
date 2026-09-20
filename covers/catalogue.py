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
