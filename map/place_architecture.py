from random import randint, choice

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import ARCHITECTURE_DATA_MERGED, pick_from_data_dict_by_chance, gen_architecture


def place_architecture(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities

    # first, remove all items that can't be spawned on the current level
    possible_objects = {k: v for k, v in ARCHITECTURE_DATA_MERGED.items() if dlvl in v.get('dlvls', [0, 0])}

    # pick a random room
    for room in game_map.rooms:

        # place up to the allowed maximum of items
        num_of_staticobjects = (randint(0, cfg.MAX_ROOM_STATICOBJECTS))
        for i in range(num_of_staticobjects):
            so_key = pick_from_data_dict_by_chance(possible_objects)
            data = possible_objects[so_key]

            # Get a random position for the item
            if data.get('blocks', False):
                free_tiles = room.free_tiles(game.map, allow_exits=False)
                if len(free_tiles) > 0:
                    x, y = choice(free_tiles)
            else:
                x, y = room.ranpos(game_map)

            arch = gen_architecture(data, x, y)
            entities.append(arch)

def place_doors(game):
    game_map = game.map
    entities = game.entities

    # pick a random room
    for room in game_map.rooms:

        exits = room.exits(game_map, max_width=1)
        for e in exits:
            if randint(0,1):

                key = pick_from_data_dict_by_chance(arch_doors_data)
                data = arch_doors_data[key]

                x, y = e
                door = gen_architecture(data, x, y)
                if randint(0, 1):
                    door.char = '-'
                    door.blocks = False

                entities.append(door)