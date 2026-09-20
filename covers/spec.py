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
