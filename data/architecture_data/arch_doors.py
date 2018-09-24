from components.architecture import Architecture
from data.data_types import Material
from data.data_types import RarityType
from gameobjects.block_level import BlockLevel

arch_doors_data = {
    'door': {
        'name': 'Door',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': "A creaky old door.",
        'rarity': RarityType.COMMON,
        'blocks': {BlockLevel.FLOOR: True, BlockLevel.WALK: False},
        'dlvls': (1, 99),
        "char": '-',
        'on_collision': Architecture.toggle_door,
        'on_interaction': Architecture.toggle_door
    }
}
