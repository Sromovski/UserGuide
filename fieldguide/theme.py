"""Palettes. One skeleton, three skins.

The Claude series hardcoded its colours into all 23 build scripts, which is why the
cover-badge width bug had to be fixed 23 times instead of once. New series get their
colours from here.

Only the background and the two accents change between series. Everything else — text
greys, panel fills, success green, warning amber, code background — stays identical, so
the three series read as one family of products from one publisher while still being
instantly distinguishable on a search grid.
"""
from __future__ import annotations

from dataclasses import dataclass

from reportlab.lib.colors import HexColor


@dataclass(frozen=True)
class Theme:
    name: str
    series: str            # printed in the cover strap and running footer
    bg: str                # page background
    accent: str            # primary accent — headings, bars, badges
    accent_light: str      # secondary accent — subheads, footer text
    accent_dark: str       # decorative circles
    accent_darker: str     # badge background

    # Shared across every series.
    cream: str = '#F5F0E8'
    light_grey: str = '#D4CFC7'
    mid_grey: str = '#9B9690'
    panel: str = '#1C1C2E'
    panel2: str = '#161625'
    green: str = '#5CB85C'
    amber: str = '#F59E0B'
    purple: str = '#8B5CF6'
    dark_green_bg: str = '#0D2B0D'
    dark_amber_bg: str = '#2B1A00'
    code_bg: str = '#0A0A15'
    white: str = '#FFFFFF'

    def c(self, key: str):
        """Colour by attribute name, as a reportlab colour."""
        return HexColor(getattr(self, key))


CLAUDE = Theme(
    name='claude',
    series='CLAUDE AI FIELD GUIDE SERIES',
    bg='#0F0F1A',
    accent='#E07A38',
    accent_light='#F5A66B',
    accent_dark='#C86820',
    accent_darker='#B85C18',
)

COPILOT = Theme(
    name='copilot',
    series='COPILOT FIELD GUIDE SERIES',
    bg='#0D1117',
    accent='#58A6FF',
    accent_light='#8CC5FF',
    accent_dark='#2F6FB8',
    accent_darker='#1F4E85',
    # Panels tuned to the cooler background so they do not read as a colour clash.
    panel='#161B22',
    panel2='#11161C',
    code_bg='#070A0E',
)

CODEX = Theme(
    name='codex',
    series='CODEX FIELD GUIDE SERIES',
    bg='#0B0F0E',
    accent='#10A37F',
    accent_light='#4FD1AC',
    accent_dark='#0B7A5E',
    accent_darker='#075C46',
    panel='#141A18',
    panel2='#0F1413',
    code_bg='#060908',
)

GPT = Theme(
    name='gpt',
    series='CHATGPT FIELD GUIDE SERIES',
    bg='#0F0F1A',
    # CODEX already owns teal-green (#10A37F) across four live products. A second
    # near-identical green would make the two OpenAI-adjacent series indistinguishable
    # on a shelf, so GPT takes a violet accent instead — distinct in hue from Claude's
    # orange, Copilot's blue and Codex's green, and bright enough to read on the dark
    # #0F0F1A interior. accent_dark/accent_darker follow the same darkening relationship
    # the other three themes use for decorative circles and the badge background.
    accent='#B45CFF',
    accent_light='#D9A3FF',
    accent_dark='#7A2EBF',
    accent_darker='#5C1F94',
)

THEMES = {t.name: t for t in (CLAUDE, COPILOT, CODEX, GPT)}
