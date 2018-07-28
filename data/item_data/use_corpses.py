from gameobjects.items.useables import Useable
from common import colors, item_use as iu

CORPSE_COLOR = colors.darker_red
CORPSE_CHAR = '%'
CORPSE_CLASS = Useable

corpse_data = {
    'corpse_standard': {
        'name': 'An unidentifieable corpse.',
        'chance': 10,
        'dlvls': range(1,99),
        'char': CORPSE_CHAR,
        'color': CORPSE_COLOR,
        'item_class': CORPSE_CLASS,
        'descr': 'The mangled corpse of a poor adventurer.',
        'on_use': iu.eat_corpse,
        'on_use_params': 'You almost vomit from the taste.'
    },

    'corpse_bits': {
        'name': 'Pieces of flesh and guts.',
        'chance': 0,
        'dlvls': range(1,99),
        'char': '~',
        'color': CORPSE_COLOR,
        'item_class': CORPSE_CLASS,
        'descr': 'A heap of bits that must have come loose during battle.',
        'on_use': iu.eat_corpse,
        'on_use_params': 'You almost vomit from the taste.'
    }
}
