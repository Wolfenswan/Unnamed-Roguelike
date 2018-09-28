""" Windows are temporary panels """
import textwrap

import tcod

from config_files import cfg, colors
from gameobjects.util_functions import entities_at_pos, entity_at_pos
from rendering.util_functions import center_x_for_text, draw_console_borders, pos_on_screen, print_string, dynamic_wrap


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
                sort_by = 'str', show_cancel_option=True, forced_width=None, extend_body=None,
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
    # TODO: Wrapping is sometimes odd, as it does consider the (later removed) %colorcoding%-strings when wrapping
    body_wrapped = dynamic_wrap(body, width - padding_x * 2, replace_whitespace=False)
    if extend_body:
        for line in extend_body:
            body_wrapped.extend([' ', line])

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
        #print_string(window, padding_x, y, line)
        print_string(window, padding_x, y, line)
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
            color = options_colors[i] if options_colors else colors.white
            print_string(window, padding_x, i + y, f'{line}', color=color)

    draw_console_borders(window, color=colors.white)
    print_string(window, padding_x, 0, f'{title}', color=title_color)

    if show_cancel_option:
        # print_string(window, 0, height - 1, '<ESC TO CANCEL>')
        string = '<ESC TO CANCEL>'
        x = center_x_for_text(width, string)
        print_string(window, x, height - 1, string)

    window_x, window_y = set_window_on_screen(window_x, window_y, width, height)
    tcod.console_blit(window, 0, 0, width, height, 0, window_x, window_y, 1, 1)

    tcod.console_flush()


def render_description_window(game):
    ent = None
    ents = entities_at_pos(game.npc_ents + game.architecture_ents, *game.cursor.pos)
    if ents:
        if len(ents) > 1:
            ent = entity_at_pos(ents, *game.cursor.pos)
        if len(ents) == 1 or ent is None:
            ent = ents[0]
        x, y = pos_on_screen(ent.x + 2, ent.y - 2, game.player)

        #title = f'{ent.char} {ent.name}'
        title = f' {ent.full_name} '
        body = ent.descr
        extend_body = ent.extended_descr(game)

        width = min(len(body), round(cfg.SCREEN_WIDTH//2))
        draw_window(title, body, window_x=x, window_y=y, forced_width=width, show_cancel_option=False, title_color=ent.color, extend_body=extend_body)

def render_equipment_window(equipment): # Experimental - Not implemented#

    x_coord = {
        # left side
        'torso': (0, 5, 28),
        'head': (0, 15, 28),
        'weapon_arm': (0, 40, 10),
        # right side
        'shield_arm': (85, 15, -10),
    }
    x_coord = {
        # left side
        'armor': cfg.MAP_SCREEN_WIDTH//2,
        'weapon': 0,
        'shield': cfg.MAP_SCREEN_WIDTH + 30,
        'belt': cfg.MAP_SCREEN_WIDTH//2
    }
    y_coord = {
        'torso': 10,
        'head': 2,
        'weapon_arm': 5,
        # right side
        'shield_arm': 5,
    }

    body = []
    
    for item_ent in equipment:
        type = item_ent.item.equipment.e_to # Entity.type is a enum member of the ItemType Class.
        #px, py = w_coord[type][0], w_coord[type][1]
        py = y_coord[item_ent.item.equipment.e_to]
        px = x_coord[item_ent.type.name.lower()]

        draw_window(item_ent.name, item_ent.descr, window_x=px, window_y=py, forced_width=30, show_cancel_option=False,
                    title_color=item_ent.color, extend_body=item_ent.item.attr_list(max_width=30))
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



