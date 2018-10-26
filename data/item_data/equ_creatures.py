from data.data_keys import Key
from data.data_types import Material, ItemType, RarityType, AttackType, Element
from data.item_data._movesets import moveset_mandibles, moveset_claws, moveset_spit

equ_creature_data = {
    'ins_mandibles': {
        Key.NAME: 'mandibles',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.MELEE_WEAPON,
        Key.EQUIP_TO: 'weapon_arm',
        Key.DMG_POTENTIAL: (4, 8),
        Key.MOVESET: moveset_mandibles,
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False # TODO not implemented
    },
    'ins_claws': {
        Key.NAME: 'claws',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.MELEE_WEAPON,
        Key.EQUIP_TO: 'weapon_arm',
        Key.DMG_POTENTIAL: (6, 6),
        Key.MOVESET: moveset_claws,
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False # TODO not implemented
    },
    'ins_ranged': {
        Key.NAME: 'spit',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.RANGED_WEAPON,
        Key.EQUIP_TO: 'weapon_arm',
        Key.DMG_POTENTIAL: (6, 6),
        Key.MOVESET: moveset_spit,
        Key.ATTACKTYPE: AttackType.NORMAL,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False, # TODO not implemented
        Key.ELEMENT: Element.ACID # TODO not implemented
    },
}