"""Shared engine for the Field Guide series — Claude, Copilot, Codex.

    from fieldguide import COPILOT, Painter, MX, CW, H

Scope note: the 23 shipped Claude guide scripts are deliberately NOT retrofitted onto
this. They are correct, audited and selling; rewriting them would risk live products to
buy nothing. This exists so the Copilot and Codex series do not become a third
copy-paste of the design system.
"""
from .draw import CW, FOOTER_H, H, HEADER_H, MX, Painter, W, wrap
from .theme import CLAUDE, CODEX, COPILOT, THEMES, Theme

__all__ = ['Painter', 'Theme', 'THEMES', 'CLAUDE', 'COPILOT', 'CODEX',
           'W', 'H', 'MX', 'CW', 'FOOTER_H', 'HEADER_H', 'wrap']
