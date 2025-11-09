"""WGZ Prompts."""

from .. import WgzInvalidParameterError, _wgz_crossplatform_const

from ..wgzdcs import WgzPassword, WgzPromptReturn

from ..wgzconsts import (
    WgzPromptFilter,

    WGZ_PROMPT_FILTER_ONLY_LETTERS, WGZ_PROMPT_FILTER_ONLY_LETTERS_AND_SPACES,
    WGZ_PROMPT_FILTER_ONLY_SINGLE_CHAR, WGZ_PROMPT_FILTER_ONLY_SYMBOLS,
    WGZ_PROMPT_FILTER_ONLY_NUMBERS,

    WgzValidator,

    WgzInterruptionCallback,

    WGZ_PASSWORD_NONE, WGZ_PASSWORD_SQUARE
)

from ..wgztheme import WgzSharedTheme, WgzStyReset, wgzstcmb, wgzstfm

from .._wgzkpm import _wgz_pkm_readkey

from ..wgztlm import wgztlm_move_cursor_right, wgztlm_move_cursor_left, wgztlm_refresh

from readchar import key

from string import punctuation

from typing import Union

# Key constants.
_KEY_CTRL_RIGHT = _wgz_crossplatform_const('\x00t', '\x1b[1;5C')
_KEY_CTRL_LEFT = _wgz_crossplatform_const('\x00s', '\x1b[1;5D')
_KEY_CTRL_BACKSPACE = _wgz_crossplatform_const('\x7f', '\x08')

# NOPW Flags.
_WGZ_FIND_NEXT_WORD = 0
_WGZ_FIND_PREVIOUS_WORD = 1

# Find a next or previous word index.
def _wgz_nop_word_idx(cursor_pos: int, uinp: str, word_flag: int) -> Union[int, None]:
    _slice = None

    if word_flag == _WGZ_FIND_NEXT_WORD:
        _slice = slice(cursor_pos, None)

    elif word_flag == _WGZ_FIND_PREVIOUS_WORD:
        _slice = slice(0, cursor_pos)

    else:
        return None

    _input_slice = uinp[_slice]

    if word_flag == _WGZ_FIND_NEXT_WORD:
        _next_space = _input_slice.find(' ')

        if _next_space == -1:
            return len(uinp) - cursor_pos

        _nonspace_after = next(
            (idx for idx, char in enumerate(_input_slice[_next_space:], _next_space) if not char.isspace()),

            len(_input_slice)
        )

        return _nonspace_after

    elif word_flag == _WGZ_FIND_PREVIOUS_WORD:
        _rev_slice = _input_slice.rstrip()

        if not _rev_slice:
            return 0

        _last_space = _rev_slice.rstrip().rfind(' ')

        if _last_space == -1:
            return -cursor_pos

        while _last_space > 0 and _rev_slice[_last_space - 1].isspace():
            _last_space -= 1

        return _last_space - cursor_pos

# WGZ Raw Input.
def _wgz_raw_input(
        placeholder: str,
        default_text: str=None,
        mask: WgzPassword=WGZ_PASSWORD_NONE,
        filter: WgzPromptFilter=None,
        validator: WgzValidator=None) -> WgzPromptReturn:
    if filter not in (None, 1, 2, 3, 4, 5):
        raise WgzInvalidParameterError('Invalid WGZ-Prompt Filter.')

    if mask and type(mask) != WgzPassword:
        raise WgzInvalidParameterError('Invalid password mask.')

    uinp = '' if not default_text or filter == WGZ_PROMPT_FILTER_ONLY_SINGLE_CHAR \
        else default_text

    _wgzst_text = wgzstcmb(
        WgzSharedTheme.regular_text_fg,
        WgzSharedTheme.regular_text_bg)

    _wgzst_mask = wgzstcmb(
        WgzSharedTheme.mask_text_fg,
        WgzSharedTheme.mask_text_ef)

    _wgzst_qm = wgzstcmb(
        WgzSharedTheme.placeholder_prompt_question_mark_fg,
        WgzSharedTheme.placeholder_prompt_question_mark_bg,
        WgzSharedTheme.placeholder_prompt_question_mark_ef)

    print(f'{_wgzst_qm}?{WgzStyReset} ', end='', flush=True)

    if placeholder:
        _wgzst_placeholder = wgzstcmb(WgzSharedTheme.placeholder_text_fg,
                                      WgzSharedTheme.placeholder_text_bg,
                                      WgzSharedTheme.placeholder_text_ef)

        print(wgzstfm(placeholder + ' ', _wgzst_placeholder), end='', flush=True)

    if mask.password and uinp:
        print(_wgzst_mask + mask.mask, end='', flush=True)

    else:
        print(_wgzst_text + uinp, end='', flush=True)

    cursor_pos = len(uinp)

    while 1:
        try:
            ikey = _wgz_pkm_readkey()

            if ikey == key.ENTER:
                break

            elif ikey == key.BACKSPACE:
                if uinp and cursor_pos > 0:
                    uinp = uinp[:cursor_pos-1] + uinp[cursor_pos:]

                    cursor_pos -= 1

                    _rest_b = uinp[cursor_pos:] if not mask.password else mask.mask * len(uinp[cursor_pos:])
                    _refr_style_b = _wgzst_text if not mask.password else _wgzst_mask

                    print(f'\b{_refr_style_b}{_rest_b} ', end='', flush=True)

                    print('\b' * (len(_rest_b) + 1), end='', flush=True)

            elif ikey == key.RIGHT:
                if cursor_pos < len(uinp):
                    wgztlm_move_cursor_right(flush=True)

                    cursor_pos += 1

            elif ikey == key.LEFT:
                if cursor_pos > 0:
                    wgztlm_move_cursor_left(flush=True)

                    cursor_pos -= 1

            elif ikey == _KEY_CTRL_RIGHT:
                if cursor_pos < len(uinp):
                    wgztlm_move_cursor_right(_nwi := _wgz_nop_word_idx(cursor_pos, uinp, _WGZ_FIND_NEXT_WORD), True)

                    cursor_pos += _nwi

            elif ikey == _KEY_CTRL_LEFT:
                if cursor_pos > 0:
                    wgztlm_move_cursor_left(-(_pwi := _wgz_nop_word_idx(cursor_pos, uinp, _WGZ_FIND_PREVIOUS_WORD)), True)

                    cursor_pos += _pwi

            elif ikey == key.END:
                if cursor_pos < len(uinp):
                    wgztlm_move_cursor_right((_ui_len := len(uinp)) - cursor_pos, True)

                    cursor_pos = _ui_len

            elif ikey == key.HOME:
                if cursor_pos > 0:
                    wgztlm_move_cursor_left(len(uinp), True)

                    cursor_pos = 0

            elif ikey == _KEY_CTRL_BACKSPACE:
                if cursor_pos > 0 and uinp:
                    _c_npos = cursor_pos - 1

                    while _c_npos > 0 and uinp[_c_npos].isspace(): _c_npos -= 1
                    while _c_npos > 0 and not uinp[_c_npos - 1].isspace(): _c_npos -= 1

                    _rm_word_len = cursor_pos - _c_npos

                    uinp = uinp[:_c_npos] + uinp[cursor_pos:]

                    cursor_pos = _c_npos

                    _rest = uinp[cursor_pos:]

                    _rest = mask.mask * len(_rest) if mask.password else _rest

                    print('\b' * _rm_word_len + _rest + ' ' * _rm_word_len, end='', flush=True)

                    print('\b' * (len(_rest) + _rm_word_len), end='', flush=True)

            else:
                if not ikey.isprintable(): continue

                if filter == WGZ_PROMPT_FILTER_ONLY_LETTERS and \
                    not ikey.isalpha(): continue
                if filter == WGZ_PROMPT_FILTER_ONLY_LETTERS_AND_SPACES and \
                    not ikey.isalpha() and not ikey.isspace(): continue
                if filter == WGZ_PROMPT_FILTER_ONLY_NUMBERS:
                    if not ikey.isdigit():
                        if ikey == '-' and cursor_pos == 0:
                            pass

                        else:
                            continue
                if filter == WGZ_PROMPT_FILTER_ONLY_SYMBOLS and \
                    ikey not in punctuation: continue

                uinp = uinp[:cursor_pos] + ikey + uinp[cursor_pos:]

                cursor_pos += 1

                _rest_display_ins = uinp[cursor_pos:] if not mask.password else mask.mask * len(uinp[cursor_pos:])
                _rest_display_char_ins = ikey if not mask.password else mask.mask
                _rest_display_style_ins = _wgzst_text if not mask.password else _wgzst_mask

                print(f'{_rest_display_style_ins}{_rest_display_char_ins}{_rest_display_ins} ', end='', flush=True)

                print('\b' * (len(_rest_display_ins) + 1), end='', flush=True)

                if filter == WGZ_PROMPT_FILTER_ONLY_SINGLE_CHAR:
                    break
        except KeyboardInterrupt:
            wgztlm_refresh()

            return WgzPromptReturn(True, validator(uinp) if validator else None, uinp)

    wgztlm_refresh()

    return WgzPromptReturn(False, validator(uinp) if validator else None, uinp)

# WGZ Prompt.
def wgz_prompt(placeholder: str=None,
               default_text: str=None,
               filter_: WgzPromptFilter=None,
               validator: WgzValidator=None,
               kinterrupt_callback: WgzInterruptionCallback=None) -> WgzPromptReturn:
    """Simplest WGZ prompt. Returns WGZ-Prompt class with user input data."""
    uinput = _wgz_raw_input(placeholder, default_text, WGZ_PASSWORD_NONE, filter_, validator)

    if uinput.interrupted and kinterrupt_callback:
        kinterrupt_callback(uinput.p_return)

    return uinput

# WGZ Password prompt.
def wgz_password(placeholder: str=None,
                 mask: WgzPassword=WGZ_PASSWORD_SQUARE,
                 filter_: WgzPromptFilter=None,
                 validator: WgzValidator=None,
                 kinterrupt_callback: WgzInterruptionCallback=None) -> WgzPromptReturn:
    """WGZ password prompt. Returns WGZ-Prompt class with user input password data."""
    uinput = _wgz_raw_input(placeholder, None, mask or WGZ_PASSWORD_SQUARE, filter_, validator)

    if uinput.interrupted and kinterrupt_callback:
        kinterrupt_callback(uinput.p_return)

    return uinput
