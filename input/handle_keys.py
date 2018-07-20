""" Translates key events into game-related actions """

# TODO Consider using tdl for event handling instead? Might allow using a large dictionary instead of if/elif snake

import tcod

def handle_keys(key):
    # Movement keys
    if key.vk == tcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
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
