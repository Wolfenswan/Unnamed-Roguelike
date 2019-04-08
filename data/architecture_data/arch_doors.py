from components.architecture import Architecture
from data.data_keys import Key
from data.data_types import Material
from data.data_types import RarityType
from gameobjects.block_level import BlockLevel
from rendering.render_order import RenderOrder

arch_doors_data = {
    'door': {
        Key.NAME: 'Door',
        Key.MATERIAL: (Material.OAK, Material.IRON, Material.STEEL),
        Key.DESCR: "A creaky old door.",
        Key.RARITY: RarityType.COMMON,
        Key.BLOCKS: {BlockLevel.FLOOR: True, BlockLevel.WALK: True, BlockLevel.SIGHT: True},
        Key.DLVLS: (1, 99),
        Key.CHAR: '+',
        Key.RENDERING: RenderOrder.ALWAYS,
        Key.ON_COLLISION: Architecture.toggle_door,
        Key.ON_INTERACTION: Architecture.toggle_door
    }
}
