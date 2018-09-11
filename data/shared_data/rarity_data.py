from data.shared_data.types_data import MonsterType, ContainerType, ItemType, GenericType, Material, Condition, \
    RarityType, Craftsmanship

# Each type is assigned a weight value that is taken into account when creating an item of the corresponding type
# RarityType can be assigned as an additional value to data entries, to add a weight specific to that data entry
rarity_values = {
    GenericType.DEFAULT: 100,
    GenericType.UNIQUE: -1,

    RarityType.COMMON: 100,
    RarityType.UNCOMMON: 75,
    RarityType.RARE: 50,
    RarityType.EXOTIC: 30,
    RarityType.LEGENDARY: 10,
    RarityType.UNIQUE: -1,

    ItemType.USEABLE: 100,
    ItemType.MISC: 80,
    ItemType.WEAPON: 60,
    ItemType.SHIELD: 60,
    ItemType.ARMOR: 40,
    ItemType.BELT: 30,

    ContainerType.BARREL: 100,
    ContainerType.CHEST_BASIC: 65,

    MonsterType.GENERIC: 100,
    MonsterType.ELITE: 60,
    MonsterType.LEADER: 10,

    Material.OAK: 100,
    Material.LINEN: 100,
    Material.LEATHER: 90,
    Material.IRON: 80,
    Material.STEEL: 50,

    Condition.POOR: 100,
    Condition.NORMAL: 80,
    Condition.GOOD: 60,
    Condition.LEGENDARY: 10,

    Craftsmanship.POOR: 100,
    Craftsmanship.NORMAL: 80,
    Craftsmanship.GOOD: 60,
    Craftsmanship.LEGENDARY: 10
}
