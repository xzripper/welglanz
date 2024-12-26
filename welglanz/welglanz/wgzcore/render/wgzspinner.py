"""WGZ Spinners."""

from ..wgzdcs import WgzSpinnerIcon, WgzStopSignal, WgzData

from ..wgzconsts import WgzSpinnerTarget, WgzInterruptionCallback, WGZ_SPINNER_ICON_CIRCLE, WGZ_DEFAULT_SPINNER_RENDER_INTERVAL, WGZ_DEFAULT_SPINNER_ICON_ON_FINISH

from ..wgztheme import WgzSharedTheme, WgzStyReset, wgzstget, wgzstcmb

from threading import Thread, Event

from itertools import cycle

from time import sleep

from typing import Union


# WGZ Spinner.
def wgz_spinner(
        text: str,
        final_text: str,
        canceled_text: str,
        targets: Union[WgzSpinnerTarget, tuple[WgzSpinnerTarget]],
        spinner: WgzSpinnerIcon=WGZ_SPINNER_ICON_CIRCLE,
        spinner_render_interval: float=WGZ_DEFAULT_SPINNER_RENDER_INTERVAL,
        kinterrupt_callback: WgzInterruptionCallback=None) -> None:
    """WGZ Spinner. Display a spinner animation while executing targets."""
    if not spinner:
        return

    targets_finished = Event()

    canceled = Event()

    stop_signal = WgzStopSignal()

    wgzdata = WgzData()

    original = text

    def _run_targets():
        try:
            if callable(targets):
                targets(stop_signal, wgzdata)

            else:
                for target in targets:
                    target(stop_signal, wgzdata)
        except KeyboardInterrupt:
            canceled.set()

            stop_signal.stop_required = True
        finally:
            targets_finished.set()

    tthr = Thread(target=_run_targets)

    tthr.start()

    _txt_cmb = wgzstcmb(WgzSharedTheme.spinner_text_fg,
                        WgzSharedTheme.spinner_text_bg,
                        WgzSharedTheme.spinner_text_ef)

    _ctxt_cmb = wgzstcmb(WgzSharedTheme.spinner_text_canceled_fg,
                        WgzSharedTheme.spinner_text_canceled_bg,
                        WgzSharedTheme.spinner_text_canceled_ef)

    _ftxt_cmb = wgzstcmb(WgzSharedTheme.spinner_text_finished_fg,
                        WgzSharedTheme.spinner_text_finished_bg,
                        WgzSharedTheme.spinner_text_finished_ef)

    try:
        for icon in cycle(spinner.icon):
            if targets_finished.isSet():
                break

            text = original.replace('$wgzdata', str(wgzdata.data))

            print(f'\r{wgzstget(WgzSharedTheme.spinner_icon_working_fg) + icon + WgzStyReset} {_txt_cmb + text + WgzStyReset}', end='', flush=True)

            sleep(spinner_render_interval)
    except KeyboardInterrupt:
        canceled.set()

        stop_signal.stop_required = True

        if kinterrupt_callback:
            kinterrupt_callback(None)
    finally:
        print(f'\r{" " * (len(text) + len(spinner.icon[0]))}', end='\r')

        _atxt = _ctxt_cmb + canceled_text if canceled.isSet() else _ftxt_cmb + final_text

        print(f'{wgzstget(WgzSharedTheme.spinner_icon_finished_fg) + WGZ_DEFAULT_SPINNER_ICON_ON_FINISH + WgzStyReset} {_atxt + WgzStyReset}', flush=True)

        tthr.join()
