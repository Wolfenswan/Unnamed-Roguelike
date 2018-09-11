from config_files import colors
from data.data_types import Material

item_material_data = {
    Material.OAK: {
        'name': 'oak',
        'color': colors.oak
    },
    Material.LINEN: {
        'name': 'linen',
        'color': colors.linen
    },
    Material.COTTON: {
        'name': 'cotton',
        'color': colors.cotton
    },
    Material.LEATHER: {
        'name': 'leather',
        'color': colors.leather
    },
    Material.IRON: {
        'name': 'iron',
        'color': colors.iron
    },
    Material.STEEL: {
        'name': 'steel',
        'color': colors.steel,
        'dmg_mod': 1,
        'av_mod': 1
    }
}