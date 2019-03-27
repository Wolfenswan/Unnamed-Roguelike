from random import choice

from dataclasses import dataclass

from debug.timer import debug_timer


@dataclass
class Rect:
    x1 : int
    y1 : int
    w : int
    h : int

    def __post_init__(self):
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h
        self.center = int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)
        self.pos_list = []
        for y in range(self.y1, self.y2):
            for x in range(self.x1, self.x2):
                self.pos_list.append((x, y))

    def create_room(self, game_map):
        # go through the tiles in the rectangle and make them passable
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                game_map.tiles[(x,y)].set_attributes(floor=True)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def ranpos(self, game_map, floor = True):
        """
        Returns a random position within the room.
        If floor is True a floor position will be returned, otherwise a wall position will be returned.
        If floor is None any position will be returned.
        """
        if floor:
            positions = [pos for pos in self.pos_list if game_map.is_floor(*pos)]
            if positions:
                pos = choice(positions)
            else:
                return False
        elif not floor:
            positions = [pos for pos in self.pos_list if game_map.is_wall(*pos)]
            if positions:
                pos = choice(positions)
            else:
                return False
        else:
            pos = choice(self.pos_list)
        return pos

    def free_tiles(self, game, allow_exits = True, filter=('walks',)):
        """
        Returns all free (walkable and not occupied by a blocking object) tiles in a room

        :return: list of free coordinates in the room
        :rtype: list of tuples
        """

        game_map = game.map
        exits = self.exits(game_map)
        free_tiles = [pos for pos in self.pos_list if not game_map.is_blocked(*pos, game.blocking_ents, filter=filter) and (allow_exits or pos not in exits)]

        return free_tiles

    @debug_timer
    def exits(self, game_map, max_width = 3, set_attr = True):
        """
        :return: room exits
        :rtype: list of tuples
        """

        # TODO properly avoid out of index errors
        # TODO Should this turn out to be time intensitive: Run once at rectangle creation, setting exits as attribute (rather than calling exits() whenever needed)
        # Further optimization would be proper list comprehension and using game_map.is_floor/.is_wall methods

        exits = []

        # left side
        x, y = self.x1, self.y1
        for i in range(self.h + 1):
            try:
                if game_map.tiles[(x,y)].walkable:
                    if not game_map.tiles[(x, y+max_width)].walkable and not game_map.tiles[(x,y-max_width)].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                y += 1
            except:
                pass

        # right side
        x, y = self.x2, self.y1+1
        for i in range(self.h + 1):
            try:
                if game_map.tiles[(x,y)].walkable:
                    if not game_map.tiles[(x,y + max_width)].walkable and not game_map.tiles[(x,y - max_width)].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                y += 1
            except:
                pass

        # top
        x, y = self.x1, self.y2
        for i in range(self.w + 1):
            try:
                if game_map.tiles[(x,y)].walkable:
                    if not game_map.tiles[(x + max_width,y)].walkable and not game_map.tiles[(x - max_width,y)].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                x += 1
            except:
                pass

        # bottom
        x, y = self.x1, self.y1
        for i in range(self.w + 1):
            try:
                if game_map.tiles[(x,y)].walkable:
                    if not game_map.tiles[(x + max_width,y)].walkable and not game_map.tiles[(x - max_width,y)].walkable:
                        #tcod.console_set_char_foreground(game.con, *pos_on_screen(x, y, game.player), colors.green)
                        exits.append((x, y))
                x += 1
            except:
                pass

        # if set_attr:
        #     self.exits = exits
        return exits