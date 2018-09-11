from data.data_types import Material
from data.shared_data.rarity_data import Rarity

qual_cond_data = {
    'poor_cond': {
        'names': {
            Material.OAK: 'splintered',
            Material.LINEN: 'frayed',
            Material.COTTON: 'frayed',
            Material.LEATHER: 'brittle',
            Material.IRON: 'rusty',
            Material.STEEL: 'rusty'
        },
        'rarity': Rarity.COMMON,
        'dmg_mod': -2,
        'av_mod': -2
    },
    'normal_cond': {
        'names': {}, # defaults to 'ordinary'
        'rarity': Rarity.UNCOMMON,
    },
    'good_cond': {
        'names': {
            Material.OAK: 'sturdy',
            Material.LINEN: 'well fitting',
            Material.COTTON: 'well fitting',
            Material.LEATHER: 'hardened',
            Material.IRON: 'well honed',
            Material.STEEL: 'well honed'
        },
        'rarity': Rarity.RARE,
        'dmg_mod': 2,
        'av_mod': 2
    },
    'legendary_cond': {
        'names': {
            Material.OAK: 'legendary',
            Material.LINEN: 'legendary',
            Material.COTTON: 'legendary',
            Material.LEATHER: 'legendary',
            Material.IRON: 'legendary',
            Material.STEEL: 'legendary'
        },
        'rarity': Rarity.LEGENDARY,
        'dmg_mod': 4,
        'av_mod': 4
    }
}

qual_craft_data = {

}