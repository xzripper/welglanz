"""WGZ Colors."""

from . import WgzInvalidParameterError

from sty import fg, bg, Style


# Valid RGB range.
_VALID_RGB_RANGE = range(0, 256)

# Is RGB in its range?
def wgz_valid_rgb(r: int, g: int, b: int) -> bool:
    """Is RGB in its range?"""
    return r in _VALID_RGB_RANGE and g in _VALID_RGB_RANGE and b in _VALID_RGB_RANGE

# WGZ Custom RGB Fore.
def wgz_fore(r: int, g: int, b: int) -> Style:
    """Create a new foreground color."""
    if not wgz_valid_rgb(r, g, b):
        raise WgzInvalidParameterError('Invalid Foreground RGB range.')

    return fg(r, g, b)

# WGZ Custom RGB Back.
def wgz_back(r: int, g: int, b: int) -> Style:
    """Create a new background color."""
    if not wgz_valid_rgb(r, g, b):
        raise WgzInvalidParameterError('Invalid Background RGB range.')

    return bg(r, g, b)

# Welglanz Foreground Colors.
FERRARI_RED_FORE: Style = wgz_fore(250, 15, 15)
ORANGEY_RED_FORE: Style = wgz_fore(250, 60, 40)
LIGHT_RED_FORE: Style = wgz_fore(255, 75, 75)
BITTERSWEET_FORE: Style = wgz_fore(255, 110, 110)
PORTLAND_ORANGE_FORE: Style = wgz_fore(255, 90, 50)

SUPERNOVA_FORE: Style = wgz_fore(255, 200, 0)
GOLDEN_FIZZ_FORE: Style = wgz_fore(230, 255, 50)

LIGHT_BRIGHT_GREEN_FORE: Style = wgz_fore(50, 205, 50)

AQUAMARINE_FORE: Style = wgz_fore(100, 255, 220)

FOLLY_FORE: Style = wgz_fore(255, 0, 90)
DEEP_PINK_FORE: Style = wgz_fore(255, 20, 150)
NEON_FUCHSIA_FORE: Style = wgz_fore(255, 80, 180)
LIGHT_FUCHSIA_PINK_FORE: Style = wgz_fore(255, 128, 220)
ARTY_CLICK_MAGENTA_FORE: Style = wgz_fore(255, 0, 255)

CHARCOAL_GRAY_FORE: Style = wgz_fore(64, 64, 64)
ASH_GRAY_FORE: Style = wgz_fore(186, 186, 186)
DESERT_STOM_FORE: Style = wgz_fore(232, 232, 232)
WHITE_FORE: Style = wgz_fore(255, 255, 255)
