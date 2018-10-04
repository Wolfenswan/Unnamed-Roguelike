import time

import tcod

from config_files import colors
from gameobjects.entity import Entity
from rendering.render_main import render_map_screen
from rendering.render_order import RenderOrder

def render_animation(game, anim_delay):
    render_map_screen(game, game.fov_map, debug=game.debug['map'])
    time.sleep(anim_delay)
    tcod.console_flush()


def animate_move_line(ent, dx, dy, steps, game, ignore_entities=False, anim_delay = 0.05):
    """
    The entity will attempt to move the number of steps into the give direction.
    """
    for i in range(steps):
        blocked = ent.try_move(dx, dy, game, ignore_entities=ignore_entities)
        if blocked is None:
            render_animation(game, anim_delay)
        elif blocked is False:
            return False
        else:
            return blocked


def animate_move_to(ent, tx, ty, game, ignore_entities=False, anim_delay = 0.05):
    """
    The entity will attempt to move to the given target position.
    """
    while ((ent.x, ent.y) != (tx, ty)):
        dx, dy = ent.direction_to_pos(tx, ty)
        blocked = ent.try_move(dx, dy, game, ignore_entities=ignore_entities)
        if blocked is None:
            render_animation(game, anim_delay)
        elif blocked is False:
            return False
        else:
            return blocked


def animate_projectile(start_x, start_y, target_x, target_y, distance, game, homing=True, ignore_entities=True, anim_delay = 0.05):
    """
    Creates a temporary projectile and animates its movement from start position to target position.

    TODO additonal switches: color, character
    TODO doesn't return anything atm. Add return as needed
    """
    projectile = Entity(start_x, start_y, '*', colors.flame, 'Projectile', render_order=RenderOrder.ALWAYS)
    game.entities.append(projectile)
    if homing:
        animate_move_to(projectile, target_x, target_y, game, anim_delay = anim_delay, ignore_entities=ignore_entities)
    else:
        dx, dy = projectile.direction_to_pos(target_x, target_y)
        animate_move_line(projectile, dx, dy, distance, game, anim_delay = anim_delay, ignore_entities=True)
    game.entities.remove(projectile)


def animate_explosion(center_x, center_y, spread, game, ignore_walls=False, anim_delay = 0.02):
    """
    Creates a projectiles moving outward from the center position.

    TODO additonal switches: color, character
    TODO doesn't return anything atm. Add return as needed
    """
    projectiles = []
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    for dir in directions:
        projectile = Entity(center_x, center_y, '*', colors.flame, 'Projectile', render_order=RenderOrder.ALWAYS)
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


def animate_cone():
    pass