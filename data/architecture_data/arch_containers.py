from components.architecture import Architecture
from config_files import colors

arch_containers_data = {
    'barrel_wood': {
        'name': 'Wooden Barrel',
        'descr': "A barrel of unknown contents.",
        'chance': 100,
        'dlvls': (1, 99),
        "char": 'o',
        "color": colors.wood,
        "blocks": True,
        'container_room': (0,4),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.smash_object
    },
    'chest_wood': {
        'name': 'Wooden Chest',
        'descr': "A simple, yet sturdy chest.",
        'chance': 10,
        'dlvls': (1, 99),
        "char": '+',
        "color": colors.wood,
        "blocks": False,
        'container_room': (1, 6),
        'on_collision': Architecture.blocks_info,
        'on_interaction': Architecture.open_container
    },

}