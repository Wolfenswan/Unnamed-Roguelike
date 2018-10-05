# class Cave:
#     def __init__(self, x, y, w, h):
#         self.x1 = x
#         self.y1 = y
#         self.x2 = x + w
#         self.y2 = y + h
#         self.w = w
#         self.h = h
#
#     def create_room(self, game_map):
#         # go through the tiles in the rectangle and make them passable
#         for x in range(self.x1 + 1, self.x2):
#             for y in range(self.y1 + 1, self.y2):
#                 game_map.tiles[(x,y)].blocked = False
#                 game_map.tiles[(x,y)].block_sight = False
#                 game_map.tiles[(x,y)].walkable = True