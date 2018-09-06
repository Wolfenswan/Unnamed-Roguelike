from enum import Enum

class Rarity(Enum):
    COMMON = 100
    UNCOMMON = 75
    RARE = 50
    EXOTIC = 25
    LEGENDARY = 10
    UNIQUE = -1

# Values indicate rarity weight per type #
class GenericType(Enum):
    DEFAULT = 100
    UNIQUE = -1

class MonsterType(Enum):
    GENERIC = 100
    ELITE = 60
    LEADER = 20

class ItemType(Enum):
    USEABLE = 100
    WEAPON = 60
    ARMOR = 40
    OFFHAND = 40
    BELT = 30

class ContainerType(Enum):
    BARREL = 100
    CHEST_BASIC = 65