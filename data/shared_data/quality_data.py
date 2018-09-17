from data.shared_data.types_data import Condition, Craftsmanship

# Craftsmanship modifiers are added to/substracted from the base stats #

qual_craft_data = {
    'poor_craft': {
        'type': Craftsmanship.POOR,
        'dmg_mod': -2,
        'av_mod': -2
    },
    'normal_craft': {
        'type': Craftsmanship.NORMAL,
    },
    'good_craft': {
        'type': Craftsmanship.GOOD,
        'dmg_mod': 2,
        'av_mod': 2
    },
    'legendary_craft': {
        'type': Craftsmanship.LEGENDARY,
        'dmg_mod': 4,
        'av_mod': 4
    },
}

# Condition modifiers multiply the value (base stat + material mod + cond modifier) #

qual_cond_data = {
    'poor_cond': {
        'type': Condition.POOR,
        'mod_multipl': 0.8
    },
    'normal_cond': {
        'type': Condition.NORMAL
    },
    'good_cond': {
        'type': Condition.GOOD,
        'mod_multipl': 1.2
    },
    'legendary_cond': {
        'type': Condition.LEGENDARY,
        'mod_multipl': 2
    }
}