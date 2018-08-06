import tcod

from config_files import cfg
from game import GameStates
from rendering.util_functions import pos_on_screen
from rendering.render_windows import draw_window


def menu_loop(wait_for=None, cancel_with_escape=True, sort_by='str'):
    """
    The loop waits for a key input.
    If wait_for is an integer, it waits for a key that corresponds to an integer in range of (0, wait_for)
    If wait_for is a list of characters it waits for a key that corresponds to one of the characters.

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
        elif type(wait_for) == int:  # If menu is waiting to receive an index
            if type(sort_by) == str:
                index = ord(char) - ord('a')
                if 0 <= index < wait_for:
                    return index
            elif type(sort_by) == int:
                index = int(key.c - ord('1'))
                if 0 <= index < wait_for:
                    return index
        elif type(wait_for) == list:  # If menu is waiting for a specific key input
            if char.lower() in wait_for:
                return char


def inventory_menu(game):
    player = game.player
    inventory = player.inventory
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    options = [item.name for item in inventory.items]

    # TODO add optional filter
    # TODO allow cycling through filters

    if game.state == GameStates.SHOW_INVENTORY:
        body = 'Press the key next to an item to select it.'
    else:
        body = 'Press the key next to an item to drop it.'

    width = len(max(options, key=len))

    draw_window('Inventory', body, options=options, window_x=x, window_y=y, forced_width=max(width, 25))

    choice = menu_loop(wait_for=len(options))

    if choice is not None:
        return player.inventory.items[choice]
    else:
        return False


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


def equipment_menu(game):
    # TODO: Menu is a Placeholder #
    player = game.player
    inventory = player.paperdoll.equipped_items
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    options = [item.name for item in inventory]

    if game.state == GameStates.SHOW_INVENTORY:
        body = 'Press the key next to an item to select it.'
    else:
        body = 'Press the key next to an item to drop it.'

    width = len(max(options, key=len))

    draw_window('Equipment', body, options=options, window_x=x, window_y=y, forced_width=max(width, 25))

    choice = menu_loop(wait_for=len(options))

    if choice:
        return inventory[choice]
    else:
        return False


def item_menu(item_ent, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    title = item_ent.name
    body = item_ent.descr

    options = []
    wait_for = ['d']

    if item_ent.item.useable is not None and not player.in_combat(game):
        options.append('(U)se')
        wait_for.append('u')
    if item_ent.item.equipment is not None and not player.in_combat(game):
        if player.paperdoll.is_equipped(item_ent):
            options.append('(R)emove')
            wait_for.append('r')
        else:
            options.append('(E)quip')
            wait_for.append('e')
    options.append('(D)rop')

    draw_window(title, body, options=options, window_x=x, window_y=y, sort_by=None)

    choice = menu_loop(wait_for=wait_for)

    return choice
