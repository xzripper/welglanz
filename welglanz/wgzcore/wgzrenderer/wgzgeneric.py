"""WGZ Generic Renderer."""

from ..wgzgeneric import wgzwst

from ..wgzconsts import WgzInterruptionCallback

from ..wgztheme import WgzSharedTheme, wgzstcmb, wgzstfm

from ..wgztlm import wgztlm_clearline

from readchar import readchar


# Welglanz Styled Text print function.
def wgzwst_print(*wst: str, sep: str=', ', end='\n') -> None:
    """Print text formatted using Welglanz Style."""
    print(*[wgzwst(_wst) for _wst in wst], sep=sep, end=end)

# WGZ Wait for a key function (alternative to GETCH).
def wgz_wait(text: str='Press any key to continue...', dynamic: bool=True, kinterrupt_callback: WgzInterruptionCallback=None) -> None:
    """Wait for a key before continuing."""
    _wgzst_wait = wgzstcmb(WgzSharedTheme.wait_fg,
                           WgzSharedTheme.wait_bg,
                           WgzSharedTheme.wait_ef)

    _dyn_chars = ('\r' if dynamic else '', '' if dynamic else '\n')

    print(f'{_dyn_chars[0]}{wgzstfm(text, _wgzst_wait)}', end=_dyn_chars[1])

    if readchar() == '\x03':
        if kinterrupt_callback:
            kinterrupt_callback(None)

        else:
            raise KeyboardInterrupt

    if dynamic:
        wgztlm_clearline()
