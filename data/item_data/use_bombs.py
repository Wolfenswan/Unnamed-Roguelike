from config_files import colors
from data.data_types import ItemType, RarityType
from data.shared_data.effect_combinations import explosion_targeted

BOMB_CHAR = chr(162)

use_bombs_data = {
    'bomb_1': {
        'name': 'Black Powder Bomb',
        'descr': 'TODO Black Powder Bomb.',
        'type': ItemType.USEABLE,
        "char": BOMB_CHAR,
        "color": colors.dark_gray,
        'on_use': explosion_targeted,
        "on_use_params": {'pwr': (8,15), 'radius': 3, 'range': (1,5)},
        'rarity': RarityType.UNCOMMON,
        'rarity_mod': -5,
        'dlvls': (1, 99)
    }
}
