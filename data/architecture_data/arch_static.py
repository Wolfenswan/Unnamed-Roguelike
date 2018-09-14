from config_files import colors
from data.shared_data.types_data import RarityType

arch_static_data = {
    'pillar': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'dlvls': (1, 99),
        "char": chr(20), #tcod.CHAR_PILCROW
        "color": colors.white,
        "blocks": {'walk':True,'sight':True,'floor':True}
    },
    'arch': {
        'name': 'Arch',
        'descr': 'The decrepit arch looms over you.',
        'dlvls': (1, 99),
        "char": '^',
        "color": colors.white
    },
    'moss': {
        'name': 'Moss',
        'descr': 'Sickly green patches are spreading across this wall.',
        'char': '#',
        'walls_only': True,
        'color': colors.dark_green
    }
}
