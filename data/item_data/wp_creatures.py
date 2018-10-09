from data.data_types import Material, ItemType, RarityType, AttackType
from data.item_data.wp_movesets import moveset_mandibles, moveset_claws

wp_creature_data = {
    'ins_mandibles': {
        'name': 'mandibles',
        'materials': (Material.CHITIN,),
        'type': ItemType.WEAPON,
        'e_to': 'weapon_arm',
        'dmg_potential': (4, 8),
        'moveset': moveset_mandibles,
        'attack': AttackType.NORMAL,
        'rarity': RarityType.FORBIDDEN,
        'can_drop': False
    },
    'ins_claws': {
        'name': 'claws',
        'materials': (Material.CHITIN,),
        'type': ItemType.WEAPON,
        'e_to': 'weapon_arm',
        'dmg_potential': (6, 6),
        'moveset': moveset_claws,
        'attack': AttackType.NORMAL,
        'rarity': RarityType.FORBIDDEN,
        'can_drop': False
    }
}