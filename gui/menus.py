import tcod

from config_files import cfg
from rendering.util_functions import pos_on_screen
from rendering.render_windows import draw_window


def menu_loop(wait_for=None, cancel_with_escape=True, sort_by='str'):
    """
    The loop waits for a key input.
    If wait_for is an integer, it waits for a key that corresponds to an integer in range of (0, wait_for)
    If wait_for is a list of characters or tcod key codes it waits for a key that corresponds to one of the characters or key codes.

    :param wait_for:
    :type wait_for: int or list
    :return:
    :rtype: int or str
    """
    key = tcod.Key()

    while True:
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, '', False)
        char = chr(key.c)
        if key.vk == tcod.KEY_ESCAPE and cancel_with_escape:
            return None
        # elif type(wait_for) is dict:
        #     if char.lower() in wait_for.keys():
        #         return wait_for[char]
        elif isinstance(wait_for, int):  # If menu is waiting to receive an index
            if isinstance(sort_by, str):
                index = ord(char) - ord('a')
                if 0 <= index < wait_for:
                    return index
            elif isinstance(sort_by, int):
                index = int(key.c - ord('1'))
                if 0 <= index < wait_for:
                    return index
        elif isinstance(wait_for, list):  # If menu is waiting for a specific key input
            if char.lower() in wait_for:
                return char
            if key.vk in wait_for:
                return key.vk


def options_menu(title, body, options, sort_by='str', cancel_with_escape=True):
    draw_window(title, body, options, show_cancel_option=cancel_with_escape, sort_by=sort_by)

    choice = menu_loop(wait_for=len(options), sort_by=sort_by, cancel_with_escape=cancel_with_escape)
    return choice


def yesno_menu(title, body, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    options = ['(Y)es', '(N)o']
    wait_for = ['y', 'n']

    draw_window(title, body, options, window_x=x, window_y=y, forced_width=len(body), sort_by=None)

    choice = menu_loop(wait_for=wait_for)

    return True if choice == 'y' else False


def item_list_menu(entity, item_list, title='Inventory', body='Press the key next to an item to select it.', colorize_options=True):
    # TODO add optional filter
    # TODO allow cycling through filters

    x, y = pos_on_screen(entity.x + 2, entity.y - 2, entity)

    options = [item.full_name for item in item_list]
    if colorize_options:
        options_colors = [item.color for item in item_list]
    else:
        options_colors = None

    width = len(max(options, key=len)) + 4 if options else 0

    draw_window(title, body, options=options, window_x=x, window_y=y, forced_width=width, options_colors=options_colors)

    choice = menu_loop(wait_for=len(options))

    if choice is not None:
        return item_list[choice]
    else:
        return False

# def inventory_menu(entity, title='Inventory'):
#     inventory = entity.inventory
#     x, y = pos_on_screen(entity.x + 2, entity.y - 2, entity)
#
#     options = [item.name for item in inventory.items]
#     options_colors = [item.color for item in inventory.items]
#
#     # TODO add optional filter
#     # TODO allow cycling through filters
#
#     body = 'Press the key next to an item to select it.'
#
#     width = len(max(options, key=len)) + 4 if options else 0
#
#     draw_window(title, body, options=options, window_x=x, window_y=y, forced_width=width, options_colors=options_colors)
#
#     choice = menu_loop(wait_for=len(options))
#
#     if choice is not None:
#         return inventory.items[choice]
#     else:
#         return False
#
#
# def equipment_menu(entity):
#     # TODO: Menu will be expanded to provide more detailled information #
#     inventory = entity.paperdoll.equipped_items
#     x, y = pos_on_screen(entity.x + 2, entity.y - 2, entity)
#
#     body = 'Press the key next to an item to select it.'
#     options = [item.name for item in inventory]
#     options_colors = [item.color for item in inventory]
#
#     width = len(max(options, key=len)) + 4
#
#     draw_window('Equipment', body, options=options, window_x=x, window_y=y, forced_width=width, options_colors=options_colors)
#
#     choice = menu_loop(wait_for=len(options))
#
#     if choice is not None:
#         return inventory[choice]
#     else:
#         return False


def item_menu(item_ent, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    title = item_ent.full_name
    body = item_ent.descr

    options = []
    wait_for = []

    if item_ent.item.useable is not None:
        if item_ent in player.qu_inventory:
            if not player.in_combat(game):
                options.append('Un-(p)repare')
                wait_for.append('p')
            options.append('(U)se')
            wait_for.append('u')

        elif item_ent in player.inventory and not player.in_combat(game):
            options.append('(P)repare')
            wait_for.append('p')
            options.append('(U)se')
            wait_for.append('u')

    if item_ent.item.equipment is not None and not player.in_combat(game):
        if player.paperdoll.is_equipped(item_ent):
            options.append('(R)emove')
            wait_for.append('r')
            options.append('(D)rop')
            wait_for.append('d')
        else:
            options.append('(E)quip')
            wait_for.append('e')

    if not item_ent in player.paperdoll.equipped_items:
        options.append('(D)rop')
        wait_for.append('d')

    width = min(len(body), round(cfg.SCREEN_WIDTH//2.5))
    draw_window(title, body, options=options, window_x=x, window_y=y, sort_by=None, forced_width=width,
                extend_body = item_ent.item.attr_list(max_width=width), title_color=item_ent.color)

    choice = menu_loop(wait_for=wait_for)

    return choice