from data.data_enums import Key, ItemType, RarityType, Material, EquipTo
from data.moveset_data.weapon_movesets import moveset_sword, moveset_spear, moveset_flail, moveset_bow, moveset_dagger

default_values = {
    Key.CHAR: '\\',
    Key.DESCR: 'TODO Placeholder',
    Key.TYPE: ItemType.MELEE_WEAPON,
    Key.EQUIP_TO: EquipTo.WEAPON_ARM,
    Key.DLVLS: (1,99)
}

equ_weapon_data = {
    'sword': {
        **default_values,
        Key.NAME: 'sword',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Kills enemies and cuts bread. Clean it in between.',
        Key.DMG_POTENTIAL: (4, 6),
        Key.MOVESET: moveset_sword,
        Key.RARITY: RarityType.COMMON
    },
    'dagger': {
        **default_values,
        Key.NAME: 'dagger',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'A short and nimble blade, easier to conceal than its larger cousins.',
        Key.DMG_POTENTIAL: (2, 4),
        Key.MOVESET: moveset_dagger,
        Key.RARITY: RarityType.COMMON
    },
    'spear': {
        **default_values,
        Key.NAME: 'spear',
        Key.MATERIAL: (Material.OAK, Material.IRON, Material.STEEL),
        Key.DESCR: 'Easy to use, yet efficient in the right hands. It can be wielded with only hand, but will be slightly weaker when doing so.',
        Key.CHAR: '|',
        Key.DMG_POTENTIAL: (2,6),
        Key.TWO_HANDED: True,
        Key.ONE_HANDED_PENALTY_MOD: 0.75, # multiply damage by this amount if not wielded two-handed
        Key.MOVESET: moveset_spear,
        Key.RARITY: RarityType.COMMON
    },
    'flail': {
        **default_values,
        Key.NAME: 'flail',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: 'Shields matter little if you can swing a spiked ball over them.',
        Key.CHAR: '?',
        Key.DMG_POTENTIAL: (2,4),
        Key.MOVESET: moveset_flail,
        Key.RARITY: RarityType.COMMON
    },
    'bow': {
        **default_values,
        Key.NAME: 'bow',
        Key.MATERIAL: (Material.OAK, Material.CHITIN),
        Key.DESCR: 'Surprisingly difficult to use properly, despite its simple concept.',
        Key.TYPE: ItemType.RANGED_WEAPON,
        Key.DMG_POTENTIAL: (1,3),
        Key.ATTACK_RANGE: (1,6),
        Key.RARITY: RarityType.RARE,
        Key.CHAR: '(',
        Key.TWO_HANDED: True,
        Key.MOVESET: moveset_bow
    }
}