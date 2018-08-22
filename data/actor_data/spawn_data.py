"""

    template:
    'Dataentry': { # If values are not set, they default to None
        'name': 'Entity name'
        'char': 'Entity ascii symbol'
        'colors': list of possible colors
        'descr': 'Enemy descprition'
        'max_hp': Tuple of min/max values
        'max_stamina': Tuple of min/max values
        'nat_armor': Tuple of min/max values
        'nat_power': Tuple of min/max values
        'vision': Integer
        'ai_behavior':
        'barks': Tuple of strings, referring to barks as defined in barks_data
        'skills': Tuple of strings, referring to skills as defined in skills_data
        'loadouts': { # Dictionary defining loadout and backpack
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
        'group_size': Tuple of min/max group size
    }

"""

from components.AI.baseAI import BaseAI
from components.AI.behavior.simple import Simple
from components.AI.behavior.swarm import Swarm
from config_files import colors

spawn_data = {
    'Roach': {
        'name': 'Roach',
        'char': 'r',
        'color': colors.light_amber,
        'descr': 'Twitching antennae and six legs beneath a hardy carapace.',
        'max_hp': (1,4),
        'max_stamina':(4,8),
        'nat_armor': (0,0),
        'nat_power': (2,4),
        #'nat_vision': 6,
        'ai_movement': Swarm,
        'ai_attack': Swarm,
        'barks': ('insect'),
        'dlvls': (1,100),
        'chance': 60,
        'group_size': (2,4)
    },
    'Dung Beetle': {
        'name': 'Dung Beetle',
        'char': 'd',
        'color': colors.beige,
        'descr': "There is something uniquely unsettling about a giant beetle behaving like a agitated bull.",
        'max_hp': (6,8),
        'max_stamina':(4,8),
        'nat_armor': (1,1),
        'nat_power': (6,8),
        #'nat_vision': 6,
        'ai_movement': Simple,
        'ai_attack': Simple,
        'barks': ('insect'),
        'skills': ('skill_charge',  ),
        'dlvls': (1,100),
        'chance': 60,
        'group_size': (1,2)
    },



    # 'Exploding Beetle': {
    #     'name': 'Volatile Beetle',
    #     'char': 'v',
    #     'color': colors.flame,
    #     'descr': "You can see combustive liquid swirling through the thin skin of this creature's bloated belly.",
    #     'max_hp': (3,3),
    #     'max_stamina':(4,8),
    #     'nat_armor': (0,0),
    #     'nat_power': (1,1),
    #     'nat_vision': 6,
    #     'ai': BasicAI,
    #     'barks': ('insect'),
    #     'skills': ('skill_prime_expl_beetle',  ),
    #     'loadouts': None,
    #     'dlvls': (1,100),
    #     'chance': 60,
    #     'group_size': (1,3)
    # },
}