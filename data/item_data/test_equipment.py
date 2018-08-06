from config_files import colors

WP_CHAR = '\\'
WP_COLOR = colors.turquoise
WP_EQUIP = 'arms'  # which extremity the item is equipped to
WP_TYPE = 'weapon'  # which slot it will take

ARM_CHAR = ']'
ARM_COLOR = colors.brass
ARM_EQUIP = 'torso'  # which extremity the item is equipped to
ARM_TYPE = 'armor'  # which slot it will take

H_CHAR = '('
H_COLOR = colors.turquoise
H_EQUIP = 'head'  # which extremity the item is equipped to
H_TYPE = 'helmet'  # which slot it will take

M_CHAR = '='
M_COLOR = colors.dark_amber
M_EQUIP = 'torso'  # which extremity the item is equipped to
M_TYPE = 'belt'  # which slot it will take

OH_CHAR = '/'
OH_COLOR = colors.light_purple
OH_EQUIP = 'arms'  # which extremity the item is equipped to
OH_TYPE = 'offhand'  # which slot it will take

test_equipment_data = {
    'sword_rusty': {
        'name': 'Rusty Sword',
        'descr': 'You are not sure if this sword has seen better days, or if time simply has caught up to shoddy craftsmanship.',
        'chance': 50,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'dmg_range': (2, 5)
    },
    'leather_brittle': {
        'name': 'Brittle Leather Armor',
        'descr': 'A squeaking old piece of leather armor.',
        'chance': 50,
        'dlvls': range(1, 99),
        "char": ARM_CHAR,
        "color": ARM_COLOR,
        'e_to': ARM_EQUIP,
        'e_type': ARM_TYPE,
        'av': 2,
        'slots': 2
    },
    'helmet_rusty': {
        'name': 'Rusty Helmet',
        'descr': 'Hardly better than a bucket.',
        'chance': 50,
        'dlvls': range(1,99),
        "char": H_CHAR,
        "color": H_COLOR,
        'e_to': H_EQUIP,
        'e_type': H_TYPE,
        'av': 1
    },
    'belt_generic': {
        'name': 'Belt',
        'descr': 'A basic utility belt.',
        'chance': 50,
        'dlvls': range(1,99),
        "char": M_CHAR,
        "color": M_COLOR,
        'e_to': M_EQUIP,
        'e_type': M_TYPE,
        'slots': 6,
    },
    'torch': {
        'name': 'Torch',
        'descr': 'A wooden torch to light your way.',
        'chance': 80,
        'dlvls': range(1,99),
        "char": OH_CHAR,
        "color": colors.light_orange,
        'e_to': OH_EQUIP,
        'e_type': OH_TYPE,
        'l_radius': 2
    },
    'shield_wood': {
        'name': 'Wooden Shield',
        'descr': 'A wooden plank, full of worm holes.',
        'chance': 80,
        'dlvls': range(1,99),
        "char": ')',
        "color": OH_COLOR,
        'e_to': OH_EQUIP,
        'e_type': OH_TYPE,
        'av': 1
    }
}
