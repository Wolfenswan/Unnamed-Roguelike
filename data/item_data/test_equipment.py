from config_files import colors
from data.data_keys import Key
from data.data_types import ItemType, Material, AttackType
from data.data_types import RarityType
from data.item_data.wp_movesets import moveset_sword, moveset_spear, moveset_flail, moveset_bow

WP_CHAR = '\\'
WP_EQUIP = 'weapon_arm'  # which extremity the item is equipped to
WP_TYPE = ItemType.MELEE_WEAPON  # which slot it will take

ARM_CHAR = ']'
ARM_EQUIP = 'torso'  # which extremity the item is equipped to
ARM_TYPE = ItemType.ARMOR  # which slot it will take

H_CHAR = '('
H_EQUIP = 'head'  # which extremity the item is equipped to
H_TYPE = ItemType.ARMOR  # which slot it will take

M_CHAR = '='
M_EQUIP = 'torso'  # which extremity the item is equipped to
M_TYPE = ItemType.BELT  # which slot it will take

OH_CHAR = '/'
OH_EQUIP = 'shield_arm'  # which extremity the item is equipped to
#OH_TYPE = ItemType.SHIELD, ItemType.MISC  # which slot it will take

test_equipment_data = {
    'sword': {
        Key.NAME: 'sword',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Kills enemies and cuts bread, what else could you wish for. Just make sure to clean it in between.',
        Key.CHAR: WP_CHAR,
        Key.TYPE: WP_TYPE,
        Key.EQUIP_TO: WP_EQUIP,
        Key.DMG_POTENTIAL: (4, 6),
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_sword,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99)
    },
    'dagger': {
        Key.NAME: 'dagger',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A short and nimble blade.',
        Key.CHAR: WP_CHAR,
        Key.TYPE: WP_TYPE,
        Key.EQUIP_TO: WP_EQUIP,
        Key.DMG_POTENTIAL: (2, 4),
        Key.ATTACKTYPE: AttackType.QUICK,
        Key.MOVESET: moveset_sword,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99)
    },
    'spear': {
        Key.NAME: 'spear',
        Key.MATERIAL: (Material.OAK, Material.IRON, Material.STEEL),
        Key.DESCR: 'A simple weapon that has stood the test of time.',
        Key.CHAR: '|',
        Key.TYPE: WP_TYPE,
        Key.EQUIP_TO: WP_EQUIP,
        Key.DMG_POTENTIAL: (2,8),
        Key.TWO_HANDED: True,
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_spear,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99)
    },
    'flail': {
        Key.NAME: 'flail',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Swing it round, round like the murder tool it is.',
        Key.CHAR: '?',
        Key.TYPE: WP_TYPE,
        Key.EQUIP_TO: WP_EQUIP,
        Key.DMG_POTENTIAL: (2,4),
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_flail,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99)
    },
    'gambeson': {
        Key.NAME: 'Gambeson',
        Key.MATERIAL: (Material.LINEN, ),
        Key.DESCR: 'A sewn coat with padded fodder for added protection.',
        Key.CHAR: ARM_CHAR,
        Key.TYPE: ARM_TYPE,
        Key.EQUIP_TO: ARM_EQUIP,
        Key.AV: 1,
        Key.QU_SLOTS: 2,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99)
    },
    'brigandine': {
        Key.NAME: 'Brigandine',
        Key.MATERIAL: (Material.LEATHER, Material.LINEN),
       Key.DESCR: 'A flexible armor with layers of small, riveted plates.',
        Key.CHAR: ARM_CHAR,
        Key.TYPE: ARM_TYPE,
        Key.EQUIP_TO: ARM_EQUIP,
        Key.AV: 2,
        Key.RARITY: RarityType.UNCOMMON,
        Key.DLVLS: (1, 99)
    },
    'helmet': {
        Key.NAME: 'Round Helmet',
        Key.MATERIAL: (Material.LEATHER, Material.IRON),
        Key.DESCR: 'At least it is not a bucket.',
        Key.TYPE: H_TYPE,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99),
        Key.CHAR: H_CHAR,
        Key.EQUIP_TO: H_EQUIP,
        Key.AV: 1
    },
    'belt_generic': {
        Key.NAME: 'Belt',
        Key.DESCR: 'A basic utility belt.',
        Key.COLOR: colors.leather,
        Key.TYPE: M_TYPE,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99),
        Key.CHAR: M_CHAR,
        Key.EQUIP_TO: M_EQUIP,
        Key.QU_SLOTS: 4,
    },
    'torch': {
        Key.NAME: 'Torch',
        Key.DESCR: 'A wooden torch to light your way.',
        Key.TYPE: ItemType.MISC,
        Key.COLOR: colors.wood,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99),
        Key.CHAR: OH_CHAR,
        Key.EQUIP_TO: OH_EQUIP,
        Key.L_RADIUS: 3
    },
    'round_shield': {
        Key.NAME: 'Shield',
        Key.MATERIAL: (Material.LEATHER, Material.OAK, Material.IRON),
        Key.DESCR: 'A simple, round shield.',
        Key.TYPE: ItemType.SHIELD,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1,99),
        Key.CHAR: ')',
        Key.EQUIP_TO: OH_EQUIP,
        Key.BLOCK_DEF: 8
    },
    'tower_shield': {
        Key.NAME: 'tower shield',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A large shield, covering most of your upper body.',
        Key.TYPE: ItemType.SHIELD,
        Key.RARITY: RarityType.RARE,
        Key.DLVLS: (1,99),
        Key.CHAR: ')',
        Key.EQUIP_TO: OH_EQUIP,
        Key.BLOCK_DEF: 14
    },
    'bow': { # TODO Placeholder #
        Key.NAME: 'bow',
        Key.MATERIAL: (Material.OAK, Material.CHITIN),
        Key.DESCR: 'TODO Bow. Longer Line. Test.',
        Key.TYPE: ItemType.RANGED_WEAPON,
        Key.DMG_POTENTIAL: (2,4),
        Key.ATTACK_RANGE: (1,6),
        Key.RARITY: RarityType.RARE,
        Key.DLVLS: (1,99),
        Key.CHAR: '(',
        Key.TWO_HANDED: True,
        Key.MOVESET: moveset_bow,
        Key.EQUIP_TO: WP_EQUIP
    }
}
