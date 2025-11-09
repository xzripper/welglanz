"""WGZ Selectables."""

from .. import WgzMissingParameterError

from ..wgzdcs import WgzSelectable, WgzSelectableIcon, WgzSelectReturn, WgzMultiselectReturn, WgzConfirmText, WgzConfirmReturn

from ..wgzconsts import WgzInterruptionCallback, WGZ_SELECTABLE_ICON_CIRCLE, WGZ_CONFIRM_TEXT_YES_NO, WGZ_CONFIRM_FOCUS_YES, WGZ_CONFIRM_FOCUS_NO, WGZ_CONFIRM_SEPARATOR_SLASH

from ..wgztheme import WgzSharedTheme, WgzStyReset, WgzStyEf, wgzstget, wgzstcmb

from ..wgztlm import wgztlm_clearline, wgztlm_clearlines, wgztlm_alloc_rcp_ansii, CUR, WGZTLM_TERMINAL_CODE_REWRITE

from readchar import readkey, key


# WGZ Remove duplicate selectables based on ID.
def _wgz_remove_sid_dups(selectables: tuple[WgzSelectable]) -> tuple[WgzSelectable]:
    _prev_sids = set(); return tuple(selectable for selectable in selectables 
                 if not (selectable.selectable_id in _prev_sids 
                 or _prev_sids.add(selectable.selectable_id)))

# WGZ Select dialog.
def wgz_select(
        selectables: tuple[WgzSelectable],
        title: str='Select',
        post_title: str='Selected',
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_id: str=None,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzSelectReturn:
    """WGZ select menu. Render a vertical menu for the user to select an option."""
    if not selectables:
        return WgzSelectReturn(False, None)

    selectables = _wgz_remove_sid_dups(selectables)

    if len(selectables) <= 1:
        return WgzMultiselectReturn(False, None)

    current = next((ind for ind, selobj in enumerate(selectables) if selobj.selectable_id == focus_id), 0)

    _wgzst_title = wgzstcmb(WgzSharedTheme.select_dialog_title_fg,
                            WgzSharedTheme.select_dialog_title_bg,
                            WgzSharedTheme.select_dialog_title_ef)

    _title = '' if not title else f'☰{WgzSharedTheme._adj_padding_BINT}{_wgzst_title}{title}{WgzStyReset}'

    print(_title)

    _rcp_ansii = wgztlm_alloc_rcp_ansii(len(selectables))

    def _wgz_srender() -> None:
        print(_rcp_ansii, end='')

        for index, selectable in enumerate(selectables):
            highlighted = index == current

            icon = ''

            if selectable_icon:
                icon = wgzstget(WgzSharedTheme.selectable_icon_default_fg) + selectable_icon.icon_default + '  ' + WgzStyReset \
                    if not highlighted else \
                        wgzstget(WgzSharedTheme.selectable_icon_highlighted_fg) + selectable_icon.icon_selected + '  ' + WgzStyReset

            hint = f' {wgzstcmb(WgzSharedTheme.selectable_hint_fg, WgzSharedTheme.selectable_hint_ef)}{selectable.selectable_hint}{WgzStyReset}' \
                if selectable.selectable_hint and highlighted else ''

            color = wgzstcmb(WgzSharedTheme.selectable_highlighted_fg,
                             WgzSharedTheme.selectable_highlighted_bg,
                             WgzSharedTheme.selectable_highlighted_ef) if highlighted \
                else wgzstcmb(WgzSharedTheme.selectable_default_fg,
                              WgzSharedTheme.selectable_default_bg,
                              WgzSharedTheme.selectable_default_ef)

            print(f'{WGZTLM_TERMINAL_CODE_REWRITE}{icon}{color}{selectable.selectable_text}{WgzStyReset}{hint}')

    def _wgz_post_srender(choice: str) -> None:
        wgztlm_clearlines(len(selectables) + 1)

        _wgzst_post_title = wgzstcmb(WgzSharedTheme.select_dialog_post_title_fg,
                                     WgzSharedTheme.select_dialog_post_title_bg,
                                     WgzSharedTheme.select_dialog_post_title_ef)

        print(f'{WgzStyEf.bold}>{WgzStyReset} {_wgzst_post_title}{post_title}{WgzStyReset}{WgzStyEf.bold}: {choice}.{WgzStyReset}')

    print('\n' * len(selectables), end='')

    _wgz_srender()

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
                _wgz_post_srender(selectables[current].selectable_text)

                return WgzSelectReturn(False, selectables[current].selectable_id)

            elif ckey == key.UP:
                current = (current - 1) % len(selectables)

            elif ckey == key.DOWN:
                current = (current + 1) % len(selectables)

            _wgz_srender()
        except KeyboardInterrupt:
            selected = selectables[current].selectable_id

            if kinterrupt_callback:
                kinterrupt_callback(selected)

            _wgz_post_srender('None')

            return WgzSelectReturn(True, selected)

# WGZ Multiselect dialog.
def wgz_multiselect(
        selectables: tuple[WgzSelectable],
        title: str='Multi-Select',
        post_title: str='Selected',
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_id: str=None,
        unique_id: str=None,
        default_selected_ids: tuple[str]=None,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzMultiselectReturn:
    """WGZ multiselect menu. Render a vertical menu for the user to select multiple options."""
    if not selectables:
        return WgzMultiselectReturn(False, None)

    selectables = _wgz_remove_sid_dups(selectables)

    if len(selectables) <= 1:
        return WgzMultiselectReturn(False, None)

    current = next((ind for ind, selobj in enumerate(selectables) if selobj.selectable_id == focus_id), 0)

    selected_ids = {selobj.selectable_id: selobj.selectable_id in (default_selected_ids or []) for selobj in selectables}

    _wgzst_title = wgzstcmb(WgzSharedTheme.select_dialog_title_fg,
                            WgzSharedTheme.select_dialog_title_bg,
                            WgzSharedTheme.select_dialog_title_ef)

    _title = '' if not title else f'☰{WgzSharedTheme._adj_padding_BINT}{_wgzst_title}{title}{WgzStyReset}'

    print(_title)

    _rcp_ansii = wgztlm_alloc_rcp_ansii(len(selectables))

    def _wgz_msrender() -> None:
        print(_rcp_ansii, end='')

        for index, selectable in enumerate(selectables):
            highlighted = index == current

            icon = ''

            if selectable_icon:
                icon = '  ' + WgzStyReset

                if highlighted:
                    if selected_ids[selectable.selectable_id]:
                        icon = wgzstget(WgzSharedTheme.multiselect_icon_highlighted_selected_fg) + selectable_icon.icon_selected + icon

                    else:
                        icon = wgzstget(WgzSharedTheme.multiselect_icon_highlighted_not_selected_fg) + selectable_icon.icon_default + icon

                else:
                    if selected_ids[selectable.selectable_id]:
                        icon = wgzstget(WgzSharedTheme.multiselect_icon_not_highlighted_selected_fg) + selectable_icon.icon_selected + icon

                    else:
                        icon = wgzstget(WgzSharedTheme.multiselect_icon_not_highlighted_not_selected_fg) + selectable_icon.icon_default + icon

            hint = f' {wgzstcmb(WgzSharedTheme.selectable_hint_fg, WgzSharedTheme.selectable_hint_ef)}{selectable.selectable_hint}{WgzStyReset}' \
                if selectable.selectable_hint and highlighted else ''

            color = wgzstcmb(WgzSharedTheme.selectable_highlighted_fg,
                             WgzSharedTheme.selectable_highlighted_bg,
                             WgzSharedTheme.selectable_highlighted_ef) if highlighted \
                else wgzstcmb(WgzSharedTheme.selectable_default_fg,
                              WgzSharedTheme.selectable_default_bg,
                              WgzSharedTheme.selectable_default_ef)

            print(f'{WGZTLM_TERMINAL_CODE_REWRITE}{icon}{color}{selectable.selectable_text}{WgzStyReset}{hint}')

    def _wgz_post_msrender(choices: tuple[str]) -> None:
        wgztlm_clearlines(len(selectables) + 1)

        _wgzst_post_title = wgzstcmb(WgzSharedTheme.select_dialog_post_title_fg,
                                     WgzSharedTheme.select_dialog_post_title_bg,
                                     WgzSharedTheme.select_dialog_post_title_ef)

        print(f'{WgzStyEf.bold}>{WgzStyReset} {_wgzst_post_title}{post_title}{WgzStyReset}{WgzStyEf.bold}: {", ".join(choices) if choices else "None"}.{WgzStyReset}')

    print('\n' * len(selectables), end='')

    _wgz_msrender()

    _selected_objs = lambda: tuple([selobj for selobj in selected_ids.keys() if selected_ids[selobj]])

    _selected_objs_str = lambda: [
        _s_objs := _selected_objs(),

        [_sel.selectable_text for _sel in selectables if _sel.selectable_id in _s_objs]
    ][1]

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
                _wgz_post_msrender(_selected_objs_str())

                return WgzMultiselectReturn(False, _selected_objs())

            elif ckey == key.UP:
                current = (current - 1) % len(selectables)

            elif ckey == key.DOWN:
                current = (current + 1) % len(selectables)

            elif ckey == key.SPACE:
                if unique_id and selectables[current].selectable_id == unique_id:
                    for selected_id in selected_ids:
                        selected_ids[selected_id] = selected_id == unique_id

                else:
                    selected_ids[selectables[current].selectable_id] = not selected_ids[selectables[current].selectable_id]

                    if unique_id: selected_ids[unique_id] = False

            _wgz_msrender()
        except KeyboardInterrupt:
            selected = _selected_objs()

            if kinterrupt_callback:
                kinterrupt_callback(selected)

            _wgz_post_msrender(_selected_objs_str())

            return WgzMultiselectReturn(True, selected)

# WGZ Confirm dialog.
def wgz_confirm(
        placeholder: str=None,
        separator: str=WGZ_CONFIRM_SEPARATOR_SLASH,
        ctext: WgzConfirmText=WGZ_CONFIRM_TEXT_YES_NO,
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_option: int=WGZ_CONFIRM_FOCUS_YES,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzConfirmReturn:
    """WGZ confirm dialog. Render a dialog for the user to confirm."""
    if not ctext:
        raise WgzMissingParameterError('Missing CText parameter.')

    if focus_option not in (0, 1):
        focus_option = WGZ_CONFIRM_FOCUS_YES

    current = focus_option

    _wgzst_placeholder = wgzstcmb(WgzSharedTheme.confirm_placeholder_fg,
                                  WgzSharedTheme.confirm_placeholder_bg,
                                  WgzSharedTheme.confirm_placeholder_ef)

    _placeholder_str = '' if not placeholder else f'{_wgzst_placeholder}{placeholder}{WgzStyReset}'

    def _wgz_crender() -> None:
        _deficon = '' if not selectable_icon else \
            wgzstget(WgzSharedTheme.confirm_icon_default_fg) + selectable_icon.icon_default + ' ' + WgzStyReset

        _highicon = '' if not selectable_icon else \
            wgzstget(WgzSharedTheme.confirm_icon_selected_fg) + selectable_icon.icon_selected + ' ' + WgzStyReset

        icon_yes = _highicon if current == WGZ_CONFIRM_FOCUS_YES else _deficon
        icon_no = _highicon if current == WGZ_CONFIRM_FOCUS_NO else _deficon

        _def_c = wgzstcmb(WgzSharedTheme.confirm_default_fg, WgzSharedTheme.confirm_default_bg, WgzSharedTheme.confirm_default_ef)
        _sel_c = wgzstcmb(WgzSharedTheme.confirm_selected_fg, WgzSharedTheme.confirm_selected_bg, WgzSharedTheme.confirm_selected_ef)

        color_yes = _sel_c if current == WGZ_CONFIRM_FOCUS_YES else _def_c
        color_no = _sel_c if current == WGZ_CONFIRM_FOCUS_NO else _def_c

        print(f'{CUR}{_placeholder_str} {icon_yes}{color_yes}{ctext.yes}{WgzStyReset} {separator} {icon_no}{color_no}{ctext.no}{WgzStyReset}', end='')

    def _wgz_post_crender(choice: str) -> None:
        wgztlm_clearline()

        print(f'{WgzStyEf.bold}>{WgzStyReset} {_placeholder_str}{WgzStyEf.bold}: {choice}{WgzStyReset}')

    _wgz_crender()

    _selected_str = lambda: (ctext.yes, ctext.no)[current ^ 1]

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
                _wgz_post_crender(_selected_str())

                return WgzConfirmReturn(False, current ^ 1)

            elif ckey == key.LEFT:
                current = (current - 1) % 2

            elif ckey == key.RIGHT:
                current = (current + 1) % 2

            _wgz_crender()
        except KeyboardInterrupt:
            _wgz_post_crender(_selected_str())

            if kinterrupt_callback:
                kinterrupt_callback(current ^ 1)

            return WgzConfirmReturn(True, current ^ 1)
