import logging
from random import choice


def create_ent_position(room, data, game, allow_exits=True):
    # Get a random position for an entity in the given room
    game_map = game.map
    blocks = data.get('blocks', {})
    if data.get('walls_only', False):
        pos = room.ranpos(game_map, floor=False)
        if pos is False:
            logging.debug(f'No wall positions found in {room}')
        return pos
    elif blocks.get('walk', False):
        free_tiles = room.free_tiles(game, allow_exits=allow_exits, filter=('walks', 'floor'))
        if free_tiles:
            pos = choice(free_tiles)
        else:
            logging.debug(f'No free spots in {room}, thus aborting.')
            return False
    else:
        #pos = room.ranpos(game_map)
        free_tiles = room.free_tiles(game, allow_exits=allow_exits, filter=('walks'))
        if free_tiles:
            pos = choice(free_tiles)
        else:
            logging.debug(f'No free spots in {room}, thus aborting.')
            return False



    return pos