from config_files import colors
from data.data_types import ItemType, Material, AttackType
from data.data_types import RarityType
from data.item_data.wp_movesets import moveset_sword, moveset_spear, moveset_flail

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
        'descr': 'Kills enemies and cuts bread, what else could you wish for. Just make sure to clean it in between.',
        "char": WP_CHAR,
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_potential': (4, 6),
        'attack': AttackType.NORMAL,
        'moveset': moveset_sword,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99)
    },
    'dagger': {
        'name': 'dagger',
        'materials': (Material.IRON, Material.STEEL),
        'descr': 'A short and nimble blade.',
        "char": WP_CHAR,
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_potential': (2, 4),
        'attack': AttackType.QUICK,
        'moveset': moveset_sword,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99)
    },
    'spear': {
        'name': 'spear',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': 'A simple weapon that has stood the test of time.',
        'char': '|',
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_potential': (2,8),
        'two_handed': True,
        'attack': AttackType.NORMAL,
        'moveset': moveset_spear,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99)
    },
    'flail': {
        'name': 'flail',
        'materials': (Material.IRON, Material.STEEL),
        'descr': 'Swing it round, round like the murder tool it is.',
        'char': '?',
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_potential': (2,4),
        'attack': AttackType.NORMAL,
        'moveset': moveset_flail,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99)
    },
    'gambeson': {
        'name': 'Gambeson',
        'materials': (Material.LINEN, ),
        'descr': 'A sewn coat with padded fodder for added protection.',
        "char": ARM_CHAR,
        'type': ARM_TYPE,
        'e_to': ARM_EQUIP,
        'av': 1,
        'qu_slots': 2,
        'rarity': RarityType.COMMON,
        'dlvls': (1, 99)
    },
    'brigandine': {
        'name': 'Brigandine',
        'materials': (Material.LEATHER, Material.LINEN),
        'descr': 'A flexible armor with layers of small, riveted plates.',
        "char": ARM_CHAR,
        'type': ARM_TYPE,
        'e_to': ARM_EQUIP,
        'av': 2,
        'rarity': RarityType.UNCOMMON,
        'dlvls': (1, 99)
    },
    'helmet': {
        'name': 'Round Helmet',
        'materials': (Material.LEATHER, Material.IRON),
        'descr': 'At least it is not a bucket.',
        'type': H_TYPE,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99),
        "char": H_CHAR,
        'e_to': H_EQUIP,
        'av': 1
    },
    'belt_generic': {
        'name': 'Belt',
        'descr': 'A basic utility belt.',
        'color': colors.leather,
        'type': M_TYPE,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99),
        "char": M_CHAR,
        'e_to': M_EQUIP,
        'qu_slots': 4,
    },
    'torch': {
        'name': 'Torch',
        'descr': 'A wooden torch to light your way.',
        'type': ItemType.MISC,
        'color': colors.wood,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99),
        "char": OH_CHAR,
        'e_to': OH_EQUIP,
        'l_radius': 3
    },
    'round_shield': {
        'name': 'Shield',
        'materials': (Material.LEATHER, Material.OAK, Material.IRON),
        'descr': 'A simple, round shield.',
        'type': ItemType.SHIELD,
        'rarity': RarityType.COMMON,
        'dlvls': (1,99),
        "char": ')',
        'e_to': OH_EQUIP,
        'block_def': 4
    },
    'tower_shield': {
        'name': 'tower shield',
        'materials': (Material.IRON, Material.STEEL),
        'descr': 'A large shield, covering most of your upper body.',
        'type': ItemType.SHIELD,
        'rarity': RarityType.RARE,
        'dlvls': (1,99),
        "char": ')',
        'e_to': OH_EQUIP,
        'block_def': 8
    },
    'bow': { # TODO Placeholder #
        'name': 'bow',
        'materials': (Material.OAK, Material.CHITIN),
        'descr': 'TODO Bow. Longer Line. Test.',
        'type': ItemType.RANGED,
        'rarity': RarityType.RARE,
        'dlvls': (1,99),
        "char": '(',
        'two_handed': True,
        'e_to': WP_EQUIP
    }
}
