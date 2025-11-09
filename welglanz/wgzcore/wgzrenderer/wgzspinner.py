"""WGZ Spinners."""

from .. import WgzMissingParameterError, WgzInvalidParameterError, _wgz_ensure_char

from ..wgzdcs import WgzInterruptionSignal, WgzData, WgzSpinnerIcon

from ..wgzconsts import WgzInterruptionCallback, WgzSpinnerTarget, WgzSpinnerStateIcon, WGZ_SPINNER_ICON_FALLING_SAND, WGZ_SPINNER_FINISHED_ICON_STAR, WGZ_SPINNER_INTERRUPTED_ICON_BALLOT, WGZ_DEFAULT_SPINNER_RENDER_INTERVAL

from ..wgztheme import WgzSharedTheme, wgzstget, wgzstcmb, wgzstfm

from ..wgztlm import (
    wgztlm_clearline,
    wgztlm_posix_enable_raw_mode, wgztlm_posix_disable_raw_mode, WGZTLM_MODE_CBREAK,
    CUR, WGZTLM_TERMINAL_CODE_REWRITE
)

from threading import Thread, Event

from itertools import cycle

from time import sleep

from typing import Union


# WGZ Spinner.
def wgz_spinner(
        text: str,
        final_text: str,
        interrupted_text: str,
        targets: Union[WgzSpinnerTarget, tuple[WgzSpinnerTarget]],
        spinner: WgzSpinnerIcon=WGZ_SPINNER_ICON_FALLING_SAND,
        spinner_finished_icon: WgzSpinnerStateIcon=WGZ_SPINNER_FINISHED_ICON_STAR,
        spinner_interrupted_icon: WgzSpinnerStateIcon=WGZ_SPINNER_INTERRUPTED_ICON_BALLOT,
        spinner_render_interval: float=WGZ_DEFAULT_SPINNER_RENDER_INTERVAL,
        kinterrupt_callback: WgzInterruptionCallback=None) -> None:
    """WGZ Spinner. Display a spinner animation while executing targets."""
    if not all((spinner, spinner_finished_icon, spinner_interrupted_icon)):
        raise WgzMissingParameterError('Missing Spinner related parameter(s).')

    if type(spinner_render_interval) != float or spinner_render_interval < 0:
        raise WgzInvalidParameterError('Invalid spinner render interval.')

    if not targets:
        raise WgzMissingParameterError('Missing Spinner Targets parameter.')

    _wgz_ensure_char(spinner_finished_icon)

    targets_finished = Event()

    interrupted = Event()

    interruption_signal = WgzInterruptionSignal()

    wgzdata = WgzData()

    original_text = text

    def _run_targets():
        try:
            if callable(targets):
                targets(interruption_signal, wgzdata)

            else:
                for target in targets:
                    target(interruption_signal, wgzdata)
        except KeyboardInterrupt:
            interrupted.set()

            interruption_signal.interrupted = True
        finally:
            targets_finished.set()

    tthr = Thread(target=_run_targets)

    tthr.start()

    _wgzst_text = wgzstcmb(WgzSharedTheme.spinner_text_fg,
                           WgzSharedTheme.spinner_text_bg,
                           WgzSharedTheme.spinner_text_ef)

    _wgzst_itext = wgzstcmb(WgzSharedTheme.spinner_text_interrupted_fg,
                            WgzSharedTheme.spinner_text_interrupted_bg,
                            WgzSharedTheme.spinner_text_interrupted_ef)

    _wgzst_ftext = wgzstcmb(WgzSharedTheme.spinner_text_finished_fg,
                            WgzSharedTheme.spinner_text_finished_bg,
                            WgzSharedTheme.spinner_text_finished_ef)

    _otd = wgztlm_posix_enable_raw_mode(WGZTLM_MODE_CBREAK)

    try:
        for icon in cycle(spinner.icon):
            if targets_finished.is_set():
                break

            if interruption_signal.inner_interruption:
                interrupted.set()

                interruption_signal.interrupted = True

            text = original_text \
                .replace('$wgzdata1', str(wgzdata.data1)) \
                .replace('$wgzdata2', str(wgzdata.data2)) \
                .replace('$wgzdata3', str(wgzdata.data3))

            _icon = wgzstfm(icon, wgzstget(WgzSharedTheme.spinner_icon_working_color))

            print(f'{CUR}{WGZTLM_TERMINAL_CODE_REWRITE}{_icon} {wgzstfm(text, _wgzst_text)}', end='')

            sleep(spinner_render_interval)
    except KeyboardInterrupt:
        interrupted.set()

        interruption_signal.interrupted = True

        if kinterrupt_callback:
            kinterrupt_callback(None)
    finally:
        wgztlm_posix_disable_raw_mode(_otd)

        wgztlm_clearline()

        _is_interrupted = interrupted.is_set()

        _atxt = wgzstfm(interrupted_text, _wgzst_itext) if _is_interrupted else wgzstfm(final_text, _wgzst_ftext)

        _icon = wgzstfm(
            spinner_interrupted_icon if _is_interrupted \
                else spinner_finished_icon,
            wgzstget(WgzSharedTheme.spinner_icon_interrupted_color if _is_interrupted \
                     else wgzstget(WgzSharedTheme.spinner_icon_finished_color)))

        print(f'{_icon}{WgzSharedTheme._adj_padding_BINT}{_atxt}')

        tthr.join()
