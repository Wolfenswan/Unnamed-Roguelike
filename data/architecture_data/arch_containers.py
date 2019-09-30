from components.architecture import Architecture
from data.data_keys import Key
from data.data_types import ItemType, ContainerType, Material
from data.data_types import RarityType
from gameobjects.block_level import BlockLevel

arch_containers_data = {
    'barrel': {
        Key.NAME: 'barrel',
        Key.MATERIAL: (Material.OAK, Material.IRON),
        Key.DESCR: "A barrel of unknown contents.",
        Key.TYPE: ContainerType.BARREL,
        Key.RARITY: RarityType.COMMON,
        Key.DLVLS: (1, 99),
        Key.CHAR: 'o',
        Key.BLOCKS: {BlockLevel.WALK:True, BlockLevel.FLOOR:True},
        Key.CONTAINER_ROOM: (0,4),
        Key.CONTENTS_RARITY: (RarityType.COMMON,),
        Key.CONTENTS_TYPE: (ItemType.USEABLE, ItemType.MISC),
        Key.ON_COLLISION: Architecture.blocks_info,
        Key.ON_INTERACTION: Architecture.smash_object
    },
    'chest_basic': {
        Key.NAME: 'chest',
        Key.MATERIAL: (Material.OAK, Material.IRON, Material.STEEL),
        Key.DESCR: "A simple, yet sturdy chest.",
        Key.TYPE: ContainerType.CHEST_BASIC,
        Key.RARITY: RarityType.UNCOMMON,
        Key.DLVLS: (1, 99),
        Key.CHAR: chr(61),
        Key.BLOCKS: {BlockLevel.FLOOR:True},
        Key.CONTAINER_ROOM: (1, 5),
        Key.CONTENTS_RARITY: (RarityType.COMMON, RarityType.UNCOMMON, RarityType.RARE),
        Key.CONTENTS_TYPE: (ItemType.USEABLE, ItemType.MELEE_WEAPON, ItemType.SHIELD, ItemType.MISC, ItemType.BELT),
        Key.ON_COLLISION: Architecture.blocks_info,
        Key.ON_INTERACTION: Architecture.open_container
    },
    'weapon_rack': {
        Key.NAME: 'weapon rack',
        Key.MATERIAL: (Material.IRON, Material.STEEL),
        Key.DESCR: "Rust makes it hard to tell where the rack ends and its content begins.",
        Key.TYPE: ContainerType.CHEST_BASIC,
        Key.RARITY: RarityType.UNCOMMON,
        Key.RARITY_MOD: +5,
        Key.DLVLS: (1, 99),
        Key.CHAR: chr(61),
        Key.BLOCKS: {BlockLevel.FLOOR:True, BlockLevel.WALK:True},
        Key.CONTAINER_ROOM: (1, 3),
        Key.CONTENTS_RARITY: (RarityType.COMMON, RarityType.UNCOMMON),
        Key.CONTENTS_TYPE: (ItemType.MELEE_WEAPON, ItemType.SHIELD),
        Key.ON_COLLISION: Architecture.blocks_info,
        Key.ON_INTERACTION: Architecture.open_container
    },
}