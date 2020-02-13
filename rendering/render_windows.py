""" Windows are temporary panels """
from typing import Union, List, Optional

import tcod

from config_files import cfg, colors
from gameobjects.util_functions import entity_at_pos
from rendering.util_functions import center_x_for_text, draw_console_borders, pos_on_screen, print_string, dynamic_wrap


def set_window_on_screen(window_x, window_y, width, height):
    # if no coordinates have been passed, window will drawn at screen center
    if window_x is None or window_y is None:
        window_x = (cfg.SCREEN_WIDTH - width) // 2
        window_y = (cfg.SCREEN_HEIGHT - height) // 2
    # elif window_x < cfg.SCREEN_WIDTH // 2:
    # #     # Make sure the window does not cut off screen
    # #     # width + 3 creates a minor offset to make sure the player is not concealed by the window
    #      window_x -= width + 3
    # elif width + 4 > cfg.MAP_SCREEN_WIDTH//2:
    #     print(window_x, width)

    return window_x, window_y


def draw_window(title, body, game, options:Optional[List]=None,
                window_x:Optional[int]=None, window_y:Optional[int]=None, padding_x:Optional[int]=1, padding_y:Optional[int]=2,
                sort_by = 'str', show_cancel_option=True, forced_width:Optional[int]=None, title_color=colors.white, options_colors=None, clear_screen=False):

    # TODO param game -> root_console

    cancel_string = '<ESC TO CANCEL>'

    if clear_screen:
        game.root.clear()

    if options is None:
        options  = []

    # Calculate window width #
    if forced_width is not None:
        width = forced_width + padding_x * 2
    else:
        # calculate total width for the box, using the longest unwrapped string from either all possibly displayed strings
        all_strings = (options + [title, body])
        if show_cancel_option:
            all_strings.append(cancel_string)
        longest_string = max(all_strings, key=len)
        width = min(len(longest_string), round(cfg.SCREEN_WIDTH//2)) + padding_x * 2
        if longest_string in options:
            width += 4 # This accounts for the listing points (i.e.' (1) <option>')

    body_wrapped = dynamic_wrap(body, width-padding_x*2)
    options_wrapped = [dynamic_wrap(opt, width-padding_x*2-4) for opt in options] # substract 4 from width as otherwise the listing points break the wrapping

    # Calculate window height #
    height = padding_y * 2 + len(body_wrapped)
    if options:
        for opt in options_wrapped:
            height += len(opt) # opt is a list of strings
        if body_wrapped:
            height += 1 # gap between body-text and options

    # Create the window #
    window = tcod.console.Console(width, height)

    # Print the body to the window #
    y = padding_y
    if body_wrapped:
        for i, line in enumerate(body_wrapped):
            print_string(window, padding_x, y, line)
            y += 1
            if line.count('\n') > 0:
                y += 1
        if options:
            y += 1 # add a gap between body and options, if body exists

    # Print options to the window #
    if options:
        letter_idx = ord('a')
        line_idx = 0
        list_counter = 1
        for option in options_wrapped:
            if isinstance(sort_by, str):
                line = f'({chr(letter_idx)}) {option[0]}'
                letter_idx += 1  # cycle the alphabet by incrementing the ascii code referencing a letter
            elif isinstance(sort_by, int):
                line = f'({list_counter}) {option[0]}'
            else:
                line = option[0]

            color = options_colors[line_idx] if options_colors else colors.white
            print_string(window, padding_x, line_idx + y, f'{line}', color=color)
            line_idx += 1
            list_counter += 1

            if len(option) > 0: # if the option has been wrapped, add the following lines with sufficient spaces
                for line in option[1:]:
                    print_string(window, padding_x, line_idx + y, f'{" " * 4}{line}', color=color)
                    line_idx += 1

    draw_console_borders(window, color=colors.white)

    tcod.console_put_char(window, padding_x, 0, tcod.CHAR_TEEW)
    print_string(window, padding_x+1, 0, f'{title}', color=title_color)
    tcod.console_put_char(window, padding_x+len(title)+1, 0, tcod.CHAR_TEEE)

    if show_cancel_option:
        string = '<ESC TO CANCEL>'
        x = center_x_for_text(width, string)
        print_string(window, x, height - 1, string)

    window_x, window_y = set_window_on_screen(window_x, window_y, width, height)
    window.blit(game.root, window_x, window_y, 0, 0, width, height,)

    tcod.console_flush()

    return window


def render_description_window(game):
    ent = entity_at_pos(game.npc_ents + game.architecture_ents, *game.cursor.pos)
    if ent is not None:
        x, y = pos_on_screen(ent.x - 5, ent.y + 2, game.player)

        title = f'{ent.full_name}'
        body = ent.extended_descr(game)

        draw_window(title, body, game, window_x=x, window_y=y, show_cancel_option=False, title_color=ent.color)


# def render_equipment_window(equipment): # Experimental - Not implemented#
#
#     x_coord = {
#         # left side
#         'torso': (0, 5, 28),
#         'head': (0, 15, 28),
#         'weapon_arm': (0, 40, 10),
#         # right side
#         'shield_arm': (85, 15, -10),
#     }
#     x_coord = {
#         # left side
#         'armor': cfg.MAP_SCREEN_WIDTH//2,
#         'weapon': 0,
#         'shield': cfg.MAP_SCREEN_WIDTH + 30,
#         'belt': cfg.MAP_SCREEN_WIDTH//2
#     }
#     y_coord = {
#         'torso': 10,
#         'head': 2,
#         'weapon_arm': 5,
#         # right side
#         'shield_arm': 5,
#     }
#
#     body = []
#
#     for item_ent in equipment:
#         type = item_ent.item.equipment.e_to # Entity.type is a enum member of the ItemType Class.
#         #px, py = w_coord[type][0], w_coord[type][1]
#         py = y_coord[item_ent.item.equipment.e_to]
#         px = x_coord[item_ent.type.name.lower()]
#
#         draw_window(item_ent.name, item_ent.descr, game, window_x=px, window_y=py, forced_width=30, show_cancel_option=False,
#                     title_color=item_ent.color)
        #
        # descr_wrapped = textwrap.wrap(item_ent.descr, width)
        # height = len(descr_wrapped)
        #
        # window = tdl.Window(gv.root, px, py, width, height)
        # # window.caption = type.title() + ':'
        # window.caption = '({0}) {1}'.format(character, item_ent.name)
        # window.border_color = settings.PANELS_BORDER_COLOR
        #
        # setup_panel(window)
    
        # window.draw_str(1,2,'{0}'.format(item_ent.name))
        #
        # y = 2
        # lines = draw_wrapped_text(window, item_ent.description, width, o_y=y)
        #
        # y += 1 + lines
        # # if getattr(item_ent, 'weight', 0):
        # # lines = draw_wrapped_text(window, 'It is {0}.'.format(item_ent.get_weight_as_string()), window.width - 2, o_y=y)
        # # y += lines + 2
        #
        # if getattr(item_ent, 'slots', 0):
        #     lines = draw_wrapped_text(window, 'It has {0} pockets for quick access.'.format(item_ent.slots),
        #                               window.width - 2, o_y=y)
        #     y += lines + 2
        #
        # dist = w_coord[type][2]
        # if dist > 0:
        #     for i in range(dist):
        #         gv.root.draw_char(px + width + i, py + 2, '196', bg=None, fg=colors.grey)
        # else:
        #     for i in range(-dist):
        #         gv.root.draw_char(px - i, py + 2, '196', bg=None, fg=colors.grey)



