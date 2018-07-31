import logging
from random import randint


# Store all data dictionaries in a constant for convenience
from components.items.equipment import Equipment
from components.items.item import Item
from components.items.useable import Useable
from config_files import cfg
from data.item_data.use_potions import use_potions_data
from data.item_data.use_scrolls import use_scrolls_data
from data.item_data.wp_swords import wp_swords_data
from data.util_functions import pick_from_data_dict_by_chance
from gameobjects.entity import Entity
from rendering.render_order import RenderOrder

GAME_DATA = [use_scrolls_data, use_potions_data, wp_swords_data]
# Create a super dictionary
DATA_DICT = {}
for data in GAME_DATA:
    DATA_DICT = dict(DATA_DICT, **data)

def gen_item_from_data(data, x, y):
    try:
        name = data['name']
        char = data['char']
        color = data['color']
        descr = data['descr']
        on_use = data.get('on_use', None)
        equip_to = data.get('e_to', None)

        arguments = (x, y, char, color, name, descr)
    except Exception as err:
        logging.error(f'Failed generating item from {data} with error: {err}')
    else:
        useable_component = None
        if on_use is not None:
        # depending on the item's class new values are received and the arguments tuple expanded
            targeting = data['targeting']
            on_use_msg = data['on_use_msg']
            on_use_params = data['on_use_params']
            useable_component = Useable(use_function = on_use, targeting = targeting, on_use_msg = on_use_msg, **on_use_params)

        equipment_component = None
        if equip_to is not None:
            equip_type = data['e_type']
            dmg = data.get('dmg_range', None)
            av = data.get('av', None)
            qu_slots = data.get('qu_slots', None)
            l_radius = data.get('l_radius', None)
            equipment_component = Equipment(equip_to, equip_type, dmg_range = dmg, av = av, qu_slots = qu_slots, l_radius = l_radius)

        item_component = Item(useable=useable_component, equipment=equipment_component)

        logging.debug(f'Preparing to generate {name} with {arguments}, {item_component}')
        # create the item using item_class and the arguments tuple
        i = Entity(*arguments, render_order=RenderOrder.ITEM, item = item_component)

        return i

def place_items(game):
    """ fills the dungeon with items """

    dlvl = game.dlvl
    game_map = game.map

    # first, remove all items that can't be spawned on the current level
    possible_items = {k: v for k, v in DATA_DICT.items() if dlvl in v.get('dlvls',[0,0])}

    # pick a random room
    for room in game_map.rooms:

        # place up to the allowed maximum of items
        num_of_items = (randint(0, cfg.MAX_ROOM_ITEMS))
        for i in range(num_of_items):
            i_key = pick_from_data_dict_by_chance(possible_items)
            i_dict = possible_items[i_key]

            # Get a random position for the item
            x, y = room.ranpos(game)

            # Generate the item at the given position
            item = gen_item_from_data(i_dict, x, y)
            game.entities.append(item)