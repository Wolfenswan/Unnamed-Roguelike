from config_files import colors
from data.data_enums import Key, ItemType, RarityType
from data.shared_data.effect_combinations import explosion_targeted, explosion, entangle_targeted, incendiary_targeted

BOMB_CHAR = chr(162)

use_throw_data = {
    'bomb_1': {
        Key.NAME: 'Black Powder Bomb',
        Key.DESCR: 'TODO Black Powder Bomb.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: BOMB_CHAR,
        Key.COLOR: colors.dark_gray,
        Key.ON_USE_EFFECT: explosion_targeted,
        Key.ON_USE_PROJECTILE: BOMB_CHAR,
        Key.ON_USE_PARAMS: {'pwr': (8,14), 'radius': 3, 'range': (1,6)},
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
        Key.ON_USE_EFFECT: explosion_targeted,
        Key.ON_USE_PROJECTILE: BOMB_CHAR,
        Key.ON_USE_PARAMS: {'pwr': (4,8), 'radius': 2, 'range': (1,8)},
        Key.RARITY: RarityType.COMMON,
        Key.RARITY_MOD: 0,
        Key.DLVLS: (1, 99)
    },
    'bomb_3': {
        Key.NAME: 'Incendiary Bomb',
        Key.DESCR: 'TODO Incendiary Bomb.',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: BOMB_CHAR,
        Key.COLOR: colors.light_red,
        Key.ON_USE_EFFECT: incendiary_targeted,
        Key.ON_USE_PROJECTILE: BOMB_CHAR,
        Key.ON_USE_PARAMS: {'pwr': (4,8), 'radius': 2, 'range': (1,8)},
        Key.RARITY: RarityType.UNCOMMON,
        Key.RARITY_MOD: 0,
        Key.DLVLS: (1, 99)
    },
    'net_1': {
        Key.NAME: 'Throwing Net',
        Key.DESCR: 'TODO Net',
        Key.TYPE: ItemType.USEABLE,
        Key.CHAR: '#',
        Key.COLOR: colors.linen,
        Key.ON_USE_EFFECT: entangle_targeted,
        Key.ON_USE_PROJECTILE: '#',
        Key.ON_USE_PARAMS: {'pwr': (2,6), 'range': (1,4)},
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99)
    }
}
