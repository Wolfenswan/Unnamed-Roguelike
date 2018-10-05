from random import choice

# Todo @dataclass
class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h
        self.center = int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)
        self.pos_list = []
        for y in range(self.y1, self.y2):
            for x in range(self.x1, self.x2):
                self.pos_list.append((x, y))

    # @property
    # def center(self):
    #     center_x = int((self.x1 + self.x2) / 2)
    #     center_y = int((self.y1 + self.y2) / 2)
    #     return center_x, center_y

    # @property
    # def pos_list(self):
    #     pos_list = []
    #     for y in range(self.y1, self.y2):
    #         for x in range(self.x1, self.x2):
    #             pos_list.append((x, y))
    #     return pos_list

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
        #free_tiles = []
        # for x in range(self.x1, self.x2):
        #     for y in range(self.y1, self.y2):
        #         if not game_map.is_blocked(x, y, game):
        #             if allow_exits or ((x, y) not in exits):
        #                 free_tiles.append((x, y))
                # except:
                #     logging.error(f'Position {x}/{y} in room {self} of size {self.w}/{self.h} at x{self.x1}/y{self.y1}-x{self.x2}/y{self.y2} is out of bounds')

        return free_tiles

    def exits(self, game_map, max_width = 3):
        """
        :return: room exists
        :rtype: list of tuples
        """

        # TODO properly avoid out of index errors
        # TODO Candidate for list comprehension and using game_map.is_floor/.is_wall methods

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

        return exits