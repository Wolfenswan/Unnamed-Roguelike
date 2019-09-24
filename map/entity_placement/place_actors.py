""" Generators for monster-type objects """

import logging
from random import randint, choice

from config_files import cfg
#from data.actor_data.test_spawns import spawn_data
from data.data_keys import Key
from data.data_processing import gen_npc_from_data, NPC_DATA
from data.data_util import filter_data_dict, dlvl_filter
from debug.timer import debug_timer
from gameobjects.block_level import BlockLevel
from map.entity_placement.util_functions import find_ent_position


@debug_timer
def place_monsters(game):
    """ generates monsters in the current dungeon level """

    dlvl = game.dlvl
    game_map = game.map
    rooms = game_map.rooms.copy() # rooms is copied in order to avoid overwriting the map.rooms attribute
    spawn_data = NPC_DATA
    max_monsters = int(len(rooms) * cfg.MONSTERS_DUNGEON_FACTOR)

    logging.debug(f'Creating actors for dungeon-level {0}. Max. {max_monsters} for {len(rooms)} rooms)')

    while len(game.npc_ents) < max_monsters and len(rooms) > 1:
        # monsters are created in all rooms but the first (where the player spawns)
        room = choice(rooms[1:])
        rooms.remove(room)

        max_room_monsters = (room.w * room.h) // cfg.MONSTERS_ROOM_LIMIT
        num_of_monsters = randint(0, max_room_monsters)
        logging.debug(f'Placing monsters in {room} of size {(room.w * room.h)} and limit of {num_of_monsters} (max possible: {max_room_monsters})')

        if num_of_monsters > 0:
            # place up to as many monsters as the settings allow
            m = 0
            while m <= num_of_monsters and len(game.npc_ents) < max_monsters:
                key = filter_data_dict(spawn_data, dlvl)
                entry = spawn_data[key]
                group_size = randint(*entry[Key.GROUP_SIZE])
                for i in range(group_size):
                    logging.debug('Creating monster #{0} of #{1} total.'.format(m + 1, num_of_monsters))
                    logging.debug(
                        'Attempting to add {0} #{1} to group of size {2}, in room {3}...'.format(entry[Key.NAME], i+1, group_size, room))

                    # check if room would be overfilled
                    if m + 1 > num_of_monsters:
                        logging.debug(
                            f'... but new monster would bring room total to {m+1} thus exceed room maximum({num_of_monsters})')
                        m += 1
                        break
                    elif  len(game.npc_ents) + 1 > max_monsters:
                        logging.debug(
                            f'... but new monster would bring overall total to {len(game.npc_ents)+1} thus exceed total maximum: ({max_monsters})')
                        break
                    else:
                        m += 1
                        entry['blocks'] = {BlockLevel.WALK: True}
                        pos = find_ent_position(room, entry, game)
                        if pos:
                            ent = gen_npc_from_data(entry, *pos, game)
                            game.entities.append(ent)
                            logging.debug(f'... and created {ent} at {pos} in {room}, #{m} out of {num_of_monsters}')


    logging.debug(f'Placed {len(game.npc_ents)} (maximum: {max_monsters}) monsters with {len(rooms)} rooms untouched.')
