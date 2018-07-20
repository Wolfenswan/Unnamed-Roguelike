""" commonly used functions """
from random import choice, randint

import tcod as libtcod
from builtins import getattr

from rendering.render_order import RenderOrder

# Constants and global variables
from common import global_vars as gv, config

def tile_blocked_by(x, y):
    """ if given tile is occupied by a blocking object the object is returned, otherwise returns None """

    # first collect all blocking objects
    blocking_objects = [obj for obj in gv.game_objects if obj.blocks and (obj.x, obj.y) == (x, y)]
    # if there is any, return the blocking object
    if len(blocking_objects):
        return blocking_objects[0]
    else:
        return None

def same_pos(obj1, obj2):
    if obj1.pos() == obj2.pos():
        return True
    else:
        return False

def get_path_to(start, end, max_dist=25):
    """
        returns a tcod.Path object if a path between start and end has been found.
        start and end are tuples of (x,y)
        max_size defines the maximum length of the path
    """

    sx, sy = start
    ex, ey = end

    # Create a FOV map that has the dimensions of the map
    fov = libtcod.map_new(config.MAP_SCREEN_WIDTH, config.MAP_SCREEN_HEIGHT)

    # Scan the current map each turn and set all the walls as unwalkable
    for y1 in range(config.MAP_SCREEN_HEIGHT):
        for x1 in range(config.MAP_SCREEN_WIDTH):
            libtcod.map_set_properties(fov, x1, y1, gv.game_map.transparent[x1][y1], gv.game_map.walkable[x1][y1])

    # Scan all the objects to see if there are objects that must be navigated around
    # Check also that the object isn't self or the target (so that the start and the end points are free)
    # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
    for obj in gv.game_objects:
        if obj.blocks and (obj.x, obj.y) != (ex, ey):
            # Set the tile as a wall so it must be navigated around
            libtcod.map_set_properties(fov, obj.x, obj.y, True, False)

    # Allocate a A* path
    # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
    my_path = libtcod.path_new_using_map(fov, 2)

    # Compute the path between self's coordinates and the target's coordinates
    libtcod.path_compute(my_path, sx, sy, ex, ey)

    if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < max_dist:
        return my_path
    else:
        return None

def get_items():
    """ returns an array of all items present in the game """
    # TODO: This solution is hacky and will probably break at one point. That's why this TODO is here.
    items = [obj for obj in gv.game_objects if getattr(obj,'render_order') in [RenderOrder.ITEM,RenderOrder.CORPSE]]
    return items

def get_actors():
    """ returns an array of all actors present in the game """
    actors = [ent for ent in gv.game_objects if ent is gv.player or getattr(ent, 'ai', None)]
    return actors

def get_monsters():
    """ returns an array of all monsters present in the game """
    monsters = [ent for ent in gv.game_objects if ent is not gv.player and getattr(ent, 'ai', None)]
    return monsters

def pick_from_dict_by_chance(dict):
    """ picks a random item from the given dictionary, using the items 'chance' value """
    keys = list(dict.keys())
    candidate = choice(keys)

    # keep picking items at random until the rarity chance passes
    while randint(0, 100) > dict[candidate].get('chance'):
        candidate = choice(keys)

    return candidate

def get_octants(x, y):
    """
    Returns the octants of the given position

    :return: List of positions: (NW, W, SW, N, S, NE, E, SE)
    :rtype: List of Tuples
    """

    octants = []
    for dx in range(-1, 2):
        for dy in range (-1,2):
            octants.append((x+dx,y+dy))

    octants.pop(4) # Remove the center position (where dx, dy = 0, 0)
    octants.sort()
    return octants