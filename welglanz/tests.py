# # import itertools
# # import sys
# # import time

# # from welglanz._wgz import wgz_prompt, wgz_password, wgz_select, WgzSelectable, WGZ_SELECTABLE_ICON_DIAMOND, wgz_multiselect, wgz_confirm, wgz_new_confirm_text, WGZ_CONFIRM_FOCUS_NO
# # from sty import bg
# # # print(wgz_password('Enter password: '))

# # print(wgz_select((
# #     WgzSelectable('hi', 'h', None),
# #     WgzSelectable('bye', 'b', 'why so?')), WGZ_SELECTABLE_ICON_DIAMOND, 'b'))


# # # # print(wgz_multiselect((
# # # #     WgzSelectable('Python', 'py', '(my favorite)'),
# # # #      WgzSelectable('Java', 'java', '(my favorite)'),
# # # #      WgzSelectable('C++', 'cpp'),
# # # #      WgzSelectable('C', 'c')), WGZ_SELECTABLE_ICON_DIAMOND, 'c',  ('py', 'java')))

# # # print(wgz_confirm(wgz_new_confirm_text('Be', 'Or not to be'), WGZ_SELECTABLE_ICON_DIAMOND, WGZ_CONFIRM_FOCUS_NO))

# # # from welglanz._wgz import wgz_spinner, WGZ_SPINNER_ICON_SQUARE_BOUNCE, WgzStopSignal, WgzData

# # # def x(stop: WgzStopSignal, data: WgzData):
# # #     for i in range(99999999):
# # #         if stop.stop_required: break

# # #         data.data = i

# # # wgz_spinner('Iterating 90M+/$wgzdata', 'Finished.', 'Canceled.', x, WGZ_SPINNER_ICON_SQUARE_BOUNCE)

# from welglanz.wgzcore.render.wgzprompt import wgz_prompt, wgz_password

# from welglanz.wgzcore.render.wgzselectable import wgz_select, wgz_multiselect, wgz_confirm, WgzSelectable

# from welglanz.wgzcore.render.wgzspinner import wgz_spinner

# from welglanz.wgzcore.wgzconsts import WGZ_SELECTABLE_ICON_DIAMOND, WGZ_SPINNER_ICON_FALLING_SAND

# # print(wgz_prompt('Your name: ', 'John Doe'))
# # print(wgz_password('Password: '))

# # print(wgz_select((WgzSelectable('Python', 'py', 'XD'), WgzSelectable('Java', 'java'))))

# # print(wgz_multiselect((WgzSelectable('Python', 'py', 'Recommended'),
# #                        WgzSelectable('Java', 'java', 'Recommended'),
# #                        WgzSelectable('C++', 'c++'),
# #                        WgzSelectable('C', 'c'),
# #                        WgzSelectable('Golang', 'go'))))

# # print(wgz_confirm(selectable_icon=WGZ_SELECTABLE_ICON_DIAMOND))

# def target(_, __):
#     for _1 in range(99999999):
#         if _.stop_required:
#             break

# wgz_spinner('Loading...', 'Finished.', 'Canceled!', target, WGZ_SPINNER_ICON_FALLING_SAND)
from time import sleep

from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn

text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
progress = Progress(text_column, bar_column, expand=True)

with progress:
    for n in progress.track(range(100)):
        progress.print(n)
        sleep(0.1)