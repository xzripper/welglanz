"""WGZ Terminal Module."""

from welglanz.wgzcore import WINDOWS

from welglanz.wgzcore.wgztheme import R

from welglanz.wgzcore.wgzgeneric import wgzwst

from typing import Any

# POSIX Imports.
if not WINDOWS:
    from termios import tcsetattr, tcgetattr, TCSADRAIN

    from tty import setraw, setcbreak

    from sys import stdin


# Old Terminal Data List.
OldTerminalData = list[int, Any]

# Flags for terminal modes.
WGZTLM_MODE_RAW = 0
WGZTLM_MODE_CBREAK = 1

# Fallback to recover terminal from being blocked by raw mode.
_WGZTLM_TRM_OLD_STD_DESCR_FALLBACK = None
_WGZTLM_TRM_OLD_ATTRS_FALLBACK = None

# WGZ Terminal Codes.
WGZTLM_TERMINAL_CODE_REWRITE = '\033[K'

WGZTLM_TERMINAL_CODE_CLEAR_LINE = f'\r{WGZTLM_TERMINAL_CODE_REWRITE}'

WGZTLM_TERMINAL_CODE_MULT_LINE_REMOVAL = '\033[2K\033[1A\033[2K\r'

WGZTLM_TERMINAL_CODE_MOVE_CURSOR_RIGHT = '\033[1C'
WGZTLM_TERMINAL_CODE_MOVE_CURSOR_LEFT = '\033[1D'

WGZTLM_TERMINAL_CODE_CURSOR_UP = '\033[F'

WGZTLM_CURSOR_HERE = '\r'

CUR = WGZTLM_CURSOR_HERE

# WGZTLM Multiple ANSI code execution.
def _wgztlm_mult_ansii_code_exec(ansii_c: str, times: int, flush: bool=False) -> None:
    for _ in range(times):
        print(ansii_c, end='', flush=flush)

# Clear terminal line.
def wgztlm_clearline(flush: bool=False) -> None:
    """Clear terminal line."""
    print(WGZTLM_TERMINAL_CODE_CLEAR_LINE, end='', flush=flush)

# Clear multiple terminal lines.
def wgztlm_clearlines(lines: int, flush: bool=False) -> None:
    """Clear mulitple terminal lines."""
    print(WGZTLM_TERMINAL_CODE_MULT_LINE_REMOVAL * lines, end='', flush=flush)

# Move cursor right N times.
def wgztlm_move_cursor_right(times: int=1, flush: bool=False) -> None:
    """Move cursor right N times."""
    _wgztlm_mult_ansii_code_exec(WGZTLM_TERMINAL_CODE_MOVE_CURSOR_RIGHT, times, flush)

# Move cursor left N times.
def wgztlm_move_cursor_left(times: int=1, flush: bool=False) -> None:
    """Move cursor left N times."""
    _wgztlm_mult_ansii_code_exec(WGZTLM_TERMINAL_CODE_MOVE_CURSOR_LEFT, times, flush)

# Allocate an ANSI code N times for rewinding cursor position. 
def wgztlm_alloc_rcp_ansii(size: int) -> str:
    """Allocate an ANSI code N times for rewinding cursor position."""
    return WGZTLM_TERMINAL_CODE_CURSOR_UP * size

# Enable raw mode for terminal. Only for POSIX terminals.
def wgztlm_posix_enable_raw_mode(mode: int=WGZTLM_MODE_RAW) -> OldTerminalData:
    """Enable raw mode for terminal. Only for POSIX terminals."""
    global _WGZTLM_TRM_OLD_STD_DESCR_FALLBACK, _WGZTLM_TRM_OLD_ATTRS_FALLBACK

    if WINDOWS:
        return

    std_descr = stdin.fileno()

    old_attrs = tcgetattr(std_descr)

    _WGZTLM_TRM_OLD_STD_DESCR_FALLBACK = std_descr
    _WGZTLM_TRM_OLD_ATTRS_FALLBACK = old_attrs

    if mode == WGZTLM_MODE_RAW:
        setraw(std_descr)

    elif mode == WGZTLM_MODE_CBREAK:
        setcbreak(std_descr)

    else:
        raise TypeError('WGZ-TLM-DEV: Invalid terminal mode.')

    return (std_descr, old_attrs)

# Disable raw mode for terminal. Only for POSIX terminals.
def wgztlm_posix_disable_raw_mode(old_attrs: OldTerminalData) -> None:
    """Disable raw mode for terminal. Only for POSIX terminals."""
    if WINDOWS:
        return

    if not old_attrs:
        tcsetattr(_WGZTLM_TRM_OLD_STD_DESCR_FALLBACK, TCSADRAIN, _WGZTLM_TRM_OLD_ATTRS_FALLBACK)

        raise TypeError(wgzwst('[E:B][CF:255:0:0]Welglanz::TerminalModule: Critical error. Old termonal data is required to disable raw mode. Falling back to previously reserved data to recover the terminal.[R]'))

    tcsetattr(old_attrs[0], TCSADRAIN, old_attrs[1])

# Refresh the styles and move cursor down.
def wgztlm_refresh() -> None:
    """Refresh the styles and move cursor down."""
    print(R)
