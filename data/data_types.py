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
    UNIQUE = auto()


# Entity Quality #
class Material(Enum):
    OAK = auto()
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


class BodyType(Enum):
    NORMAL = auto()
    SCRAWNY = auto()
    OBESE = auto()
    TINY = auto()
    SMALL = auto()
    LARGE = auto()
    GARGANTUAN = auto()
