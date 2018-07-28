""" Windows are temporary panels """
import textwrap

import tcod

from config_files import cfg, colors
from rendering.common_functions import center_x_for_text, draw_console_borders


def draw_options_window(caption, header, options, window_x = None, window_y = None, sort_by = 'letter', show_cancel_option=True, forced_width=None):
    padding_x = 5
    padding_y = 4

    # calculate total width for the box, using the longest unwrapped string from either all options or the caption
    width = forced_width if forced_width else max(len(option) for option in options + [caption, header]) + padding_x
    header_wrapped = textwrap.wrap(header, width - padding_x // 2)

    # calculate total height for the window
    header_height = len(header_wrapped) if len(header_wrapped) else 0
    height = len(options) + padding_y
    if header_height:
        height += header_height + padding_y // 2

    # if no coordinates have been passed, calculate center-screen
    if window_x is None or window_y is None:
        window_x = (cfg.SCREEN_WIDTH - width) // 2
        window_y = (cfg.SCREEN_HEIGHT - height) // 2
    else:
        # Make sure the window does not cut off screen
        if window_x > cfg.SCREEN_WIDTH//2:
            window_x -= width + 1
        else:
            window_x += 2

    window = tcod.console_new(width, height)

    y = 2
    for i, line in enumerate(header_wrapped):
        tcod.console_print(window, 1, y + i, line)

    if header_height:
        y = 3 + header_height

    letter_index = ord('a')
    for i, option in enumerate(options):
        if sort_by == 'letter':
            line = '(' + chr(letter_index) + ')' + option
            letter_index += 1  # by incrementing the ascii code for the letter, we go through the alphabet
        elif sort_by == 'number':
            line = '(' + str(i + 1) + ')' + option
        else:
            line = option
        tcod.console_print(window, 1, i + y, line)

    draw_console_borders(window, color=colors.white)
    tcod.console_print(window, 2, 0, caption)

    if show_cancel_option:
        #tcod.console_print(window, 0, height - 1, '<ESC TO CANCEL>')
        string = '<ESC TO CANCEL>'
        x = center_x_for_text(width, '<ESC TO CANCEL>')
        tcod.console_print(window, x, height - 1, string)

    tcod.console_blit(window, 0, 0, width, height, 0, window_x, window_y, 1, 0.7)