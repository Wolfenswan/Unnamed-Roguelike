import logging
from random import choice, randint

from dataclasses import dataclass

from config_files import colors
from gameobjects.block_level import BlockLevel
from map.directions_util import DIRECTIONS_CIRCLE
from map.algorithms import Tunneling, DrunkWalk
from map.rooms import Rect
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

    def create_map(self, room_min_size, room_max_size):

        map_width, map_height = self.width, self.height
        max_rooms = int((map_width / room_min_size) + (map_height / room_min_size))
        self.create_rooms(max_rooms, room_min_size, room_max_size, map_width, map_height, fuzzy=10)
        Tunneling.create_tunnels(self, randomize=True, drunk_chance=50)

        # Fill the rest of the map with a pathfinding algorithm
        # algo = choice([Tunneling, DrunkWalk])
        # algo.make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)
        #DrunkWalk().make_map(self, map_width, map_height)
        #Tunneling().make_map(self)

        blocked_rooms = [r for r in self.rooms if len(r.exits(self)) == 0]
        if len(blocked_rooms) > 0:
            logging.warning(f'Blocked room fail safe activated for {len(blocked_rooms)} rooms: {blocked_rooms}')
            Tunneling.create_tunnels(self, room_list = blocked_rooms, randomize=True)

        for i in range(randint(6,15)):
            color = choice([colors.clay, colors.granite])
            self.color_random_area(color)

    def create_rooms(self, max_rooms, room_min_size, room_max_size, map_width, map_height, fuzzy=-1):
        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in self.rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                new_room.create(self, fuzzy=fuzzy)
                # finally, append the new room to the list
                self.rooms.append(new_room)

    def color_random_area(self, color):
        """ Simple function to colorize an area of the map to emulate Biomes """
        rand_x, rand_y = randint(2, self.width - 2), randint(2, self.height - 2)
        tile = self.tiles[rand_x, rand_y]
        tiles = [tile] + tile.surrounding_tiles(dist = randint(4,10))
        for i, t in enumerate(tiles):
            chance = (100 - t.distance_to_tile(tiles[0])*8) + randint(0,20)
            if (chance) >= randint(0, 100):
                t.fg_color = color
                # for t_2 in tile.surrounding_tiles():
                #     if randint(0, 100) <= 75:
                #         t_2.fg_color = color

    def gib_area(self, x, y, dist, color, chunks=False):
        self.tiles[(x, y)].gib(color=color)
        for i in range(1, dist):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            self.tiles[(c_x, c_y)].gib(color=color)
            if not self.tiles[(c_x, c_y)].blocked and randint(0, 100) > 85 and chunks:
                self.tiles[(c_x, c_y)].gib('~', color)

    def is_floor(self, x, y):
        return self.tiles[(x, y)].walkable

    def is_wall(self, x, y):
        tile = self.tiles.get((x,y), None)
        if tile is None:
            return True
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

    def all_free_pos_near_ent_in_dist(self, ent, game, dist=1, block_level = (BlockLevel.WALK,)):
        """ returns list of free (by default: only walkable) coordinates in given distance"""
        near_empty_tiles = []
        for steps in range(dist):
            for dir in DIRECTIONS_CIRCLE:
                to_x, to_y = ent.x + dir[0] + steps, ent.y + dir[1] + steps
                if not self.is_blocked(to_x, to_y, game.walk_blocking_ents, filter=block_level):
                    near_empty_tiles.append((to_x, to_y))
        return near_empty_tiles

    def all_free_pos_near_ent(self, ent, game, block_level = (BlockLevel.WALK,)):
        """ returns list of nearby free (by default: only walkable) coordinates """
        tiles = self.all_free_pos_near_ent_in_dist(ent, game, dist=1, block_level=block_level)
        return tiles

    def random_free_pos_near_ent(self, ent, game, block_level = (BlockLevel.WALK,)):
        tiles = self.all_free_pos_near_ent(ent, game, block_level = block_level)
        if len(tiles) > 0:
            return choice(tiles)
        else:
            return False

