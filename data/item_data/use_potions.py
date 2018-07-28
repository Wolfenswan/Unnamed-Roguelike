from random import randint

from config_files import colors
from effects.spells import heal_entity
from gui.messages import Message

POTION_CHAR = '!'

use_potions_data = {
    'pot_heal': {
        'name': 'Potion of Healing',
        'descr': 'This potion will heal you for a moderate amount.',
        "char": POTION_CHAR,
        "color": colors.violet,
        'on_use': heal_entity,
        'on_use_msg': Message('You drink down the potion.'),
        'targeting': False,
        "on_use_params": {'pwr': (6, 10)},
        'chance': 60,
        'dlvls': (1, 99)
    }
}
