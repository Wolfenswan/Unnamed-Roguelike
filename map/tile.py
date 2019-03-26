from config_files import colors
from rendering.util_functions import multiply_rgb_color

# TODO dataclass
class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, x, y, block_sight=None, block_walk = None, block_projectile=None):
        self.blocked = blocked
        self.x, self.y = x, y
        self.char = chr(178)

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            self.block_sight = blocked

        if block_walk is None:
            self.walkable = not blocked

        if block_projectile is None:
            self.block_projectile = not blocked

        self.fg_color = colors.stone

        self.explored = 0

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def wall(self):
        return self.walkable

    @property
    def floor(self):
        return self.walkable

    @property
    def dark_color(self):
        color = multiply_rgb_color(self.fg_color, factor_range=(0.85, 0.85), darken=True)
        return color

    def set_char(self, force=None):
        if not force:
            self.char = '.' if self.walkable else chr(178)

    def gib(self, char=None):
        if char and self.walkable:
            self.char = char
        self.fg_color = colors.corpse

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

    def surrounding_tiles(self, dist = 1):
        game_map = self.owner
        tiles = []
        for dx in range(-dist, dist):
            for dy in range(-dist, dist):
                if not (dx == 0 and dy == 0) and game_map.tiles.get((self.x + dx, self.y + dy)):
                    tiles += [game_map.tiles[self.x + dx, self.y + dy]]
        return tiles