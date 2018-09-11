from data.shared_data.types_data import Condition, Craftsmanship
from data.shared_data.types_data import RarityType

qual_cond_data = {
    'poor_cond': {
        'type': Condition.POOR,
        'dmg_mod': -2,
        'av_mod': -2
    },
    'normal_cond': {
        'type': Condition.NORMAL
    },
    'good_cond': {
        'type': Condition.GOOD,

        'dmg_mod': 2,
        'av_mod': 2
    },
    'legendary_cond': {
        'type': Condition.LEGENDARY,
        'dmg_mod': 4,
        'av_mod': 4
    }
}

qual_craft_data = {
    'poor_craft': {
        'type': Craftsmanship.POOR
    },
    'normal_craft': {
        'type': Craftsmanship.NORMAL,
    },
    'good_craft': {
        'type': Craftsmanship.GOOD
    },
    'legendary_craft': {
        'type': Craftsmanship.LEGENDARY
    },
}