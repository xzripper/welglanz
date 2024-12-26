"""WGZ Constants."""

from .wgzdcs import *

from sty import fg, bg, ef, Style

from typing import Callable


# Aliases.
WgzValidator = Callable[[str], bool]
WgzInterruptionCallback = Callable[[str], None]
WgzSpinnerTarget = Callable[[WgzStopSignal, WgzData], None]
WgzProgressBarTarget = Callable[[WgzPBValueLink], None]

# Shortcuts for STY (https://github.com/feluxe/sty).
WgzStyFg = fg
WgzStyBg = bg
WgzStyEf = ef

WgzStyReset = fg.rs + bg.rs + ef.rs

WgzStyle = Style

# WGZ Default password masks.
WGZ_PASSWORD_ASTERISK: WgzPassword = wgz_new_password('*')
WGZ_PASSWORD_CIRCLE: WgzPassword = wgz_new_password('●')
WGZ_PASSWORD_SQUARE: WgzPassword = wgz_new_password('▪')
WGZ_PASSWORD_HASH: WgzPassword = wgz_new_password('#')
WGZ_PASSWORD_DOT: WgzPassword = wgz_new_password('.')
WGZ_PASSWORD_QUESTION: WgzPassword = wgz_new_password('?')

WGZ_PASSWORD_NONE: WgzPassword = WgzPassword(False, None)

# WGZ Default selectable icons.
WGZ_SELECTABLE_ICON_CIRCLE: WgzSelectableIcon = wgz_new_selectable_icon('○', '●')
WGZ_SELECTABLE_ICON_DIAMOND: WgzSelectableIcon = wgz_new_selectable_icon('◇', '◆')
WGZ_SELECTABLE_ICON_STAR: WgzSelectableIcon = wgz_new_selectable_icon('☆', '★')
WGZ_SELECTABLE_ICON_ARROW: WgzSelectableIcon = wgz_new_selectable_icon(' ', '➔')

# WGZ Default confirm text.
WGZ_CONFIRM_TEXT_YES_NO: WgzConfirmText = wgz_new_confirm_text('Yes', 'No')

# WGZ Confirm dialog focus constants.
WGZ_CONFIRM_FOCUS_YES: int = 1
WGZ_CONFIRM_FOCUS_NO: int = 0

# WGZ Default spinner icons.
WGZ_SPINNER_ICON_CIRCLE: WgzSpinnerIcon = wgz_new_spinner_icon('circle', '◒', '◐', '◓', '◑')
WGZ_SPINNER_ICON_CIRCLE_QUADRANT: WgzSpinnerIcon = wgz_new_spinner_icon('circle_q', '◵', '◴', '◷', '◶')
WGZ_SPINNER_ICON_SQUARE_QUADRANT: WgzSpinnerIcon = wgz_new_spinner_icon('square_q', '◱', '◰', '◳', '◲')
WGZ_SPINNER_ICON_NOISE: WgzSpinnerIcon = wgz_new_spinner_icon('noise', '▓', '▒', '░')
WGZ_SPINNER_ICON_CIRCLE_BOUNCE: WgzSpinnerIcon = wgz_new_spinner_icon('circle_bounce', '⠁', '⠂', '⠄', '⠂')
WGZ_SPINNER_ICON_SQUARE_BOUNCE: WgzSpinnerIcon = wgz_new_spinner_icon('square_bounce', '▖', '▘', '▝', '▗')
WGZ_SPINNER_ICON_TRIANGLE: WgzSpinnerIcon = wgz_new_spinner_icon('triangle', '◢', '◣', '◤', '◥')
WGZ_SPINNER_ICON_TRIANGLE_HALF: WgzSpinnerIcon = wgz_new_spinner_icon('triangle_half', '◭', '◮')
WGZ_SPINNER_ICON_SWITCH: WgzSpinnerIcon = wgz_new_spinner_icon('switch', '⊷', '⊶')
WGZ_SPINNER_ICON_BOUNCING_BALL: WgzSpinnerIcon = wgz_new_spinner_icon('bouncing_ball', '( ●    )', '(  ●   )', '(   ●  )', '(    ● )', '(     ●)', '(    ● )', '(   ●  )', '(  ●   )', '( ●    )', '(●     )')
WGZ_SPINNER_ICON_ARC: WgzSpinnerIcon = wgz_new_spinner_icon('arc', '◜', '◠', '◝', '◞', '◡', '◟')
WGZ_SPINNER_ICON_FALLING_SAND: WgzSpinnerIcon = wgz_new_spinner_icon('falling_sand', '⠁', '⠂', '⠄', '⡀', '⡈', '⡐', '⡠', '⣀', '⣁', '⣂', '⣄', '⣌', '⣔', '⣤', '⣥', '⣦', '⣮', '⣶', '⣷', '⣿', '⡿', '⠿', '⢟', '⠟', '⡛', '⠛', '⠫', '⢋', '⠋', '⠍', '⡉', '⠉', '⠑', '⠡', '⢁')
WGZ_SPINNER_ICON_DOTS: WgzSpinnerIcon = wgz_new_spinner_icon('dots', '⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏')
WGZ_SPINNER_ICON_SPINNING_DOTS: WgzSpinnerIcon = wgz_new_spinner_icon('spinning_dots', '⢎⡰', '⢎⡡', '⢎⡑', '⢎⠱', '⠎⡱', '⢊⡱', '⢌⡱', '⢆⡱')
WGZ_SPINNER_ICON_ARROWS: WgzSpinnerIcon = wgz_new_spinner_icon('arrows', '←', '↑', '→', '↓')
WGZ_SPINNER_ICON_STAIRS: WgzSpinnerIcon = wgz_new_spinner_icon('stairs', '▁', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃')
WGZ_SPINNER_ICON_VERTICAL_BAR_WAVE: WgzSpinnerIcon = wgz_new_spinner_icon('vertical_bar_wave', '▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉')
WGZ_SPINNER_ICON_DIAMOND: WgzSpinnerIcon = wgz_new_spinner_icon('diamond', '◇', '◈', '◆')
WGZ_SPINNER_ICON_CLASSIC: WgzSpinnerIcon = wgz_new_spinner_icon('classic', '|', '/', '-', '\\')

# WGZ Default spinner render interval.
WGZ_DEFAULT_SPINNER_RENDER_INTERVAL: float = .01

# WGZ Default spinner icon after processes are finished.
WGZ_DEFAULT_SPINNER_ICON_ON_FINISH: str = '★'
