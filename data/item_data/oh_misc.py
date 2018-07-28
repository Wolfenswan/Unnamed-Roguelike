from gameobjects.items.equipment import Offhand
from common import colors

OH_CHAR = '/'
OH_COLOR = colors.light_purple
OH_CLASS = Offhand
OH_EQUIP = 'arms'  # which extremity the item is equipped to
OH_TYPE = 'offhand'  # which slot it will take

oh_misc_data = {
    'torch': {
        'name': 'Torch',
        'descr': 'A wooden torch to light your way.',
        'chance': 80,
        'dlvls': range(1,99),
        "char": OH_CHAR,
        "color": colors.light_orange,
        'item_class': OH_CLASS,
        'e_to': OH_EQUIP,
        'e_type': OH_TYPE,
        'l_radius': 3,
        'weight': 1
    }
}