from config_files import colors
from data.data_enums import Key, ItemType, RarityType
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
        Key.ON_USE_PARAMS: {'pwr': (15, 20), 'percentage':True},
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99)
    },
}

use_potions_variants_data = {
    'lar_pot_heal': {
        **use_potions_data['pot_heal'],
        Key.NAME: 'Large Pot of Honey',
        Key.COLOR: colors.dark_amber,
        Key.ON_USE_PARAMS: {'pwr': (30, 40), 'percentage':True},
    },
    'sm_pot_heal': {
        **use_potions_data['pot_heal'],
        Key.NAME: 'Small Pot of Honey',
        Key.COLOR: colors.light_amber,
        Key.ON_USE_PARAMS: {'pwr': (10, 15), 'percentage':True},
    },
}
