from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType, Material, RarityType

default_values = {
    Key.CHAR: ']',
    Key.TYPE: ItemType.ARMOR,
    Key.EQUIP_TO: 'torso',
    Key.DLVLS: (1,99)
}

equ_armor_data = {
    'gambeson': {
        **default_values,
        Key.NAME: 'Gambeson',
        Key.MATERIAL: (Material.LINEN,),
        Key.DESCR: 'A sewn coat with padded fodder for added protection.',
        Key.AV: 1,
        Key.QU_SLOTS: 2,
        Key.RARITY: RarityType.COMMON,
    },
    'brigandine': {
        **default_values,
        Key.NAME: 'Brigandine',
        Key.MATERIAL: (Material.LEATHER, Material.LINEN),
        Key.DESCR: 'A flexible armor with layers of small, riveted plates.',
        Key.AV: 2,
        Key.RARITY: RarityType.UNCOMMON,
    },
    'round_helmet': {
        **default_values,
        Key.NAME: 'Round Helmet',
        Key.MATERIAL: (Material.LEATHER, Material.IRON),
        Key.DESCR: 'A simple, round helmet.',
        Key.RARITY: RarityType.COMMON,
        Key.CHAR: '(',
        Key.EQUIP_TO: 'head',
        Key.AV: 1
    },
    'belt': {
        **default_values,
        Key.NAME: 'Belt',
        Key.DESCR: 'A basic utility belt.',
        Key.COLOR: colors.leather,
        Key.TYPE: ItemType.BELT,
        Key.RARITY: RarityType.COMMON,
        Key.CHAR: '=',
        Key.QU_SLOTS: 4,
    },
}