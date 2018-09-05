from enum import Enum

class Rarity(Enum):
    COMMON = 100
    UNCOMMON = 75
    RARE = 50
    EXOTIC = 25
    LEGENDARY = 10
    UNIQUE = -1

class RarityItemType(Enum):
    USEABLE = 100
    WEAPON = 60
    ARMOR = 40
    SHIELD = 40
    ACS = 30

class RarityContainerType(Enum):
    BARREL = 100
    CHEST_BASIC = 65
