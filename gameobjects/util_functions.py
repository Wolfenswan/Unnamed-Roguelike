from cmath import sqrt

from game import Game
from map.directions_util import direction_between_pos


def entities_at_pos(entities, x, y):
    return [ent for ent in entities if ent.pos == (x, y)]


def entity_at_pos(entities, x, y):
    return next((ent for ent in entities if ent.pos == (x, y)), None)


def distance_between_pos(x1, y1, x2, y2, rounding=True):
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if rounding:
        distance = round(distance.real)
    return distance


def free_line_between_pos(x1, y1, x2, y2, game:Game):
    dist = distance_between_pos(x1, y1, x2, y2)
    x, y = x1, y1
    for s in range(dist):
        dir = direction_between_pos(x, y, x2, y2)
        x += dir[0]
        y += dir[1]
        if (x, y) == (x2, y2):
            break
        if game.map.is_blocked(x, y, game.blocking_ents):
            return False
    return True

# def entity_matrix(game, center):
#     ents = []
#     x,y = center
#     for dir in DIRECTIONS_CIRCLE:
#         dx, dy = dir
#         pos = x+dx, y+dy
#         ents.append(entity_at_pos(game.entities, *pos))
#     return ents