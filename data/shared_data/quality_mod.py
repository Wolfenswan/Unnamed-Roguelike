from data.data_enums import Key, Mod, Condition, Craftsmanship

# Craftsmanship modifiers are added to/substracted from the base stats #

qual_craft_data = {
    'poor_craft': {
        Key.TYPE: Craftsmanship.POOR,
        Mod.DMG_FLAT: -1,
        Mod.AV_FLAT: -1
    },
    'normal_craft': {
        Key.TYPE: Craftsmanship.NORMAL,
    },
    'good_craft': {
        Key.TYPE: Craftsmanship.GOOD,
        Mod.DMG_FLAT: 2,
        Mod.AV_FLAT: 2
    },
    'legendary_craft': {
        Key.TYPE: Craftsmanship.LEGENDARY,
        Mod.DMG_FLAT: 4,
        Mod.AV_FLAT: 4
    },
}

# Condition modifiers multiply the item's primary value (base stat + material mod + cond modifier) #

qual_cond_data = {
    'poor_cond': {
        Key.TYPE: Condition.POOR,
        Mod.COND_MULTIPL: 0.8
    },
    'normal_cond': {
        Key.TYPE: Condition.NORMAL
    },
    'good_cond': {
        Key.TYPE: Condition.GOOD,
        Mod.COND_MULTIPL: 1.2
    },
    'legendary_cond': {
        Key.TYPE: Condition.LEGENDARY,
        Mod.COND_MULTIPL: 2
    }
}