from config_files import colors
from data.shared_data.types_data import Material

item_material_data = {
    'wood_1': {
        'type': Material.OAK,
        'color': colors.oak
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