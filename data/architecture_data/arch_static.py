from components.architecture import Architecture
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
    'lichen': {
        Key.NAME: 'Lichen',
        Key.DESCR: 'A callous growth of dry, hoarse fungi.',
        Key.CHAR: chr(177),
        Key.WALLS_ONLY: True,
        Key.COLOR: colors.dark_amber
    },
    'chains': {
        Key.NAME: 'Chains',
        Key.DESCR: 'Rusted chains, caked in dried liquids.',
        Key.CHAR: '%',
        Key.WALLS_ONLY: True,
        Key.COLOR: colors.dark_gray
    },
    'portal': {
        Key.NAME: 'Portal',
        Key.DESCR: 'TODO Portal',
        Key.CHAR: '0',
        Key.COLOR: colors.turquoise,
        Key.BLOCKS: {BlockLevel.SIGHT:True, BlockLevel.FLOOR:True},
        Key.RARITY: RarityType.FORBIDDEN,
        Key.RENDERING: RenderOrder.ALWAYS,
        Key.EVERY_TURN_END: ['self.set_random_color([colors.turquoise, colors.crimson, colors.azure, colors.amber])']
    },
    'stairs_down': {
        Key.NAME: 'Downward Stairs',
        Key.DESCR: 'TODO Stairs Down',
        Key.CHAR: '>',
        Key.COLOR: colors.white,
        Key.BLOCKS: {BlockLevel.SIGHT: False, BlockLevel.FLOOR: True},
        Key.RARITY: RarityType.FORBIDDEN,
        Key.RENDERING: RenderOrder.ALWAYS,
        #Key.ON_INTERACTION: Architecture.change_level
    },
    'stairs_up': {
        Key.NAME: 'Upward Stairs',
        Key.DESCR: 'TODO Stairs UP',
        Key.CHAR: '<',
        Key.COLOR: colors.white,
        Key.BLOCKS: {BlockLevel.SIGHT: False, BlockLevel.FLOOR: True},
        Key.RARITY: RarityType.FORBIDDEN,
        Key.RENDERING: RenderOrder.ALWAYS,
        #Key.ON_INTERACTION: Architecture.change_level
    },
}
