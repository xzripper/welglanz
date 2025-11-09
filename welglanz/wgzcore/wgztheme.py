"""WGZ Theme."""

from .wgzconsts import WgzStyle, WgzStyFg, WgzStyBg, WgzStyEf, WgzStyReset

from .wgzcolors import *

from dataclasses import dataclass

from typing import Union


# Shortcut for Style Reset.
R = WgzStyReset
"""Shortcut for Style Reset."""

# WGZ dataclasses, shared setup & utilities.
@dataclass
class WgzTheme:
    """WGZ Shared theme dataclass."""

    icon_text_padding: int = 2

    regular_text_fg: WgzStyle = WgzStyFg.white
    regular_text_bg: WgzStyle = None

    placeholder_prompt_question_mark_fg: WgzStyle = GOLDEN_FIZZ_FORE
    placeholder_prompt_question_mark_bg: WgzStyle = None
    placeholder_prompt_question_mark_ef: WgzStyle = (WgzStyEf.bold, WgzStyEf.underl)

    placeholder_text_fg: WgzStyle = BITTERSWEET_FORE
    placeholder_text_bg: WgzStyle = None
    placeholder_text_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    mask_text_fg: WgzStyle = DESERT_STOM_FORE
    mask_text_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_icon_default_fg: WgzStyle = LIGHT_FUCHSIA_PINK_FORE

    selectable_icon_highlighted_fg: WgzStyle = DEEP_PINK_FORE

    selectable_hint_fg: WgzStyle = CHARCOAL_GRAY_FORE
    selectable_hint_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_default_fg: WgzStyle = ASH_GRAY_FORE
    selectable_default_bg: WgzStyle = None
    selectable_default_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_highlighted_fg: WgzStyle = WHITE_FORE
    selectable_highlighted_bg: WgzStyle = None
    selectable_highlighted_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    multiselect_icon_not_highlighted_not_selected_fg: WgzStyle = WHITE_FORE
    multiselect_icon_not_highlighted_selected_fg: WgzStyle = DEEP_PINK_FORE

    multiselect_icon_highlighted_not_selected_fg: WgzStyle = NEON_FUCHSIA_FORE
    multiselect_icon_highlighted_selected_fg: WgzStyle = ARTY_CLICK_MAGENTA_FORE

    select_dialog_title_fg: WgzStyle = WHITE_FORE
    select_dialog_title_bg: WgzStyle = None
    select_dialog_title_ef: WgzStyle = (WgzStyEf.bold, )

    select_dialog_post_title_fg: WgzStyle = PORTLAND_ORANGE_FORE
    select_dialog_post_title_bg: WgzStyle = None
    select_dialog_post_title_ef: WgzStyle = (WgzStyEf.bold, )

    confirm_icon_default_fg: WgzStyle = WHITE_FORE

    confirm_icon_selected_fg: WgzStyle = DEEP_PINK_FORE

    confirm_placeholder_fg: WgzStyle = PORTLAND_ORANGE_FORE
    confirm_placeholder_bg: WgzStyle = None
    confirm_placeholder_ef: WgzStyle = (WgzStyEf.bold, )

    confirm_default_fg: WgzStyle = ASH_GRAY_FORE
    confirm_default_bg: WgzStyle = None
    confirm_default_ef: WgzStyle = (WgzStyEf.bold, )

    confirm_selected_fg: WgzStyle = WHITE_FORE
    confirm_selected_bg: WgzStyle = None
    confirm_selected_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_icon_working_color: WgzStyle = FOLLY_FORE

    spinner_icon_finished_color: WgzStyle = SUPERNOVA_FORE

    spinner_icon_interrupted_color: WgzStyle = FERRARI_RED_FORE

    spinner_text_fg: WgzStyle = WHITE_FORE
    spinner_text_bg: WgzStyle = None
    spinner_text_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_text_finished_fg: WgzStyle = WHITE_FORE
    spinner_text_finished_bg: WgzStyle = None
    spinner_text_finished_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_text_interrupted_fg: WgzStyle = WHITE_FORE
    spinner_text_interrupted_bg: WgzStyle = None
    spinner_text_interrupted_ef: WgzStyle = (WgzStyEf.bold, )

    pb_text_fg: WgzStyle = PORTLAND_ORANGE_FORE
    pb_text_bg: WgzStyle = None
    pb_text_ef: WgzStyle = (WgzStyEf.bold, )

    pb_text_finished_fg: WgzStyle = ORANGEY_RED_FORE
    pb_text_finished_bg: WgzStyle = None
    pb_text_finished_ef: WgzStyle = (WgzStyEf.bold, )

    pb_text_interrupted_fg: WgzStyle = FERRARI_RED_FORE
    pb_text_interrupted_bg: WgzStyle = None
    pb_text_interrupted_ef: WgzStyle = (WgzStyEf.bold, )

    pb_status_fg: WgzStyle = LIGHT_BRIGHT_GREEN_FORE
    pb_status_bg: WgzStyle = None
    pb_status_ef: WgzStyle = (WgzStyEf.bold, )

    pb_time_fg: WgzStyle = AQUAMARINE_FORE
    pb_time_bg: WgzStyle = None
    pb_time_ef: WgzStyle = (WgzStyEf.bold, )

    pb_loaded_segment_color: WgzStyle = LIGHT_RED_FORE
    pb_not_loaded_segment_color: WgzStyle = CHARCOAL_GRAY_FORE

    wait_fg: WgzStyle = WgzStyFg.white
    wait_bg: WgzStyle = None
    wait_ef: WgzStyle = (WgzStyEf.bold, )

    @property
    def _adj_padding_BINT(self) -> str:
        """Get adjusted space by config preferences between icon and text."""
        return ' ' * self.icon_text_padding

# WGZ Shared Theme.
WgzSharedTheme = WgzTheme()

# Get WGZ style.
def wgzstget(style: WgzStyle) -> Union[WgzStyle, str]:
    """Get shared theme style if specified."""
    return (''.join([style_ for style_ in style if style_]) if type(style) in (tuple, list) else (style or ''))

# Combine WGZ style(s).
def wgzstcmb(*styles: WgzStyle) -> str:
    """Combine shared theme styles and check each for specification."""
    return ''.join([wgzstget(style) for style in styles])

# Format string with a style.
def wgzstfm(text: str, *styles: WgzStyle, reset: bool=True) -> str:
    """Shortcut for formatting string with a style."""
    return f'{wgzstcmb(styles)}{text}{R if reset else ""}'
