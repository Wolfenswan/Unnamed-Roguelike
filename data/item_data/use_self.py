from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType
from data.data_types import RarityType
from data.shared_data.effect_combinations import heal_self

POTION_CHAR = '!'

use_potions_data = {
    'pot_heal': {
        Key.NAME: 'Pot of Honey',
        Key.DESCR: 'Precious goo, both for healing and as treasure.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: POTION_CHAR,
        Key.COLOR: colors.amber,
        Key.ON_USE_EFFECT: heal_self,
        Key.ON_USE_MSG: 'You enjoy a pot of honey.', # TODO various messages
        Key.ON_USE_PARAMS: {'pwr': (6, 10)},
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99)
    },
}

use_potions_variants_data = {
    'lar_pot_heal': {
        **use_potions_data['pot_heal'],
        Key.NAME: 'Large Pot of Honey',
        Key.COLOR: colors.dark_amber,
        Key.ON_USE_PARAMS: {'pwr': (10, 14)},
    },
    'sm_pot_heal': {
        **use_potions_data['pot_heal'],
        Key.NAME: 'Small Pot of Honey',
        Key.COLOR: colors.light_amber,
        Key.ON_USE_PARAMS: {'pwr': (2, 4)},
    },
}
