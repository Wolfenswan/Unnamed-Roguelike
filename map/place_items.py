import logging
from random import randint, choice

from config_files import cfg
from data.data_processing import gen_item_from_data, pick_from_data_dict_by_rarity, ITEM_DATA_MERGED


def place_items(game):
    """ fills the dungeon with items """

    dlvl = game.dlvl
    game_map = game.map
    rooms = game_map.rooms.copy()

    # first, remove all items that can't be spawned on the current level
    possible_items = {k: v for k, v in ITEM_DATA_MERGED.items() if dlvl in v.get('dlvls',[0,99])}

   #max_items = (game_map.width * game_map.height) // cfg.ITEMS_DUNGEON_DIVISOR
    max_items = int(len(rooms) * cfg.ITEMS_DUNGEON_FACTOR)

    logging.debug(f'Max allowed: {max_items} for {len(rooms)} rooms)')
    while len(game.item_ents) < max_items and len(rooms) > 0:
        room = choice(rooms)
        rooms.remove(room)
        
        max_room_items = (room.w * room.h) // cfg.ITEMS_ROOM_LIMIT
        num_of_items = randint(0, max_room_items)
        if num_of_items > 0:
            logging.debug(f'Placing items in {room} of size {(room.w * room.h)} and limit of {num_of_items} (max possible: {max_room_items})')

            for i in range(num_of_items):
                logging.debug('Creating item #{0} of #{1} total.'.format(i + 1, num_of_items))

                i_key = pick_from_data_dict_by_rarity(possible_items)
                i_dict = possible_items[i_key]

                if len(game.item_ents) + 1 > max_items:
                    logging.debug(
                        f'New item would bring dungeon total to {len(game.item_ents)+1} thus exceed total maximum: ({max_items})')
                    break
                else:
                    # Get a random position for the item
                    # TODO make sure items are not placed on blocking architecture
                    x, y = room.ranpos(game_map)
                    # Generate the item at the given position
                    item = gen_item_from_data(i_dict, x, y)
                    game.entities.append(item)
                    logging.debug(f'Created {item} at {x},{y} in {room}.')

    logging.debug(f'Placed {len(game.item_ents)} items with {len(rooms)} rooms untouched.')
