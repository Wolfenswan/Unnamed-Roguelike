""" Generators for monster-type objects """

import logging
from random import randint, choice

from components.skills import Skill
from data.util_functions import pick_from_data_dict_by_chance
from components.actors.fighter import Fighter
from config_files import cfg
from data.actor_data.spawn_data import spawn_data
from gameobjects.npc import NPC


def gen_ent_from_dict(dict, entry, x, y):
    data = dict[entry]
    name = data['name']
    char = data['char']
    color = choice(data['colors'])
    descr = data['descr']
    hp = randint(*data['max_hp'])
    defense = randint(*data['nat_armor'])
    power = randint(*data['nat_power'])
    vision = data['nat_vision']
    ai = data['ai']
    skills = data.get('skills', None)

    skills_component = None

    if skills is not None:
        skills_component = []
        for k in skills:
            skill = Skill(**skills[k])
            skills_component.append(skill)

    fighter_component = Fighter(hp, defense, power, vision, skills=skills_component)
    ai_component = ai()


    # create the arguments tuple out of the values we've got so far
    arguments = (x, y, char, color, name, descr)
        #logging.error(f'Failed generating item from {data} with error: {err}')

    # create the static object using the arguments tuple
    logging.debug(f'Generating {name} with {arguments, fighter_component, ai_component, skills_component}')
    ent = NPC(*arguments, fighter=fighter_component, ai=ai_component)
    return ent

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
                        ent = gen_ent_from_dict(spawn_data, entry, x, y)
                        game.entities.append(ent)
                        m += 1
                        logging.debug(f'... and created {ent} at {x},{y} in {room}, #{m} out of {num_of_monsters}')
                    else:
                        logging.debug(
                           f'... but no more free spots left to create monster in {room}, #{m} out of {num_of_monsters}')

