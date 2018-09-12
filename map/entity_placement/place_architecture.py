import logging
from random import randint, choice

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import ARCHITECTURE_DATA_MERGED, pick_from_data_dict_by_rarity, gen_architecture

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

    for room in rooms:

        # place up to the allowed maximum of items
        max_in_room = (room.w * room.h) // cfg.SOBJECTS_ROOM_DIVISOR
        num_to_place = (randint(0, max_in_room))

        for i in range(num_to_place):
            key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
            data = possible_objects[key]

            # Get a random position for the item
            if data.get('blocks', False):
                free_tiles = room.free_tiles(game, allow_exits=False)
                if len(free_tiles) > 0:
                    x, y = choice(free_tiles)
                else:
                    logging.debug(f'No more free spots in {room}, thus aborting.')
                    break
            else:
                x, y = room.ranpos(game_map)

            arch = gen_architecture(data, x, y)
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
