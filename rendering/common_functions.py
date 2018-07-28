import tcod

from config_files import colors


def center_x_for_text(width, text, padding=0):
    """returns the x for a text centered in the passed width"""
    x = padding + (width - len(text)) // 2
    return x


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def draw_console_borders(con, width=None, height=None, color=colors.dark_grey):
    """ draws an outline around the passed console. By default, the console's width & height will be used """
    tcod.console_set_default_foreground(con, color)

    if width is None:
        width = con.width
    if height is None:
        height = con.height

    for x in range(width):
        tcod.console_put_char(con, x, 0, 196)
        tcod.console_put_char(con, x, height - 1, 196)

    for y in range(height):
        tcod.console_put_char(con, 0, y, 179)
        tcod.console_put_char(con, width - 1, y, 179)

    tcod.console_put_char(con, 0, 0, 218)
    tcod.console_put_char(con, width - 1, 0, 191)
    tcod.console_put_char(con, 0, height - 1, 192)
    tcod.console_put_char(con, width - 1, height - 1, 217)