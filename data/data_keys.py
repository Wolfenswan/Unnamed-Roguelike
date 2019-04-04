from enum import Enum, auto

"""
All data entries refer to members of the Key class as dictionary keys.
"""

class Key(Enum):
    # Generic #
    NAME = auto()
    CHAR = auto()
    COLOR = auto()
    DESCR = auto()
    TYPE = auto()
    ELEMENT = auto()
    BLOCKS = auto()
    RENDERING = auto()
    DLVLS = auto()
    RARITY = auto()
    RARITY_MOD = auto()
    EVERY_TURN_START = auto()
    EVERY_TURN_END = auto()

    # Actors #
    MAX_HP = auto()
    MAX_STAMINA = auto()
    BASE_ARMOR = auto()
    BASE_STRENGTH = auto()
    BASE_VISION = auto()
    LOADOUT = auto()
    LOADOUTS = auto()
    EQUIPMENT = auto()
    BACKPACK = auto()
    AI_BEHAVIOR = auto()
    SKILL = auto()
    SKILLS = auto()
    BARKS = auto()
    BODYTYPES = auto()
    GROUP_SIZE = auto()
    FORCED_MOVESET = auto()

    # Items #
    MATERIAL = auto()
    CONDITION = auto()
    CRAFTSMANSHIP = auto()
    CAN_DROP = auto()

    # Useables #
    ON_USE = auto()
    ON_USE_MSG = auto()
    ON_USE_PARAMS = auto()
    CHARGES = auto()

    # Equipment #
    EQUIP_TO = auto()
    DMG_POTENTIAL = auto()
    AV = auto()
    BLOCK_DEF = auto()
    ATTACK_RANGE = auto()
    QU_SLOTS = auto()
    L_RADIUS = auto()
    TWO_HANDED = auto()
    MOVESET = auto()

    # Movesets & Skills #
    DEFAULT = auto()
    VERB = auto()
    VERBS = auto()
    EXTEND_ATTACK = auto()
    ACTIVATE_CONDITIONS = auto()
    ACTIVATE_CONDITION_KWARGS = auto()
    ON_ACTIVATE_KWARGS = auto()
    COOLDOWN_LENGTH = auto()
    RANDOM = auto()

    # Architecture #
    CONTAINER_ROOM = auto()
    CONTENTS_TYPE = auto()
    CONTENTS_RARITY = auto()
    ON_COLLISION = auto()
    ON_INTERACTION = auto()
    WALLS_ONLY = auto()

    # Modifiers #
    HP_MULTIPL = auto()
    STR_MULTIPL = auto()
    AV_MULTIPL = auto()
    BLOCK_DEF_MULTIPL = auto()
    BLOCK_STA_DMG_MULTIPL = auto()
    DMG_MULTIPL = auto()
    DMG_FLAT = auto()
    AV_FLAT = auto()
    MOD_MULTIPL = auto()
    EXERT_MULTIPL = auto()
