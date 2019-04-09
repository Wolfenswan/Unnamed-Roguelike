from components.AI.behavior.queen import Queen
from components.actors.fighter_util import State
from config_files import colors
from data.data_keys import Key
from data.data_types import RarityType

spawn_data_unique = {
    'queen': {
        Key.NAME: 'Insect Queen',
        Key.CHAR: 'Q',
        Key.COLOR: colors.purple,
        Key.DESCR: 'TODO QUEEN.',
        Key.MAX_HP: (50, 50),
        Key.MAX_STAMINA: (100, 100),
        Key.BASE_ARMOR: (5, 5),
        Key.BASE_STRENGTH: (5, 5),
        Key.EFFECTS: {
            State.IMMOBILE: True
        },
        Key.LOADOUT: {
            Key.EQUIPMENT: {'ins_ranged': {}},
            Key.BACKPACK: {}
        },
        Key.AI_BEHAVIOR: Queen,
        Key.SKILLS: (),
        Key.BARKS: ('insect',),
        Key.GROUP_SIZE: (1, 1),
        Key.DLVLS: (10, 10),
        Key.RARITY: RarityType.UNIQUE
    },
}