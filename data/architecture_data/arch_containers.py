from components.architecture import Architecture
from config_files import colors
from data.entitytypes import ItemType, Rarity, ContainerType

arch_containers_data = {
    'barrel_wood': {
        'name': 'Wooden Barrel',
        'descr': "A barrel of unknown contents.",
        'type': ContainerType.BARREL,
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99),
        "char": 'o',
        "color": colors.wood,
        "blocks": True,
        'container_room': (0,4),
        'contents_rarity': (Rarity.COMMON),
        'contents_type': (ItemType.USEABLE),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.smash_object
    },
    'chest_wood': {
        'name': 'Wooden Chest',
        'descr': "A simple, yet sturdy chest.",
        'rarity': Rarity.COMMON,
        'rarity_type': ContainerType.CHEST_BASIC,
        'dlvls': (1, 99),
        "char": '+',
        "color": colors.wood,
        "blocks": False,
        'container_room': (1, 6),
        'contents_rarity': (Rarity.COMMON, Rarity.UNCOMMON, Rarity.RARE),
        'contents_type': (ItemType.USEABLE, ItemType.WEAPON, ItemType.ARMOR, ItemType.BELT),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },

}