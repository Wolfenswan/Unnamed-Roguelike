import logging
from random import randint

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h

    def create_room(self, game_map):
        # go through the tiles in the rectangle and make them passable
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                game_map.tiles[x][y].set_attributes(floor=True)

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def ranpos(self, game_map, ignore_blocked = True):
        """returns a random, walkable position within the room"""
        x = randint(self.x1 + 1, self.x2 - 1)
        y = randint(self.y1 + 1, self.y2 - 1)
        if not ignore_blocked:
            while game_map.is_blocked(x, y):
                x = randint(self.x1 + 1, self.x2 - 1)
                y = randint(self.y1 + 1, self.y2 - 1)
        return x, y

    def free_tiles(self, game_map, allow_exits = True):
        """
        Returns all free (walkable and not occupied by a blocking object) tiles in a room

        :return: list of free coordinates in the room
        :rtype: list of tuples
        """
        exits = self.exits(game_map)
        free_tiles = []
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                #print(game.map.is_blocked(x, y))
                try:
                    if not game_map.is_blocked(x, y):
                        if allow_exits or (x, y) not in exits:
                            free_tiles.append((x, y))
                except:
                    logging.error(f'Position {x}/{y} in room {self} of size {self.w}/{self.h} is out of bounds')

        return free_tiles

    def exits(self, game_map, max_width = 3):
        """
        :return: room exists
        :rtype: list of tuples
        """

        # TODO properly avoid out of index errors

        exits = []

        # left side
        x, y = self.x1, self.y1
        for i in range(self.h + 1):
            try:
                if game_map.tiles[x][y].walkable:
                    if not game_map.tiles[x][y+max_width].walkable and not game_map.tiles[x][y-max_width].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                y += 1
            except:
                pass

        # right side
        x, y = self.x2, self.y1+1
        for i in range(self.h + 1):
            try:
                if game_map.tiles[x][y].walkable:
                    if not game_map.tiles[x][y + max_width].walkable and not game_map.tiles[x][y - max_width].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                y += 1
            except:
                pass

        # top
        x, y = self.x1, self.y2
        for i in range(self.w + 1):
            try:
                if game_map.tiles[x][y].walkable:
                    if not game_map.tiles[x + max_width][y].walkable and not game_map.tiles[x - max_width][y].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                x += 1
            except:
                pass

        # bottom
        x, y = self.x1, self.y1
        for i in range(self.w + 1):
            try:
                if game_map.tiles[x][y].walkable:
                    if not game_map.tiles[x + max_width][y].walkable and not game_map.tiles[x - max_width][y].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                x += 1
            except:
                pass

        return exits