from random import randint, random, choice

class Tunneling:
    # def make_map(self, game_map):
    #     self.create_tunnels(game_map, randomize=True, drunk_chance=50)

    @staticmethod
    def create_tunnels(game_map, room_list = None, randomize=False, drunk_chance=0):
        all_rooms = game_map.rooms
        rooms = all_rooms if room_list is None else room_list
        for i, r in enumerate(rooms):
                x, y = r.center
                if not randomize:
                    idx = i - 1 if i - 1 >= 0 else i + 1
                    dest_r = rooms[idx]
                else:
                    dest_r = choice(all_rooms)
                    while r == dest_r:
                        dest_r = choice(all_rooms)

                dest_x, dest_y = dest_r.center

                if randint(0,100) > drunk_chance:
                    if randint(0, 1):
                        Tunneling.h_tunnel(game_map, x, dest_x, y)
                        Tunneling.v_tunnel(game_map, y, dest_y, dest_x)
                    else:
                        Tunneling.v_tunnel(game_map, y, dest_y, x)
                        Tunneling.h_tunnel(game_map, x, dest_x, dest_y)
                else:
                    Tunneling.drunk_tunnel(game_map, r, dest_r)

    @staticmethod
    def h_tunnel(game_map, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map.tiles[(x,y)].set_attributes(floor = True)

    @staticmethod
    def v_tunnel(game_map, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map.tiles[(x,y)].set_attributes(floor = True)

    @staticmethod
    def drunk_tunnel(game_map, room1, room2):
        """
        Run a heavily weighted random Walk from point2 to point1
        Based on /u/at_the_matinee's examples:
        https://github.com/AtTheMatinee/dungeon-generation
        """
        drunkardX, drunkardY = room2.center
        goalX, goalY = room1.center
        while not (room1.x1 <= drunkardX <= room1.x2) or not (room1.y1 < drunkardY < room1.y2):  #
            # ==== Choose Direction ====
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1.5

            # weight the random walk against edges
            if drunkardX < goalX:  # drunkard is left of point1
                east += weight
            elif drunkardX > goalX:  # drunkard is right of point1
                west += weight
            if drunkardY < goalY:  # drunkard is above point1
                south += weight
            elif drunkardY > goalY:  # drunkard is below point1
                north += weight

            # normalize probabilities so they form a range from 0 to 1
            total = north + south + east + west
            north /= total
            south /= total
            east /= total
            west /= total

            # choose the direction
            choice = random()
            if 0 <= choice < north:
                dx, dy = 0, -1
            elif north <= choice < (north + south):
                dx, dy = 0, 1
            elif (north + south) <= choice < (north + south + east):
                dx, dy = 1, 0
            else:
                dx, dy = -1, 0

            # ==== Walk ====
            # check colision at edges
            if (0 < drunkardX + dx < game_map.width - 1) and (0 < drunkardY + dy < game_map.height - 1):
                drunkardX += dx
                drunkardY += dy
                if not game_map.tiles[(drunkardX,drunkardY)].floor:
                    game_map.tiles[(drunkardX,drunkardY)].set_attributes(floor = True)


class DrunkWalk:
    """
    Based on /u/at_the_matinee's examples:
    https://github.com/AtTheMatinee/dungeon-generation
    """
    def __init__(self):
        self._percentGoal = .15
        self.walkIterations = 25000  # cut off in case _percentGoal in never reached
        self.weightedTowardCenter = 0.1
        self.weightedTowardPreviousDirection = 0.4

    def make_map(self, game_map, map_width, map_height):
        self.walk_iterations = max(self.walkIterations, (map_width * map_height * 10))

        self._filled = 0
        self._previousDirection = None
        self.drunkardX = randint(round(map_width/4), round(map_width/4*3))
        self.drunkardY = randint(round(map_height/4), round(map_height/4*3))
        self.filledGoal = map_width * map_height * self._percentGoal

        for i in range(self.walkIterations):
            self.walk(game_map, map_width, map_height)
            if (self._filled >= self.filledGoal):
                break

    def walk(self, game_map, map_width, map_height):
        # ==== Choose Direction ====
        north = 1.0
        south = 1.0
        east = 1.0
        west = 1.0

        # weight the random walk against edges
        if self.drunkardX < map_width * 0.1:  # drunkard is at far left side of map
            east += self.weightedTowardCenter
        elif self.drunkardX > map_width * 0.9:  # drunkard is at far right side of map
            west += self.weightedTowardCenter
        if self.drunkardY < map_height * 0.1:  # drunkard is at the top of the map
            south += self.weightedTowardCenter
        elif self.drunkardY > map_height * 0.9:  # drunkard is at the bottom of the map
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
        # check collision at edges
        if (0 < self.drunkardX + dx < map_width - 1) and (0 < self.drunkardY + dy < map_height - 1):
            self.drunkardX += dx
            self.drunkardY += dy
            if game_map.tiles[(self.drunkardX, self.drunkardY)].blocked:
                game_map.tiles[(self.drunkardX, self.drunkardY)].toggle_attributes()
                self._filled += 1
            self._previousDirection = direction


# class MessyBSPTree:
#     '''
#     A Binary Space Partition connected by a severely weighted
#     drunkards walk algorithm.
#     Requires Leaf and Rect classes.
#     '''
#
#     def __init__(self):
#             self.level = []
#             self.room = None
#             self.MAX_LEAF_SIZE = 24
#             self.ROOM_MAX_SIZE = 15
#             self.ROOM_MIN_SIZE = 6
#             self.smoothEdges = True
#             self.smoothing = 1
#             self.filling = 3
#
#     def make_map(self, map_width, map_height):
#         self.map_width = map_width
#         self.map_height = map_height
#         # Creates an empty 2D array or clears existing array
#         self.level = [[1
#             for y in range(map_height)]
#                 for x in range(map_width)]
#
#         self._leafs = []
#
#         rootLeaf = Leaf(0,0,map_width,map_height)
#         self._leafs.append(rootLeaf)
#
#         splitSuccessfully = True
#         # loop through all leaves until they can no longer split successfully
#         while (splitSuccessfully):
#             splitSuccessfully = False
#             for l in self._leafs:
#                 if (l.child_1 == None) and (l.child_2 == None):
#                     if ((l.width > self.MAX_LEAF_SIZE) or
#                     (l.height > self.MAX_LEAF_SIZE) or
#                     (random.random() > 0.8)):
#                         if (l.splitLeaf()): #try to split the leaf
#                             self._leafs.append(l.child_1)
#                             self._leafs.append(l.child_2)
#                             splitSuccessfully = True
#
#         rootLeaf.createRooms(self)
#         self.cleanUpMap(map_width,map_height)
#
#         return self.level
#
#     def createRoom(self, room):
#         # set all tiles within a rectangle to 0
#         for x in range(room.x1 + 1, room.x2):
#             for y in range(room.y1+1, room.y2):
#                 self.level[x][y] = 0
#
#     def createHall(self, room1, room2):
#         # run a heavily weighted random Walk
#         # from point2 to point1
#         drunkardX, drunkardY = room2.center()
#         goalX,goalY = room1.center()
#         while not (room1.x1 <= drunkardX <= room1.x2) or not (room1.y1 < drunkardY < room1.y2): #
#             # ==== Choose Direction ====
#             north = 1.0
#             south = 1.0
#             east = 1.0
#             west = 1.0
#
#             weight = 1
#
#             # weight the random walk against edges
#             if drunkardX < goalX: # drunkard is left of point1
#                 east += weight
#             elif drunkardX > goalX: # drunkard is right of point1
#                 west += weight
#             if drunkardY < goalY: # drunkard is above point1
#                 south += weight
#             elif drunkardY > goalY: # drunkard is below point1
#                 north += weight
#
#             # normalize probabilities so they form a range from 0 to 1
#             total = north+south+east+west
#             north /= total
#             south /= total
#             east /= total
#             west /= total
#
#             # choose the direction
#             choice = random.random()
#             if 0 <= choice < north:
#                 dx = 0
#                 dy = -1
#             elif north <= choice < (north+south):
#                 dx = 0
#                 dy = 1
#             elif (north+south) <= choice < (north+south+east):
#                 dx = 1
#                 dy = 0
#             else:
#                 dx = -1
#                 dy = 0
#
#             # ==== Walk ====
#             # check colision at edges
#             if (0 < drunkardX+dx < self.map_width-1) and (0 < drunkardY+dy < self.map_height-1):
#                 drunkardX += dx
#                 drunkardY += dy
#                 if self.level[drunkardX][drunkardY] == 1:
#                     self.level[drunkardX][drunkardY] = 0
#
#     def cleanUpMap(self,map_width,map_height):
#         if (self.smoothEdges):
#             for i in range (3):
#                 # Look at each cell individually and check for smoothness
#                 for x in range(1,map_width-1):
#                     for y in range (1,map_height-1):
#                         if (self.level[x][y] == 1) and (self.getAdjacentWallsSimple(x,y) <= self.smoothing):
#                             self.level[x][y] = 0
#
#                         if (self.level[x][y] == 0) and (self.getAdjacentWallsSimple(x,y) >= self.filling):
#                             self.level[x][y] = 1
#
#     def getAdjacentWallsSimple(self, x, y): # finds the walls in four directions
#         wallCounter = 0
#         #print("(",x,",",y,") = ",self.level[x][y])
#         if (self.level[x][y-1] == 1): # Check north
#             wallCounter += 1
#         if (self.level[x][y+1] == 1): # Check south
#             wallCounter += 1
#         if (self.level[x-1][y] == 1): # Check west
#             wallCounter += 1
#         if (self.level[x+1][y] == 1): # Check east
#             wallCounter += 1
#
#         return wallCounter
#
# class Leaf: # used for the BSP tree algorithm
#     def __init__(self, x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.MIN_LEAF_SIZE = 10
#         self.child_1 = None
#         self.child_2 = None
#         self.room = None
#         self.hall = None
#
#     def splitLeaf(self):
#         # begin splitting the leaf into two children
#         if (self.child_1 is not None) or (self.child_2 is not None):
#             return False # This leaf has already been split
#
#         '''
#         ==== Determine the direction of the split ====
#         If the width of the leaf is >25% larger than the height,
#         split the leaf vertically.
#         If the height of the leaf is >25 larger than the width,
#         split the leaf horizontally.
#         Otherwise, choose the direction at random.
#         '''
#         splitHorizontally = random.choice([True, False])
#         if (self.width/self.height >= 1.25):
#             splitHorizontally = False
#         elif (self.height/self.width >= 1.25):
#             splitHorizontally = True
#
#         if (splitHorizontally):
#             max = self.height - self.MIN_LEAF_SIZE
#         else:
#             max = self.width - self.MIN_LEAF_SIZE
#
#         if (max <= self.MIN_LEAF_SIZE):
#             return False # the leaf is too small to split further
#
#         split = random.randint(self.MIN_LEAF_SIZE,max) #determine where to split the leaf
#
#         if (splitHorizontally):
#             self.child_1 = Leaf(self.x, self.y, self.width, split)
#             self.child_2 = Leaf( self.x, self.y+split, self.width, self.height-split)
#         else:
#             self.child_1 = Leaf( self.x, self.y,split, self.height)
#             self.child_2 = Leaf( self.x + split, self.y, self.width-split, self.height)
#
#         return True
#
#     def createRooms(self, bspTree):
#         if (self.child_1) or (self.child_2):
#             # recursively search for children until you hit the end of the branch
#             if (self.child_1):
#                 self.child_1.createRooms(bspTree)
#             if (self.child_2):
#                 self.child_2.createRooms(bspTree)
#
#             if (self.child_1 and self.child_2):
#                 bspTree.createHall(self.child_1.getRoom(),
#                     self.child_2.getRoom())
#
#         else:
#         # Create rooms in the end branches of the bsp tree
#             w = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.width-1))
#             h = random.randint(bspTree.ROOM_MIN_SIZE, min(bspTree.ROOM_MAX_SIZE,self.height-1))
#             x = random.randint(self.x, self.x+(self.width-1)-w)
#             y = random.randint(self.y, self.y+(self.height-1)-h)
#             self.room = Rect(x,y,w,h)
#             bspTree.createRoom(self.room)
#
#     def getRoom(self):
#         if (self.room): return self.room
#
#         else:
#             if (self.child_1):
#                 self.room_1 = self.child_1.getRoom()
#             if (self.child_2):
#                 self.room_2 = self.child_2.getRoom()
#
#             if (not self.child_1 and not self.child_2):
#                 # neither room_1 nor room_2
#                 return None
#
#             elif (not self.room_2):
#                 # room_1 and !room_2
#                 return self.room_1
#
#             elif (not self.room_1):
#                 # room_2 and !room_1
#                 return self.room_2
#
#             # If both room_1 and room_2 exist, pick one
#             elif (random.random() < 0.5):
#                 return self.room_1
#             else:
#                 return self.room_2
#
#