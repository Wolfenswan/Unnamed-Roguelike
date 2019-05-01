from components.AI.behavior.queen import Queen
from components.actors.fighter_util import State
from config_files import colors
from data.actor_data.act_skills import skill_generic_slam, skill_hatch
from data.data_keys import Key
from data.data_types import RarityType

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
        Key.DLVLS: (10, 10),
        Key.RARITY: RarityType.UNIQUE
    },
    # 'egg': {
    #         Key.NAME: 'Egg',
    #         Key.CHAR: 'e',
    #         Key.COLOR: colors.beige,
    #         Key.COLOR_BLOOD : colors.blood_slime,
    #         Key.DESCR: 'TODO EGG.',
    #         Key.MAX_HP: 1,
    #         Key.MAX_STAMINA: 100,
    #         Key.BASE_ARMOR: 10,
    #         Key.BASE_STRENGTH: 0,
    #         Key.EFFECTS: {
    #             State.IMMOBILE: True
    #         },
    #         Key.SKILLS: (skill_hatch,),
    #     },
    # 'hatchling': {
    #         Key.NAME: 'Hatchling',
    #         Key.CHAR: 'h',
    #         Key.COLOR: colors.beige,
    #         Key.COLOR_BLOOD : colors.blood_slime,
    #         Key.DESCR: 'TODO hatchling.',
    #         Key.MAX_HP: 5,
    #         Key.MAX_STAMINA: 100,
    #         Key.BASE_ARMOR: 0,
    #         Key.BASE_STRENGTH: 3,
    #         Key.EFFECTS: {
    #             State.IMMOBILE: True
    #         },
    #         Key.SKILLS: (skill_hatch,),
    # }
}