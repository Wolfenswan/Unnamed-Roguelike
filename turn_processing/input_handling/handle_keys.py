""" Translates key events into game-related actions """

# TODO Consider using tdl for event handling instead? Might allow using a large dictionary instead of if/elif snake
import logging

import tcod
import tcod.event as e

from game import GameState
from map.directions_util import Direction
from turn_processing.input_handling.input_keys import keys_dict


def handle_keys(key_event, game_state):
    # logging.debug(f'Handling {key}')

    # Inputs valid in all game states #
    key = key_event.sym
    mod = key_event.mod

    # if key.vk == tcod.KEY_ENTER and key.lalt:
    #     # Alt+Enter: toggle full screen
    #     return {'fullscreen': True}
    # elif key.vk == tcod.KEY_ESCAPE:
    #     # Exit the game
    #     return {'exit': True}
    # elif chr(key.c) == keys_dict['manual'] and key.shift:
    #     return {'manual': True}
    # elif chr(key.c) == keys_dict['debug'] and key.lalt:
    #     return {'debug': True}


    # Game state specific inputs #
    # if game_state in [GameState.PLAYERS_TURN, GameState.PLAYER_RESTING, GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]:
    #     return handle_player_turn_keys(key)
    # elif game_state == GameState.PLAYER_DEAD:
    #     return handle_player_dead_keys(key)
    # elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.SHOW_ITEM):
    #     return handle_menu_keys(key)
    # elif game_state == GameStates.TARGETING:
    #     results = dict(handle_targeting_keys())

    return {}

def handle_keys_legacy(key, game_state):
    logging.debug(f'Handling {key}, with state {game_state}')

    # Inputs valid in all game states #
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    elif chr(key.c) == keys_dict['map']:
        return {'toggle_map': True}
    elif chr(key.c) == keys_dict['manual'] and key.shift:
        return {'manual': True}
    elif chr(key.c) == keys_dict['spawn'] and key.lalt:
        return {'spawn': True}
    elif chr(key.c) == keys_dict['debug'] and key.lctrl:
        return {'debug': True}


    # Game state specific inputs #
    if game_state in [GameState.PLAYER_ACTIVE, GameState.PLAYER_RESTING, GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]:
        return handle_player_turn_keys(key)
    elif game_state == GameState.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    # elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.SHOW_ITEM):
    #     return handle_menu_keys(key)
    # elif game_state == GameStates.TARGETING:
    #     results = dict(handle_targeting_keys())

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement Modifiers #
    action = 'move'
    if key.lctrl or key.rctrl:
        action = 'interact'
    # elif key.lalt:
    #     action = 'dodge'

    # Movement #
    if key.vk == tcod.KEY_UP or key_char == keys_dict['vim_up'] or key.vk == tcod.KEY_KP8:
        return {action: True, 'dir': Direction.UP.value}
    elif key.vk == tcod.KEY_DOWN or key_char == keys_dict['vim_down'] or key.vk == tcod.KEY_KP2:
        return {action: True, 'dir': Direction.DOWN.value}
    elif key.vk == tcod.KEY_LEFT or key_char == keys_dict['vim_left'] or key.vk == tcod.KEY_KP4:
        return {action: True, 'dir': Direction.LEFT.value}
    elif key.vk == tcod.KEY_RIGHT or key_char == keys_dict['vim_right'] or key.vk == tcod.KEY_KP6:
        return {action: True, 'dir': Direction.RIGHT.value}
    elif key_char == keys_dict['vim_lup'] or key.vk == tcod.KEY_KP7:
        return {action: True, 'dir': Direction.UP_LEFT.value}
    elif key_char == keys_dict['vim_rup'] or key.vk == tcod.KEY_KP9:
        return {action: True, 'dir': Direction.UP_RIGHT.value}
    elif key_char == keys_dict['vim_ldown'] or key.vk == tcod.KEY_KP1:
        return {action: True, 'dir': Direction.DOWN_LEFT.value}
    elif key_char == keys_dict['vim_rdown'] or key.vk == tcod.KEY_KP3:
        return {action: True, 'dir': Direction.DOWN_RIGHT.value}
    elif key_char == keys_dict['down']:
        return {'level_change':+1}
    elif key_char == keys_dict['up']:
        return {'level_change':-1}
    elif key.vk == tcod.KEY_KP5 or key_char == keys_dict['wait']:
        return {'wait': True}

    # Inventory Quick Use #
    elif key_char in ['1','2','3','4','5','6','7','8','9']:
        return {'quick_use': int(key_char)}

    # Toggles #
    elif key.vk == tcod.KEY_TAB:
        return {'toggle_weapon': True}
    elif key_char == keys_dict['block']:
        return {'toggle_block': True}
    elif key_char == keys_dict['dash']:
        return {'toggle_dash': True}
    elif key_char == keys_dict['look']:
        return {'toggle_look': True}
    elif key_char == keys_dict['fire']:
        return {'toggle_fire': True}

    # Item & Inventory Interaction #
    if key_char == keys_dict['get']:
        return {'pickup': True}
    elif key_char == keys_dict['inventory']:
        return {'show_inventory': True}
    elif key_char == keys_dict['equip'] and key.shift:
        return {'show_equipment': True}
    elif key_char == keys_dict['equip'] and not key.shift:
        return {'equip': True}
    elif key_char == keys_dict['prepare'] and key.shift:
        return {'show_prepared': True}
    elif key_char == keys_dict['prepare'] and not key.shift:
        return {'prepare': True}

    # General Keys #
    elif key.vk in [tcod.KEY_ENTER, tcod.KEY_KPENTER]:
        return {'confirm': True}

    # No key was pressed
    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == keys_dict['inventory']:
        return {'show_inventory': True}

    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
