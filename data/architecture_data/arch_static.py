from config_files import colors
from data.shared_data.types_data import RarityType

SO_COLOR = colors.white

arch_static_data = {
    'pillar': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'rarity': RarityType.COMMON,
        'dlvls': (1, 99),
        "char": chr(186),
        "color": SO_COLOR,
        "blocks": True,
        'blocks_sight': True
    },
    'arch': {
        'name': 'Arch',
        'descr': 'The decrepit arch looms over you.',
        'rarity': RarityType.COMMON,
        'dlvls': (1, 99),
        "char": '^',
        "color": SO_COLOR
    }
}
