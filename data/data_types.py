from enum import Enum, auto

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
    OFFHAND = auto()
    ARMOR = auto()
    BELT = auto()

class ContainerType(Enum):
    BARREL = auto()
    CHEST_BASIC = auto()

class Material(Enum):
    OAK = auto()
    LINEN = auto()
    COTTON = auto()
    LEATHER = auto()
    # BUFF LEATHER
    IRON = auto()
    STEEL = auto()
