import logging


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def free_tiles(self, game):
        """
        Returns all free (walkable and not occupied by a blocking object) tiles in a room

        :return: list of free coordinates in the room
        :rtype: list of tuples
        """

        free_tiles = []
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                #print(game.map.is_blocked(x, y))
                try:
                    #if game.map.walkable[x][y] and not game.map.is_blocked(x, y):
                    if not game.map.is_blocked(x, y):
                        free_tiles.append((x, y))
                except:
                    logging.error(f'Position {x}/{y} in room {self} of size {self.w}/{self.h} is out of bounds')

        return free_tiles