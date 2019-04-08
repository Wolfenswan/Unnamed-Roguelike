import tcod

import config_files.cfg as cfg
from gameobjects.block_level import BlockLevel
from gameobjects.util_functions import entity_at_pos


def initialize_fov(game):
    game_map = game.map
    fov_map = tcod.map.Map(game_map.width, game_map.height)

    for x in range(game_map.width):
        for y in range(game_map.height):
            fov_map.transparent[y,x] = not game_map.tiles[(x,y)].block_sight
            fov_map.walkable[y,x] = not game_map.tiles[(x,y)].blocked

            ent = entity_at_pos(game.sight_blocking_ents, x, y)
            if ent:
                fov_map.transparent[y,x] = not ent.blocks.get(BlockLevel.SIGHT, False)#game_map.tiles[(x, y)].block_sight
                fov_map.walkable[y,x] = not ent.blocks.get(BlockLevel.WALK, False)

    return fov_map


def recompute_fov(game, x, y):

    algorithm = cfg.FOV_ALGO
    light_walls = cfg.FOV_LIGHT_WALLS
    radius = game.player.fighter.vision

    game.fov_map.compute_fov(x, y, radius, light_walls, algorithm)


def darken_color_by_fov_distance(ent, color, x, y, randomness = 0, min=0.1):
    """
    Darkens the given color by distance between given entity and x,y coordinates

    :param randomness:
    :type randomness:
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

    color_coefficient = 1 - ent.distance_to_pos(x, y)/ent.fighter.vision #+ random.uniform(0, randomness)

    if color_coefficient > 1:
        color_coefficient = 1

    if color_coefficient < min:
        color_coefficient = min

    new_color = (int(color_coefficient * x) for x in color)
    return tcod.Color(*new_color)