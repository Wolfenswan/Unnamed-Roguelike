from random import choice

from map.map_algo import Tunneling, DrunkWalk
from map.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rooms = []
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True, x, y, self) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, game, room_min_size, room_max_size, map_width, map_height):

        max_rooms = int((map_width / room_min_size) + (map_height / room_min_size))
        algo = choice([Tunneling, DrunkWalk])
        DrunkWalk().make_map(game, max_rooms, room_min_size, room_max_size, map_width, map_height)


    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

