from enum import Enum, auto

# Entity Types #
class GenericType(Enum):
    DEFAULT = auto()
    UNIQUE = auto()


class MonsterType(Enum): # currently unused
    GENERIC = auto()
    ELITE = auto()
    LEADER = auto()


class ItemType(Enum):
    USEABLE = auto()
    WEAPON = auto()
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


class AttackType(Enum): # AttackType can either be an attribute of a specific weapon, or a move within a moveset
    NORMAL = auto() # No special rules apply
    HEAVY = auto() # increased stress when blocking
    QUICK = auto() # ignores blocks


class BodyType(Enum):
    NORMAL = auto()
    SCRAWNY = auto()
    OBESE = auto()
    TINY = auto()
    SMALL = auto()
    LARGE = auto()
    GARGANTUAN = auto()
