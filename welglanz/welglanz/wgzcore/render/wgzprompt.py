"""WGZ Prompts."""

from ..wgzdcs import WgzPassword, WgzPromptReturn

from ..wgzconsts import WgzValidator, WgzInterruptionCallback, WGZ_PASSWORD_NONE, WGZ_PASSWORD_SQUARE

from ..wgztheme import WgzSharedTheme, WgzStyReset, wgzstcmb

from readchar import readkey, key


# WGZ Raw Input.
def _wgz_raw_input(
        placeholder: str,
        default_text: str=None,
        mask: WgzPassword=WGZ_PASSWORD_NONE,
        validator: WgzValidator=None) -> WgzPromptReturn:
    uinp = default_text or ''

    _wgzst_text = wgzstcmb(
        WgzSharedTheme.regular_text_fg,
        WgzSharedTheme.regular_text_bg,
        WgzSharedTheme.regular_text_ef)

    _wgzst_mask = wgzstcmb(
        WgzSharedTheme.mask_text_fg,
        WgzSharedTheme.mask_text_ef)

    if placeholder:
        print(wgzstcmb(
            WgzSharedTheme.placeholder_text_fg,
            WgzSharedTheme.placeholder_text_bg,
            WgzSharedTheme.placeholder_text_ef) + placeholder, end='', flush=True)

    if mask.password and uinp:
        print(_wgzst_mask + mask.mask, end='', flush=True)

    else:
        print(_wgzst_text + uinp, end='', flush=True)

    while 1:
        try:
            ikey = readkey()

            if ikey == key.ENTER:
                break

            elif ikey == key.BACKSPACE:
                if uinp:
                    uinp = uinp[:-1]

                    print(f'\b \b{_wgzst_text}', end='', flush=True)

            else:
                uinp += ikey

                if mask.password:
                    print(_wgzst_mask + mask.mask, end='', flush=True)

                else:
                    print(_wgzst_text + ikey, end='', flush=True)
        except KeyboardInterrupt:
            print(WgzStyReset)

            return WgzPromptReturn(True, validator(uinp) if validator else None, uinp)

    print(WgzStyReset)

    return WgzPromptReturn(False, validator(uinp) if validator else None, uinp)

# WGZ Prompt.
def wgz_prompt(placeholder: str=None,
               default_text: str=None,
               validator: WgzValidator=None,
               kinterrupt_callback: WgzInterruptionCallback=None) -> WgzPromptReturn:
    """Simplest WGZ prompt. Returns WGZ-Prompt class with user input data."""
    uinput = _wgz_raw_input(placeholder, default_text, WGZ_PASSWORD_NONE, validator)

    if uinput.interrupted and kinterrupt_callback:
        kinterrupt_callback(uinput.ureturn)

    return uinput

# WGZ Password prompt.
def wgz_password(placeholder: str=None,
                 mask: WgzPassword=WGZ_PASSWORD_SQUARE,
                 validator: WgzValidator=None,
                 kinterrupt_callback: WgzInterruptionCallback=None) -> WgzPromptReturn:
    """WGZ password prompt. Returns WGZ-Prompt class with user input password data."""
    uinput = _wgz_raw_input(placeholder, None, mask or WGZ_PASSWORD_SQUARE, validator)

    if uinput.interrupted and kinterrupt_callback:
        kinterrupt_callback(uinput.ureturn)

    return uinput
