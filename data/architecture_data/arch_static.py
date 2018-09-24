from config_files import colors
from gameobjects.block_level import BlockLevel

arch_static_data = {
    'pillar': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'dlvls': (1, 99),
        "char": chr(20), #tcod.CHAR_PILCROW
        "color": colors.white,
        "blocks": {BlockLevel.WALK:True,BlockLevel.SIGHT:True,BlockLevel.FLOOR:True}
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
        'char': chr(177),
        'walls_only': True,
        'color': colors.dark_green
    }
}
