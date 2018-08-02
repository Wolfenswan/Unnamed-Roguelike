from components.architecture import Architecture, toggle_door
from config_files import colors

arch_doors_data = {
    'door_wooden': {
        'name': 'Door',
        'descr': "A wooden door.",
        'chance': 100,
        "char": '-',
        "color": colors.beige,
        'on_collision': toggle_door,
        'on_interaction': toggle_door
    }
}