from random import randint


# Store all data dictionaries in a constant for convenience
from config_files import cfg
from data.data_processing import gen_item_from_data, pick_from_data_dict_by_chance, ITEM_DATA_MERGED
from data.item_data.use_potions import use_potions_data
from data.item_data.use_scrolls import use_scrolls_data
from data.item_data.wp_swords import wp_swords_data


# GAME_DATA = [use_scrolls_data, use_potions_data, wp_swords_data]
# # Create a super dictionary
# DATA_DICT = {}
# for data in GAME_DATA:
#     DATA_DICT = dict(DATA_DICT, **data)


def place_items(game):
    """ fills the dungeon with items """

    dlvl = game.dlvl
    game_map = game.map

    # first, remove all items that can't be spawned on the current level
    possible_items = {k: v for k, v in ITEM_DATA_MERGED.items() if dlvl in v.get('dlvls',[0,99])}

    # pick a random room
    for room in game_map.rooms:

        # place up to the allowed maximum of items
        num_of_items = (randint(0, cfg.MAX_ROOM_ITEMS))
        for i in range(num_of_items):
            i_key = pick_from_data_dict_by_chance(possible_items)
            i_dict = possible_items[i_key]

            # Get a random position for the item
            # TODO make sure items are not placed on blocking architecture
            x, y = room.ranpos(game_map)

            # Generate the item at the given position
            item = gen_item_from_data(i_dict, x, y)
            game.entities.append(item)