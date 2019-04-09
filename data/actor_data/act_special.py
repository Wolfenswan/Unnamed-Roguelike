from components.actors.fighter_util import State
from config_files import colors
from data.data_keys import Key
from data.data_types import RarityType

spawn_data_special = {
    'egg': {    # Only for debug purposes; the actual eggs spawned by the queen are defined in special_entities.py
            Key.NAME: 'Egg',
            Key.CHAR: 'e',
            Key.COLOR: colors.beige,
            Key.DESCR: 'TODO EGG.',
            Key.MAX_HP: 1,
            Key.MAX_STAMINA: 100,
            Key.BASE_ARMOR: 10,
            Key.EFFECTS: {
                State.IMMOBILE: True
            },
            Key.AI_BEHAVIOR: None,
            # Key.SKILLS: (skill_hatch),
        }
}