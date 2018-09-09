from config_files import colors
from data.entitytypes import ItemType, Rarity
from data.item_data.moveset_data import moveset_sword, moveset_spear

WP_CHAR = '\\'
WP_COLOR = colors.turquoise
WP_EQUIP = 'arms'  # which extremity the item is equipped to
WP_TYPE = ItemType.WEAPON  # which slot it will take

ARM_CHAR = ']'
ARM_COLOR = colors.brass
ARM_EQUIP = 'torso'  # which extremity the item is equipped to
ARM_TYPE = ItemType.ARMOR  # which slot it will take

H_CHAR = '('
H_COLOR = colors.turquoise
H_EQUIP = 'head'  # which extremity the item is equipped to
H_TYPE = ItemType.ARMOR  # which slot it will take

M_CHAR = '='
M_COLOR = colors.dark_amber
M_EQUIP = 'torso'  # which extremity the item is equipped to
M_TYPE = ItemType.BELT  # which slot it will take

OH_CHAR = '/'
OH_COLOR = colors.light_purple
OH_EQUIP = 'arms'  # which extremity the item is equipped to
OH_TYPE = ItemType.OFFHAND  # which slot it will take

test_equipment_data = {
    'sword_rusty': {
        'name': 'Rusty Sword',
        'descr': 'You are not sure if this sword has seen better days, or if time simply has caught up to shoddy craftsmanship.',
        "char": WP_CHAR,
        "color": WP_COLOR,
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_range': (2, 5),
        'moveset': moveset_sword,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99)
    },
    'spear_rusty': {
        'name': 'Rusty Spear',
        'descr': 'The tip might break off, but the rust will hopefully poison your enemies.',
        'char': '|',
        'color': WP_COLOR,
        'type': WP_TYPE,
        'e_to': WP_EQUIP,
        'dmg_range': (1,7),
        'moveset': moveset_spear,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99)
    },
    'leather_brittle': {
        'name': 'Brittle Leather Armor',
        'descr': 'A squeaking old piece of leather armor.',
        "char": ARM_CHAR,
        "color": ARM_COLOR,
        'type': ARM_TYPE,
        'e_to': ARM_EQUIP,
        'av': 2,
        'qu_slots': 2,
        'rarity': Rarity.UNCOMMON,
        'dlvls': (1, 99)
    },
    'helmet_rusty': {
        'name': 'Rusty Helmet',
        'descr': 'Hardly better than a bucket.',
        'type': H_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": H_CHAR,
        "color": H_COLOR,
        'e_to': H_EQUIP,
        'av': 1
    },
    'belt_generic': {
        'name': 'Belt',
        'descr': 'A basic utility belt.',
        'type': M_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": M_CHAR,
        "color": M_COLOR,
        'e_to': M_EQUIP,
        'qu_slots': 6,
    },
    'torch': {
        'name': 'Torch',
        'descr': 'A wooden torch to light your way.',
        'type': OH_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": OH_CHAR,
        "color": colors.light_orange,
        'e_to': OH_EQUIP,
        'l_radius': 2
    },
    'shield_wood': {
        'name': 'Wooden Shield',
        'descr': 'A wooden plank, full of worm holes.',
        'type': OH_TYPE,
        'rarity': Rarity.COMMON,
        'dlvls': (1,99),
        "char": ')',
        "color": OH_COLOR,
        'e_to': OH_EQUIP,
        'av': 1
    }
}
