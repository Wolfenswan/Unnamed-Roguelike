from random import randint

import tcod

from config_files import colors
from debug.timer import debug_timer
from game import GameState
from rendering.fov_functions import darken_color_by_fov_distance
from rendering.render_order import RenderOrder
from rendering.render_panels import render_panels, draw_quickslots, render_status_panel
from rendering.render_windows import render_description_window
from rendering.util_functions import draw_console_borders, pos_on_screen
from rendering import render_constants as r_cons

@debug_timer
def render_all(game, fov_map, debug=False):

    render_map_screen(game, fov_map, debug=debug)
    render_panels(game)

    if game.state == GameState.CURSOR_ACTIVE:
        render_description_window(game)  # Description window is drawn under the cursor if active

    tcod.console_flush()

@debug_timer
def render_map_screen(game, fov_map, debug=False):
    con = game.map_panel
    entities = game.entities

    # Render game map #
    con.clear()
    render_map_centered_on_player(game, con, fov_map, debug=debug)

    # Draw all entities #
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(game, con, entity, fov_map, debug=debug)

    if game.state in [GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]:
        draw_entity(game, con, game.cursor, fov_map, debug=debug)

    draw_console_borders(con, color=colors.white)
    render_status_panel(game, game.status_panel, 0, r_cons.STATUS_BAR_Y, r_cons.STATUS_BAR_WIDTH,
                        r_cons.STATUS_BAR_HEIGHT)

    #game.con.blit(game.map_panel, width=cfg.MAP_SCREEN_WIDTH, height=cfg.MAP_SCREEN_HEIGHT)
    con.blit(game.root, 0, 0, 0, 0, r_cons.MAP_SCREEN_WIDTH, r_cons.MAP_SCREEN_HEIGHT)
    #tcod.console_blit(con, 0, 0, cons.MAP_SCREEN_WIDTH, cons.MAP_SCREEN_HEIGHT, 0, 0, 0)

@debug_timer
def render_map_centered_on_player(game, con, fov_map, debug=False):

    game_map = game.map
    player = game.player
    px, py = player.x, player.y

    # get the ranges for all possible map coordinates, using the player's coordinates as center
    render_range_x = list(range(px - r_cons.MAP_SCREEN_WIDTH // 2, px + r_cons.MAP_SCREEN_WIDTH // 2))
    render_range_y = list(range(py - r_cons.MAP_SCREEN_HEIGHT // 2, py + r_cons.MAP_SCREEN_HEIGHT // 2))

    for screen_y in range(r_cons.MAP_SCREEN_HEIGHT):
       for screen_x in range(r_cons.MAP_SCREEN_WIDTH):
            if screen_x == len(render_range_x) or screen_y == len(render_range_y):
                break
            tile_x = render_range_x[screen_x]
            tile_y = render_range_y[screen_y]

            if tile_x in range(game_map.width) and tile_y in range(game_map.height):
                draw_tile(game, con, fov_map, tile_x, tile_y, screen_x, screen_y, debug=debug)


def draw_tile(game, con, fov_map, tile_x, tile_y, screen_x, screen_y, debug=False):
    tile = game.map.tiles[(tile_x, tile_y)]
    visible = fov_map.fov[tile_y, tile_x] or debug

    if visible:
        if debug or game.state == GameState.SHOW_MAP:
            color = tile.fg_color
        else:
            color = darken_color_by_fov_distance(game.player, tile.fg_color, tile_x, tile_y, min = 0.3)
        tcod.console_put_char_ex(con, screen_x, screen_y, tile.char, color, colors.black)
        tile.explored = 50

    elif tile.explored > 0: #and not game.player.in_combat(game):
        # "forgetting" tiles disabled for now
        # if  game.state == GameState.PLAYERS_TURN:   # Only active player movement lowers tile exploration state
        #     tile.explored -= randint(0, 1)
        #if game.state == GameStates.PLAYER_RESTING: # Automap is only displayed outside of combat when actively pausing #
        color = tile.dark_color if not game.state == GameState.SHOW_MAP else tile.fg_color
        tcod.console_put_char_ex(con, screen_x, screen_y, tile.char, color, colors.black)


def draw_entity(game, con, entity, fov_map, debug=False):
    if entity.render_order != RenderOrder.NONE:
        x, y = pos_on_screen(*entity.pos, game.player)

        if debug or entity.is_visible(fov_map) or (entity.render_order == RenderOrder.ALWAYS and game.map.tiles[entity.pos].explored > 0):
            if entity.is_visible(fov_map) and entity is not game.cursor and not debug:
                color = darken_color_by_fov_distance(game.player, entity.color, entity.x, entity.y, min=0.3)
            elif entity.render_order == RenderOrder.ALWAYS and not debug and not game.state == GameState.SHOW_MAP:
                color = colors.darkest_gray
            else:
                color = entity.color

            bg_color = colors.black if entity.color_bg is None else entity.color_bg
            tcod.console_put_char_ex(con, x, y, entity.char, color, bg_color)