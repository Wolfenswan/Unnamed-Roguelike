from components.AI.behavior.queen import Queen
from components.combat.fighter_util import State
from config_files import colors
from data.actor_data.act_skills import skill_generic_slam
from data.data_enums import Key, RarityType

npc_data_unique = {
    'queen': {
        Key.NAME: 'Insect Queen',
        Key.CHAR: 'Q',
        Key.COLOR: colors.purple,
        Key.COLOR_BLOOD : colors.blood_ins,
        Key.DESCR: 'TODO QUEEN.',
        Key.MAX_HP: (50, 50),
        Key.MAX_STAMINA: (100, 100),
        Key.BASE_ARMOR: (5, 5),
        Key.BASE_STRENGTH: (5, 5),
        Key.EFFECTS: {
            State.IMMOBILE: True
        },
        Key.LOADOUT: {
            Key.EQUIPMENT: {'ins_ranged': {},
                            'ins_mandibles': {}},
            Key.BACKPACK: {}
        },
        Key.AI_BEHAVIOR: Queen,
        Key.SKILLS: (skill_generic_slam,),
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (5, 5),
        Key.RARITY: RarityType.UNIQUE
    },
}