from data.data_keys import Key
from data.data_types import Material, Condition, Craftsmanship

classes_data = {
    'generic': {
        Key.NAME : 'generic',
        Key.MAX_HP : (60, 60),
        Key.MAX_STAMINA: (200, 200),
        Key.BASE_ARMOR: (0, 0),
        Key.BASE_STRENGTH: (3, 3),
        Key.LOADOUTS: { # one loadout is randomly chosen
            'loadout1': {
                Key.EQUIPMENT: {
                    'sword': {},
                    'gambeson': {},
                    'round_helmet': {},
                    'belt': {},
                    'round_shield': {}
                },
                Key.BACKPACK: ('pot_heal', 'bomb_2', 'net_1', 'torch',)
            },
            'loadout2': {
                Key.EQUIPMENT: {
                    'flail': {},
                    'brigandine': {},
                    'full_helmet': {},
                    'belt': {},
                },
                Key.BACKPACK: ('pot_heal', 'bomb_1', 'net_1', 'torch',)
            },
            'loadout3': {
                Key.EQUIPMENT: {
                    'spear': {},
                    'vest': {},
                    'full_helmet': {},
                    'belt': {},
                },
                Key.BACKPACK: ('pot_heal', 'bomb_1', 'net_1', 'torch','bow')
            },
        }
    },
}