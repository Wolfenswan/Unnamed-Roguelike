from config_files import colors
from data.data_keys import Key
from data.data_types import Material

item_material_data = {
    'wood_1': {
        Key.TYPE: Material.OAK,
        Key.COLOR: colors.oak
    },
    'creature_1': {
        Key.TYPE: Material.CHITIN,
        Key.COLOR: colors.dark_gray
    },
    'cloth_1': {
        Key.TYPE: Material.LINEN,
        Key.COLOR: colors.linen
    },
    # 'cloth_2': {
    #     Key.NAME: 'cotton',
    #     Key.TYPE: Material.WOOL,
    #     Key.RARITY: RarityType.COMMON,
    #     Key.COLOR: colors.WOOL
    # },
    'leather_1': {
        Key.TYPE: Material.LEATHER,
        Key.COLOR: colors.leather
    },
    'metal_1': {
        Key.TYPE: Material.IRON,
        Key.COLOR: colors.iron,
        Key.AV_FLAT: 1
    },
    'metal_2': {
        Key.TYPE: Material.STEEL,
        Key.COLOR: colors.steel,
        Key.DMG_FLAT: 2,
        Key.AV_FLAT: 2
    },

}