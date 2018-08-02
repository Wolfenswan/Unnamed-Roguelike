""" Translates key events into game-related actions """

# TODO Consider using tdl for event handling instead? Might allow using a large dictionary instead of if/elif snake

import tcod

from game import GameStates


def handle_keys(key, game_state):
    # Inputs valid in all game states #
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # Game state specific inputs #
    if game_state in [GameStates.PLAYERS_TURN, GameStates.PLAYER_RESTING, GameStates.CURSOR_ACTIVE]:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    # elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.SHOW_ITEM):
    #     return handle_menu_keys(key)
    # elif game_state == GameStates.TARGETING:
    #     results = dict(handle_targeting_keys())

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)
    
    action = 'move' if not key.lctrl else 'interact'

    if key.vk == tcod.KEY_UP or key_char == 'k' or key.vk == tcod.KEY_KP8:
        return {action: (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 'j' or key.vk == tcod.KEY_KP2:
        return {action: (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'h' or key.vk == tcod.KEY_KP4:
        return {action: (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'l' or key.vk == tcod.KEY_KP6:
        return {action: (1, 0)}
    elif key_char == 'y' or key.vk == tcod.KEY_KP7:
        return {action: (-1, -1)}
    elif key_char == 'u' or key.vk == tcod.KEY_KP9:
        return {action: (1, -1)}
    elif key_char == 'b' or key.vk == tcod.KEY_KP1:
        return {action: (-1, 1)}
    elif key_char == 'n' or key.vk == tcod.KEY_KP3:
        return {action: (1, 1)}
    elif key.vk == tcod.KEY_KP5:
        return {'rest': True}

    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'e' and key.shift:
        return {'show_equipment': True}
    elif key_char == 's':
        return {'toggle_look': True}
    elif key.vk in [tcod.KEY_ENTER, tcod.KEY_KPENTER]:
        return {'confirm': True}
    # elif key_char == 'd':
    #     return {'drop_inventory': True}

    # No key was pressed
    return {}


# def handle_menu_keys(key):
#     return {'menu_selection': key.c}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    return {}

#
# def handle_targeting_keys():
#     return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
