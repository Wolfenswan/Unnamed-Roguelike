import logging
from random import randint, choice

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import ARCHITECTURE_DATA_MERGED, pick_from_data_dict_by_rarity, gen_architecture
from map.entity_placement.util_functions import get_ent_position


def place_staticobjects(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()
    possible_objects = ARCHITECTURE_DATA_MERGED

    # placed = 0
    # max_placed = len(rooms) * cfg.SOBJECTS_DUNGEON_FACTOR
    #
    # logging.debug(f'Max allowed: {max_items} for {len(rooms)} rooms)')
    # while placed <= max_placed and len(rooms) > 0:
    #     room = choice(rooms)
    #     rooms.remove(room)

    logging.debug(f'Placing architecture in {len(rooms)} rooms')

    for room in rooms:

        # place up to the allowed maximum of items
        max_in_room = (room.w * room.h) // cfg.SOBJECTS_ROOM_DIVISOR
        num_to_place = (randint(0, max_in_room))

        for i in range(num_to_place):
            key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
            data = possible_objects[key]

            pos = get_ent_position(room, data, game)
            if pos:
                arch = gen_architecture(data, *pos)
                entities.append(arch)


def place_doors(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    possible_objects = arch_doors_data

    for room in game_map.rooms:

        exits = room.exits(game_map, max_width=1)
        for e in exits:
            if randint(0,1):

                key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
                data = possible_objects[key]

                x, y = e
                door = gen_architecture(data, x, y)
                if randint(0, 1):
                    door.architecture.on_interaction(None, door, game)

                entities.append(door)
