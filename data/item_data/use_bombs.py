from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType, RarityType
from data.shared_data.effect_combinations import explosion_targeted

BOMB_CHAR = chr(162)

use_bombs_data = {
    'bomb_1': {
        Key.NAME: 'Black Powder Bomb',
        Key.DESCR: 'TODO Black Powder Bomb.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: BOMB_CHAR,
        Key.COLOR: colors.dark_gray,
        Key.ON_USE: explosion_targeted,
        Key.ON_USE_PARAMS: {'pwr': (6,10), 'radius': 3, 'range': (1,6)},
        Key.RARITY: RarityType.UNCOMMON,
        Key.RARITY_MOD: -5,
        Key.DLVLS: (1, 99)
    },
    'bomb_2': {
        Key.NAME: 'Cherry Bomb',
        Key.DESCR: 'TODO Cherry Bomb.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: BOMB_CHAR,
        Key.COLOR: colors.dark_red,
        Key.ON_USE: explosion_targeted,
        Key.ON_USE_PARAMS: {'pwr': (4,6), 'radius': 2, 'range': (1,8)},
        Key.RARITY: RarityType.COMMON,
        Key.RARITY_MOD: 0,
        Key.DLVLS: (1, 99)
    }
}
