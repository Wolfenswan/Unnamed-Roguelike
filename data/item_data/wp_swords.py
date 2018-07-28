from gameobjects.items.equipment import Weapon
from common import colors

WP_CHAR = '\\'
WP_COLOR = colors.turquoise
WP_CLASS = Weapon
WP_EQUIP = 'arms'  # which extremity the item is equipped to
WP_TYPE = 'weapon'  # which slot it will take

wp_sword_data = {
    'dagger_dirk': {
        'name': 'Dirk',
        'descr': 'This is a slender, long dagger. If you hit the right spot, it will do a lot of damage.',
        'chance': 10,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'item_class': WP_CLASS,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'wp_dmg': range(5, 20),
        'wp_intdm': 1,
        'weight': 1
    },
    'sword_rusty': {
        'name': 'Rusty Sword',
        'descr': 'You are not sure if this sword has seen better days, or if time simply has caught up to shoddy craftsmanship.',
        'chance': 40,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'item_class': WP_CLASS,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'wp_dmg': range(2, 5),
        'wp_intdm': 1,
        'weight': 5
    },
    'sword_orc': {
        'name': 'Orcish Sword',
        'descr': 'A mean weapon, made by mean creatures.',
        'chance': 20,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'item_class': WP_CLASS,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'wp_dmg': range(6, 12),
        'wp_intdm': 1,
        'weight': 6
    },
    'sword_long': {
        'name': 'Longsword',
        'descr': 'This sword will serve you well, if you keep it in good condition.',
        'chance': 10,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'item_class': WP_CLASS,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'wp_dmg': range(7, 14),
        'wp_intdm': 1,
        'weight': 5
    }
}
