import logging
from cmath import sqrt
from random import choice

from gameobjects.util_functions import get_blocking_entity_at_location
from map.map_algo import Tunneling, DrunkWalk
from map.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms = []
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True, x, y) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, game, room_min_size, room_max_size, map_width, map_height):

        max_rooms = int((map_width / room_min_size) + (map_height / room_min_size))
        # TODO placeholder for later implementation
        # algo = choice([Tunneling, DrunkWalk])
        # algo.make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)
        DrunkWalk().make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)

        blocked_rooms = [r for r in self.rooms if len(r.exits(self)) == 0]
        if len(blocked_rooms) > 0:
            logging.debug(f'Blocked room fail safe activated for {len(blocked_rooms)} rooms: {blocked_rooms}')
            Tunneling.create_tunnels(self, blocked_only=True, randomize=False) # safety measure

    def is_wall(self, x, y):
        """
        Returns True if position is a wall.

        :param x: x-coord
        :type x: int
        :param y: y-coord
        :type y: int
        :return: wall
        :rtype: bool
        """
        if self.tiles[x][y].blocked:
            return True

        return False

    def is_blocked(self, x, y, game):
        """
        Returns True if position is either a wall or occupied by a blocking object.

        :param x: x-coord
        :type x: int
        :param y: y-coord
        :type y: int
        :param game: game-object
        :type game: game-object
        :return: blocked
        :rtype: bool
        """
        if self.is_wall(x, y):
            return True

        print(x, y, game.entities)
        if get_blocking_entity_at_location(game.entities, x, y) > 0:
            return True

        return False

    def empty_tiles_near_ent(self, ent, game):
        """ returns list of nearby empty (= walkable and not occupied by blocking object) coordinates """
        near_empty_tiles = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                to_x, to_y = ent.x + dx, ent.y + dy
                cond1 = not self.tiles[to_x][to_y].blocked
                cond2 = not any([obj.x, obj.y] == [to_x, to_y] and obj.blocks for obj in game.entities)
                if cond1 and cond2:
                    near_empty_tiles.append((to_x, to_y))

        return near_empty_tiles

    @staticmethod
    def distance_between_pos(x1, y1, x2, y2):
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return round(distance.real)

    def free_line_between_pos(self, x1, y1, x2, y2, game):
        dist = self.distance_between_pos(x1, y1, x2, y2)
        for s in range(dist):
            x = round(x1 + s/dist * (x2-x1))
            y = round(x1 + s/dist * (x2-x1))
            if self.is_blocked(x, y, game):
                return False
        return True

