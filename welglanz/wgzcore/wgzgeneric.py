"""WGZ Generic."""

from welglanz.wgzcore.wgztheme import (
    WgzStyFg, WgzStyBg, WgzStyEf,
    Style, R, wgz_fore, wgz_back, wgz_valid_rgb, wgzstfm
)

from typing import Literal, Union


# WST Exceptions.
class WgzWstInvalidSyntaxError(Exception):
    """WGZ-WST Invalid Syntax Error."""
    def __init__(self, message: str) -> None:
        """New WGZWSTISE error."""
        super().__init__(message)

class WgzWstInvalidFormulationError(Exception):
    """WGZ-WST Invalid Formulation Error."""
    def __init__(self, message: str) -> None:
        """New WGZWSTIFE error."""
        super().__init__(message)

# WGZ Tags & Syntax Constants.
_WGZWST_CF, _WGZWST_CB = 'CF', 'CB'
_WGZWST_FORE, _WGZWST_BACK = 'F', 'B'
_WGZWST_EFF = 'E'
_WGZWST_RESET = 'R'

_WGZWST_SYNT_START, _WGZWST_SYNT_END = '[', ']'

_WGZWST_SYNT_SEP = ':'

# WGZ-WST Defined effects.
_WGZWST_EFFECTS = {
    'bold': WgzStyEf.bold, 'b': WgzStyEf.b,
    'dim': WgzStyEf.dim, 'd': WgzStyEf.dim,
    'italic': WgzStyEf.italic, 'i': WgzStyEf.i,
    'underline': WgzStyEf.underl, 'u': WgzStyEf.u,
    'strike': WgzStyEf.strike, 's': WgzStyEf.strike,
    'inverse': WgzStyEf.inverse, 'hidden': WgzStyEf.hidden
}

# Construct a parameterless syntax tag.
def _wgzwst_constr_synt_tag(tag_str: str) -> str:
    return f'[{tag_str}]'

# Construct a syntax tag with parameters.
def _wgzwst_constr_synt_tag_p(tag_str: str) -> str:
    return f'[{tag_str}' + _WGZWST_SYNT_SEP

# Check for a tag.
def _wgzwst_strtag(string: str, tag: str, params: bool=True) -> bool:
    return string.startswith(
        _wgzwst_constr_synt_tag_p(tag) if params \
              else _wgzwst_constr_synt_tag(tag))

# Remove brackets and a tag in a string element.
def _wgzwst_rmtag(string: str, tag: str) -> str:
    return string \
        .replace(_WGZWST_SYNT_START, '') \
        .replace(_WGZWST_SYNT_END, '') \
        .replace(tag + _WGZWST_SYNT_SEP, '')

# Process raw RGB color.
def _wgzwst_proc_raw_rgbc(raw_rgbc: list[str]) -> Union[tuple[int], None]:
    if len(raw_rgbc) != 3:
        raise WgzWstInvalidSyntaxError('Expected three colors of RGB color model.')

    if not all([_color.isdigit() for _color in raw_rgbc]):
        raise WgzWstInvalidSyntaxError('Expected numbers in RGB-Fore tag.')

    i_rgbc = [int(_color) for _color in raw_rgbc]

    if not wgz_valid_rgb(*i_rgbc):
        raise WgzWstInvalidFormulationError('Expected RGB to be in its 0-255 range.')

    return i_rgbc

# Process raw Fore/Back color.
def _wgzwst_proc_raw_fbc(raw_fbc: list[str], type_: Literal[0, 1]) -> Union[Style, None]:
    _c_str = 'Fore' if type_ else 'Back'
    _c_obj = WgzStyFg if type_ else WgzStyBg

    if len(raw_fbc) != 1 or not raw_fbc[0]:
        raise WgzWstInvalidSyntaxError(f'Expected single color name in {_c_str} tag.')

    if type(_color := getattr(_c_obj, raw_fbc[0].lower(), None)) != Style:
        raise WgzWstInvalidFormulationError(f'Invalid {_c_str} color.')

    return _color

# Welglanz Styled Text.
def wgzwst(wst: str) -> str:
    """Format a string using the WST format."""
    styled_text = wst

    tags = []

    _wst_start = 0

    for cpos, char in enumerate(styled_text):
        if char == _WGZWST_SYNT_START:
            _wst_start = cpos

        elif char == _WGZWST_SYNT_END:
            tags.append(styled_text[_wst_start:cpos+1])

    for tag in tags:
        if _wgzwst_strtag(tag, _WGZWST_CF):
            _cf_rgb = _wgzwst_rmtag(tag, _WGZWST_CF).split(_WGZWST_SYNT_SEP)

            _proc_rgbc = _wgzwst_proc_raw_rgbc(_cf_rgb)

            styled_text = styled_text.replace(tag, wgz_fore(*_proc_rgbc))

        elif _wgzwst_strtag(tag, _WGZWST_CB):
            _cb_rgb = _wgzwst_rmtag(tag, _WGZWST_CB).split(_WGZWST_SYNT_SEP)

            _proc_rgbc = _wgzwst_proc_raw_rgbc(_cb_rgb)

            styled_text = styled_text.replace(tag, wgz_back(*_proc_rgbc))

        elif _wgzwst_strtag(tag, _WGZWST_FORE):
            _fore_color = _wgzwst_rmtag(tag, _WGZWST_FORE).split(_WGZWST_SYNT_SEP)

            styled_text = styled_text.replace(tag, _wgzwst_proc_raw_fbc(_fore_color, 1))

        elif _wgzwst_strtag(tag, _WGZWST_BACK):
            _back_color = _wgzwst_rmtag(tag, _WGZWST_BACK).split(_WGZWST_SYNT_SEP)

            styled_text = styled_text.replace(tag, _wgzwst_proc_raw_fbc(_back_color, 0))

        elif _wgzwst_strtag(tag, _WGZWST_EFF):
            _effect = _wgzwst_rmtag(tag, _WGZWST_EFF).split(_WGZWST_SYNT_SEP)

            if len(_effect) != 1 or not _effect[0]:
                raise WgzWstInvalidSyntaxError('Expected effect name in Effect tag.')

            _effect = _effect[0].lower()

            if _effect not in _WGZWST_EFFECTS:
                raise WgzWstInvalidFormulationError('Non-existent effect.')

            styled_text = styled_text.replace(tag, _WGZWST_EFFECTS[_effect])

    styled_text = styled_text.replace(_wgzwst_constr_synt_tag(_WGZWST_RESET), R)

    return styled_text

# Apply a style for a key.
def wgzwstkey(key: str) -> str:
    """Apply a style for a key."""
    return wgzstfm(f'[{key.upper()}]', wgz_fore(200, 200, 200), wgz_back(64, 64, 64), WgzStyEf.bold)
