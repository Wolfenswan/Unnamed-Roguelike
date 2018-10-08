from cmath import sqrt


def entities_at_pos(entities, x, y):
    return [ent for ent in entities if ent.pos == (x, y)]


def entity_at_pos(entities, x, y):
    return next((ent for ent in entities if ent.pos == (x, y)), None)


def distance_between_pos(x1, y1, x2, y2):
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return round(distance.real)

# def entity_matrix(game, center):
#     ents = []
#     x,y = center
#     for dir in DIRECTIONS_CIRCLE:
#         dx, dy = dir
#         pos = x+dx, y+dy
#         ents.append(entity_at_pos(game.entities, *pos))
#     return ents