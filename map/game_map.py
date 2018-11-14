import logging
from cmath import sqrt
from random import choice, randint

from dataclasses import dataclass

from config_files import colors
from gameobjects.block_level import BlockLevel
from gameobjects.util_functions import distance_between_pos
from map.directions_util import DIRECTIONS_CIRCLE
from map.map_algo import Tunneling, DrunkWalk
from map.tile import Tile

@dataclass
class GameMap:
    width : int
    height : int

    def __post_init__(self):
        self.rooms = []
        self.tiles = {}

        positions = [[y for y in range(self.height)] for x in range(self.width)]
        for x, y_list in enumerate(positions):
            for y in y_list:
                self.tiles.setdefault((x, y), Tile(True, x, y))
                self.tiles[x, y].owner = self

    @property
    def floor_tiles(self):
        return [tile for tile in self.tiles.values() if tile.walkable]

    @property
    def wall_tiles(self):
        return [tile for tile in self.tiles.values() if tile.blocked]

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

        for i in range(randint(5,10)):
            color = choice([colors.clay, colors.granite])
            self.color_area(color)


    def color_area(self, color):
        """ Simple function to colorize an area of the map """
        rand_x = randint(2, self.width - 2)
        rand_y = randint(2, self.height - 2)
        tile = self.tiles[rand_x, rand_y]
        tiles = [tile] + tile.surrounding_tiles(dist = randint(3,15))
        for i, t in enumerate(tiles):
            chance = 100*i/len(tiles)
            if (150-chance) >= randint(0, 100):
                t.fg_color = color
                for t_2 in tile.surrounding_tiles():
                    if randint(0, 1):
                        t_2.fg_color = color

    def is_floor(self, x, y):
        return self.tiles[(x, y)].walkable

    def is_wall(self, x, y):
        tile = self.tiles.get((x,y))
        if tile is None:
            print(f'Checking {(x,y)} is None')
        return tile.blocked

    def is_blocked(self, x, y, entities_to_consider, filter = (BlockLevel.WALK,)):
        """
        Returns True if position is either a wall or occupied by a blocking object.
        Filter corresponds to values in the Entity.blocks attribute (dictionary).
        By default only walk-blocking entities are filtered.

        :return: blocked?
        :rtype: bool
        """
        if self.is_wall(x, y):
            return True

        for value in filter:
            if any((ent.pos == (x, y) and ent.blocks.get(value, False)) for ent in entities_to_consider):
                return True

        return False

    def surrounding_pos(self, x, y, dist = 1):
        pos_list = [] # TODO refactor using direction_utils
        for dx in range(-dist, dist + 1):
            for dy in range(-dist, dist + 1):
                if not (dx == 0 and dy == 0) and self.tiles.get((x + dx, y + dy)) is not None:
                    pos_list.append((x + dx, y + dy))
        return pos_list

    def empty_pos_near_ent(self, ent, game):
        """ returns list of nearby empty (= walkable and not occupied by blocking object) coordinates """
        near_empty_tiles = []
        # TODO list comprehension candidate
        # for dx in [-1, 0, 1]:
        #     for dy in [-1, 0, 1]:
        #         if not (dx == 0 and dy == 0):
        for dir in DIRECTIONS_CIRCLE:
            dx, dy = dir
            to_x, to_y = ent.x + dx, ent.y + dy
            if not self.is_blocked(to_x, to_y, game.blocking_ents):
                near_empty_tiles.append((to_x, to_y))

        return near_empty_tiles

