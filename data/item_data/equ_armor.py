from config_files import colors
from data.data_enums import Key, ItemType, RarityType, Material, EquipTo

default_values = {
    Key.CHAR: ']',
    Key.TYPE: ItemType.ARMOR,
    Key.EQUIP_TO: EquipTo.TORSO,
    Key.DLVLS: (1,99)
}

equ_armor_data = {
    'gambeson': {
        **default_values,
        Key.NAME: 'Gambeson',
        Key.MATERIAL: (Material.LINEN,),
        Key.DESCR: 'A sewn coat with padding for additional protection.',
        Key.AV: 2,
        Key.QU_SLOTS: 1,
        Key.RARITY: RarityType.UNCOMMON,
    },
    'brigandine': {
        **default_values,
        Key.NAME: 'Brigandine',
        Key.MATERIAL: (Material.LEATHER, Material.LINEN),
        Key.DESCR: 'A flexible armor from layers of small, riveted plates.',
        Key.AV: 4,
        Key.RARITY: RarityType.RARE,
    },
    'vest': {
        **default_values,
        Key.NAME: 'Vest',
        Key.MATERIAL: {Material.LEATHER, Material.LINEN},
        Key.DESCR: 'A light vest with several pockets.',
        Key.AV: 1,
        Key.QU_SLOTS: 3,
        Key.RARITY: RarityType.UNCOMMON,
    },
    'round_helmet': {
        **default_values,
        Key.NAME: 'Round Helmet',
        Key.MATERIAL: (Material.LEATHER, Material.IRON),
        Key.DESCR: 'A simple, round helmet.',
        Key.RARITY: RarityType.COMMON,
        Key.CHAR: '(',
        Key.EQUIP_TO: EquipTo.HEAD,
        Key.AV: 1
    },
    'full_helmet': {
        **default_values,
        Key.NAME: 'Full Helmet',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A large, inflexible helmet.',
        Key.RARITY: RarityType.UNCOMMON,
        Key.CHAR: '(',
        Key.EQUIP_TO: EquipTo.HEAD,
        Key.AV: 2,
        Key.L_RADIUS: -1,
    },
    'belt': {
        **default_values,
        Key.NAME: 'Belt',
        Key.DESCR: 'A basic utility belt.',
        Key.COLOR: colors.leather,
        Key.TYPE: ItemType.BELT,
        Key.RARITY: RarityType.RARE,
        Key.CHAR: '=',
        Key.QU_SLOTS: 4,
    },
}