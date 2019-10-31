from typing import Union

import tcod

from config_files import cfg, colors
from loader_functions.data_loader import save_game
from loader_functions.initialize_font import initialize_font, all_fonts
from rendering.util_functions import pos_on_screen
from rendering.render_windows import draw_window


def input_loop(wait_for=None, cancel_with_escape=True, sort_by:Union[int, str]= 'string'):
    """
    The loop waits for a key input.
    If wait_for is an integer, it waits for a key that corresponds to an integer in range of (0, wait_for)
    If wait_for is a list of characters or tcod key codes it waits for a key that corresponds to one of the characters or key codes.

    :param wait_for: whether to wait for any integer, any string or a specific list of inputs
    :type wait_for: int, str, list
    :return: int if waiting for int, str if waiting for str or specific list of inputs, True for enter, None for Escape (if cancel_with_escape is True)
    :rtype: int, str, True, None
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
        # TODO accept backspace
        elif key.vk == tcod.KEY_KPENTER:
            return True
        elif isinstance(wait_for, int):  # If menu is waiting to receive an index
            if isinstance(sort_by, str):  # if sorting is using letters, return index according to letter position
                index = ord(char) - ord('a')
                if 0 <= index < wait_for:
                    return index
            elif isinstance(sort_by, int):  # otherwise convert the input into an integer directly
                index = int(key.c - ord('1'))
                if 0 <= index < wait_for:
                    return index
        elif isinstance(wait_for, str):  # If menu is waiting for any string
            return char.lower()
        elif isinstance(wait_for, list):  # If menu is waiting for a specific key input
            if char.lower() in wait_for:
                return char
            if key.vk in wait_for:
                return key.vk


def generic_options_menu(title:str, body:str, options:list, game, sort_by:Union[str, int]='str', cancel_with_escape=True, clear_screen=False):
    window = draw_window(title, body, game, options, show_cancel_option=cancel_with_escape, sort_by=sort_by, clear_screen=clear_screen)

    choice = input_loop(wait_for=len(options), sort_by=sort_by, cancel_with_escape=cancel_with_escape)

    return choice


def yesno_menu(title, body, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    options = ['(Y)es', '(N)o']
    wait_for = ['y', 'n']

    draw_window(title, body, game, options, window_x=x, window_y=y, forced_width=len(body), sort_by=None)

    choice = input_loop(wait_for=wait_for)

    return True if choice == 'y' else False


def item_list_menu(entity, item_list, game, title='Inventory', body='Press the key next to an item to select it.', colorize_options=True):
    # TODO add optional filter
    # TODO allow cycling through filters

    x, y = pos_on_screen(entity.x + 2, entity.y - 2, entity)

    options = [f'{item.char} {item.full_name}' for item in item_list]
    if colorize_options:
        options_colors = [item.color for item in item_list]
    else:
        options_colors = None

    width = len(max(options, key=len)) + 4 if options else 0
    draw_window(title, body, game, options=options, window_x=x, window_y=y, forced_width=width, options_colors=options_colors)

    choice = input_loop(wait_for=len(options))

    if choice is not None:
        return item_list[choice]
    else:
        return False


def item_menu(item_ent, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    title = f'{item_ent.char} {item_ent.full_name}'
    body = item_ent.extended_descr(game)

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

    width = min(len(body), round(cfg.SCREEN_WIDTH // 2.5))
    draw_window(title, body, game, options=options, window_x=x, window_y=y, sort_by=None, forced_width=width, title_color=item_ent.color)

    choice = input_loop(wait_for=wait_for)

    return choice


def options_menu(game):
    choice = generic_options_menu('Game Options', '',
                                  ['Toggle Fullscreen', 'Change Font', f'Configure Debug Options'], game,
                                  sort_by=1, clear_screen=True)
    if choice == 0:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif choice == 1:
        available_fonts = all_fonts()
        font_id = generic_options_menu('Font Selection', f'Default font:\n{cfg.FONT_DEFAULT.capitalize()}',
                                       available_fonts, game,
                                       sort_by=1, clear_screen=True)
        if font_id is not None:
            initialize_font(available_fonts[font_id])
    elif choice == 2:
        debug_menu(game, clear=True)

    # Unless menu was exited with ESC, the menu remains open
    if choice is not None:
        options_menu(game)


def debug_menu(game, clear=False):
    options = []
    for k, v in game.debug.items():
        options.append(f'{"Enable" if v is False else "Disable"} {k.replace("_"," ").title()}')
    choice = generic_options_menu('Debug Options','' , options, game, sort_by=1, clear_screen=clear)

    if choice in range(0,len(options)):
        key = list(game.debug)[choice]
        game.debug[key] = not game.debug[key]

    if choice is not None:
        debug_menu(game, clear=clear)


def main_menu(game):
    choice = generic_options_menu(cfg.GAME_NAME, 'Welcome to the Dungeon',
                                  ['Play a new game', 'Continue last game', 'Game Options', 'Quit'], game, cancel_with_escape=False,
                                  sort_by=1, clear_screen=True)
    # Choice 0 or 1 are returned to engine.py, prompting a new game or loading a game
    if choice == 2:
        options_menu(game)
    else:
        return choice


def ingame_menu(game, can_save=True):
    title = cfg.GAME_NAME
    body = f'You are on level {game.dlvl} at turn {game.turn}.' # TODO expand
    options = ['Show Options']
    if can_save:
        options.extend(['Save & Quit','Just Quit'])
    else:
        options.append('Quit to Title')
    choice = generic_options_menu(title, body, options, game,
                              sort_by=1, cancel_with_escape=True)
    if choice == 0:
        options_menu(game)
    elif choice in [1,2]:
        if can_save:
            save_game(game)
        return False
    return True


def input_prompt(game, title="Input prompt", body="Provide your input and finish with enter"):
    input_str =''
    input = input_loop(wait_for=str, cancel_with_escape=False)

    if isinstance(input, str):
        input_str += input
    # elif input is backspace: TODO
    #     input_str[:-1]
    elif input is True:
        return input  # Todo confirmation prompt