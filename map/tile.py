from config_files import colors
from rendering.util_functions import multiply_rgb_color


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, x, y, block_sight=None, walkable = None):
        self.blocked = blocked
        self.x, self.y = x, y
        self.char = chr(178)

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            self.block_sight = blocked

        if walkable is None:
            self.walkable = not blocked

        self.fg_color = colors.stone

        self.explored = 0

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def dark_color(self):
        color = multiply_rgb_color(self.fg_color, factor_range=(0.8, 0.8), darken=True)
        return color

    def set_char(self, force=None):
        if not force:
            self.char = '.' if self.walkable else chr(178)

    def set_fov_color(self, color=False):
        if color:
            self.fov_color = color
        else:
            self.fov_color = colors.floor_default if self.walkable else colors.wall_default

    def gib(self, char=None):
        if char and self.walkable:
            self.char = char
        self.fov_color = colors.corpse

    def toggle_attributes(self):
        self.blocked = not self.blocked
        self.block_sight = not self.block_sight
        self.walkable = not self.walkable
        self.set_char()

    def set_attributes(self, floor=False):
        if floor:
            self.blocked = False
            self.block_sight = False
            self.walkable = True
        else:
            self.blocked = True
            self.block_sight = True
            self.walkable = False
        self.set_char()