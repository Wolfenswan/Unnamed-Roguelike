from config_files import colors
from abilities.spells import heal_entity
from data.entitytypes import ItemType, Rarity
from gui.messages import Message

POTION_CHAR = '!'

use_potions_data = {
    'pot_heal': {
        'name': 'Potion of Healing',
        'descr': 'This potion will heal you for a moderate amount.',
        'type': ItemType.USEABLE,
        "char": POTION_CHAR,
        "color": colors.violet,
        'on_use': heal_entity,
        'on_use_msg': Message('You drink down the potion.'),
        'targeting': False,
        "on_use_params": {'pwr': (6, 10)},
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99)
    }
}
