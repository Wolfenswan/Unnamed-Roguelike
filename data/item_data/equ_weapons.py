from data.data_keys import Key
from data.data_types import Material, AttackType, RarityType, ItemType
from data.item_data._movesets import moveset_sword, moveset_spear, moveset_flail, moveset_bow

default_values = {
    Key.CHAR: '\\',
    Key.TYPE: ItemType.MELEE_WEAPON,
    Key.EQUIP_TO: 'weapon_arm',
    Key.DLVLS: (1,99)
}

equ_weapon_data = {
    'sword': {
        **default_values,
        Key.NAME: 'sword',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Kills enemies and cuts bread, what else could one wish for. Just make sure to clean it in between.',
        Key.DMG_POTENTIAL: (4, 6),
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_sword,
        Key.RARITY: RarityType.COMMON
    },
    'dagger': {
        **default_values,
        Key.NAME: 'dagger',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A short and nimble blade.',
        Key.DMG_POTENTIAL: (2, 4),
        Key.ATTACKTYPE: AttackType.QUICK,
        Key.MOVESET: moveset_sword,
        Key.RARITY: RarityType.COMMON
    },
    'spear': {
        **default_values,
        Key.NAME: 'spear',
        Key.MATERIAL: (Material.OAK, Material.IRON, Material.STEEL),
        Key.DESCR: 'A simple weapon that has stood the test of time.',
        Key.CHAR: '|',
        Key.DMG_POTENTIAL: (2,8),
        Key.TWO_HANDED: True,
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_spear,
        Key.RARITY: RarityType.COMMON
    },
    'flail': {
        **default_values,
        Key.NAME: 'flail',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Swing it round, round like the murder tool it is.',
        Key.CHAR: '?',
        Key.DMG_POTENTIAL: (2,4),
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.MOVESET: moveset_flail,
        Key.RARITY: RarityType.COMMON
    },
    'bow': { # TODO Placeholder #
        **default_values,
        Key.NAME: 'bow',
        Key.MATERIAL: (Material.OAK, Material.CHITIN),
        Key.DESCR: 'TODO Bow. Longer Line. Test.',
        Key.TYPE: ItemType.RANGED_WEAPON,
        Key.DMG_POTENTIAL: (2,4),
        Key.ATTACK_RANGE: (1,6),
        Key.RARITY: RarityType.RARE,
        Key.CHAR: '(',
        Key.TWO_HANDED: True,
        Key.MOVESET: moveset_bow
    }
}