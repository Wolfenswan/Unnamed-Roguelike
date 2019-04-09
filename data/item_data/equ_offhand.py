from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType, Material, RarityType

default_values = {
    Key.CHAR: '/',
    Key.TYPE: ItemType.SHIELD,
    Key.EQUIP_TO: 'shield_arm',
    Key.DLVLS: (1,99)
}

equ_offhand_data = {
    'torch': {
        **default_values,
        Key.NAME: 'Torch',
        Key.DESCR: 'A wooden torch to light your way.',
        Key.TYPE: ItemType.MISC,
        Key.COLOR: colors.wood,
        Key.RARITY: RarityType.COMMON,
        Key.L_RADIUS: 3
    },
    'round_shield': {
        **default_values,
        Key.NAME: 'Round Shield',
        Key.MATERIAL: (Material.LEATHER, Material.OAK, Material.IRON),
        Key.DESCR: 'A simple, round shield.',
        Key.RARITY: RarityType.COMMON,
        Key.BLOCK_DEF: 4
    },
    'tower_shield': {
        **default_values,
        Key.NAME: 'tower shield',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A large shield, covering most of your upper body.',
        Key.RARITY: RarityType.RARE,
        Key.BLOCK_DEF: 8
    }
}