import logging
from random import randint, random, choice

from cffi.backend_ctypes import xrange

from map.rectangle import Rect


class Tunneling:

    def make_map(self, game, max_rooms, room_min_size, room_max_size, map_width, map_height):
        game_map = game.map

        self.create_rooms(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height)
        self.create_tunnels(game_map, randomize=True)

    @staticmethod
    def create_rooms(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height):
        rooms = game_map.rooms
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
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid
                # "paint" it to the map's tiles
                Tunneling.create_room(game_map, new_room)
                # finally, append the new room to the list
                rooms.append(new_room)

    @staticmethod
    def create_tunnels(game_map, room_list = None, randomize=False):
        all_rooms = game_map.rooms
        rooms = all_rooms if room_list is None else room_list
        for i, r in enumerate(rooms):
                x, y = r.center
                if not randomize:
                    idx = i - 1 if i - 1 >= 0 else i + 1
                    dest_r = rooms[idx]
                else:
                    dest_r = choice(all_rooms)

                dest_x, dest_y = dest_r.center

                if randint(0, 1):
                    Tunneling.create_h_tunnel(game_map, x, dest_x, y)
                    Tunneling.create_v_tunnel(game_map, y, dest_y, dest_x)
                else:
                    Tunneling.create_v_tunnel(game_map, y, dest_y, x)
                    Tunneling.create_h_tunnel(game_map, x, dest_x, dest_y)

    @staticmethod
    def create_room(game_map, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                game_map.tiles[(x,y)].set_attributes(floor=True)

    @staticmethod
    def create_h_tunnel(game_map, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map.tiles[(x,y)].set_attributes(floor = True)

    @staticmethod
    def create_v_tunnel(game_map, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map.tiles[(x,y)].set_attributes(floor = True)

class DrunkWalk:
    """
    Based on /u/at_the_matinee's examples:
    https://github.com/AtTheMatinee/dungeon-generation
    """
    def __init__(self):
        self._percentGoal = .25
        self.walkIterations = 25000  # cut off in case _percentGoal in never reached
        self.weightedTowardCenter = 0.05
        self.weightedTowardPreviousDirection = 0.9

    def make_map(self, game, max_rooms, room_min_size, room_max_size, map_width, map_height):
        game_map = game.map
        self.walk_iterations = max(self.walkIterations, (map_width * map_height * 10))

        self._filled = 0
        self._previousDirection = None
        self.drunkardX = randint(2, map_width - 2)
        self.drunkardY = randint(2, map_height - 2)
        self.filledGoal = map_width * map_height * self._percentGoal

        for i in xrange(self.walkIterations):
            self.walk(game_map, map_width, map_height)
            if (self._filled >= self.filledGoal):
                break

        Tunneling.create_rooms(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height)
        Tunneling.create_tunnels(game_map, randomize=True)

    def walk(self, game_map, mapWidth, mapHeight):
        # ==== Choose Direction ====
        north = 1.0
        south = 1.0
        east = 1.0
        west = 1.0

        # weight the random walk against edges
        if self.drunkardX < mapWidth * 0.1:  # drunkard is at far left side of map
            east += self.weightedTowardCenter
        elif self.drunkardX > mapWidth * 0.9:  # drunkard is at far right side of map
            west += self.weightedTowardCenter
        if self.drunkardY < mapHeight * 0.1:  # drunkard is at the top of the map
            south += self.weightedTowardCenter
        elif self.drunkardY > mapHeight * 0.9:  # drunkard is at the bottom of the map
            north += self.weightedTowardCenter

        # weight the random walk in favor of the previous direction
        if self._previousDirection == "north":
            north += self.weightedTowardPreviousDirection
        if self._previousDirection == "south":
            south += self.weightedTowardPreviousDirection
        if self._previousDirection == "east":
            east += self.weightedTowardPreviousDirection
        if self._previousDirection == "west":
            west += self.weightedTowardPreviousDirection

        # normalize probabilities so they form a range from 0 to 1
        total = north + south + east + west

        north /= total
        south /= total
        east /= total
        west /= total

        # choose the direction
        choice = random()
        if 0 <= choice < north:
            dx = 0
            dy = -1
            direction = "north"
        elif north <= choice < (north + south):
            dx = 0
            dy = 1
            direction = "south"
        elif (north + south) <= choice < (north + south + east):
            dx = 1
            dy = 0
            direction = "east"
        else:
            dx = -1
            dy = 0
            direction = "west"

        # ==== Walk ====
        # check colision at edges
        if (0 < self.drunkardX + dx < mapWidth - 1) and (0 < self.drunkardY + dy < mapHeight - 1):
            self.drunkardX += dx
            self.drunkardY += dy
            if game_map.tiles[(self.drunkardX, self.drunkardY)].blocked:
                game_map.tiles[(self.drunkardX, self.drunkardY)].toggle_attributes()
                self._filled += 1
            self._previousDirection = direction