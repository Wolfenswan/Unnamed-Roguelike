""" Panels are permanently displayed consoles containing information relevant to the game """
import textwrap

import tcod

from config_files import colors, cfg as cfg
from rendering.util_functions import center_x_for_text, setup_console


def render_panels(game):

    render_player_panel(game, game.top_right_panel, cfg.SIDE_PANEL_X, 1, cfg.SIDE_PANEL_WIDTH,
                       cfg.PLAYER_PANEL_HEIGHT)
    render_enemy_panel(game, game.center_right_panel, cfg.SIDE_PANEL_X, cfg.PLAYER_PANEL_HEIGHT + 1, cfg.SIDE_PANEL_WIDTH,
                       cfg.COMBAT_PANEL_HEIGHT)
    render_object_panel(game, game.lower_right_panel, cfg.SIDE_PANEL_X, cfg.PLAYER_PANEL_HEIGHT + cfg.COMBAT_PANEL_HEIGHT + 1, cfg.SIDE_PANEL_WIDTH,
                       cfg.OBJECT_PANEL_HEIGHT)
    render_status_panel(game, game.status_panel, cfg.STATUS_PANEL_Y, cfg.BOTTOM_PANELS_WIDTH, cfg.STATUS_PANEL_HEIGHT)
    render_message_panel(game.observation_log, 'Observations', game.bottom_left_panel, 0, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    render_message_panel(game.event_log, 'Combat', game.bottom_center_panel, cfg.MSG_PANEL2_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)

    # OLD BOTTOM GUI
    # render_enemy_panel(game, game.bottom_left_panel, 0, cfg.BOTTOM_PANELS_Y, cfg.COMBAT_PANEL_WIDTH,
    #                    cfg.BOTTOM_PANELS_HEIGHT)
    # render_message_panel(game.observation_log, 'Observations', game.bottom_center_panel, cfg.MSG_PANEL1_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    # render_message_panel(game.event_log, 'Combat', game.bottom_right_panel, cfg.MSG_PANEL2_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)


def render_player_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, caption='Player Status', borders=True)

    player = game.player

    #draw_quickslots(con, game)

    # Armor
    # Weapon  Damage
    # Display weapon move information #
    if player.fighter.weapon and player.fighter.weapon.moveset:
        tcod.console_print(con, 1, 1, f'{game.player.fighter.weapon.moveset.current_move}')

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)

def render_object_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, caption='Objects', borders=True)

    # check for objects in FOV
    spotted = [ent for ent in (game.item_ents + game.architecture_ents) if ent.is_visible(game.fov_map)]
    #spotted = [ent for ent in game.entities if ent.is_visible(game.fov_map) and (ent.item is not None or ent.architecture is not None)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width

            # Draw creature name and stats #
            tcod.console_set_color_control(tcod.COLCTRL_1, ent.color, tcod.black)
            symbol = '*' if (ent.x, ent.y) == (game.player.x, game.player.y) else f'{ent.char}'
            wrapped_name = textwrap.wrap(f'{symbol} {ent.name}', width-3)
            for i, line in enumerate(wrapped_name):
                tcod.console_print(con, 1+i, y, f'%c{line}%c' % (
                tcod.COLCTRL_1, tcod.COLCTRL_STOP))

                y += 2
                if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                    x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                    tcod.console_print(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                    break

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)

def render_enemy_panel(game, con, panel_x, panel_y, width, height):

    color = colors.dark_gray if not game.player.visible_enemies(game.entities, game.fov_map) else colors.dark_red
    setup_console(con, caption='Enemies', borders=True, bordercolor=color)
    
    # check for monsters in FOV
    spotted = [ent for ent in game.monster_ents if ent.is_visible(game.fov_map) and ent.fighter.hp > 0]
    #spotted = [ent for ent in game.entities if ent.ai and ent.fighter.hp > 0 and ent.is_visible(game.fov_map)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width

            # Draw creature name and stats #
            tcod.console_set_color_control(tcod.COLCTRL_1, ent.color, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_2, ent.fighter.hp_color, tcod.black) # TODO make dynamic
            tcod.console_print(con, 1, y, f'%c{ent.char} {ent.name}%c | %c{ent.fighter.hp_string.capitalize()}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP, tcod.COLCTRL_2, tcod.COLCTRL_STOP))

            y += 2
            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                tcod.console_print(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_message_panel(message_log, title, con, panel_x, panel_y, width, height):
    setup_console(con, caption=title, borders=True)

    y = 2
    color_coefficient = 1.0
    for message in reversed(message_log.messages):
        color = tuple(int(color_coefficient * x) for x in message.color)
        tcod.console_set_color_control(tcod.COLCTRL_1, color, colors.black)
        tcod.console_print(con, message_log.x, y, f'%c{message.text}%c' %(tcod.COLCTRL_1, tcod.COLCTRL_STOP))
        y += 1

        if color_coefficient >= 0.4:
            color_coefficient -= 0.1

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_status_panel(game, console, panel_y, width, height):
    setup_console(console, fgcolor=colors.light_gray)

    draw_bar(console, 1, 1, 20, 'HP', int(game.player.fighter.hp), game.player.fighter.max_hp,
             tcod.light_red, tcod.darker_red)

    draw_bar(console, width-21, 1, 20, 'Stamina', int(game.player.fighter.stamina), game.player.fighter.max_stamina,
             colors.blue, colors.darker_blue)

    draw_quickslots(console, game)

    tcod.console_blit(console, 0, 0, width, height, 0, 0, panel_y)
    tcod.console_print_frame(console, 0, 0, width, height)


def draw_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)


    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_color_control(tcod.COLCTRL_1, colors.white, bar_color)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, f'%c{name}: {value}/{maximum}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP))


def draw_quickslots(con, game):

    player = game.player

    total_slots = player.qu_inventory.capacity
    width = 3 * total_slots # every slot needs 3 pixels
    start_x = cfg.BOTTOM_PANELS_WIDTH // 2 - width // 2
    #start_x = cfg.SIDE_PANEL_WIDTH // 2 - width // 2 + 4
    start_y = 0

    if total_slots > 0:
        o_x = start_x
        o_y = start_y
        tcod.console_set_char(con, o_x, o_y, 218)
        tcod.console_set_char(con, o_x, o_y+1, 179)
        tcod.console_set_char(con, o_x, o_y+2, 192)
        o_x += 1
        for s in range(1,total_slots):
            tcod.console_set_char(con, o_x, o_y, 196)
            tcod.console_set_char(con, o_x, o_y+2, 196)
            o_x += 1
            tcod.console_set_char(con, o_x, o_y, 194)
            tcod.console_set_char(con, o_x, o_y+1, 179)
            tcod.console_set_char(con, o_x, o_y+2, 193)
            o_x += 1
        tcod.console_set_char(con, o_x, o_y, 196)
        tcod.console_set_char(con, o_x, o_y+2, 196)
        o_x += 1
        tcod.console_set_char(con, o_x, o_y, 191)
        tcod.console_set_char(con, o_x, o_y+1, 179)
        tcod.console_set_char(con, o_x, o_y+2, 217)

        o_x = start_x + 1
        for i, item in enumerate(player.qu_inventory.items):
            tcod.console_set_char_foreground(con, o_x, 0, colors.white)
            tcod.console_set_char(con, o_x, 0, f'{i+1}')
            tcod.console_set_color_control(tcod.COLCTRL_1, item.color, colors.black)
            tcod.console_print(con, o_x, 1, f'%c{item.char}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP))
            o_x += 2
