from enum import Enum, auto

class Key(Enum):
    """
    All keys for data-dictionary entries (exlcuding attribute modifiers, which are defined in Mod.
    """

    # Generic #
    NAME = auto()               # entity's name
    CHAR = auto()               # character to display the entity with
    COLOR = auto()              # color of the entity when rendered
    COLOR_BLOOD = auto()        # blood color of the entity
    DESCR = auto()              # entity description
    TYPE = auto()               # generic key used whenever entities need to be distinguished by a type (e.g. itemtype or bodytpe)
    ELEMENT = auto()            # UNUSED
    BLOCKS = auto()             # blocking level of the entity
    RENDERING = auto()          # rendering level of the entity
    DLVLS = auto()              # inclusive range in which the entity can be created. by default entities can spawn up to 4 lvls outsider their range (25% less chance each step)
    RARITY = auto()             # general RarityType of the item
    RARITY_MOD = auto()         # modifier applied to overall rarity value
    UNIQUE_CHANCE = auto()      # Only for RarityType.UNIQUE items: chance the unique will spawn, even within its dlvl range
    EVERY_TURN_START = auto()   # function to run for ent on turn start
    EVERY_TURN_END = auto()     # function to run for ent on turn end

    # Actor Attributes, Skills etc. #
    MAX_HP = auto()
    MAX_STAMINA = auto()
    BASE_ARMOR = auto()
    BASE_STRENGTH = auto()
    BASE_VISION = auto()
    EFFECTS = auto()
    LOADOUT = auto()
    LOADOUTS = auto()
    EQUIPMENT = auto()
    BACKPACK = auto()
    AI_BEHAVIOR = auto()
    IMMOBILE = auto()
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
    ON_USE_EFFECT = auto()
    ON_USE_PROJECTILE = auto()
    ON_USE_MSG = auto()
    ON_USE_PARAMS = auto()
    ON_USE_CHARGES = auto()

    # Equipment #
    EQUIP_TO = auto()
    DMG_POTENTIAL = auto()
    AV = auto()
    BLOCK_DEF = auto()
    ATTACK_RANGE = auto()
    QU_SLOTS = auto()
    L_RADIUS = auto()
    TWO_HANDED = auto()
    ONE_HANDED_PENALTY_MOD = auto()
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

class Mod(Enum):
    """
    Attribute modifiers used as key-names in the data-dict and accessed primarily through the Fighter component.
    """
    HP_MULTIPL = auto()
    STR_MULTIPL = auto()
    AV_MULTIPL = auto()
    BLOCK_DEF_MULTIPL = auto()
    BLOCK_STA_DMG_MULTIPL = auto()
    DMG_MULTIPL = auto()
    DMG_FLAT = auto()
    ARMOR_PIERCING_FLAT = auto()
    AV_FLAT = auto()                # adds or substracts a flat amount from the armor value
    COND_MULTIPL = auto()           # modifies the corresponding primary value of an item, i.e. armor value for armor and damage for weapons.
    EXERT_MULTIPL = auto()
    CAN_MOVE = auto()
    CAN_ATTACK = auto()
    SKIP_TURN_CHANCE = auto()


# ENTITY TYPES #

class GenericType(Enum):
    DEFAULT = auto()
    UNIQUE = auto()

class MonsterType(Enum): # Unused at the moment
    GENERIC = auto()
    ELITE = auto()
    LEADER = auto()
    SUMMON = auto()

class Behavior(Enum):
    # AI #
    # To avoid circular imports, these are later used to link to the Behavior of the same Name
    SIMPLE = auto()
    RANGED = auto()
    QUEEN = auto()
    CONFUSED = auto()
    SWARM = auto()

class ItemType(Enum):
    USEABLE = auto()
    MELEE_WEAPON = auto()
    RANGED_WEAPON = auto()
    SHIELD = auto()
    ARMOR = auto()
    BELT = auto()
    MISC = auto()

class ContainerType(Enum):
    BARREL = auto()
    CHEST_BASIC = auto()

class RarityType(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EXOTIC = auto()
    LEGENDARY = auto()
    UNIQUE = auto() # Unique & Forbidden function identically, and only exist to provide distinction in readability
    FORBIDDEN = auto()

class Material(Enum):
    OAK = auto()
    CHITIN = auto()
    LINEN = auto()
    COTTON = auto()
    LEATHER = auto()
    # BUFF LEATHER
    IRON = auto()
    STEEL = auto()

class Element(Enum): # Placeholder at the moment
    FIRE = auto()
    WATER = auto()
    EARTH = auto()
    AIR = auto()
    LIGHTNING = auto()
    ACID = auto()

class Condition(Enum):
    POOR = auto()
    NORMAL = auto()
    GOOD = auto()
    LEGENDARY = auto()

class EquipTo(Enum):
    HEAD = auto()
    TORSO = auto()
    SHIELD_ARM = auto()
    WEAPON_ARM = auto()

class Craftsmanship(Enum):
    POOR = auto()
    NORMAL = auto()
    GOOD = auto()
    LEGENDARY = auto()

class BodyType(Enum):
    NORMAL = auto()
    SCRAWNY = auto()
    OBESE = auto()
    TINY = auto()
    SMALL = auto()
    LARGE = auto()
    GARGANTUAN = auto()