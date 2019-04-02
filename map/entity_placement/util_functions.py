import logging
from random import choice

from data.data_keys import Key
from debug.timer import debug_timer
from gameobjects.block_level import BlockLevel

@debug_timer
def find_ent_position(room, data, game, allow_exits=True, exclusive=False):
    # Get a random position for an entity in the given room
    game_map = game.map
    blocks = data.get(Key.BLOCKS, {})
    if data.get(Key.WALLS_ONLY, False):
        pos = room.ranpos(game_map, floor=False)
        if pos is False:
            logging.debug(f'No wall positions found in {room}')
        return pos
    elif blocks.get(BlockLevel.WALK, False):
        allow_exits = False
        free_tiles = room.free_tiles(game, allow_exits=allow_exits, filter=(BlockLevel.WALK, BlockLevel.FLOOR))
    else:
        #pos = room.ranpos(game_map) # This is faster but can cause bugs with items created on blocking objects
        free_tiles = room.free_tiles(game, allow_exits=allow_exits)

    if free_tiles:
        pos = choice(free_tiles)
    else:
        logging.debug(f'No free spots in {room}, thus aborting.')
        return False

    return pos