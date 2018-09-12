""" Windows are temporary panels """
import textwrap

import tcod

from config_files import cfg, colors
from gameobjects.util_functions import blocking_entity_at_pos
from rendering.util_functions import center_x_for_text, draw_console_borders, pos_on_screen


def set_window_on_screen(window_x, window_y, width, height):
    # if no coordinates have been passed, window will drawn at screen center
    if window_x is None or window_y is None:
        window_x = (cfg.SCREEN_WIDTH - width) // 2
        window_y = (cfg.SCREEN_HEIGHT - height) // 2
    elif window_x > cfg.SCREEN_WIDTH // 2:
        # Make sure the window does not cut off screen
        # width + 3 creates a minor offset to make sure the player is not concealed by the window
        window_x -= (width + 3)

    return window_x, window_y


def draw_window(title, body, options = None, window_x = None, window_y = None, padding_x = 2, padding_y = 2,
                sort_by = 'str', show_cancel_option=True, forced_width=None, extend_body = None,
                title_color=colors.white, options_colors=None):
    if not options:
        options  = []

    if not extend_body:
        extend_body = []

    # Calculate window width #
    if forced_width:
        width = forced_width + padding_x * 2
    else:
        # calculate total width for the box, using the longest unwrapped string from either all options, title or body
        if options or extend_body:
            width = max(len(string) for string in (options + extend_body + [title, body])) + 4 + padding_x * 2
        else:
            width = max(len(title), len(body)) + padding_x * 2

    #width = min(width, cfg.SCREEN_WIDTH//2)
    body_wrapped = textwrap.wrap(body, width - padding_x * 2)
    if extend_body:
        body_wrapped.extend(extend_body)

    # Calculate window height #
    height = padding_y * 2
    body_height = len(body_wrapped) if len(body_wrapped) else 0
    if body_height:
        height += body_height
    if options:
        height += len(options) + padding_y

    # Create the window #
    window = tcod.console_new(width, height)

    # Print the body to the window #
    y = padding_y
    for i, line in enumerate(body_wrapped):
        tcod.console_print(window, padding_x, y, line)
        y += 1

    # Print options to the window #
    if options:
        y += padding_y
        letter_index = ord('a')
        for i, option in enumerate(options):
            if isinstance(sort_by, str):
                line = f'({chr(letter_index)}) {option}'
                letter_index += 1  # by incrementing the ascii code for the letter, we go through the alphabet
            elif isinstance(sort_by, int):
                line = f'({str(i + 1)}) {option}'
            else:
                line = option
            if options_colors:
                tcod.console_set_color_control(tcod.COLCTRL_1, options_colors[i], colors.black)
            else:
                tcod.console_set_color_control(tcod.COLCTRL_1, colors.white, colors.black)
            tcod.console_print(window, padding_x, i + y, f'%c{line}%c' %(tcod.COLCTRL_1, tcod.COLCTRL_STOP))

    draw_console_borders(window, color=colors.white)
    tcod.console_set_color_control(tcod.COLCTRL_1, title_color, colors.black)
    tcod.console_print(window, padding_x, 0, f'%c{title}%c' %(tcod.COLCTRL_1, tcod.COLCTRL_STOP))

    if show_cancel_option:
        # tcod.console_print(window, 0, height - 1, '<ESC TO CANCEL>')
        string = '<ESC TO CANCEL>'
        x = center_x_for_text(width, string)
        tcod.console_print(window, x, height - 1, string)

    window_x, window_y = set_window_on_screen(window_x, window_y, width, height)
    tcod.console_blit(window, 0, 0, width, height, 0, window_x, window_y, 1, 1)

    tcod.console_flush()


def render_description_window(game):
    ent = blocking_entity_at_pos(game.entities, game.cursor.x, game.cursor.y)
    if ent:
        x, y = pos_on_screen(ent.x + 2, ent.y - 2, game.player)

        title = ent.name
        body = ent.descr

        width = min(len(body), cfg.SCREEN_WIDTH//3)

        draw_window(title, body, window_x=x, window_y=y, forced_width=width, show_cancel_option=False)

