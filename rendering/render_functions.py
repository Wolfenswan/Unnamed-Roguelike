import tcod

from config_files import cfg as cfg, colors
from game import GameStates
from gui.menu import inventory_menu


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                          '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(game, fov_map, mouse, debug=False):
    screen_width = cfg.SCREEN_WIDTH
    screen_height = cfg.SCREEN_HEIGHT
    bar_width = 20
    panel_height = cfg.BOTTOM_PANEL_HEIGHT
    panel_y = cfg.BOTTOM_PANEL_Y

    player = game.player
    entities = game.entities
    game_map = game.map
    con = game.con
    panel = game.panel
    message_log = game.message_log
    debug = game.debug or debug

    # Render game map #
    for y in range(game_map.height):
        for x in range(game_map.width):
            visible = tcod.map_is_in_fov(fov_map, x, y) or debug
            wall = game_map.tiles[x][y].block_sight

            if visible:
                # TODO Brightness fall off with range
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.light_wall, colors.black)
                else:
                    tcod.console_put_char_ex(con, x, y, '.', colors.light_ground, colors.black)

                game_map.tiles[x][y].explored = True
            elif game_map.tiles[x][y].explored:
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.dark_wall_fg, colors.dark_wall)
                else:
                    tcod.console_put_char_ex(con, x, y, '.', colors.dark_ground_fg, colors.dark_ground)

    # Draw all entities #
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, debug=debug)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print the game messages, one line at a time #
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          get_names_under_mouse(mouse, entities, fov_map))

    # HP Bar #
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               tcod.light_red, tcod.darker_red)

    tcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    # Render inventory window #
    if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game.state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player.inventory, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, debug=False):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or debug:
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
