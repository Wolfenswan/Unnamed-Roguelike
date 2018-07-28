from gameobjects.items.equipment import Belt
from common import colors

M_CHAR = '='
M_COLOR = colors.dark_amber
M_CLASS = Belt
M_EQUIP = 'torso'  # which extremity the item is equipped to
M_TYPE = 'belt'  # which slot it will take

belts_general_data = {
    'belt_generic': {
        'name': 'Belt',
        'descr': 'A basic utility belt.',
        'chance': 60,
        'dlvls': range(1,99),
        "char": M_CHAR,
        "color": M_COLOR,
        'item_class': M_CLASS,
        'e_to': M_EQUIP,
        'e_type': M_TYPE,
        'slots': 6,
        'weight': 1
    }
}