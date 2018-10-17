from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType
from data.data_types import RarityType
from data.shared_data.effect_combinations import heal

POTION_CHAR = '!'

use_potions_data = {
    'pot_heal': {
        Key.NAME: 'Potion of Healing',
        Key.DESCR: 'This potion will heal you for a moderate amount.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: POTION_CHAR,
        Key.COLOR: colors.violet,
        Key.ON_USE: heal,
        Key.ON_USE_MSG: 'You gulp the potion.',
        Key.ON_USE_PARAMS: {'pwr': (6, 10)},
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99)
    }
}
