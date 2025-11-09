"""Welglanz Demo."""

from welglanz.wgzcore.wgzrenderer.wgzprompt import wgz_prompt, wgz_password

from welglanz.wgzcore.wgzrenderer.wgzselectable import wgz_select, wgz_multiselect, wgz_confirm

from welglanz.wgzcore.wgzrenderer.wgzspinner import wgz_spinner

from welglanz.wgzcore.wgzrenderer.wgzpb import wgz_progress_bar

from welglanz.wgzcore.wgzrenderer.wgzgeneric import wgzwst_print, wgz_wait

from welglanz.wgzcore.wgzdcs import WgzInterruptionSignal, WgzSelectable, WgzData, WgzProgressBarData

from welglanz.wgzcore.wgzconsts import WGZ_SELECTABLE_ICON_DIAMOND, WGZ_PROMPT_FILTER_ONLY_NUMBERS

from welglanz.wgzcore.wgzgeneric import wgzwstkey

from welglanz.wgzcore.wgztheme import WgzSharedTheme, WHITE_FORE

from welglanz.wgzcore.wgztlm import wgztlm_clearlines, CUR

from random import randint

from time import sleep


# WGZ Demo.
def wgz_show_demo() -> None:
    """Show Welglanz Demo."""
    WgzSharedTheme.regular_text_fg = WHITE_FORE

    def keyboard_interruption_handler(message: str) -> None:
        wgzwst_print(f'\n[E:B][CF:255:0:0]Demo\'s Raw Keyboard Interruption Callback! Latest interrupted data: "{message}".[R]')

        exit(1)

    wgzwst_print('[E:B][F:WHITE]> Welcome to Welglänz Demo![R]')

    fname = wgz_prompt('First name:', 'John', kinterrupt_callback=keyboard_interruption_handler)
    sname = wgz_prompt('Second name:', 'Smith', kinterrupt_callback=keyboard_interruption_handler)

    while True:
        password = wgz_password('Password:', kinterrupt_callback=keyboard_interruption_handler)

        if password.p_return:
            break

        else:
            wgztlm_clearlines(1)

    single_select = wgz_select(
        (WgzSelectable('ABC', 'abc', 'First three letters of the alphabet.'),
         WgzSelectable('DEF', 'def', 'Another three letters of the alphabet.'),
         WgzSelectable('XYZ', 'xyz', 'Three last letters of the alphabet (Focused).'),
         WgzSelectable('Nothing', 'nothing', None)), 'Single Select!', focus_id='xyz', kinterrupt_callback=keyboard_interruption_handler
    )

    multi_select = wgz_multiselect(
        (WgzSelectable('Apples', 'apples', 'Red and almost round (Pre-Selected).'),
         WgzSelectable('Bananas', 'bananas', 'Yellow and long (Focused/Pre-Selected).'),
         WgzSelectable('Orange', 'orange', 'Orange and round.'),
         WgzSelectable('Nothing', 'nothing', 'Unique Answer.')), f'Select the fruits with {wgzwstkey("space")}', 'Fruits selected',
         WGZ_SELECTABLE_ICON_DIAMOND, 'bananas', 'nothing', ('apples', 'bananas'), kinterrupt_callback=keyboard_interruption_handler
    )

    def spinner_target(wgzis: WgzInterruptionSignal, wgzd: WgzData) -> None:
        for i in range(1, 11):
            if wgzis.interrupted:
                break

            wgzd.data1 = i

            sleep(0.25)

    wgz_spinner('Thinking... $wgzdata1/10', 'Finished thinking.', 'Interrupted!', spinner_target, kinterrupt_callback=keyboard_interruption_handler)

    number = None

    while True:
        randint_ = randint(1_000_000, 10_000_000)

        number = int(wgz_prompt('Enter a number between 1 000 000 and 10 000 000:', str(randint_), WGZ_PROMPT_FILTER_ONLY_NUMBERS, kinterrupt_callback=keyboard_interruption_handler).p_return)

        if number < 1_000_000 or number > 10_000_000:
            wgzwst_print('[E:B][F:WHITE]> [CF:255:0:0]Invalid number![R]')

            sleep(3)

            wgztlm_clearlines(2)

        else:
            break

    def pb_target(wgzis: WgzInterruptionSignal, wgzpbd: WgzProgressBarData) -> None:
        for i in range(1, number + 1):
            if wgzis.interrupted:
                break

            wgzpbd.set_progress(i)

            wgzpbd.set_status(f'Iterated {i} out of {number}')

    wgz_progress_bar('Iteration', 'Iteration finished in $time!', 'Interrupted!', pb_target, number, 25, kinterrupt_callback=keyboard_interruption_handler)

    answer = wgz_confirm('Yes or No?', kinterrupt_callback=keyboard_interruption_handler)

    wgz_wait(kinterrupt_callback=keyboard_interruption_handler)

    for c in range(255, 0, -1):
        wgzwst_print(f'[E:B][CF:{c}:{c}:{c}]Bye Bye, {fname.p_return}![R]', end=CUR)

        sleep(0.01)
