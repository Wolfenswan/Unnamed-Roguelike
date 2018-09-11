from components.architecture import Architecture
from data.data_types import Material
from data.shared_data.rarity_data import Rarity

arch_doors_data = {
    'door': {
        'name': 'Door',
        'materials': (Material.OAK, Material.IRON, Material.STEEL),
        'descr': "A creaky old door.",
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99),
        "char": '-',
        'on_collision': Architecture.toggle_door,
        'on_interaction': Architecture.toggle_door
    }
}
