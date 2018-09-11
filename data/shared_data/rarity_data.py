from enum import Enum

from data.data_types import MonsterType, ContainerType, ItemType, GenericType, Material

# Rarity defines the overall weight for an item to appear
class Rarity(Enum):
    COMMON = 100
    UNCOMMON = 75
    RARE = 50
    EXOTIC = 25
    LEGENDARY = 10
    UNIQUE = -1

# The rarity_types dict assigns a weight to each item type
rarity_types = {
    GenericType.DEFAULT: 100,
    GenericType.UNIQUE: -1,

    ItemType.USEABLE:100,
    ItemType.WEAPON:60,
    ItemType.OFFHAND:60,
    ItemType.ARMOR:40,
    ItemType.BELT:30,

    ContainerType.BARREL: 100,
    ContainerType.CHEST_BASIC: 65,

    MonsterType.GENERIC: 100,
    MonsterType.ELITE: 60,
    MonsterType.LEADER: 10
}

# rarity_material = {
#     Material.OAK: 100,
#     Material.LINEN: 100,
#     Material.LEATHER: 90,
#     Material.COTTON: 90,
#     Material.IRON: 75,
#     Material.STEEL: 50
# }
