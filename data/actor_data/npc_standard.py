"""
    template:
    'data_key': {
        Key.NAME: str
        Key.CHAR: str
        Key.COLOR: color
        Key.DESCR: str
        Key.MAX_HP: (int min, int max)
        Key.MAX_STAMINA: (int min, int max)
        Key.BASE_ARMOR: (int min, int max)
        Key.BASE_STRENGTH: (int min, int max),
        Key.LOADOUT: {
            Key.EQUIPMENT:{}
            Key.BACKPACK:{}
        },
        Key.AI_BEHAVIOR: Behavior
        Key.SKILLS: (Skill, Skill...)
        Key.BARKS: (key, key...),
        Key.GROUP_SIZE: (int, int),
        Key.DLVLS: (int, int),
        Key.RARITY: RarityType.
    }
"""
from components.AI.behavior.simple_ranged import Ranged
from components.AI.behavior.simple_melee import Simple
from components.AI.behavior.swarm import Swarm
from config_files import colors
from data.actor_data.act_skills import skill_generic_charge, skill_generic_slam, skill_explode_self, skill_entangle, \
    skill_entangle_timed, skill_hatch
from data.data_enums import Key, MonsterType, RarityType
from data.moveset_data.creature_movesets import moveset_claws_heavy, moveset_mandibles_heavy

_default_values = {
    Key.COLOR_BLOOD: colors.blood_ins,
    Key.TYPE : MonsterType.GENERIC
}

npc_data_insects = {
    'roachling': {
        **_default_values,
        Key.NAME: 'Roachling',
        Key.CHAR: 'r',
        Key.COLOR: colors.light_amber,
        Key.DESCR: 'Waddling upright like a clumsy child, the twitching antennae and multitude of jittering legs quickly dispel any passing resemblance.',
        Key.MAX_HP: (5, 10),
        Key.MAX_STAMINA: (60, 60),
        Key.BASE_ARMOR: (0, 0),
        Key.BASE_STRENGTH: (1, 2),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_mandibles':{}
            }
        },
        Key.AI_BEHAVIOR: Swarm,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (4, 12),
        Key.DLVLS: (1, 8),
        Key.RARITY: RarityType.COMMON
    },
    'dung_beetle': {
        **_default_values,
        Key.NAME: 'Dung Beetle',
        Key.CHAR: 'd',
        Key.COLOR: colors.beige,
        Key.DESCR: "About the size of a pony, this giant beetle still acts like an agitated bull.",
        Key.MAX_HP: (12, 24),
        Key.MAX_STAMINA: (80, 80),
        Key.BASE_ARMOR: (1, 3),
        Key.BASE_STRENGTH: (3, 5),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_mandibles':{
                    Key.FORCED_MOVESET: moveset_mandibles_heavy
                }
            }
        },
        Key.SKILLS: (skill_generic_charge,),
        Key.AI_BEHAVIOR: Simple,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 3),
        Key.DLVLS: (1, 10),
        Key.RARITY: RarityType.UNCOMMON,
        Key.RARITY_MOD: +5
    },
    'mantis_ogre' : {
        **_default_values,
        Key.NAME: 'Mantis Ogre',
        Key.CHAR: 'M',
        Key.COLOR: colors.light_green,
        Key.DESCR: "Certainly not praying, the elongated frame of these creatures belies the power of their claws.",
        Key.MAX_HP: (20, 40),
        Key.MAX_STAMINA: (200, 200),
        Key.BASE_ARMOR: (2, 5),
        Key.BASE_STRENGTH: (6, 8),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_claws':{
                    Key.FORCED_MOVESET: moveset_claws_heavy
                }
            }
        },
        Key.SKILLS: (skill_generic_slam,),
        Key.AI_BEHAVIOR: Simple,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 2),
        Key.DLVLS: (7, 10),
        Key.RARITY: RarityType.RARE
    },
    'spitting_beetle' : {
        **_default_values,
        Key.NAME: 'Spitting Beetle',
        Key.CHAR: 'b',
        Key.COLOR: colors.light_green,
        Key.DESCR: "Viscous fluid seeps along tubal appendages attached to it's 'face'.",
        Key.MAX_HP: (6, 8),
        Key.MAX_STAMINA: (60, 60),
        Key.BASE_ARMOR: (0, 2),
        Key.BASE_STRENGTH: (2, 4),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_ranged':{}
            }
        },
        Key.AI_BEHAVIOR: Ranged,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 3),
        Key.DLVLS: (3, 10),
        Key.RARITY: RarityType.RARE
    },
    'volatile_larva': {
        **_default_values,
        Key.NAME: 'Volatile Larva',
        Key.CHAR: 'l',
        Key.COLOR: colors.light_flame,
        Key.DESCR: 'Red liquid swirls around in a pulsating bulb.',
        Key.MAX_HP: (1,1),
        Key.MAX_STAMINA: (20,20),
        Key.BASE_ARMOR: (0,0),
        Key.BASE_STRENGTH: (1,1),
        Key.LOADOUT: {
            Key.EQUIPMENT:{'ins_mandibles':{}},
            Key.BACKPACK:{}
        },
        Key.AI_BEHAVIOR: Simple,
        Key.SKILLS: (skill_explode_self,),
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (5, 10),
        Key.RARITY: RarityType.RARE
    },
    'centipede' : {
        **_default_values,
        Key.NAME: 'Centipede',
        Key.CHAR: 'c',
        Key.COLOR: colors.lighter_lime,
        Key.DESCR: 'The criss-crossing movement via its plethora of legs masks its impressive length.',
        Key.MAX_HP: (20,30),
        Key.MAX_STAMINA: (120,120),
        Key.BASE_ARMOR: (0,4),
        Key.BASE_STRENGTH: (2,5),
        Key.LOADOUT: {
            Key.EQUIPMENT:{'ins_mandibles':{}},
            Key.BACKPACK:{}
        },
        Key.AI_BEHAVIOR: Simple,
        Key.SKILLS: (skill_entangle_timed,),
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (5, 10),
        Key.RARITY: RarityType.UNCOMMON
    },
}