from gameobjects.items.equipment import Offhand
from common import colors

OH_CHAR = ')'
OH_COLOR = colors.light_purple
OH_CLASS = Offhand
OH_EQUIP = 'arms'  # which extremity the item is equipped to
OH_TYPE = 'offhand'  # which slot it will take

oh_shields_data = {
    'shield_wood': {
        'name': 'Wooden Shield',
        'descr': 'A brittle old piece of wood.',
        'chance': 80,
        'dlvls': range(1,99),
        "char": OH_CHAR,
        "color": OH_COLOR,
        'item_class': OH_CLASS,
        'e_to': OH_EQUIP,
        'e_type': OH_TYPE,
        'av': 1,
        'weight': 1
    }
}