import logging
from random import randint, choice

from config_files import cfg
from data.architecture_data.arch_doors import arch_doors_data
from data.data_processing import gen_architecture_from_data, ARCHITECTURE_DATA
from data.data_util import filter_data_dict
from debug.timer import debug_timer
from map.entity_placement.util_functions import find_ent_position


@debug_timer
def place_generic_architecture(game):
    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()
    possible_objects = ARCHITECTURE_DATA

    logging.debug(f'Placing architecture in {len(rooms)} rooms')

    for room in rooms:

        # place up to the allowed maximum of items
        max_in_room = (room.w * room.h) // cfg.SOBJECTS_ROOM_DIVISOR
        num_to_place = (randint(0, max_in_room))

        #logging.debug(f'Placing {num_to_place} staticobjects in {rooms} (Max: {max_in_room})')

        for i in range(num_to_place):
            key = filter_data_dict(possible_objects, dlvl)
            data = possible_objects[key]

            pos = find_ent_position(room, data, game, allow_exits=False)
            if pos:
                arch = gen_architecture_from_data(data, *pos)
                entities.append(arch)


@debug_timer
def place_special_architecture(game):
    # Portal #
    if game.dlvl == 1:
        if game.turn == 1:
            pos = game.player.pos
        else:
            pos = choice(game.map.rooms[1:-1]).ranpos(game.map)
        p = gen_architecture_from_data(ARCHITECTURE_DATA['portal'], *pos)
        game.entities.append(p)
        game.portal = p

    # Upward stairs #
    if game.dlvl > 1:
        pos = game.player.pos
        s = gen_architecture_from_data(ARCHITECTURE_DATA['stairs_up'], *pos)
        game.entities.append(s)
        game.stairs_up = s

    # Downward Stairs #
    if game.dlvl < cfg.DUNGEON_LOWEST_LEVEL:
        # TODO if player has moved up one level, stairs need to be placed under them
        pos = choice(game.map.rooms[1:-1]).ranpos(game.map)
        s = gen_architecture_from_data(ARCHITECTURE_DATA['stairs_down'], *pos)
        game.entities.append(s)
        game.stairs_down = s


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

                key = filter_data_dict(possible_objects, dlvl)
                data = possible_objects[key]

                x, y = e
                door = gen_architecture_from_data(data, x, y)

                if randint(0, 1): # 50% chance door will already be closed (TODO tweak once adding locked doors)
                    door.architecture.on_interaction(None, door, game)

                entities.append(door)
