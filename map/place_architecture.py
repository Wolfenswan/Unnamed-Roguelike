import logging
from random import randint, choice

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import ARCHITECTURE_DATA_MERGED, pick_from_data_dict_by_rarity, gen_architecture, \
    CONTAINER_DATA_MERGED


def place_staticobjects(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()

    # first, remove all items that can't be spawned on the current level
    possible_objects = {k: v for k, v in ARCHITECTURE_DATA_MERGED.items() if dlvl in v.get('dlvls', [0, 0])}

    # placed = 0
    # max_placed = len(rooms) * cfg.SOBJECTS_DUNGEON_FACTOR
    #
    # logging.debug(f'Max allowed: {max_items} for {len(rooms)} rooms)')
    # while placed <= max_placed and len(rooms) > 0:
    #     room = choice(rooms)
    #     rooms.remove(room)

    for room in rooms:

        # place up to the allowed maximum of items
        max_in_room = (room.w * room.h) // cfg.SOBJECTS_ROOM_DIVISOR
        num_to_place = (randint(0, max_in_room))

        for i in range(num_to_place):
            so_key = pick_from_data_dict_by_rarity(possible_objects)
            data = possible_objects[so_key]

            # Get a random position for the item
            if data.get('blocks', False):
                free_tiles = room.free_tiles(game.map, allow_exits=False)
                if len(free_tiles) > 0:
                    x, y = choice(free_tiles)
                else:
                    break
            else:
                x, y = room.ranpos(game_map)

            arch = gen_architecture(data, x, y)
            entities.append(arch)

def place_doors(game):
    game_map = game.map
    entities = game.entities

    for room in game_map.rooms:

        exits = room.exits(game_map, max_width=1)
        for e in exits:
            if randint(0,1):

                key = pick_from_data_dict_by_rarity(arch_doors_data)
                data = arch_doors_data[key]

                x, y = e
                door = gen_architecture(data, x, y)
                if randint(0, 1):
                    door.architecture.on_interaction(None, door)

                entities.append(door)


def place_containers(game):

    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()

    # first, remove all items that can't be spawned on the current level
    possible_objects = {k: v for k, v in CONTAINER_DATA_MERGED.items() if dlvl in v.get('dlvls', [0, 0])}

    max_containers = int(len(rooms) * cfg.CONTAINER_DUNGEON_FACTOR)

    while len(game.container_ents) < max_containers and len(rooms) > 0:
        room = choice(rooms)
        rooms.remove(room)

        # place up to the allowed maximum of items
        max_room_containers = (room.w * room.h) // cfg.CONTAINER_ROOM_DIVISOR
        num_of_containers = (randint(0, max_room_containers))

        if num_of_containers > 0:
            logging.debug(f'Placing containers in {room} of size {(room.w * room.h)} and limit of {num_of_containers} (max possible: {max_room_containers})')

            containers = 0
            for i in range(num_of_containers):
                logging.debug('Creating item #{0} of #{1} total.'.format(containers + 1, num_of_containers))

                so_key = pick_from_data_dict_by_rarity(possible_objects)
                data = possible_objects[so_key]

                # Check if new container would exceed total limit
                if len(game.container_ents) + 1 > max_containers:
                    logging.debug(
                        f'... but new container would bring dungeon total to {len(game.container_ents)+1} thus exceed total maximum: ({max_containers})')
                    break
                # If the container is a blocking object, get a free tile
                elif data.get('blocks', False):
                    free_tiles = room.free_tiles(game_map, allow_exits=False)
                    if len(free_tiles) > 0:
                        x, y = choice(free_tiles)
                    else:
                        break
                else:
                    x, y = room.ranpos(game_map)

                arch = gen_architecture(data, x, y)
                entities.append(arch)

    logging.debug(f'Placed {len(game.container_ents)} (maximum: {max_containers}) items with {len(rooms)} rooms untouched.')
