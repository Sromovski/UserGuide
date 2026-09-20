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
        grad=((250, 247, 255), (240, 233, 252), (224, 210, 246)),
        title=(26, 18, 40), muted=(110, 92, 140),
        spine_back_left=(45, 32, 66), spine_front=(180, 92, 255),
        spine_back_right=(28, 18, 44),
        badge_bg=(26, 18, 40), badge_fg=(255, 255, 255),
        shadow=(60, 30, 90)),
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
