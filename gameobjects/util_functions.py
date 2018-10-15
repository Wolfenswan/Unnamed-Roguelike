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


def line_between_pos(x1:int, y1:int, x2:int, y2:int, inclusive=False):
    """
    Draws a line from the starting position to the end position and returns all positions in between as a list.
    List does not include start/end pos by default.

    :param inclusive: True to include start/end pos
    """
    dist = distance_between_pos(x1, y1, x2, y2)
    x, y = x1, y1
    pos_list = []
    if inclusive:
        pos_list.append((x,y))
    for s in range(dist):
        dir = direction_between_pos(x, y, x2, y2)
        x += dir[0]
        y += dir[1]
        if (x, y) == (x2, y2) and not inclusive:
            break
        pos_list.append((x,y))
    return pos_list


def free_line_between_pos(x1, y1, x2, y2, game:Game, inclusive:bool=False):
    pos_list = line_between_pos(x1, y1, x2, y2, inclusive)
    for pos in pos_list:
        if game.map.is_blocked(*pos, game.blocking_ents):
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