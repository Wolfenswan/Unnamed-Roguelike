from data.data_types import Material, ItemType, RarityType
from data.item_data.wp_movesets import moveset_mandibles

wp_creature_data = {
    'ins_mandibles': {
        'name': 'mandibles',
        'materials': (Material.CHITIN,),
        'type': ItemType.WEAPON,
        'e_to': 'weapon_arm',
        'dmg_potential': (2, 6),
        'moveset': moveset_mandibles,
        'rarity': RarityType.FORBIDDEN,
        'can_drop': False
    }
}