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
from components.AI.behavior.ranged import Ranged
from components.AI.behavior.simple import Simple
from components.AI.behavior.swarm import Swarm
from config_files import colors
from data.actor_data.act_skills import skill_generic_charge, skill_generic_slam, skill_explode_self, skill_entangle
from data.data_keys import Key
from data.data_types import RarityType, AttackType

spawn_data = {
    'roachling': {
        Key.NAME: 'Roachling',
        Key.CHAR: 'r',
        Key.COLOR: colors.light_amber,
        Key.DESCR: 'Waddling upright like a clumsy child, the twitching antennae and multitude of jittering legs quickly dispell any passing resemblance.',
        Key.MAX_HP: (2, 6),
        Key.MAX_STAMINA: (80, 80),
        Key.BASE_ARMOR: (0, 0),
        Key.BASE_STRENGTH: (4, 4),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_mandibles':{}
            }
        },
        Key.AI_BEHAVIOR: Swarm,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (4, 9),
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.COMMON
    },
    'dung_beetle': {
        Key.NAME: 'Dung Beetle',
        Key.CHAR: 'd',
        Key.COLOR: colors.beige,
        Key.DESCR: "There is something uniquely unsettling about a giant beetle acting like an agitated bull. It's also the size of one, if you were wondering.",
        Key.MAX_HP: (10, 14),
        Key.MAX_STAMINA: (80, 80),
        Key.BASE_ARMOR: (2, 4),
        Key.BASE_STRENGTH: (6, 8),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_mandibles':{
                    Key.FORCED_ATTACKTYPE: AttackType.HEAVY
                }
            }
        },
        Key.SKILLS: (skill_generic_charge,),
        Key.AI_BEHAVIOR: Simple,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 3),
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.UNCOMMON,
        Key.RARITY_MOD: +5
    },
    'Mantis_Ogre' : {
        Key.NAME: 'Mantis Ogre',
        Key.CHAR: 'M',
        Key.COLOR: colors.light_green,
        Key.DESCR: "Certainly not praying, the elongated frame of these creatures belies the power of their claws.",
        Key.MAX_HP: (20, 28),
        Key.MAX_STAMINA: (100, 100),
        Key.BASE_ARMOR: (4, 5),
        Key.BASE_STRENGTH: (12, 12),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_claws':{
                    Key.FORCED_ATTACKTYPE: AttackType.HEAVY
                }
            }
        },
        Key.SKILLS: (skill_generic_slam,),
        Key.AI_BEHAVIOR: Simple,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.RARE
    },
    'spitting_beetle' : {
        Key.NAME: 'Spitting Beetle',
        Key.CHAR: 'b',
        Key.COLOR: colors.light_green,
        Key.DESCR: "Viscous fluid seeps along tubal appendages towards its front.",
        Key.MAX_HP: (6, 8),
        Key.MAX_STAMINA: (100, 100),
        Key.BASE_ARMOR: (0, 3),
        Key.BASE_STRENGTH: (2, 4),
        Key.LOADOUT: {
            Key.EQUIPMENT:{
                'ins_ranged':{}
            }
        },
        Key.AI_BEHAVIOR: Ranged,
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 3),
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.RARE
    },
    'volatile_larva': {
        Key.NAME: 'Volatile Larva',
        Key.CHAR: 'l',
        Key.COLOR: colors.light_flame,
        Key.DESCR: 'Red liquid swirls around in a pulsating bulb.',
        Key.MAX_HP: (1,1),
        Key.MAX_STAMINA: (100,100),
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
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.RARE
    },
    'centipede' : {
        Key.NAME: 'Centipede',
        Key.CHAR: 'c',
        Key.COLOR: colors.lighter_lime,
        Key.DESCR: 'The criss-crossing movement via its plethora of legs masks its impressive length.',
        Key.MAX_HP: (20,30),
        Key.MAX_STAMINA: (100,100),
        Key.BASE_ARMOR: (2,3),
        Key.BASE_STRENGTH: (6,10),
        Key.LOADOUT: {
            Key.EQUIPMENT:{'ins_mandibles':{}},
            Key.BACKPACK:{}
        },
        Key.AI_BEHAVIOR: Simple,
        Key.SKILLS: (skill_entangle,),
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (1, 100),
        Key.RARITY: RarityType.UNCOMMON
    },
    '' : {

    },
}