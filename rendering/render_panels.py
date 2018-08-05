""" Panels are permanently displayed consoles containing information relevant to the game """

import tcod

from config_files import colors, cfg as cfg
from rendering.util_functions import draw_console_borders, center_x_for_text, setup_console


def render_panels(game):

    render_status_panel(game, cfg.STATUS_PANEL_Y, cfg.SCREEN_WIDTH, cfg.STATUS_PANEL_HEIGHT)
    render_combat_panel(game, game.bottom_left_panel, cfg.BOTTOM_PANELS_Y, cfg.COMBAT_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    render_message_panel(game.observation_log, 'Observations', game.bottom_center_panel, cfg.MSG_PANEL1_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    render_message_panel(game.event_log, "Events", game.bottom_right_panel, cfg.MSG_PANEL2_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    #render_bottom_panels(game)

# TODO: Three separate panels for bottom panel - combat, message1, message 2

def render_combat_panel(game, con, panel_y, width, height):

    setup_console(con, caption='Enemies', borders=True)
    
    # check for monsters in FOV
    spotted = [ent for ent in game.entities if ent.ai and ent.is_visible(game.fov_map)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width

            # Draw creature name and stats #
            tcod.console_set_color_control(tcod.COLCTRL_1, ent.color, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_2, colors.red, tcod.black) # TODO make dynamic
            tcod.console_print(con, 2, y, f'%c{ent.name}%c %c{ent.fighter.hp}/{ent.fighter.max_hp}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP, tcod.COLCTRL_2, tcod.COLCTRL_STOP))

            y += 2
            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                tcod.console_print(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

    tcod.console_blit(con, 0, 0, width, height, 0, 0, panel_y)


def render_message_panel(message_log, title, con, panel_x, panel_y, width, height):
    setup_console(con, caption=title, borders=True)

    y = 2
    color_coefficient = 1.0
    for message in reversed(message_log.messages):
        color = tuple(int(color_coefficient * x) for x in message.color)
        tcod.console_set_default_foreground(con, color)
        tcod.console_print(con, message_log.x, y, message.text)
        y += 1

        if color_coefficient >= 0.4:
            color_coefficient -= 0.1

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_status_panel(game, panel_y, width, height):
    # TODO Stamina & Quick Use
    console = game.status_panel
    tcod.console_set_default_background(console, tcod.black)
    tcod.console_clear(console)

    draw_bar(console, 1, 1, 20, 'HP', game.player.fighter.hp, game.player.fighter.max_hp,
             tcod.light_red, tcod.darker_red)

    tcod.console_blit(console, 0, 0, width, height, 0, 0, panel_y)
    tcod.console_print_frame(console, 0, 0, width, height)


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