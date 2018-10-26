import logging
from random import choice, randint

from config_files import cfg
from data.data_keys import Key
from data.data_processing import CONTAINER_DATA_MERGED, pick_from_data_dict_by_rarity, gen_architecture, \
    gen_item_from_data, ITEM_DATA_MERGED
from data.data_types import RarityType
from debug.timer import debug_timer
from map.entity_placement.util_functions import create_ent_position

@debug_timer
def place_containers(game):

    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()
    possible_objects = CONTAINER_DATA_MERGED
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

                key = pick_from_data_dict_by_rarity(possible_objects, dlvl)
                data = possible_objects[key]

                # Check if new container would exceed total limit
                if len(game.container_ents) + 1 > max_containers:
                    logging.debug(
                        f'New container would bring dungeon total to {len(game.container_ents)+1} thus exceed total maximum: ({max_containers})')
                    break
                # If the container is a blocking object, get a free tile
                pos = create_ent_position(room, data, game)
                if pos:
                    con = gen_architecture(data, *pos)
                    fill_container(con, dlvl, rarity_filter=data[Key.CONTENTS_RARITY], type_filter=data[Key.CONTENTS_TYPE], forced_content=data.get('content_forced'))
                    entities.append(con)

    logging.debug(f'Placed {len(game.container_ents)} (maximum: {max_containers}) items with {len(rooms)} rooms untouched.')


def fill_container(container, dlvl, rarity_filter=None, type_filter=None, forced_content=None):
    """
    Fills the given container. Content can be either randomized using the content rarity and filter attributes or forced.

    :param container: Container entity.
    :type container: Entity
    :param dlvl: Current dungeon level
    :param rarity_filter: A tuple of rarity values, corresponding to Rarity Enum members.
    :type rarity_filter: tuple
    :param type_filter: A tuple of entity types, corresponding to EntityType Enum members.
    :type type_filter: tuple
    :param forced_content: A tuple of item data names, corresponding to the item's key in the data dictionaries.
    :type forced_content: tuple
    """

    logging.debug(f'Filling {container.name}({container})')

    if forced_content:
        for i in forced_content:
            item = gen_item_from_data(ITEM_DATA_MERGED.get(i), 0, 0)
            container.inventory.add(item)
            if container.inventory.is_full:
                break
    else:
        possible_items = {k: v for k, v in ITEM_DATA_MERGED.items() if
                          dlvl in range(*v.get(Key.DLVLS, (1, 99)))
                          and v.get(Key.TYPE) in type_filter
                          and v.get(Key.RARITY, RarityType.COMMON) in rarity_filter}
        num_of_items = randint(0, container.inventory.capacity)
        logging.debug(f'Creating {num_of_items} items (max: {container.inventory.capacity})')
        for i in range(num_of_items):
            key = pick_from_data_dict_by_rarity(possible_items, dlvl)
            data = possible_items[key]
            item = gen_item_from_data(data, 0, 0)
            container.inventory.add(item)