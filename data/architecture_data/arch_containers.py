from components.architecture import Architecture
from config_files import colors
from data.data_types import ItemType, Rarity, ContainerType

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
        'contents_rarity': (Rarity.COMMON,),
        'contents_type': (ItemType.USEABLE,),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.smash_object
    },
    'chest_wood': {
        'name': 'Wooden Chest',
        'descr': "A simple, yet sturdy chest.",
        'type': ContainerType.CHEST_BASIC,
        'rarity': Rarity.UNCOMMON,
        'dlvls': (1, 99),
        "char": '+',
        "color": colors.wood,
        "blocks": False,
        'container_room': (3, 8),
        'contents_rarity': (Rarity.COMMON, Rarity.UNCOMMON, Rarity.RARE),
        'contents_type': (ItemType.USEABLE, ItemType.WEAPON, ItemType.OFFHAND, ItemType.BELT),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },
    'weapon_rack_old': {
        'name': 'Old Weapon Rack',
        'descr': "The rust makes it hard to tell where the rack ends and its content begins.",
        'type': ContainerType.CHEST_BASIC,
        'rarity': Rarity.UNCOMMON,
        'rarity_mod': +5,
        'dlvls': (1, 99),
        "char": '+',
        "color": colors.dark_gray,
        "blocks": False,
        'container_room': (1, 4),
        'contents_rarity': (Rarity.COMMON, Rarity.UNCOMMON),
        'contents_type': (ItemType.WEAPON, ItemType.OFFHAND),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },
}