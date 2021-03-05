from data.data_enums import Key, ItemType, RarityType, Material, Element, EquipTo
from data.moveset_data.creature_movesets import moveset_mandibles, moveset_claws, moveset_spit

equ_creature_data = {
    'ins_mandibles': {
        Key.NAME: 'mandibles',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.MELEE_WEAPON,
        Key.EQUIP_TO: EquipTo.WEAPON_ARM,
        Key.DMG_POTENTIAL: (4, 8),
        Key.MOVESET: moveset_mandibles,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False # TODO not implemented
    },
    'ins_claws': {
        Key.NAME: 'claws',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.MELEE_WEAPON,
        Key.EQUIP_TO: EquipTo.WEAPON_ARM,
        Key.DMG_POTENTIAL: (4, 6),
        Key.MOVESET: moveset_claws,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False # TODO not implemented
    },
    'ins_ranged': {
        Key.NAME: 'spit',
        Key.MATERIAL: (Material.CHITIN,),
        Key.TYPE: ItemType.RANGED_WEAPON,
        Key.EQUIP_TO: EquipTo.WEAPON_ARM,
        Key.DMG_POTENTIAL: (6, 8),
        Key.MOVESET: moveset_spit,
        Key.RARITY: RarityType.FORBIDDEN,
        Key.CAN_DROP: False, # TODO not implemented
        Key.ELEMENT: Element.ACID # TODO not implemented
    },
}