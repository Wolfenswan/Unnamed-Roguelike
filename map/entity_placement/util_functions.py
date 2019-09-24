import logging
from random import choice

from data.data_keys import Key
from data.data_processing import NPC_DATA, gen_npc_from_data, ITEM_DATA, gen_item_from_data, ARCHITECTURE_DATA, \
    gen_architecture_from_data, UNIQUE_DATA
from debug.timer import debug_timer
from game import Game
from gameobjects.block_level import BlockLevel

@debug_timer
def find_ent_position(room, data, game, allow_exits=True, exclusive=False):
    # Get a random position for an entity in the given room
    game_map = game.map
    blocks = data.get(Key.BLOCKS, {})
    if data.get(Key.WALLS_ONLY, False):
        pos = room.ranpos(game_map, floor=False)
        if pos is False:
            logging.warning(f'No wall positions found in {room}')
        return pos
    elif blocks.get(BlockLevel.WALK, False):
        allow_exits = False
        free_tiles = room.free_tiles(game, allow_exits=allow_exits, filter=(BlockLevel.WALK, BlockLevel.FLOOR))
    else:
        #pos = room.ranpos(game_map) # This is faster but might spawn items on blocking objects
        free_tiles = room.free_tiles(game, allow_exits=allow_exits)

    if free_tiles:
        pos = choice(free_tiles)
    else:
        logging.warning(f'No free spots in {room}, thus aborting.')
        return False

    return pos


def gen_entity_at_pos(data, pos, game:Game):
    """
    Takes a data entry & creates the corresponding entity at the given pos (if possible).
    """
    if data in NPC_DATA.keys() and not game.map.is_blocked(*pos, game.blocking_ents):
        ent = gen_npc_from_data(NPC_DATA[data], *pos, game)
    elif data in ITEM_DATA.keys() and not game.map.is_blocked(*pos, []):
        ent = gen_item_from_data(ITEM_DATA[data], *pos)
    elif data in ARCHITECTURE_DATA.keys() and not game.map.is_blocked(*pos, []):
        ent = gen_architecture_from_data(ARCHITECTURE_DATA[data], *pos)
    elif data in UNIQUE_DATA.keys() and not game.map.is_blocked(*pos, []):
        if UNIQUE_DATA[data].get(Key.AI_BEHAVIOR) is not None:
            ent = gen_npc_from_data(UNIQUE_DATA[data], *pos, game)
        else:
            ent = gen_item_from_data(UNIQUE_DATA[data], *pos)
    else:
        return False
    game.entities.append(ent)
    return ent