import logging
import re
import textwrap
from random import uniform

import tcod
from tcod import Color

from config_files import colors
from rendering import render_constants as cons


def center_x_for_text(width, text, padding=0):
    """returns the x for a text centered in the passed width"""
    x = padding + (width - len(text)) // 2
    return x


def get_names_under_cursor(mouse, entities, fov_map):
    # TODO get names under cursor
    # TODO description window for NPCs
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and entity.is_visible(fov_map)]
    names = ', '.join(names)

    return names.title()


def setup_console(con, caption=None, fgcolor=tcod.white, bgcolor =tcod.black, borders=False, bordercolor = colors.dark_gray):
    con.default_fg = fgcolor
    con.default_bg = bgcolor
    con.clear()
    if borders:
        draw_console_borders(con, color = bordercolor)
    if caption:
        print_line(con, 2, 0, caption, color=fgcolor)


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
    x = max(cons.MAP_SCREEN_WIDTH // 2 + (x - player.x), 0)
    y = max(cons.MAP_SCREEN_HEIGHT // 2 + (y - player.y), 0)

    return x, y


def multiply_rgb_color(color, factor_range = (0, 0.25), darken=False):
    factor = uniform(*factor_range)
    if darken:
        color = (int(v * (1 - factor)) for v in color)
    else:
        color = (int(v + (255 - v) * factor) for v in color)
    color = tcod.Color(*color)
    return color


COLOR_WRAP_PATTERN = re.compile(
r"""
%{1}            # % indicating beginning of color-code
\w+             # the color (either name or Color()
[(\d,\s)]*      # Optional: The tuple for Color()
%{1}            # % indicating end of color-code
[.()+:\s\w-]+    # the word or string to color
%{2}            # %% indicating end of color-wrapping
""", re.X)

# %{1}\w+%{1}([()+:\s\w-]+%{2})
color_code_pattern = re.compile('%{1}(\w+[(\d,\s)]*)%{1}')


def dynamic_wrap(string, max_width):
    """
    This function makes sure that textwrap.wrap() does ignore formatting strings
    such as %c and %color% when wrapping words.

    # BUG line breaks through color-wrapped words break colorization (workaround could be color-wrapping each word individually - but that would be a false positives nightmare)
    """

    if len(string) == 0:
        return []

    codes = {} # codes makes a temporary copy of all color coded strings, so they can safely be removed before wrapping, then reapplied
    color_coded_words = COLOR_WRAP_PATTERN.findall(string)

    for coded_string in color_coded_words:
        color_code = color_code_pattern.match(coded_string)
        stripped_code = coded_string.replace(color_code.group(),'') # Replace the leading marker, e.g. %dark_red%
        stripped_code = stripped_code.replace('%%','') # replacing the trailing marker (%%)
        string = string.replace(coded_string,stripped_code) # Remove all color code wrappers from the string
        codes[stripped_code] = coded_string # pair the "bare" string as key with the color-coded string as value
        codes[f'{stripped_code}#uses'] = codes.get(f'{stripped_code}#uses', 0) + 1 # the name#uses key counts how often the string needs to be replaced. It is neccessary in order to avoid false partial hits in longer paragraphs.

    # Split the string at pre-defined line-breaks to preserve indentation.
    split_str = string.split('\n')
    wrapped = []
    # Create a textwrap-list, using the new string without color-wrappers
    for sub_str in split_str:
        if sub_str == '':
            wrapped.append(' ')
        else:
            wrapped.extend(textwrap.wrap(sub_str, max_width, replace_whitespace=False))

    # Re-add the color-wrapped strings
    if codes:
        for i, line in enumerate(wrapped):
            for k in codes.keys():
                if k in line and codes[f'{k}#uses'] > 0:
                    line = line.replace(k, codes[k])
                    wrapped[i] = line
                    codes[f'{k}#uses'] -= 0
    
    return wrapped


def print_line(con, x, y, string, max_length=None, color=None, fgcolor=colors.white, bgcolor=colors.black, color_coefficient=None, alignment=tcod.LEFT, background=tcod.BKGND_DEFAULT):
    """
    Prints a string to tcods console, supporting custom color-code wrappers.
    """

    color_coded_words = COLOR_WRAP_PATTERN.findall(string)

    col_ctrls = ()

    if color_coded_words:
        for i, word in enumerate(color_coded_words):
            color_code = color_code_pattern.match(word)
            if color_code.group(1)[0:5] == 'Color': # if the string is wrapped as %Color(int,int,int)%String%%
                color_str = eval(color_code.group(1))
            else: # if the string is wrapped as %color_name%String%%
                color_str = eval(f'colors.{color_code.group(1)}') # Resolve the color-code as a config.colors.py entry: %red%->Color(colors.red)
            if color_coefficient:
                color_str = tuple(int(color_coefficient * x) for x in color_str)
            new_word = word.replace(color_code.group(), '%c') # Replace the custom color-code with tcod's color-wrappers: %red%word% -> %cword%c
            new_word = new_word.replace('%%', '%c')
            string = string.replace(word, new_word) # Update the original string
            col_ctrl = eval(f'tcod.COLCTRL_{i+1}')
            tcod.console_set_color_control(col_ctrl, color_str, bgcolor)
            col_ctrls += (col_ctrl, tcod.COLCTRL_STOP)

    if color:
        if not '%c' in string: # If no tcod wrappers are present, wrap the entire string
            string = f'%c{string}%c'
        if color_coefficient:
            color = tuple(int(color_coefficient * x) for x in color)
        tcod.console_set_color_control(tcod.COLCTRL_1, color, bgcolor)
        col_ctrls = (tcod.COLCTRL_1, tcod.COLCTRL_STOP)

    string = string % col_ctrls

    if fgcolor and color_coefficient:
        fgcolor = tuple(int(color_coefficient * x) for x in fgcolor)

    if max_length is not None and len(string) > max_length:
        string = dynamic_wrap(string,max_length)

    con.print(x, y, string, fg=fgcolor, alignment=alignment, bg_blend=background)