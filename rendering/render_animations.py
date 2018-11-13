import time

import tcod

from config_files import colors
from game import Game
from gameobjects.entity import Entity
from gameobjects.util_functions import distance_between_pos, entity_at_pos
from map.directions_util import DIRECTIONS_CIRCLE
from rendering.render_main import render_map_screen
from rendering.render_order import RenderOrder


def render_animation(game:Game, anim_delay:float):
    render_map_screen(game, game.fov_map, debug=game.debug['map'])
    time.sleep(anim_delay)
    tcod.console_flush()


def animate_move_line(ent, dx:int, dy:int, steps:int, game:Game, ignore_entities=False, anim_delay = 0.05):
    """
    The entity will attempt to move the number of steps into the give direction.
    """
    for i in range(steps):
        move_attempt = ent.try_move(dx, dy, game, ignore_entities=ignore_entities)
        if move_attempt is True:
            render_animation(game, anim_delay)
        else:
            return move_attempt


def animate_move_to(ent, tx:int, ty:int, game:Game, ignore_entities=False, anim_delay = 0.05):
    """
    The entity will attempt to move to the given target position.

    :returns: True if animation was successful. False if animation was blocked by a wall. Entity if animation was blocked by an entity.
    """
    while ((ent.x, ent.y) != (tx, ty)):
        dx, dy = ent.direction_to_pos(tx, ty)
        move_attempt = ent.try_move(dx, dy, game, ignore_entities=ignore_entities)
        if move_attempt is True:
            render_animation(game, anim_delay)
        else:
            return move_attempt
    return True


def animate_projectile(start_x:int, start_y:int, target_x:int, target_y:int, game:Game, forced_distance:int=0, homing=True, ignore_entities=True, anim_delay = 0.05, color=colors.flame):
    """
    Creates a temporary projectile and animates its movement from start position to target position.

    TODO additonal switches: character
    TODO doesn't return anything atm. Add return as needed
    """

    distance = forced_distance if forced_distance > 0 else distance_between_pos(start_x, start_y, target_x, target_y)

    projectile = Entity(start_x, start_y, '*', color, 'Projectile', render_order=RenderOrder.ALWAYS)
    game.entities.append(projectile)
    if homing:
        animate_move_to(projectile, target_x, target_y, game, anim_delay = anim_delay, ignore_entities=ignore_entities)
    else:
        dx, dy = projectile.direction_to_pos(target_x, target_y)
        animate_move_line(projectile, dx, dy, distance, game, anim_delay = anim_delay, ignore_entities=True)
    game.entities.remove(projectile)


def animate_explosion(center_x:int, center_y:int, spread:int, game:Game, ignore_walls=False, anim_delay = 0.05, color=colors.flame):
    """
    Creates a projectiles moving outward from the center position.

    TODO additonal switches: character to use for projectile
    TODO doesn't return anything atm. Add return as needed
    """
    projectiles = []
    directions = DIRECTIONS_CIRCLE
    for _x in directions:
        projectile = Entity(center_x, center_y, '*', color, 'Projectile', render_order=RenderOrder.ALWAYS)
        projectiles.append(projectile)
        game.entities.append(projectile)

    for s in range(spread):
        for i, dir in enumerate(directions):
            projectile = projectiles[i]
            projectile.try_move(*dir, game, ignore_entities=True, ignore_walls=ignore_walls)
        render_animation(game, anim_delay)

    for p in projectiles:
        if p in game.entities:
            game.entities.remove(p)


def animate_sparkle(center_x:int, center_y:int, game:Game, tickss:int=3, radius:int=1, anim_delay:float=0.05, color=colors.flame):
    """
    Creates a 'sparkling' effect  around the center, by rendering several randomly created projectiles at the same time.
    """
    
    projectiles = []
    directions = DIRECTIONS_CIRCLE
    for _tick in ticks:
        for _dir in directions:
            for _dist in radius:
                if randint(0,1):
                    projectile = Entity(center_x, center_y, '*', color, 'Projectile', render_order=RenderOrder.ALWAYS)
                    projectiles.append(projectile)
        render_animation(game, anim_delay)

    for p in projectiles:
        game.entities.remove(p)




def animate_cone():
    pass


def animate_ray():
    pass