from random import choice
from random import randint

from gameobjects.items.useables import Useable
from common import colors, item_use as iu

SCROLL_CHAR = '='
SCROLL_COLOR = colors.light_yellow
SCROLL_CLASS = Useable

use_scrolls_data = {
    'scr_tel': {
        'name': 'Scroll of Teleport',
        'descr': 'A scroll of Teleport.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        'item_class': SCROLL_CLASS,
        'on_use': iu.cast_teleport,
        "on_use_params": {'max_range': 4}
    },

    'scr_magicmissile': {
        "name": 'Scroll of Magic Missile',
        'descr': 'A scroll of Magic Missile.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        "item_class": SCROLL_CLASS,
        'on_use': iu.cast_magicmissile,
        "on_use_params": {'pwr': randint(4, 8), 'spell_range': 6}
    },

    'scr_confusion': {
        "name": 'Scroll of Confusion',
        'descr': 'It will bedazzle any monster.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        "item_class": SCROLL_CLASS,
        'on_use': iu.cast_confusion,
        "on_use_params": {'pwr': randint(4, 6), 'spell_range': choice([0, 3])}
    },

    'scr_fireball': {
        "name": 'Scroll of Fireball',
        'descr': 'A timeless classic.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        "item_class": SCROLL_CLASS,
        'on_use': iu.cast_fireball,
        "on_use_params": {'pwr': 12, 'radius': 3}
    },

    'scr_lightning': {
        "name": 'Scroll of Lightning',
        'descr': 'This will zap your enemies.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        "item_class": SCROLL_CLASS,
        'on_use': iu.cast_lightning,
        "on_use_params": {'pwr': randint(8, 10), 'spell_range': 3}
    },

    'scr_cone': {
        "name": 'Scroll of Conestuff',
        'descr': 'It is a cone.',
        'chance': 30,
        'dlvls': range(1,99),
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        "item_class": SCROLL_CLASS,
        'on_use': iu.cast_cone,
        "on_use_params": {'pwr': randint(8, 10), 'spell_range': 3}
    }
}
