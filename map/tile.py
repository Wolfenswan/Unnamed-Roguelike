from dataclasses import dataclass

from config_files import colors
from rendering.util_functions import multiply_rgb_color

@dataclass
class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    blocked : bool
    x : int
    y : int
    block_sight : bool = None
    block_walk : bool = None
    block_projectile : bool = None

    def __post_init__(self):
        self.char = chr(178)
        self.fg_color = colors.stone
        self.explored = 0

        # By default, if a tile is blocked, it also blocks sight
        if self.block_sight is None:
            self.block_sight = self.blocked

        if self.block_walk is None:
            self.walkable = not self.blocked

        if self.block_projectile is None:
            self.block_projectile = not self.blocked

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

    def gib(self, char=None, color=colors.corpse):
        if char and self.walkable:
            self.char = char
        self.fg_color = color

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