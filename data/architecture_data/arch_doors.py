from components.architecture import Architecture
from config_files import colors

arch_doors_data = {
    'door_wooden': {
        'name': 'Door',
        'descr': "A wooden door.",
        'chance': 100,
        "char": '-',
        "color": colors.beige,
        'blocks': False,
        'on_collision': Architecture.toggle_door,
    }
}