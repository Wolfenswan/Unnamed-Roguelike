from data.data_enums import GenericType, MonsterType, ItemType, ContainerType, RarityType, Material, Condition, \
    Craftsmanship, BodyType

rarity_values = {
    GenericType.DEFAULT: 100,
    GenericType.UNIQUE: -1,

    RarityType.COMMON: 100,
    RarityType.UNCOMMON: 75,
    RarityType.RARE: 50,
    RarityType.EXOTIC: 30,
    RarityType.LEGENDARY: 10,
    RarityType.UNIQUE: -1,      # Wont be spawned from generic placement functions, only through place_uniques or direct call of create-functions
    RarityType.FORBIDDEN: -1,   # Functionally identical to UNIQUE, exists only to distinguish the purpose of both

    ItemType.USEABLE: 100,
    ItemType.MISC: 80,
    ItemType.MELEE_WEAPON: 60,
    ItemType.RANGED_WEAPON: 60,
    ItemType.SHIELD: 60,
    ItemType.ARMOR: 40,
    ItemType.BELT: 30,

    ContainerType.BARREL: 100,
    ContainerType.CHEST_BASIC: 65,

    MonsterType.GENERIC: 100,
    MonsterType.ELITE: 60,
    MonsterType.LEADER: 10,

    Material.OAK: 100,
    Material.CHITIN: 100,
    Material.LINEN: 100,
    Material.LEATHER: 90,
    Material.IRON: 80,
    Material.STEEL: 50,

    Condition.POOR: 100,
    Condition.NORMAL: 80,
    Condition.GOOD: 50,
    Condition.LEGENDARY: 10,

    Craftsmanship.POOR: 80,
    Craftsmanship.NORMAL: 100,
    Craftsmanship.GOOD: 50,
    Craftsmanship.LEGENDARY: 5,

    BodyType.NORMAL: 100,
    BodyType.SCRAWNY: 50,
    BodyType.OBESE: 30,
    BodyType.TINY: 40,
    BodyType.SMALL: 80,
    BodyType.LARGE: 20,
    BodyType.GARGANTUAN: 5
}
