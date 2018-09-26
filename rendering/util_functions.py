import textwrap
from random import uniform

import tcod
import re

from config_files import colors, cfg as cfg


def center_x_for_text(width, text, padding=0):
    """returns the x for a text centered in the passed width"""
    x = padding + (width - len(text)) // 2
    return x


def get_names_under_mouse(mouse, entities, fov_map):
    # TODO get names under cursor
    # TODO description window for NPCs
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.title()


def setup_console(con, caption=None, fgcolor=tcod.white, bgcolor =tcod.black, borders=False, bordercolor = colors.dark_gray):
    tcod.console_set_default_foreground(con, fgcolor)
    tcod.console_set_default_background(con, bgcolor)
    tcod.console_clear(con)
    if borders:
        draw_console_borders(con, color = bordercolor)
    if caption:
        print_string(con, 2, 0, caption)


def draw_console_borders(con, width=None, height=None, color=colors.dark_grey, bgcolor=colors.black):
    """ draws an outline around the passed console. By default, the console's width & height will be used """
    #tcod.console_set_default_foreground(con, color)

    if width is None:
        width = con.width
    if height is None:
        height = con.height

    for x in range(width):
        tcod.console_put_char_ex(con, x, 0, 196, color, bgcolor)
        tcod.console_put_char_ex(con, x, height - 1, 196, color, bgcolor)

    for y in range(height):
        tcod.console_put_char_ex(con, 0, y, 179, color, bgcolor)
        tcod.console_put_char_ex(con, width - 1, y, 179, color, bgcolor)

    tcod.console_put_char_ex(con, 0, 0, 218, color, bgcolor)
    tcod.console_put_char_ex(con, width - 1, 0, 191, color, bgcolor)
    tcod.console_put_char_ex(con, 0, height - 1, 192, color, bgcolor)
    tcod.console_put_char_ex(con, width - 1, height - 1, 217, color, bgcolor)


def pos_on_screen(x, y, player):
    """
    Returns coordinate on the visible screen, in relation to the player

    """
    x = max(cfg.MAP_SCREEN_WIDTH // 2 + (x - player.x), 0)
    y = max(cfg.MAP_SCREEN_HEIGHT // 2 + (y - player.y), 0)

    return x, y


def randomize_rgb_color(color, factor_range = (0, 0.25), darken=False):
    factor = uniform(*factor_range)
    if darken:
        color = (int(v * (1 - factor)) for v in color)
    else:
        color = (int(v + (255 - v) * factor) for v in color)
    color = tcod.Color(*color)
    return color


def dynamic_wrap(string, max_width, replace_whitespace=False):
    """
    This function makes sure that textwrap.wrap() does ignore formatting strings
    such as %c and %color% when wrapping words.
    """
    codes ={}
    color_coded_words = re.findall('(%{1}\w+%{1}[()+:\s\w-]+%{1})', string)
    for coded_string in color_coded_words:
        color_code = re.search('(%{1}\w+%{1})', coded_string)
        stripped_code = coded_string.replace(color_code.group(),'')
        stripped_code = stripped_code.replace('%','')
        string = string.replace(coded_string,stripped_code)
        codes[stripped_code] = coded_string

    wrapped = textwrap.wrap(string, max_width, replace_whitespace=replace_whitespace)

    # Re-add the formatting strings
    for i, line in enumerate(wrapped):
        for k in codes.keys():
            if k in line:
                line = line.replace(k, codes[k])
                wrapped[i] = line

    return wrapped


def print_string(con, x, y, string, color=None, bgcolor=colors.black, alignment=tcod.LEFT, background=tcod.BKGND_DEFAULT):

    color_coded_words = re.findall('(%{1}\w+%{1}[()+:\s\w-]+%{1})', string) # Catches any string of %color%string%
    if color_coded_words:
        col_ctrls = ()
        for i, word in enumerate(color_coded_words):
            color_code = re.match('%{1}(\w*)%{1}', word)
            color_str = eval(f'colors.{color_code.group(1)}') # Resolve the color-code as a config.colors.py entry: %red%->colors.red
            new_word = word.replace(color_code.group(), '%c') + 'c' # Replace the custom color-code with tcod's color-wrappers: %red%word% -> %cword%c
            string = string.replace(word, new_word) # Update the original string
            col_ctrl = eval(f'tcod.COLCTRL_{i+1}')
            tcod.console_set_color_control(col_ctrl, color_str, bgcolor)
            col_ctrls += (col_ctrl, tcod.COLCTRL_STOP)
        string = string % col_ctrls

    if color:
        if not '%c' in string: # If no tcod wrappers are present, wrap the entire string
            string = f'%c{string}%c'
        tcod.console_set_color_control(tcod.COLCTRL_1, color, bgcolor)
        string = string % (tcod.COLCTRL_1, tcod.COLCTRL_STOP)

    tcod.console_print_ex(con, x, y, background, alignment, string)