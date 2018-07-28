from gameobjects.items.equipment import Weapon
from common import colors

WP_CHAR = '\\'
WP_COLOR = colors.turquoise
WP_CLASS = Weapon
WP_EQUIP = 'arms'  # which extremity the item is equipped to
WP_TYPE = 'weapon'  # which slot it will take

wp_sword_data = {
    'claws_troll': {
        'name': 'Troll Claws',
        'descr': '',
        'chance': -99,
        "char": WP_CHAR,
        "color": WP_COLOR,
        'item_class': WP_CLASS,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'wp_dmg': range(1, 10),
        'wp_intdm': 1,
        'weight': 1
    }
}
