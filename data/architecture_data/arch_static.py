from config_files import colors
from data.data_keys import Key
from data.data_types import RarityType
from gameobjects.block_level import BlockLevel
from rendering.render_order import RenderOrder

arch_static_data = {
    'pillar': {
        Key.NAME: 'Old Pillar',
        Key.DESCR: 'An old, crumbling pillar.',
        Key.DLVLS: (1, 99),
        Key.CHAR: chr(20), #tcod.CHAR_PILCROW
        Key.COLOR: colors.white,
        Key.RENDERING: RenderOrder.ALWAYS,
        Key.BLOCKS: {BlockLevel.WALK:True,BlockLevel.SIGHT:True,BlockLevel.FLOOR:True}
    },
    'arch': {
        Key.NAME: 'Arch',
        Key.DESCR: 'The decrepit arch looms over you.',
        Key.DLVLS: (1, 99),
        Key.CHAR: '^',
        Key.RENDERING: RenderOrder.ALWAYS,
        Key.COLOR: colors.white
    },
    'moss': {
        Key.NAME: 'Moss',
        Key.DESCR: 'Sickly green patches are spreading across this wall.',
        Key.CHAR: chr(177),
        Key.WALLS_ONLY: True,
        Key.COLOR: colors.dark_green
    },
    'portal': {
        Key.NAME: 'Portal',
        Key.DESCR: 'TODO Portal',
        Key.CHAR: '0',
        Key.COLOR: colors.turquoise,
        Key.BLOCKS: {BlockLevel.SIGHT:True, BlockLevel.FLOOR:True},
        Key.RARITY: RarityType.UNIQUE,
        Key.RENDERING: RenderOrder.ALWAYS,
        Key.EVERY_TURN_END: ['self.set_random_color([colors.turquoise, colors.crimson, colors.azure, colors.amber])']
    }
}
