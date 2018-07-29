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
    if game_state in [GameStates.PLAYERS_TURN, GameStates.PLAYER_RESTING]:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    if key.vk == tcod.KEY_UP or key_char == 'k' or key.vk == tcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 'j' or key.vk == tcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'h' or key.vk == tcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'l' or key.vk == tcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key_char == 'y' or key.vk == tcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key_char == 'u' or key.vk == tcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key_char == 'b' or key.vk == tcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key_char == 'n' or key.vk == tcod.KEY_KP3:
        return {'move': (1, 1)}
    elif key.vk == tcod.KEY_KP5:
        return {'rest': True}

    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'd':
        return {'drop_inventory': True}

    # No key was pressed
    return {}

def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    return {}

def handle_targeting_keys(key):
    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}

'''
def handle_keys(user_input):
    """ Handles all key input made by the player """

    #logging.debug('User_input: {0}'.format(user_input)
    key = user_input.vk
    char = user_input.c
    text = user_input.text

    print(user_input.vk)

    # directions related to all movement keys
    MOVE_DICT = {
        # arrow keys
        'KEY_UP': (0, -1), 'KEY_DOWN': (0, 1), 'KEY_LEFT': (-1, 0), 'KEY_RIGHT': (1, 0),

        # Numpad
        'KP7': (-1, -1), 'KP8': (0, -1), 'KP9': (1, -1),
        'KP4': (-1, 0), 'KP5': (0, 0), 'KP6': (1, 0),
        'KP1': (-1, 1), 'KP2': (0, 1), 'KP3': (1, 1)

        # TODO: Vi keys
    }

    # TODO: Use Dictionary as switch statement rather than if/else chain

    # directional keys
    if key in MOVE_DICT.keys():
            return {'move': MOVE_DICT[key]}

    # Alt+Enter: toggle fullscreen
    if key == 'ENTER' and user_input.alt:
        return {'fullscreen': True}
    # control-q exists the game
    elif char == 'q' and user_input.lctrl:
        return {'exit': True}
    elif key == tcod.KEY_ESCAPE:
    # Exit the game
        return {'exit': True}
    else:
        return {}
    
'''
