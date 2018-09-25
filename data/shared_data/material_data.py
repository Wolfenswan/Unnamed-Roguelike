from config_files import colors
from data.data_types import Material

item_material_data = {
    'wood_1': {
        'type': Material.OAK,
        'color': colors.oak
    },
    'creature_1': {
        'type': Material.CHITIN,
        'color': colors.dark_gray
    },
    'cloth_1': {
        'type': Material.LINEN,
        'color': colors.linen
    },
    # 'cloth_2': {
    #     'name': 'cotton',
    #     'type': Material.WOOL,
    #     'rarity': RarityType.COMMON,
    #     'color': colors.WOOL
    # },
    'leather_1': {
        'type': Material.LEATHER,
        'color': colors.leather
    },
    'metal_1': {
        'type': Material.IRON,
        'color': colors.iron,
        'av_mod': 1
    },
    'metal_2': {
        'type': Material.STEEL,
        'color': colors.steel,
        'dmg_mod': 2,
        'av_mod': 2
    }
}