"""Welglänz is a very simple, compact and thorough CLI UX for Python 3."""

# Imports.
from welglanz.wgzcore.wgzrenderer.wgzgeneric import wgzwst_print, wgz_wait

from welglanz.wgzcore.wgzrenderer.wgzpb import wgz_progress_bar

from welglanz.wgzcore.wgzrenderer.wgzprompt import wgz_prompt, wgz_password

from welglanz.wgzcore.wgzrenderer.wgzselectable import wgz_select, wgz_multiselect, wgz_confirm

from welglanz.wgzcore.wgzrenderer.wgzspinner import wgz_spinner

from welglanz.wgzcore.wgzgeneric import wgzwst, wgzwstkey

from welglanz.wgzcore.wgzcolors import wgz_fore, wgz_back, wgz_valid_rgb

from welglanz.wgzcore.wgzconsts import (
    WGZ_PROMPT_FILTER_ONLY_LETTERS,
    WGZ_PROMPT_FILTER_ONLY_LETTERS_AND_SPACES,
    WGZ_PROMPT_FILTER_ONLY_SINGLE_CHAR,
    WGZ_PROMPT_FILTER_ONLY_SYMBOLS,
    WGZ_PROMPT_FILTER_ONLY_NUMBERS,

    WGZ_PASSWORD_ASTERISK,
    WGZ_PASSWORD_CIRCLE,
    WGZ_PASSWORD_SQUARE,
    WGZ_PASSWORD_HASH,
    WGZ_PASSWORD_DOT,
    WGZ_PASSWORD_QUESTION,

    WGZ_SELECTABLE_ICON_CIRCLE,
    WGZ_SELECTABLE_ICON_DIAMOND,
    WGZ_SELECTABLE_ICON_STAR,
    WGZ_SELECTABLE_ICON_ARROW,
    WGZ_SELECTABLE_ICON_ARROW_EMPTY,
    WGZ_SELECTABLE_ICON_ARROWHEAD,
    WGZ_SELECTABLE_ICON_ARROW_3D,
    WGZ_SELECTABLE_ICON_CHECKS,
    WGZ_SELECTABLE_ICON_SPARKLE_EMPTY,
    WGZ_SELECTABLE_ICON_PARALLELOGRAM,

    WGZ_CONFIRM_FOCUS_YES,
    WGZ_CONFIRM_FOCUS_NO,

    WGZ_CONFIRM_SEPARATOR_SLASH,
    WGZ_CONFIRM_SEPARATOR_BSLASH,
    WGZ_CONFIRM_SEPARATOR_VERTICAL_BAR,
    WGZ_CONFIRM_SEPARATOR_ANGLE_BRACKETS,
    WGZ_CONFIRM_SEPARATOR_AMPERSAND,
    WGZ_CONFIRM_SEPARATOR_OR,
    WGZ_CONFIRM_SEPARATOR_OR_SMALL,

    WGZ_SPINNER_ICON_CIRCLE,
    WGZ_SPINNER_ICON_CIRCLE_QUADRANT,
    WGZ_SPINNER_ICON_SQUARE_QUADRANT,
    WGZ_SPINNER_ICON_NOISE,
    WGZ_SPINNER_ICON_CIRCLE_BOUNCE,
    WGZ_SPINNER_ICON_SQUARE_BOUNCE,
    WGZ_SPINNER_ICON_TRIANGLE,
    WGZ_SPINNER_ICON_TRIANGLE_HALF,
    WGZ_SPINNER_ICON_SWITCH,
    WGZ_SPINNER_ICON_BOUNCING_BALL,
    WGZ_SPINNER_ICON_LOADING_ARC,
    WGZ_SPINNER_ICON_FALLING_SAND,
    WGZ_SPINNER_ICON_DOTS,
    WGZ_SPINNER_ICON_SPINNING_DOTS,
    WGZ_SPINNER_ICON_ARROWS,
    WGZ_SPINNER_ICON_STAIRS,
    WGZ_SPINNER_ICON_VERTICAL_BAR_WAVE,
    WGZ_SPINNER_ICON_DIAMOND,
    WGZ_SPINNER_ICON_CLASSIC,

    WGZ_SPINNER_FINISHED_ICON_CHECKMARK,
    WGZ_SPINNER_FINISHED_ICON_STAR,
    WGZ_SPINNER_FINISHED_ICON_SPARKLE,
    WGZ_SPINNER_FINISHED_ICON_EXCLAMATION_MARK_ROUNDED,

    WGZ_SPINNER_INTERRUPTED_ICON_BALLOT,
    WGZ_SPINNER_INTERRUPTED_ICON_EXCLAMATION_MARK,
    WGZ_SPINNER_INTERRUPTED_ICON_DOUBLE_EXCLAMATION_MARK,
    WGZ_SPINNER_INTERRUPTED_ICON_EXCLAMATION_MARK_ROUNDED,
    WGZ_SPINNER_INTERRUPTED_ICON_SLASH,
    WGZ_SPINNER_INTERRUPTED_ICON_CDS,

    WGZ_PB_LINE_THIN,
    WGZ_PB_LINE_MEDIUM,
    WGZ_PB_LINE_HEAVY
)

from welglanz.wgzcore.wgzdcs import (
    WgzPassword, wgz_new_password,
    WgzSelectableIcon, wgz_new_selectable_icon,
    WgzConfirmText, wgz_new_confirm_text,
    WgzSpinnerIcon, wgz_new_spinner_icon,

    WgzSelectable, WgzProgressBarData,

    WgzData, WgzInterruptionSignal
)

from welglanz.wgzcore.wgztheme import WgzTheme, WgzSharedTheme, R, wgzstfm

from welglanz.wgzdemo import wgz_show_demo


# Welglanz Version.
WELGLANZ_VERSION: str = '1.0.0'
"""Welglanz Version."""
