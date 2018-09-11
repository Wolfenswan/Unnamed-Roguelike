from config_files import colors
from data.data_types import Material
from data.shared_data.rarity_data import Rarity

# Note: atm. there's no type rarity set for material. It only takes the rarity value into account #

item_material_data = {
    Material.OAK: {
        'name': 'oak',
        'type': Material.OAK,
        'rarity': Rarity.COMMON,
        'color': colors.oak
    },
    Material.LINEN: {
        'name': 'linen',
        'type': Material.LINEN,
        'rarity': Rarity.COMMON,
        'color': colors.linen
    },
    'cloth_2': {
        'name': 'cotton',
        'type': Material.COTTON,
        'rarity': Rarity.COMMON,
        'color': colors.cotton
    },
    'leather_1': {
        'name': 'leather',
        'type': Material.LEATHER,
        'rarity': Rarity.COMMON,
        'color': colors.leather
    },
    'metal_1': {
        'name': 'iron',
        'type': Material.IRON,
        'rarity': Rarity.UNCOMMON,
        'rarity_mod': 5,
        'color': colors.iron
    },
    'metal_2': {
        'name': 'steel',
        'type': Material.STEEL,
        'rarity': Rarity.UNCOMMON,
        'rarity_mod': -5,
        'color': colors.steel,
        'dmg_mod': 1,
        'av_mod': 1
    }
}