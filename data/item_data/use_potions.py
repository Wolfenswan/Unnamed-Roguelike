from random import randint

from gameobjects.items.useables import Useable
from common import colors, item_use as iu

POTION_CHAR = '!'
POTION_CLASS = Useable

use_potions_data = {
    'pot_heal': {
        'name': 'Potion of Healing',
        'descr': 'This potion will heal you for a moderate amount.',
        'chance': 60,
        'dlvls': range(1,99),
        "char": POTION_CHAR,
        "color": colors.violet,
        'item_class': POTION_CLASS,
        'on_use': iu.cast_heal,
        "on_use_params": {'pwr': randint(6, 10)}
    },
    'pot_endurance': {
        'name': 'Potion of Endurance',
        'descr': 'This potion will make you stronger.',
        'chance': 40,
        'dlvls': range(1,99),
        "char": POTION_CHAR,
        "color": colors.red,
        'item_class': POTION_CLASS,
        'on_use': iu.cast_endup,
        "on_use_params": {'pwr': 1}
    }
}
