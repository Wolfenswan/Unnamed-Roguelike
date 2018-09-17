from random import randint, choice

import tcod

from config_files import cfg as cfg, colors
from game import GameStates
from rendering.render_windows import render_description_window
from rendering.util_functions import draw_console_borders, pos_on_screen
from rendering.fov_functions import darken_color_by_fov_distance
from rendering.render_panels import render_panels
from rendering.render_order import RenderOrder


def render_all(game, fov_map, debug=False):
    render_map_screen(game, fov_map, debug=debug)
    render_panels(game)

    if game.state == GameStates.CURSOR_ACTIVE:
        render_description_window(game)  # Description window is drawn under the cursor if active

    tcod.console_flush()

    clear_all(game.con, game.entities)


def render_map_screen(game, fov_map, debug=False):
    con = game.map_panel
    entities = game.entities

    # Render game map #
    tcod.console_clear(con)
    render_map_centered_on_player(game, con, fov_map, debug=debug)

    # Draw all entities #
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(game, con, entity, fov_map, debug=debug)

    if game.state == GameStates.CURSOR_ACTIVE:
        draw_entity(game, con, game.cursor, fov_map, debug=debug)

    draw_console_borders(con ,color=colors.white)
    tcod.console_blit(con, 0, 0, cfg.MAP_SCREEN_WIDTH, cfg.MAP_SCREEN_HEIGHT, 0, 0, 0)


def render_map_centered_on_player(game, con, fov_map, debug=False):

    game_map = game.map
    player = game.player
    px, py = player.x, player.y

    # get the ranges for all possible map coordinates, using the player's coordinates as center
    render_range_x = list(range(px - cfg.MAP_SCREEN_WIDTH // 2, px + cfg.MAP_SCREEN_WIDTH // 2))
    render_range_y = list(range(py - cfg.MAP_SCREEN_HEIGHT // 2, py + cfg.MAP_SCREEN_HEIGHT // 2))

    for screen_y in range(cfg.MAP_SCREEN_HEIGHT):
       for screen_x in range(cfg.MAP_SCREEN_WIDTH):
            tile_x = render_range_x[screen_x]
            tile_y = render_range_y[screen_y]

            if tile_x in range(game_map.width) and tile_y in range(game_map.height):
                draw_tile(game, con, fov_map, tile_x, tile_y, screen_x, screen_y, debug=debug)


def draw_tile(game, con, fov_map, tile_x, tile_y, screen_x, screen_y, debug=False):
    tile = game.map.tiles[(tile_x, tile_y)]
    visible = tcod.map_is_in_fov(fov_map, tile_x, tile_y) or debug

    wall = tile.block_sight and not tile.walkable

    if visible:
        char = chr(178) if wall else '.'

        fg_color = darken_color_by_fov_distance(game.player, colors.light_fov, tile_x, tile_y, randomness=0)
        if tile.gibbed:
            fg_color =  darken_color_by_fov_distance(game.player, colors.corpse, tile_x, tile_y, randomness = 0)
        if debug:
            fg_color = colors.light_fov

        #tcod.console_put_char(con, screen_x, screen_y, char, tcod.BKGND_NONE)
        tcod.console_put_char_ex(con, screen_x, screen_y, char, fg_color, colors.black)
        tile.explored = 50

    elif tile.explored > 0:
        tile.explored -= randint(0, 1)
        if game.state == GameStates.PLAYER_RESTING:
            if wall:
                tcod.console_put_char_ex(con, screen_x, screen_y, chr(178), colors.dark_wall_fg, colors.dark_ground)
            else:
                tcod.console_put_char_ex(con, screen_x, screen_y, '.', colors.dark_ground_fg, colors.dark_ground)


def draw_entity(game, con, entity, fov_map, debug=False):
    if entity.render_order == RenderOrder.ALWAYS or tcod.map_is_in_fov(fov_map, *entity.pos) or debug:
        x, y = pos_on_screen(*entity.pos, game.player)

        tcod.console_put_char(con, x, y, entity.char)
        # print(entity.char, entity.blocks)
        # Set the entity colors #
        color = entity.color
        if entity is not game.cursor:
            color = darken_color_by_fov_distance(game.player, entity.color, entity.x, entity.y)

        if debug:
            color = entity.color

        tcod.console_set_char_foreground(con, x, y, color)
        if entity.color_bg is not None:
            tcod.console_set_char_background(con, x, y, entity.color_bg)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)