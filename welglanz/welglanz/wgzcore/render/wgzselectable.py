"""WGZ Selectables."""

from ..wgzdcs import WgzSelectable, WgzSelectableIcon, WgzSelectReturn, WgzMultiselectReturn, WgzConfirmText, WgzConfirmReturn

from ..wgzconsts import WgzInterruptionCallback, WGZ_SELECTABLE_ICON_CIRCLE, WGZ_CONFIRM_TEXT_YES_NO, WGZ_CONFIRM_FOCUS_YES, WGZ_CONFIRM_FOCUS_NO

from ..wgztheme import WgzSharedTheme, WgzStyReset, wgzstget, wgzstcmb

from readchar import readkey, key


# WGZ Select dialog.
def wgz_select(
        selectables: tuple[WgzSelectable],
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_id: str=None,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzSelectReturn:
    """WGZ select menu. Render a vertical menu for the user to select an option."""
    if not selectables:
        return WgzSelectReturn(False, None)

    current = next((ind for ind, selobj in enumerate(selectables) if selobj.selectable_id == focus_id), 0)

    def _wgz_srender():
        print('\033[F' * len(selectables), end='')

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

            print(f'\033[K{icon}{color}{selectable.selectable_text}{WgzStyReset}{hint}')

    print('\n' * len(selectables), end='')

    _wgz_srender()

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
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

            return WgzSelectReturn(True, selected)

# WGZ Multiselect dialog.
def wgz_multiselect(
        selectables: tuple[WgzSelectable],
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_id: str=None,
        default_selected_ids: tuple[str]=None,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzMultiselectReturn:
    """WGZ multiselect menu. Render a vertical menu for the user to select multiple options."""
    if not selectables:
        return WgzMultiselectReturn(False, None)

    current = next((ind for ind, selobj in enumerate(selectables) if selobj.selectable_id == focus_id), 0)

    selected_ids = {selobj.selectable_id: selobj.selectable_id in (default_selected_ids or []) for selobj in selectables}

    def _wgz_msrender():
        print('\033[F' * len(selectables), end='')

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

            print(f'\033[K{icon}{color}{selectable.selectable_text}{WgzStyReset}{hint}')

    print('\n' * len(selectables), end='')

    _wgz_msrender()

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
                return WgzMultiselectReturn(False, tuple([selobj for selobj in selected_ids.keys() if selected_ids[selobj]]))

            elif ckey == key.UP:
                current = (current - 1) % len(selectables)

            elif ckey == key.DOWN:
                current = (current + 1) % len(selectables)

            elif ckey == key.SPACE:
                selected_ids[selectables[current].selectable_id] = not selected_ids[selectables[current].selectable_id]

            _wgz_msrender()
        except KeyboardInterrupt:
            selected = tuple([selobj for selobj in selected_ids.keys() if selected_ids[selobj]])

            if kinterrupt_callback:
                kinterrupt_callback(selected)

            return WgzMultiselectReturn(True, selected)

# WGZ Confirm dialog.
def wgz_confirm(
        ctext: WgzConfirmText=WGZ_CONFIRM_TEXT_YES_NO,
        selectable_icon: WgzSelectableIcon=WGZ_SELECTABLE_ICON_CIRCLE,
        focus_option: int=WGZ_CONFIRM_FOCUS_YES,
        kinterrupt_callback: WgzInterruptionCallback=None) -> WgzConfirmReturn:
    """WGZ confirm dialog. Render a dialog for the user to confirm."""
    if not ctext:
        return WgzConfirmReturn(False, False)

    if focus_option not in (0, 1):
        focus_option = WGZ_CONFIRM_FOCUS_YES

    current = focus_option

    def _wgz_crender():
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

        print(f'\r{icon_yes}{color_yes}{ctext.yes}{WgzStyReset} / {icon_no}{color_no}{ctext.no}{WgzStyReset}', end='')

    _wgz_crender()

    while 1:
        try:
            ckey = readkey()

            if ckey == key.ENTER:
                print()

                return WgzConfirmReturn(False, current == WGZ_CONFIRM_FOCUS_YES)

            elif ckey == key.LEFT:
                current = (current - 1) % 2

            elif ckey == key.RIGHT:
                current = (current + 1) % 2

            _wgz_crender()
        except KeyboardInterrupt:
            print()

            confirmed = current == WGZ_CONFIRM_FOCUS_YES

            if kinterrupt_callback:
                kinterrupt_callback(confirmed)

            return WgzConfirmReturn(True, confirmed)
