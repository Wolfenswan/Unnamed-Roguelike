from common import colors

SO_COLOR = colors.white

so_architecture_data = {
    'pillar_1': {
        'name': 'Old Pillar',
        'descr': 'An old, crumbling pillar.',
        'chance': 100,
        'dlvls': range(1,99),
        "char": chr(186),
        "color": SO_COLOR,
        "blocks": True,
        "transparent": False
    },
    'arch': {
        'name': 'Arch',
        'descr': 'The decrepit arch looms over you.',
        'chance': 100,
        'dlvls': range(1,99),
        "char": '^',
        "color": SO_COLOR,
        "blocks": False,
        "transparent": True
    }
}