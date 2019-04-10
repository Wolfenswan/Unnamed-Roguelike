from enum import Enum, auto

# Entity Types #
class GenericType(Enum):
    DEFAULT = auto()
    UNIQUE = auto()


class MonsterType(Enum): # Placeholder at the moment
    GENERIC = auto()
    ELITE = auto()
    LEADER = auto()
    SUMMON = auto()


class Behavior(Enum):
    # AI #
    # To avoid circular imports, these simply correspond to existing behavior sets.
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


# RarityType can be assigned as an additional value to data entries, to add a random weight specific to that data entry
class RarityType(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EXOTIC = auto()
    LEGENDARY = auto()
    UNIQUE = auto() # Unique & Forbidden function identically, and only exist to provide distinction in readability
    FORBIDDEN = auto()


# Entity Quality #
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


class Craftsmanship(Enum):
    POOR = auto()
    NORMAL = auto()
    GOOD = auto()
    LEGENDARY = auto()


# class AttackType(Enum): # AttackType can either be an attribute of a specific weapon, or a move within a moveset
#     NORMAL = auto() # No special rules apply
#     HEAVY = auto() # increased stress when blocking
#     QUICK = auto() # ignores block
#     PIERCING = auto() # ignores AV
#     QUICK_PIERCING = auto() # ignores AV & block


class BodyType(Enum):
    NORMAL = auto()
    SCRAWNY = auto()
    OBESE = auto()
    TINY = auto()
    SMALL = auto()
    LARGE = auto()
    GARGANTUAN = auto()
