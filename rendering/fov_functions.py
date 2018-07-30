import random

import tcod
import config_files.cfg as cfg


def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for x in range(game_map.width):
        for y in range(game_map.height):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                       not game_map.tiles[x][y].blocked)

    return fov_map


def recompute_fov(fov_map, x, y):

    algorithm = cfg.FOV_ALGO
    light_walls = cfg.FOV_LIGHT_WALLS
    radius = cfg.FOV_RADIUS

    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)


def pos_is_visible(fov_map, x, y):
    return tcod.map_is_in_fov(fov_map, x, y)


def darken_color_by_fov_distance(ent, color, x, y, randomness = 0):
    """
    Darkens the given color by distance between given entity and x,y coordinates

    :param ent: The entity from which to measure
    :type ent: object
    :param color: The original color value
    :type color: tuple
    :param x: x-coordinate on the dungeon grid
    :type x: int
    :param y: y-coordinate on the dungeon grid
    :type y: int
    :return: darkened color
    :rtype: tuple
    """

    color_coefficient = 1 - ent.distance_to_pos(x, y)/10 + random.uniform(0, randomness)

    if color_coefficient > 1:
        color_coefficient = 1

    if color_coefficient < 0:
        color_coefficient = 0.1

    new_color = tuple(int(color_coefficient * x) for x in color)
    return new_color