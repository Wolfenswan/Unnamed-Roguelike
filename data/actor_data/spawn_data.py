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
from config_files import colors

spawn_data = {
    'Orc': {
        'name': 'Orc',
        'char': 'o',
        'colors': [colors.green, colors.desaturated_green, colors.light_green],
        'descr': 'The most generic of monsters you could imagine. Thankfully, it will probably kill you before you are bored to death.',
        'max_hp': (8,15),
        'nat_armor': (0,2),
        'power': (3,6),
        'vision': 4,
        'ai': 'BasicMonster()',
        'barks': ('humanoid', 'orcs'),
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