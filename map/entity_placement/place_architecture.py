import logging
from random import randint

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import ARCHITECTURE_DATA_MERGED, pick_from_data_dict_by_rarity, gen_architecture
from debug.timer import debug_timer
from map.entity_placement.util_functions import create_ent_position


@debug_timer
def place_staticobjects(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()
    possible_objects = ARCHITECTURE_DATA_MERGED

    logging.debug(f'Placing architecture in {len(rooms)} rooms')

    for room in rooms:

        # place up to the allowed maximum of items
        max_in_room = (room.w * room.h) // cfg.SOBJECTS_ROOM_DIVISOR
        num_to_place = (randint(0, max_in_room))

        logging.debug(f'Placing {num_to_place} staticobjects in {rooms} (Max: {max_in_room})')

        for i in range(num_to_place):
            key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
            data = possible_objects[key]

            pos = create_ent_position(room, data, game, allow_exits=False)
            if pos:
                arch = gen_architecture(data, *pos)
                entities.append(arch)

@debug_timer
def place_doors(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    possible_objects = arch_doors_data

    for room in game_map.rooms:

        exits = room.exits(game_map, max_width=1)
        for e in exits:
            if randint(0,100) <= 75:

                key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
                data = possible_objects[key]

                x, y = e
                door = gen_architecture(data, x, y)

                if randint(0, 1): # 50% chance door will already be closed (TODO tweak once adding locked doors)
                    door.architecture.on_interaction(None, door, game)

                entities.append(door)
