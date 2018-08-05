import time

from gameobjects.util_functions import get_blocking_entity_at_location
from rendering.render_main import render_all


def animate_move(ent, game, dx, dy, steps):
    for i in range(steps):
        dest_x, dest_y = ent.x + dx, ent.y + dy
        if not game.map.is_blocked(dest_x, dest_y):
            blocked = get_blocking_entity_at_location(game.entities, dest_x, dest_y)
            if blocked:
                return blocked
            else:
                ent.move(dx, dy)
                render_all(game, game.fov_map) # TODO Placeholder until a seperate render_map function exists (requries a dedicated map console)
                time.sleep(0.1)