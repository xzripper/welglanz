"""WGZ Progress Bar."""

from welglanz.wgzcore import WgzMissingParameterError, WgzInvalidParameterError, _wgz_ensure_char

from welglanz.wgzcore.wgzdcs import WgzInterruptionSignal, WgzProgressBarData

from welglanz.wgzcore.wgzconsts import WgzInterruptionCallback, WgzProgressBarTarget, WgzProgressBarLine, WGZ_PB_LINE_HEAVY

from welglanz.wgzcore.wgztheme import WgzSharedTheme, WgzStyFg, WgzStyEf, wgzstget, wgzstcmb, wgzstfm

from welglanz.wgzcore.wgztlm import (
    wgztlm_clearline,
    wgztlm_posix_enable_raw_mode, wgztlm_posix_disable_raw_mode, WGZTLM_MODE_CBREAK,
    CUR, WGZTLM_TERMINAL_CODE_REWRITE
)

from threading import Thread, Event

from time import time

from typing import Union


# Format float to time string.
def _wgz_pb_format_time(ftime: float) -> str:
    return f'{int(ftime) // 60}:{(int(ftime) % 60):02}'

# Generate progress bar string.
def _wgz_gen_pb_str(
        l_segm: str,
        nl_segm: str,
        pb_width: int,
        max_progress: int,
        current_progress: int) -> str:
    current_progress = max(0, min(current_progress, max_progress))

    loaded = int((current_progress / max_progress) * pb_width)

    return f'{l_segm * loaded}{nl_segm * (pb_width - loaded)}'

# WGZ Progress Bar.
def wgz_progress_bar(
        text: str,
        final_text: str,
        interrupted_text: str,
        targets: Union[WgzProgressBarTarget, tuple[WgzProgressBarTarget]],
        max_progress: int=100,
        pb_width: int=40,
        line: WgzProgressBarLine=WGZ_PB_LINE_HEAVY,
        kinterrupt_callback: WgzInterruptionCallback=None
) -> None:
    """WGZ Progress Bar. Render a simple progress bar without any interactions."""
    if not all((max_progress, pb_width, line)):
        raise WgzMissingParameterError('Missing generic Progress Bar parameters.')

    if not targets:
        raise WgzMissingParameterError('Missing Progress Bar Targets parameter.')

    if pb_width <= 5:
        raise WgzInvalidParameterError('PB\'s Width paramater must be more than 5.')

    _wgz_ensure_char(line)

    targets_finished = Event()

    interrupted = Event()

    pb_data = WgzProgressBarData()

    interruption_signal = WgzInterruptionSignal()

    def _run_targets():
        try:
            if callable(targets):
                targets(interruption_signal, pb_data)

            else:
                for target in targets:
                    target(interruption_signal, pb_data)
        except KeyboardInterrupt:
            interrupted.set()

            interruption_signal.interrupted = True
        finally:
            targets_finished.set()

    tthr = Thread(target=_run_targets)

    tthr.start()

    _wgzst_pb_text = wgzstcmb(WgzSharedTheme.pb_text_fg,
                              WgzSharedTheme.pb_text_bg,
                              WgzSharedTheme.pb_text_ef)

    _wgzst_pb_itext = wgzstcmb(WgzSharedTheme.pb_text_interrupted_fg,
                               WgzSharedTheme.pb_text_interrupted_bg,
                               WgzSharedTheme.pb_text_interrupted_ef)

    _wgzst_pb_ftext = wgzstcmb(WgzSharedTheme.pb_text_finished_fg,
                               WgzSharedTheme.pb_text_finished_bg,
                               WgzSharedTheme.pb_text_finished_ef)

    _wgzst_status = wgzstcmb(WgzSharedTheme.pb_status_fg,
                             WgzSharedTheme.pb_status_bg,
                             WgzSharedTheme.pb_status_ef)

    _wgzst_time = wgzstcmb(WgzSharedTheme.pb_time_fg,
                           WgzSharedTheme.pb_time_bg,
                           WgzSharedTheme.pb_time_ef)

    _wgzst_loaded_segment = wgzstget(WgzSharedTheme.pb_loaded_segment_color) + WgzStyEf.bold
    _wgzst_not_loaded_segment = wgzstget(WgzSharedTheme.pb_not_loaded_segment_color) + WgzStyEf.bold

    _pb_loaded_segment = wgzstfm(line, _wgzst_loaded_segment)
    _pb_nloaded_segment = wgzstfm(line, _wgzst_not_loaded_segment)

    _dot = wgzstfm('•', WgzStyFg.white)

    _time = None

    t_before = time()

    _otd = wgztlm_posix_enable_raw_mode(WGZTLM_MODE_CBREAK)

    try:
        while not targets_finished.is_set():
            if interruption_signal.inner_interruption:
                interrupted.set()

                interruption_signal.interrupted = True

            _status = wgzstfm(pb_data.str_status, _wgzst_status) if pb_data.str_status else ''

            _time = _wgz_pb_format_time(time() - t_before)

            _time_p = wgzstfm(_time, _wgzst_time)

            _pb_str = _wgz_gen_pb_str(_pb_loaded_segment, _pb_nloaded_segment, pb_width, max_progress, pb_data.progress)

            _pb_p = f'{CUR}{WGZTLM_TERMINAL_CODE_REWRITE}{wgzstfm(text, _wgzst_pb_text)} {_pb_str} {_status} {_dot} {_time_p}'

            print(_pb_p, end='')
    except KeyboardInterrupt:
        interrupted.set()

        interruption_signal.interrupted = True

        if kinterrupt_callback:
            kinterrupt_callback(None)
    finally:
        wgztlm_posix_disable_raw_mode(_otd)

        wgztlm_clearline()

        _is_interrupted = interrupted.is_set()

        _text = wgzstfm(interrupted_text, _wgzst_pb_itext) if _is_interrupted \
            else wgzstfm(final_text.replace('$time', _time), _wgzst_pb_ftext)

        print(f'{wgzstfm(">", WgzStyEf.bold)} {_text}')

        tthr.join()
