"""WGZ Colors."""

from sty import fg, bg, Style


def wgz_fore(r: int, b: int, g: int) -> Style:
    """Create a new foreground color."""
    return fg(r, g, b)

def wgz_back(r: int, b: int, g: int) -> Style:
    """Create a new background color."""
    return bg(r, g, b)

AQUA_GREEN_FG: Style = fg(20, 225, 145)
AQUA_GREEN_LIGHTER_FG: Style = fg(30, 250, 190)
AQUA_GREEN_DARKER_FG: Style = fg(10, 180, 100)
ROYAL_PURPLE_FG: Style = fg(120, 55, 230)
MIDNIGHT_BLUE_FG: Style = fg(30, 60, 150)
GOLDEN_GLIMMER_FG: Style = fg(240, 190, 50)
SILVER_SHEEN_FG: Style = fg(200, 200, 210)
