"""

    template:
    'Dataentry': { # If values are not set, they default to None
        'name': 'Entity name'
        'char': 'Entity ascii symbol'
        'colors': list of possible colors
        'descr': 'Enemy descprition'
        'max_hp': Tuple of min/max values
        'max_stamina': Tuple of min/max values
        'base_armor': Tuple of min/max values
        'base_strength': Tuple of min/max values
        'ai_behavior':
        'barks': Tuple of strings, referring to barks as defined in barks_data
        'skills': Tuple of strings, referring to skills as defined in skills_data
        'dlvls': Tuple of dungeon level range
        'chance': Chance in 100 to appear
        'group_size': Tuple of min/max group size
    }

"""

from components.AI.behavior.simple import Simple
from components.AI.behavior.swarm import Swarm
from config_files import colors
from data.actor_data.act_skills import skill_charge_prep
from data.data_types import RarityType, AttackType

spawn_data = {
    'roachling': {
        'name': 'Roachling',
        'char': 'r',
        'color': colors.light_amber,
        'descr': 'Waddling upright like a clumsy child, the twitching antennae and multitude of jittering legs quickly dispell any passing resemblance.',
        'max_hp': (2,6),
        'max_stamina': (80,80),
        'base_armor': (0,0),
        'base_strength': (4,4),
        #'nat_vision': 6,
        'loadout': {
            'equipment':{
                'ins_mandibles':{}
            }
        },
        'ai_movement': Swarm,
        'ai_attack': Swarm,
        'barks': ('insect',),
        'dlvls': (1,100),
        'rarity': RarityType.COMMON,
        'group_size': (3,7)
    },
    'dung_beetle': {
        'name': 'Dung Beetle',
        'char': 'd',
        'color': colors.beige,
        'descr': "There is something uniquely unsettling about a giant beetle acting like an agitated bull. It's also the size of one, if you were wondering.",
        'max_hp': (12,16),
        'max_stamina': (100,100),
        'base_armor': (2,4),
        'base_strength': (6,10),
        'loadout': {
            'equipment':{
                'ins_mandibles':{
                    'forced_attacktype': AttackType.HEAVY
                }
            }
        },
        #'nat_vision': 6,
        'ai_movement': Simple,
        'ai_attack': Simple,
        'barks': ('insect',),
        'skills': (skill_charge_prep,  ),
        'dlvls': (1,100),
        'rarity': RarityType.UNCOMMON,
        'rarity_mod': +5,
        'group_size': (1,2)
    },

    # 'Bomb_Beetle': {
    #     'name': 'Bombardier Beetle',
    #     'char': 'b',
    #     'color': colors.cyan,
    #     'descr': ".",
    #     'max_hp': (4,6),
    #     'max_stamina':(4,8),
    #     'nat_armor': (0,0),
    #     'nat_power': (1,1),
    #     'nat_vision': 6,
    #     'ai': BasicAI,
    #     'barks': ('insect'),
    #     'ai_movement': Distance,
    #     'ai_attack': Ranged,
    #     'loadouts': None,
    #     'dlvls': (1,100),
    #     'chance': 50,
    #     'group_size': (1,3)
    # },

    # 'Suicide_Beetle': {
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
    #     'chance': 10,
    #     'group_size': (1,1)
    # },
}