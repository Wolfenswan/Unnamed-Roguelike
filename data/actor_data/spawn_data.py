"""

    template:
    'Dataentry': {
        'name': 'Entity name'
        'char': 'Entity ascii symbol'
        'colors': list of possible colors
        'descr': 'Enemy descprition'
        'max_hp': Tuple of min/max values
        'nat_armor': Tuple of min/max values
        'nat_power': Tuple of min/max values
        'vision': Integer
        'ai': 'BasicMonster'
        'barks': ('humanoid', 'orcs')
        'skills': (),
        'loadouts': {
                'melee1': {
                    'chance': 50,
                    'equipment': ('sword_orc', 'helmet_rusty', 'leather_orc')
                },
                'melee2': {
                    'chance': 50,
                    'equipment': ('sword_orc', 'leather_orc')
                }
        },
        'dlvls': Tuple of dungeon level range
        'chance': Chance in 100 to appear
        'group_size': Tuple of min/max s
    }

"""

from components.AI.basicAI import BasicAI
from config_files import colors

spawn_data = {
    'Roach': {
        'name': 'Roach',
        'char': 'r',
        'color': colors.light_amber,
        'descr': 'Twitching antennae and six legs beneath a hardy carapace.',
        'max_hp': (2,5),
        'max_stamina':(4,8),
        'nat_armor': (0,2),
        'nat_power': (5,7),
        'nat_vision': 8,
        'ai': BasicAI,
        'barks': ('insect'),
        'skills': ('skill_charge_roach',  ),
        'loadouts': None,
        'dlvls': (1,100),
        'chance': 60,
        'group_size': (1,3)
    }
}