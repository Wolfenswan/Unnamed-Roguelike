from components.architecture import Architecture
from config_files import colors

arch_containers_data = {
    'barrel_wood': {
        'name': 'Wooden Barrel',
        'descr': "A brown barrel of unknown contents.",
        'chance': 100,
        'dlvls': (1, 99),
        "char": 'o',
        "color": colors.lime,
        "blocks": True,
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.smash_object
    }
}