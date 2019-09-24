import logging
from random import choice, randint

from data.data_keys import Key
from data.data_processing import UNIQUE_DATA, gen_npc_from_data, gen_item_from_data
from data.data_util import dlvl_filter
from debug.timer import debug_timer
from map.entity_placement.util_functions import find_ent_position


@debug_timer
def place_uniques(game):
    """
    Places unique entities in the dungeon and deletes placed uniques from the spawn-data-dictionary.

    :param game:
    :type game: Game
    """
    dlvl = game.dlvl
    game_map = game.map
    rooms = game_map.rooms # Unlike other placement functions this one doesnt remove rooms, thus no need to copy the dict
    spawn_data = UNIQUE_DATA

    # Uniques can spawn under 2 conditions:
    # 1. current dlvl has to be within its spawn range (no fuzzyness)
    # 2. If set, Key.UNIQUE_CHANCE defines a general chance for the entity to appear
    possible_spawns = {k: v for k, v in spawn_data.items() if dlvl_filter(dlvl, v, factor=-1) and randint(0,100) <= v.get(Key.UNIQUE_CHANCE, 100)}

    if len(possible_spawns) > 0:
        logging.debug(f'Placing unique objects: {possible_spawns}.')
        for k, data in possible_spawns.items():
            ent = None
            room = choice(rooms[1:])
            pos = find_ent_position(room, data, game)

            if data.get(Key.AI_BEHAVIOR, False) and pos:
                ent = gen_npc_from_data(data, *pos, game)
            elif data.get(Key.ON_USE, False) or data.get(Key.EQUIP_TO, False):
                ent = gen_item_from_data(data, *pos)

            if ent is not None:
                game.entities.append(ent)
                del spawn_data[k] # As UNIQUE_DATA wasn't copied, this affects the global dictionary as well
                logging.debug(f'Created unique {ent} at {pos} in {room}.')