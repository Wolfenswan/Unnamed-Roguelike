from components.architecture import Architecture
from data.shared_data.types_data import Material
from data.shared_data.types_data import RarityType

arch_doors_data = {
    'door': {
        'name': 'Door',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': "A creaky old door.",
        'rarity': RarityType.COMMON,
        'blocks': {'floor': True, 'walk': False},
        'dlvls': (1, 99),
        "char": '-',
        'on_collision': Architecture.toggle_door,
        'on_interaction': Architecture.toggle_door
    }
}
