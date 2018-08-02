""" Generators for monster-type objects """

import logging
from random import randint, choice

from data.data_processing import gen_ent_from_dict, pick_from_data_dict_by_chance
from config_files import cfg
from data.actor_data.spawn_data import spawn_data


def place_monsters(game):
    """ generates monsters in the current dungeon level """

    dlvl = game.dlvl
    game_map = game.map

    # all spawnable actors have a dlvl range, so the spawn_data dictionary is reduced to all spawn-objects where the current dlvl is within this range
    possible_spawns = {k: v for k, v in spawn_data.items() if dlvl in v['dlvls']}
    logging.debug('Creating monster for dungeon-level {0} from this list: {1}.'.format(dlvl, possible_spawns))

    for room in game_map.rooms[1:]:
        # monsters are created in all rooms but the first (where the player spawns)

        num_of_monsters = randint(0, cfg.MAX_ROOM_MONSTERS)

        # place up to as many monsters as the settings allow
        m = 0
        while m < num_of_monsters:
            logging.debug('Creating monster #{0} of #{1} total.'.format(m + 1, num_of_monsters))

            entry = pick_from_data_dict_by_chance(possible_spawns)
            group_size = randint(*spawn_data[entry]['group_size'])
            for i in range(1, group_size):
                logging.debug(
                    'Attempting to add {0} #{1} to group of size {2}, in room {3}...'.format(entry, i, group_size, room))

                # check if room would be overfilled
                if m + 1 > num_of_monsters:
                    logging.debug(
                        '... but count of {0} would exceed {1} so monster is not placed'.format(m + 1, num_of_monsters))
                    m += 1
                else:
                    free_tiles = room.free_tiles(game)
                    if len(free_tiles) > 0:
                        # Get a random position for the monster
                        x, y = choice(free_tiles)
                        ent = gen_ent_from_dict(spawn_data, entry, x, y, game)
                        game.entities.append(ent)
                        m += 1
                        logging.debug(f'... and created {ent} at {x},{y} in {room}, #{m} out of {num_of_monsters}')
                    else:
                        logging.debug(
                           f'... but no more free spots left to create monster in {room}, #{m} out of {num_of_monsters}')

