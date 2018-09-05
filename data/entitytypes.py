from enum import Enum

class Rarity(Enum):
    COMMON = 100
    UNCOMMON = 75
    RARE = 50
    EXOTIC = 25
    LEGENDARY = 10
    UNIQUE = -1

# Values indicate rarity weight of each type #
class ItemType(Enum):
    USEABLE = 100
    WEAPON = 60
    ARMOR = 40
    OFFHAND = 40
    BELT = 30

class ContainerType(Enum):
    BARREL = 100
    CHEST_BASIC = 65