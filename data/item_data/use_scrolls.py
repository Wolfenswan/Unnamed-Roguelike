from random import choice
from random import randint

from config_files import colors
from effects.spells import cast_fireball_on
from gui.messages import Message

SCROLL_CHAR = '='
SCROLL_COLOR = colors.light_yellow

use_scrolls_data = {
    'scr_fireball': {
        "name": 'Scroll of Fireball',
        'descr': 'A timeless classic.',
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        'on_use': cast_fireball_on,
        'on_use_msg': 'Left-click an enemy to burn it, or right-click to cancel.',
        'targeting': True,
        "on_use_params": {'dmg': 12, 'radius': 3},
        'chance': 30,
        'dlvls': (1, 99)
    }
}
