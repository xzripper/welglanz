"""WGZ Theme."""

from .wgzconsts import WgzStyFg, WgzStyBg, WgzStyEf, WgzStyReset, WgzStyle

from .wgzcolors import *

from dataclasses import dataclass

from typing import Union


# WGZ dataclasses, shared setup & utilities.
@dataclass
class WgzTheme:
    """WGZ Shared theme dataclass."""

    regular_text_fg: WgzStyle = WgzStyFg.white
    regular_text_bg: WgzStyle = None
    regular_text_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    placeholder_text_fg: WgzStyle = WgzStyFg.white
    placeholder_text_bg: WgzStyle = None
    placeholder_text_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    mask_text_fg: WgzStyle = WgzStyFg.red
    mask_text_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_icon_default_fg: WgzStyle = WgzStyFg.white

    selectable_icon_highlighted_fg: WgzStyle = AQUA_GREEN_FG

    selectable_hint_fg: WgzStyle = WgzStyFg.grey
    selectable_hint_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_default_fg: WgzStyle = WgzStyFg.grey
    selectable_default_bg: WgzStyle = None
    selectable_default_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    selectable_highlighted_fg: WgzStyle = WgzStyFg.white
    selectable_highlighted_bg: WgzStyle = None
    selectable_highlighted_ef: tuple[WgzStyle] = (WgzStyEf.bold, )

    multiselect_icon_not_highlighted_not_selected_fg: WgzStyle = WgzStyFg.white
    multiselect_icon_not_highlighted_selected_fg: WgzStyle = AQUA_GREEN_FG

    multiselect_icon_highlighted_not_selected_fg: WgzStyle = AQUA_GREEN_DARKER_FG
    multiselect_icon_highlighted_selected_fg: WgzStyle = AQUA_GREEN_LIGHTER_FG

    confirm_icon_default_fg: WgzStyle = WgzStyFg.white

    confirm_icon_selected_fg: WgzStyle = AQUA_GREEN_FG

    confirm_default_fg: WgzStyle = WgzStyFg.grey
    confirm_default_bg: WgzStyle = None
    confirm_default_ef: WgzStyle = (WgzStyEf.bold, )

    confirm_selected_fg: WgzStyle = WgzStyFg.white
    confirm_selected_bg: WgzStyle = None
    confirm_selected_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_icon_working_fg: WgzStyle = ROYAL_PURPLE_FG

    spinner_icon_finished_fg: WgzStyle = GOLDEN_GLIMMER_FG

    spinner_text_fg: WgzStyle = WgzStyFg.white
    spinner_text_bg: WgzStyle = None
    spinner_text_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_text_finished_fg: WgzStyle = WgzStyFg.white
    spinner_text_finished_bg: WgzStyle = None
    spinner_text_finished_ef: WgzStyle = (WgzStyEf.bold, )

    spinner_text_canceled_fg: WgzStyle = WgzStyFg.white
    spinner_text_canceled_bg: WgzStyle = None
    spinner_text_canceled_ef: WgzStyle = (WgzStyEf.bold, )

WgzSharedTheme = WgzTheme()

def wgzstget(style: WgzStyle) -> Union[WgzStyle, str]:
    """Get shared theme style if specified."""
    return (''.join([style_ for style_ in style if style_]) if type(style) in (tuple, list) else (style or ''))

def wgzstcmb(*styles: WgzStyle) -> str:
    """Combine shared theme styles and check each for specification."""
    return ''.join([wgzstget(style) for style in styles])
