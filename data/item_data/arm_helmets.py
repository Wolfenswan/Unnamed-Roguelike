from gameobjects.items.equipment import Armor
from common import colors

H_CHAR = '('
H_COLOR = colors.turquoise
H_CLASS = Armor
H_EQUIP = 'head'  # which extremity the item is equipped to
H_TYPE = 'helmet'  # which slot it will take

arm_helmets_data = {
    'helmet_rusty': {
        'name': 'Rusty Helmet',
        'descr': 'Hardly better than a bucket.',
        'chance': 50,
        'dlvls': range(1,99),
        "char": H_CHAR,
        "color": H_COLOR,
        'item_class': H_CLASS,
        'e_to': H_EQUIP,
        'e_type': H_TYPE,
        'av': 1,
        'weight': 1
    }
}
