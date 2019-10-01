from config_files import colors
from data.data_enums import Key, ItemType, RarityType, Material, EquipTo

default_values = {
    Key.TYPE: ItemType.SHIELD,
    Key.EQUIP_TO: EquipTo.SHIELD_ARM,
    Key.DLVLS: (1,99)
}

equ_offhand_data = {
    'torch': {
        **default_values,
        Key.NAME: 'Torch',
        Key.CHAR: '/',
        Key.DESCR: 'A wooden torch to light your way.',
        Key.TYPE: ItemType.MISC,
        Key.COLOR: colors.wood,
        Key.RARITY: RarityType.COMMON,
        Key.L_RADIUS: 3
    },
    'round_shield': {
        **default_values,
        Key.NAME: 'Round Shield',
        Key.CHAR: 'O',
        Key.MATERIAL: (Material.LEATHER, Material.OAK, Material.IRON),
        Key.DESCR: 'A simple, round shield.',
        Key.RARITY: RarityType.COMMON,
        Key.BLOCK_DEF: 6
    },
    'tower_shield': {
        **default_values,
        Key.NAME: 'tower shield',
        Key.CHAR: chr(221),
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A large shield, covering most of your upper body.',
        Key.RARITY: RarityType.RARE,
        Key.BLOCK_DEF: 10
    }
}