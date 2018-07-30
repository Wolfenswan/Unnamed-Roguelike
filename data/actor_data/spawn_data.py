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
        'ai': 'BasicMonster()'
        'barks': ('humanoid', 'orcs')
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
from components.AI.basicmonster import BasicMonster
from components.skills import skill_charge_activation, skill_charge_condition
from config_files import colors

spawn_data = {
    'Orc': {
        'name': 'Orc',
        'char': 'o',
        'colors': [colors.green, colors.desaturated_green, colors.light_green],
        'descr': 'The most generic of monsters you could imagine. Thankfully, it will probably kill you before you are bored to death.',
        'max_hp': (8,15),
        'nat_armor': (0,2),
        'nat_power': (3,6),
        'nat_vision': 8,
        'ai': BasicMonster,
        'barks': ('humanoid', 'orcs'),
        'skills': {
                'charge1': {
                    'on_activate': skill_charge_activation,
                    'activate_condition': skill_charge_condition,
                    'cooldown_length': 6
                }
        },
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
        'dlvls': (1,100),
        'chance': 60,
        'group_size': (1,3)
    }
}