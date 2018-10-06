from config_files import colors
from data.data_types import ItemType
from data.data_types import RarityType
from data.shared_data.effect_combinations import heal

POTION_CHAR = '!'

use_potions_data = {
    'pot_heal': {
        'name': 'Potion of Healing',
        'descr': 'This potion will heal you for a moderate amount.',
        'type': ItemType.USEABLE,
        "char": POTION_CHAR,
        "color": colors.violet,
        'on_use': heal,
        'on_use_msg': 'You gulp the potion.',
        "on_use_params": {'pwr': (6, 10)},
        'rarity': RarityType.COMMON,
        'dlvls': (1, 99)
    }
}
