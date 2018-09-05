from components.architecture import Architecture
from config_files import colors
from data.entitytypes import Rarity

arch_doors_data = {
    'door_wooden': {
        'name': 'Door',
        'descr': "A wooden door.",
        'rarity': Rarity.COMMON,
        "char": '-',
        "color": colors.wood,
        'on_collision': Architecture.toggle_door,
        'on_interaction': Architecture.toggle_door
    }
}
