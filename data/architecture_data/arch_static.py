from config_files import colors
from data.data_types import RarityType
from gameobjects.block_level import BlockLevel
from rendering.render_order import RenderOrder

arch_static_data = {
    'pillar': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'dlvls': (1, 99),
        "char": chr(20), #tcod.CHAR_PILCROW
        "color": colors.white,
        'rendering': RenderOrder.ALWAYS,
        "blocks": {BlockLevel.WALK:True,BlockLevel.SIGHT:True,BlockLevel.FLOOR:True}
    },
    'arch': {
        'name': 'Arch',
        'descr': 'The decrepit arch looms over you.',
        'dlvls': (1, 99),
        "char": '^',
        'rendering': RenderOrder.ALWAYS,
        "color": colors.white
    },
    'moss': {
        'name': 'Moss',
        'descr': 'Sickly green patches are spreading across this wall.',
        'char': chr(177),
        'walls_only': True,
        'color': colors.dark_green
    },
    'portal': {
        'name': 'Portal',
        'descr': 'TODO Portal',
        'char': '0',
        'color': colors.turquoise,
        'blocks': {BlockLevel.SIGHT:True, BlockLevel.FLOOR:True},
        'rarity': RarityType.UNIQUE,
        'rendering': RenderOrder.ALWAYS,
        'every_turn_end': ['self.set_random_color([colors.turquoise, colors.crimson, colors.azure, colors.amber])']
    }
}
