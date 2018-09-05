from config_files import colors
from abilities.spells import cast_fireball_on
from data.rarity import Rarity

SCROLL_CHAR = '='
SCROLL_COLOR = colors.light_yellow

use_scrolls_data = {
    'scr_fireball': {
        "name": 'Scroll of Fireball',
        'descr': 'A timeless classic.',
        "char": SCROLL_CHAR,
        "color": SCROLL_COLOR,
        'on_use': cast_fireball_on,
        'on_use_msg': 'Move the cursor over the intended target, press Enter to confirm.',
        'targeting': True,
        "on_use_params": {'dmg': 12, 'radius': 3, 'range': 5},
        'rarity': Rarity.COMMON,
        'rarity_mod': -5,
        'dlvls': (1, 99)
    }
}
