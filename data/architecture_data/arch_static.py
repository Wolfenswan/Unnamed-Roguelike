from config_files import colors
from data.entitytypes import Rarity

SO_COLOR = colors.white

arch_static_data = {
    'pillar': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99),
        "char": chr(186),
        "color": SO_COLOR,
        "blocks": True,
        'blocks_sight': True
    },
    'arch': {
        'name': 'Arch',
        'descr': 'The decrepit arch looms over you.',
        'rarity': Rarity.COMMON,
        'dlvls': (1, 99),
        "char": '^',
        "color": SO_COLOR
    }
}
