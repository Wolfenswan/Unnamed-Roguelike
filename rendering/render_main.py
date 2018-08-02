from random import randint

import tcod

from config_files import cfg as cfg, colors
from game import GameStates
from gui.menus import inventory_menu, item_menu
from rendering.common_functions import get_names_under_mouse, draw_console_borders, pos_on_screen
from rendering.fov_functions import darken_color_by_fov_distance
from rendering.draw_panels import draw_bar


def render_main_screen(game, fov_map, debug=False):
    screen_width = cfg.SCREEN_WIDTH
    screen_height = cfg.SCREEN_HEIGHT
    bar_width = 20 # TODO use cfg.file
    panel_height = cfg.BOTTOM_PANEL_HEIGHT
    panel_y = cfg.BOTTOM_PANEL_Y

    player = game.player
    entities = game.entities
    con = game.con
    bottom_panel = game.bottom_panel
    message_log = game.message_log
    debug = game.debug or debug

    # Render game map #
    tcod.console_clear(con)
    # render_map(game, con, fov_map, debug=debug)
    render_map_centered_on_player(game, con, fov_map, debug=debug)

    # Draw all entities #
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(game, entity, fov_map, debug=debug)

    if game.state == GameStates.CURSOR_ACTIVE:
        draw_entity(game, game.cursor, fov_map, debug=debug)

    draw_console_borders(con, height=cfg.MAP_SCREEN_HEIGHT, color=colors.white)
    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def render_panels(game, fov_map):
    screen_width = cfg.SCREEN_WIDTH
    screen_height = cfg.SCREEN_HEIGHT
    bar_width = 20  # TODO use cfg.file
    panel_height = cfg.BOTTOM_PANEL_HEIGHT
    panel_y = cfg.BOTTOM_PANEL_Y

    player = game.player
    entities = game.entities
    bottom_panel = game.bottom_panel
    message_log = game.message_log

    tcod.console_set_default_background(bottom_panel, tcod.black)
    tcod.console_clear(bottom_panel)

    # Print the game messages, one line at a time #
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(bottom_panel, message.color)
        tcod.console_print_ex(bottom_panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    tcod.console_set_default_foreground(bottom_panel, tcod.light_gray)
    # tcod.console_print_ex(bottom_panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
    #                       get_names_under_mouse(mouse, entities, fov_map))

    # HP Bar #
    draw_bar(bottom_panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
             tcod.light_red, tcod.darker_red)

    draw_console_borders(bottom_panel, height=cfg.BOTTOM_PANEL_HEIGHT, color=colors.white)
    tcod.console_blit(bottom_panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    tcod.console_print_frame(bottom_panel, 0, 0, screen_width, panel_height)


def render_windows(game, selected_item):
    # Function to render all temporary windows & popup screens #
    if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        inventory_menu(game)

    if game.state == GameStates.SHOW_ITEM and selected_item is not None:
        item_menu(selected_item, game)


def render_map(game, con, fov_map, debug=False):
    """ Obsolete rendering function """

    for screen_y in range(cfg.MAP_SCREEN_HEIGHT):
       for screen_x in range(cfg.MAP_SCREEN_WIDTH):
            tile_x, tile_y = screen_x, screen_y
            draw_tile(game, con, fov_map, tile_x, tile_y, screen_x, screen_y, debug=debug)

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
    tile = game.map.tiles[tile_x][tile_y]
    visible = tcod.map_is_in_fov(fov_map, tile_x, tile_y)
    wall = tile.block_sight and not tile.walkable

    fg_color = darken_color_by_fov_distance(game.player, colors.light_fov, tile_x, tile_y, randomness = 0)
    if debug:
        fg_color = colors.light_fov


    if visible:
        char = '#' if wall else '.'
        if tile.gibbed:
            fg_color = colors.corpse

        tcod.console_put_char_ex(con, screen_x, screen_y, char, fg_color, colors.black)
        tile.explored = 50

    elif tile.explored > 0:
        tile.explored -= randint(0, 1)
        if game.state == GameStates.PLAYER_RESTING:
            if wall:
                tcod.console_put_char_ex(con, screen_x, screen_y, '#', colors.dark_wall_fg, colors.dark_ground)
            else:
                tcod.console_put_char_ex(con, screen_x, screen_y, '.', colors.dark_ground_fg, colors.dark_ground)


def draw_entity(game, entity, fov_map, debug=False):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or debug:
        x, y = pos_on_screen(entity.x, entity.y, game.player)

        tcod.console_put_char(game.con, x, y, entity.char)

        # Set the entity colors #
        if entity is not game.cursor:
            color = darken_color_by_fov_distance(game.player, entity.color, entity.x, entity.y)
        else:
            color = entity.color
        if debug:
            color = entity.color

        tcod.console_set_char_foreground(game.con, x, y, color)
        if entity.color_bg is not None:
            tcod.console_set_char_background(game.con, x, y, entity.color_bg)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)