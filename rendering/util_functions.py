import tcod

from config_files import colors, cfg as cfg


def center_x_for_text(width, text, padding=0):
    """returns the x for a text centered in the passed width"""
    x = padding + (width - len(text)) // 2
    return x


def get_names_under_mouse(mouse, entities, fov_map):
    # TODO get names under cursor
    # TODO description window for NPCs
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def setup_console(con, caption=None, fgcolor=tcod.white, bgcolor =tcod.black, borders=False):
    tcod.console_set_default_foreground(con, fgcolor)
    tcod.console_set_default_background(con, bgcolor)
    tcod.console_clear(con)
    if borders:
        draw_console_borders(con)
    if caption:
        tcod.console_print(con, 2, 0, caption)


def draw_console_borders(con, width=None, height=None, color=colors.dark_grey, bgcolor=colors.black):
    """ draws an outline around the passed console. By default, the console's width & height will be used """
    #tcod.console_set_default_foreground(con, color)

    if width is None:
        width = con.width
    if height is None:
        height = con.height

    for x in range(width):
        tcod.console_put_char_ex(con, x, 0, 196, color, bgcolor)
        tcod.console_put_char_ex(con, x, height - 1, 196, color, bgcolor)

    for y in range(height):
        tcod.console_put_char_ex(con, 0, y, 179, color, bgcolor)
        tcod.console_put_char_ex(con, width - 1, y, 179, color, bgcolor)

    tcod.console_put_char_ex(con, 0, 0, 218, color, bgcolor)
    tcod.console_put_char_ex(con, width - 1, 0, 191, color, bgcolor)
    tcod.console_put_char_ex(con, 0, height - 1, 192, color, bgcolor)
    tcod.console_put_char_ex(con, width - 1, height - 1, 217, color, bgcolor)


def pos_on_screen(x, y, player):
    """
    Returns coordinate on the visible screen, in relation to the player

    """

    x = max(cfg.MAP_SCREEN_WIDTH // 2 + (x - player.x), 0)
    y = max(cfg.MAP_SCREEN_HEIGHT // 2 + (y - player.y), 0)

    return x, y
