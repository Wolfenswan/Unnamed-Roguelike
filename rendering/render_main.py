import tcod

from config_files import cfg as cfg, colors
from game import GameStates
from gui.menu import inventory_menu
from rendering.common_functions import get_names_under_mouse, draw_console_borders
from rendering.fov_functions import darken_color_by_fov_distance
from rendering.render_panels import render_bar


def render_all(game, fov_map, mouse, debug=False):
    screen_width = cfg.SCREEN_WIDTH
    screen_height = cfg.SCREEN_HEIGHT
    bar_width = 20 # TODO use cfg.file
    panel_height = cfg.BOTTOM_PANEL_HEIGHT
    panel_y = cfg.BOTTOM_PANEL_Y

    player = game.player
    entities = game.entities
    game_map = game.map
    con = game.con
    bottom_panel = game.bottom_panel
    message_log = game.message_log
    debug = game.debug or debug

    # Render game map #
    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.tiles[x][y]
            visible = tcod.map_is_in_fov(fov_map, x, y) or debug
            wall = tile.block_sight

            if visible:
                # TODO Brightness fall off with range
                fg_color = darken_color_by_fov_distance(player, colors.light_fov, x, y)
                if debug:
                    fg_color = colors.light_fov
                char = '#' if wall else '.'

                if tile.gibbed:
                    fg_color = colors.corpse

                tcod.console_put_char_ex(con, x, y, char, fg_color, colors.black)
                tile.explored = True

            elif tile.explored:
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.dark_wall_fg, colors.dark_wall)
                else:
                    tcod.console_put_char_ex(con, x, y, '.', colors.dark_ground_fg, colors.dark_ground)

    # Draw all entities #
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(game, entity, fov_map, debug=debug)


    draw_console_borders(con, height=cfg.MAP_SCREEN_HEIGHT, color=colors.white)
    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    tcod.console_set_default_background(bottom_panel, tcod.black)
    tcod.console_clear(bottom_panel)

    # Print the game messages, one line at a time #
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(bottom_panel, message.color)
        tcod.console_print_ex(bottom_panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    tcod.console_set_default_foreground(bottom_panel, tcod.light_gray)
    tcod.console_print_ex(bottom_panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          get_names_under_mouse(mouse, entities, fov_map))

    # HP Bar #
    render_bar(bottom_panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               tcod.light_red, tcod.darker_red)

    draw_console_borders(bottom_panel, height=cfg.BOTTOM_PANEL_HEIGHT, color=colors.white)
    tcod.console_blit(bottom_panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    tcod.console_print_frame(bottom_panel, 0, 0, screen_width, panel_height)

    # Render inventory window #
    if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game.state == GameStates.SHOW_INVENTORY:
            header = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            header = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, 'Inventory', header, player.inventory, player.x, player.y)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(game, entity, fov_map, debug=False):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or debug:
        color = darken_color_by_fov_distance(game.player, entity.color, entity.x, entity.y)
        if debug:
            color = entity.color
        tcod.console_set_default_foreground(game.con, color)
        tcod.console_put_char(game.con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
