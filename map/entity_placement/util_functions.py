import logging
from random import choice


def get_ent_position(room, data, game, allow_exits=False):
    # Get a random position for the item
    game_map = game.map
    if data.get('blocks', False):
        free_tiles = room.free_tiles(game, allow_exits=allow_exits)
        if len(free_tiles) > 0:
            x, y = choice(free_tiles)
        else:
            logging.debug(f'No more free spots in {room}, thus aborting.')
            return False
    elif data.get('walls_only', False):
        x, y = room.ranpos(game_map, force_floor=False, force_wall=True)
    else:
        x, y = room.ranpos(game_map)

    return (x, y)