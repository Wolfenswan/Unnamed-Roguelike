import logging
from cmath import sqrt
from random import choice

from gameobjects.util_functions import blocking_entity_at_pos
from map.map_algo import Tunneling, DrunkWalk
from map.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms = []
        self.tiles = self.initialize_tiles()

    @property
    def floor_tiles(self):
        return [tile for tile in self.tiles.values() if tile.walkable]

    @property
    def wall_tiles(self):
        return [tile for tile in self.tiles.values() if tile.blocked]

    def initialize_tiles(self):
        tiles_dict = {}
        positions = [[y for y in range(self.height)] for x in range(self.width)]
        for x, y_list in enumerate(positions):
            for y in y_list:
                tiles_dict.setdefault((x, y), Tile(True, x, y))
        return tiles_dict

    def make_map(self, game, room_min_size, room_max_size, map_width, map_height):

        max_rooms = int((map_width / room_min_size) + (map_height / room_min_size))
        # TODO placeholder for later implementation
        # algo = choice([Tunneling, DrunkWalk])
        # algo.make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)
        DrunkWalk().make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)
        #Tunneling().make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)

        blocked_rooms = [r for r in self.rooms if len(r.exits(self)) == 0]
        if len(blocked_rooms) > 0:
            logging.debug(f'Blocked room fail safe activated for {len(blocked_rooms)} rooms: {blocked_rooms}')
            Tunneling.create_tunnels(self, room_list = blocked_rooms, randomize=True) # safety measure

    def is_floor(self, x, y):
        """
        Returns True if position is a floor.

        :param x: x-coord
        :type x: int
        :param y: y-coord
        :type y: int
        :return: floor?
        :rtype: bool
        """
        if self.tiles[(x, y)].walkable:
            return True

        return False

    def is_wall(self, x, y):
        """
        Returns True if position is a wall.

        :param x: x-coord
        :type x: int
        :param y: y-coord
        :type y: int
        :return: wall?
        :rtype: bool
        """
        if self.tiles[(x,y)].blocked:
            return True

        return False

    def is_blocked(self, x, y, blocking_ents, filter = ('walks',)):
        """
        Returns True if position is either a wall or occupied by a blocking object.
        Filter corresponds to values in the Entity blocks attribute (dictionary)

        :return: blocked?
        :rtype: bool
        """
        if self.is_wall(x, y):
            return True

        for value in filter:
            if any(ent.pos == (x, y) and ent.blocks.get(value, False) for ent in blocking_ents):
                return True

        return False

    def empty_tiles_near_ent(self, ent, game):
        """ returns list of nearby empty (= walkable and not occupied by blocking object) coordinates """
        near_empty_tiles = []
        # TODO list comprehension candidate
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not (dx, dy == 0, 0):
                    to_x, to_y = ent.x + dx, ent.y + dy
                    if not game.map.is_blocked(to_x, to_y, game.blocking_ents):
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

