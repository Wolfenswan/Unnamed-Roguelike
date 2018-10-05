import tcod

from components.effects import Effects
from config_files import colors
from data.data_types import ItemType, RarityType

BOMB_CHAR = chr(162)

use_bombs_data = {
    'bomb_1': {
        'name': 'Black Powder Bomb',
        'descr': 'TODO Black Powder Bomb.',
        'type': ItemType.USEABLE,
        "char": BOMB_CHAR,
        "color": colors.dark_gray,
        'on_use': Effects.explosion,
        'on_use_msg': 'Move the cursor over the intended target, press Enter to confirm.',
        'targeting': True,
        "on_use_params": {'dmg': 12, 'radius': 3, 'range': 5},
        'rarity': RarityType.UNCOMMON,
        'rarity_mod': -5,
        'dlvls': (1, 99)
    }
}
