""" Windows are temporary panels """
import textwrap

import tcod

from config_files import cfg, colors
from rendering.common_functions import center_x_for_text, draw_console_borders


def draw_window(window, caption, window_x, window_y, width, height, show_cancel_option):
    draw_console_borders(window, color=colors.white)
    tcod.console_print(window, 2, 0, caption)

    if show_cancel_option:
        #tcod.console_print(window, 0, height - 1, '<ESC TO CANCEL>')
        string = '<ESC TO CANCEL>'
        x = center_x_for_text(width, '<ESC TO CANCEL>')
        tcod.console_print(window, x, height - 1, string)

    tcod.console_blit(window, 0, 0, width, height, 0, window_x, window_y, 1, 1)

    tcod.console_flush()

def draw_options_window(caption, body, options, window_x = None, window_y = None, sort_by = 'letter', show_cancel_option=True, forced_width=None):
    padding_x = 5
    padding_y = 4
    width = max(len(option) for option in options + [caption, body]) + padding_x

    # calculate total width for the box, using the longest unwrapped string from either all options or the caption
    if forced_width:
        width = forced_width + padding_x

    body_wrapped = textwrap.wrap(body, width - padding_x // 2)

    # calculate total height for the window
    body_height = len(body_wrapped) if len(body_wrapped) else 0
    height = len(options) + padding_y
    if body_height:
        height += body_height + padding_y // 2

    # if no coordinates have been passed, calculate center-screen
    if window_x is None or window_y is None:
        window_x = (cfg.SCREEN_WIDTH - width) // 2
        window_y = (cfg.SCREEN_HEIGHT - height) // 2
    else:
        # Make sure the window does not cut off screen
        # width + 3creates a minor offset to make sure the player is not concealed by the window
        if window_x > cfg.SCREEN_WIDTH//2:
            window_x -= width + 3

    window = tcod.console_new(width, height)

    y = 2
    for i, line in enumerate(body_wrapped):
        tcod.console_print(window, 1, y + i, line)

    if body_height:
        y = 3 + body_height

    letter_index = ord('a')
    for i, option in enumerate(options):
        if sort_by == 'letter':
            line = '(' + chr(letter_index) + ') ' + option
            letter_index += 1  # by incrementing the ascii code for the letter, we go through the alphabet
        elif sort_by == 'number':
            line = '(' + str(i + 1) + ') ' + option
        else:
            line = option
        tcod.console_print(window, 1, i + y, line)

    draw_window(window, caption, window_x, window_y, width, height, show_cancel_option)



