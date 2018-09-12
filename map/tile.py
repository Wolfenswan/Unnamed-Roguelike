class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, x, y, block_sight=None, walkable = None, gibbed=False):
        self.blocked = blocked
        self.x, self.y = x, y

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            self.block_sight = blocked

        if walkable is None:
            self.walkable = not blocked

        self.explored = 0
        self.gibbed = gibbed

    @property
    def pos(self):
        return (self.x, self.y)

    def toggle_attributes(self):
        self.blocked = not self.blocked
        self.block_sight = not self.block_sight
        self.walkable = not self.walkable

    def set_attributes(self, floor=False):
        if floor:
            self.blocked = False
            self.block_sight = False
            self.walkable = True
        else:
            self.blocked = True
            self.block_sight = True
            self.walkable = False