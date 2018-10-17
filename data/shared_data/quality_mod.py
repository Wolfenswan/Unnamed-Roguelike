from data.data_keys import Key
from data.data_types import Condition, Craftsmanship

# Craftsmanship modifiers are added to/substracted from the base stats #

qual_craft_data = {
    'poor_craft': {
        Key.TYPE: Craftsmanship.POOR,
        Key.DMG_FLAT: -2,
        Key.AV_FLAT: -2
    },
    'normal_craft': {
        Key.TYPE: Craftsmanship.NORMAL,
    },
    'good_craft': {
        Key.TYPE: Craftsmanship.GOOD,
        Key.DMG_FLAT: 2,
        Key.AV_FLAT: 2
    },
    'legendary_craft': {
        Key.TYPE: Craftsmanship.LEGENDARY,
        Key.DMG_FLAT: 4,
        Key.AV_FLAT: 4
    },
}

# Condition modifiers multiply the value (base stat + material mod + cond modifier) #

qual_cond_data = {
    'poor_cond': {
        Key.TYPE: Condition.POOR,
        Key.MOD_MULTIPL: 0.8
    },
    'normal_cond': {
        Key.TYPE: Condition.NORMAL
    },
    'good_cond': {
        Key.TYPE: Condition.GOOD,
        Key.MOD_MULTIPL: 1.2
    },
    'legendary_cond': {
        Key.TYPE: Condition.LEGENDARY,
        Key.MOD_MULTIPL: 2
    }
}