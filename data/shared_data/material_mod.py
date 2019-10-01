from config_files import colors
from data.data_enums import Key, Mod, Material

item_material_data = {
    'oak': {
        Key.TYPE: Material.OAK,
        Key.COLOR: colors.oak
    },
    'chitin': {
        Key.TYPE: Material.CHITIN,
        Key.COLOR: colors.dark_gray
    },
    'linen': {
        Key.TYPE: Material.LINEN,
        Key.COLOR: colors.linen
    },
    # 'cloth_2': {
    #     Key.NAME: 'cotton',
    #     Key.TYPE: Material.WOOL,
    #     Key.RARITY: RarityType.COMMON,
    #     Key.COLOR: colors.WOOL
    # },
    'leather': {
        Key.TYPE: Material.LEATHER,
        Key.COLOR: colors.leather
    },
    'iron': {
        Key.TYPE: Material.IRON,
        Key.COLOR: colors.iron,
        Mod.AV_FLAT: 1
    },
    'steel': {
        Key.TYPE: Material.STEEL,
        Key.COLOR: colors.steel,
        Mod.DMG_FLAT: 1,
        Mod.AV_FLAT: 2
    },

}