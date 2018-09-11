from data.data_types import ItemType, Material
from data.shared_data.rarity_data import Rarity
from data.item_data.wp_movesets import moveset_sword, moveset_spear

WP_CHAR = '\\'
WP_EQUIP = 'weapon_arm'  # which extremity the item is equipped to
WP_TYPE = ItemType.WEAPON  # which slot it will take

ARM_CHAR = ']'
ARM_EQUIP = 'torso'  # which extremity the item is equipped to
ARM_TYPE = ItemType.ARMOR  # which slot it will take

H_CHAR = '('
H_EQUIP = 'head'  # which extremity the item is equipped to
H_TYPE = ItemType.ARMOR  # which slot it will take

M_CHAR = '='
M_EQUIP = 'torso'  # which extremity the item is equipped to
M_TYPE = ItemType.BELT  # which slot it will take

OH_CHAR = '/'
OH_EQUIP = 'shield_arm'  # which extremity the item is equipped to
#OH_TYPE = ItemType.SHIELD, ItemType.MISC  # which slot it will take

test_equipment_data = {
    'sword': {
        'name': 'sword',
        'materials': (Material.IRON, Material.STEEL),
        'descr': 'Kill enemies, cut bread, what else could you wish for.',
        "char": WP_CHAR,
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_range': (2, 5),
        'moveset': moveset_sword,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99)
    },
    'spear': {
        'name': 'spear',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': 'A simple weapon that has stood the test of time.',
        'char': '|',
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_range': (1,7),
        'two_handed': True,
        'moveset': moveset_spear,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99)
    },
    'gambeson': {
        'name': 'Gambeson',
        'materials': (Material.LINEN, Material.COTTON),
        'descr': 'No descr.',
        "char": ARM_CHAR,
        'type': ARM_TYPE,
        'e_to': ARM_EQUIP,
        'av': 2,
        'qu_slots': 1,
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99)
    },
    'brigandine': {
        'name': 'Brigadine',
        'materials': (Material.COTTON, Material.LEATHER, Material.IRON),
        'descr': 'No descr.',
        "char": ARM_CHAR,
        'type': ARM_TYPE,
        'e_to': ARM_EQUIP,
        'av': 2,
        'rarity': Rarity.UNCOMMON,
        'dlvls': (1, 99)
    },
    'helmet': {
        'name': 'Helmet',
        'materials': (Material.LEATHER, Material.IRON),
        'descr': 'At least it is not a bucket.',
        'type': H_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": H_CHAR,
        'e_to': H_EQUIP,
        'av': 1
    },
    'belt_generic': {
        'name': 'Belt',
        'materials': (Material.LEATHER,),
        'descr': 'A basic utility belt.',
        'type': M_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": M_CHAR,
        'e_to': M_EQUIP,
        'qu_slots': 4,
    },
    'torch': {
        'name': 'Torch',
        'descr': 'A wooden torch to light your way.',
        'type': ItemType.MISC,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": OH_CHAR,
        'e_to': OH_EQUIP,
        'l_radius': 3
    },
    'shield': {
        'name': 'Shield',
        'materials': (Material.LEATHER, Material.OAK, Material.IRON),
        'descr': 'A simple shield.',
        'type': ItemType.SHIELD,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": ')',
        'e_to': OH_EQUIP,
        'av': 1
    }
}
