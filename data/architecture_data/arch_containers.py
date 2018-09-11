from components.architecture import Architecture
from config_files import colors
from data.data_types import ItemType, ContainerType, Material
from data.shared_data.rarity_data import Rarity

arch_containers_data = {
    'barrel': {
        'name': 'barrel',
        'materials': (Material.OAK, Material.IRON),
        'descr': "A barrel of unknown contents.",
        'type': ContainerType.BARREL,
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99),
        "char": 'o',
        "blocks": True,
        'container_room': (0,4),
        'contents_rarity': (Rarity.COMMON,),
        'contents_type': (ItemType.USEABLE, ItemType.MISC),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.smash_object
    },
    'chest_basic': {
        'name': 'chest',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': "A simple, yet sturdy chest.",
        'type': ContainerType.CHEST_BASIC,
        'rarity': Rarity.UNCOMMON,
        'dlvls': (1, 99),
        "char": '+',
        "blocks": False,
        'container_room': (3, 8),
        'contents_rarity': (Rarity.COMMON, Rarity.UNCOMMON, Rarity.RARE),
        'contents_type': (ItemType.USEABLE, ItemType.WEAPON, ItemType.SHIELD, ItemType.MISC, ItemType.BELT),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },
    'weapon_rack_old': {
        'name': 'weapon rack',
        'materials': (Material.IRON, Material.STEEL),
        'descr': "The rust makes it hard to tell where the rack ends and its content begins.",
        'type': ContainerType.CHEST_BASIC,
        'rarity': Rarity.UNCOMMON,
        'rarity_mod': +5,
        'dlvls': (1, 99),
        "char": '+',
        "blocks": False,
        'container_room': (1, 4),
        'contents_rarity': (Rarity.COMMON, Rarity.UNCOMMON),
        'contents_type': (ItemType.WEAPON, ItemType.SHIELD, ItemType.MISC),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },
}