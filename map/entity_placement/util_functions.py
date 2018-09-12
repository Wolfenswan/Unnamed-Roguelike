import logging
from random import choice


def create_ent_position(room, data, game, allow_exits=True):
    # Get a random position for an entity in the given room
    game_map = game.map
    if data.get('walls_only', False):
        pos = room.ranpos(game_map, floor=False)
        if pos is False:
            logging.debug(f'No wall positions found in {room}')
    elif data.get('blocks', False):
        free_tiles = room.free_tiles(game, allow_exits=allow_exits)
        if free_tiles:
            pos = choice(free_tiles)
        else:
            logging.debug(f'No free spots in {room}, thus aborting.')
            return False
    else:
        pos = room.ranpos(game_map)

    return pos