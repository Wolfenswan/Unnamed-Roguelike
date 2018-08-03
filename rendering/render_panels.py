""" Panels are permanently displayed consoles containing information relevant to the game """

import tcod

from config_files import colors


def draw_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                          f'{name}: {value}/{maximum}')


"""
def draw_quickslot_panel():

    total_slots = gv.player.paperdoll.get_total_qu_slots()
    width = 2 * total_slots + 1
    height = 3
    start_x = settings.MAP_SCREEN_WIDTH // 2 - width // 2
    start_y = settings.MAP_SCREEN_HEIGHT - height

    window = tdl.Window(gv.root, start_x, start_y, width, height)
    window.caption = ''
    window.border_color = settings.PANELS_BORDER_COLOR
    setup_panel(window)

    o_x = 2
    for s in range(1,total_slots):
        window.draw_char(o_x, 0, '194', fg=settings.PANELS_BORDER_COLOR, bg=None)
        window.draw_char(o_x,1,'179', fg=settings.PANELS_BORDER_COLOR, bg=None)
        window.draw_char(o_x, 2, '193', fg=settings.PANELS_BORDER_COLOR, bg=None)
        o_x += 2

    o_x = 1
    for i, item in enumerate(gv.player.get_all_qu_items()):
        window.draw_str(o_x, 0, str(i+1), fg=colors.white, bg=None)
        window.draw_str(o_x,1,'{0}'.format(item.char),fg=item.color)
        o_x += 2
"""