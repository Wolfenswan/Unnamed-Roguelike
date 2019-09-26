""" Panels are permanently displayed consoles containing information relevant to the game """

import tcod

from components.combat.fighter_util import Surrounded
from config_files import colors
from rendering import render_constants as r_cons
from game import GameState
from rendering.util_functions import center_x_for_text, setup_console, print_string, dynamic_wrap, draw_console_borders


def render_panels(game):
    render_player_panel(game,game.top_right_panel, r_cons.SIDE_PANEL_X, 0, r_cons.SIDE_PANEL_WIDTH, r_cons.PLAYER_PANEL_HEIGHT)
    #render_status_panel(game, game.status_panel, r_cons.STATUS_BAR_Y, r_cons.BOTTOM_PANEL_WIDTH - 4, r_cons.STATUS_BAR_HEIGHT)
    color = colors.dark_gray if not game.player.visible_enemies(game.npc_ents, game.fov_map) else colors.dark_red
    render_enemy_panel(game, game.center_right_panel, r_cons.SIDE_PANEL_X, r_cons.PLAYER_PANEL_HEIGHT, r_cons.SIDE_PANEL_WIDTH,
                       r_cons.COMBAT_PANEL_HEIGHT, color)
    render_object_panel(game, game.lower_right_panel, r_cons.SIDE_PANEL_X, r_cons.PLAYER_PANEL_HEIGHT + r_cons.COMBAT_PANEL_HEIGHT, r_cons.SIDE_PANEL_WIDTH,
                       r_cons.SIDE_PANEL_HEIGHT)
    render_message_panel(game.combat_log, 'Combat', game.bottom_center_panel, r_cons.MSG_PANEL2_X, r_cons.BOTTOM_PANEL_Y, r_cons.MSG_PANEL2_WIDTH, r_cons.BOTTOM_PANEL_HEIGHT,  game)
    render_message_panel(game.observation_log, 'Observations', game.bottom_left_panel, 0, r_cons.BOTTOM_PANEL_Y,
                         r_cons.MSG_PANEL1_WIDTH, r_cons.BOTTOM_PANEL_HEIGHT, game)
    #draw_quickslots(game.root, r_cons.MAP_SCREEN_HEIGHT-2, game)

def render_player_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, caption='Status', borders=True)
        
    player = game.player
    y = 0

    # Health & Stamina #
    y += 2
    hp_string = f'HIT: %c{player.f.hp}/{player.f.max_hp}%c'
    print_string(con, 1, y, hp_string, color=game.player.f.hp_color)
    hp_diff = player.statistics.hp_change
    if hp_diff != 0:
        col = colors.darker_green if hp_diff > 0 else colors.darker_red
        print_string(con, len(hp_string)- 2, y, f'(%{col}%{hp_diff}%%)')

    sta_string = f'STA: %c{player.f.stamina}/{player.f.max_stamina}%c'
    print_string(con, 1, y+1,  sta_string, color = game.player.f.stamina_color)
    sta_diff = player.statistics.sta_change
    if sta_diff != 0:
        col = colors.lighter_sea if sta_diff > 0 else colors.darker_sea
        print_string(con, len(sta_string)-2, y+1,  f'(%{col}%{sta_diff}%%)')

    # Effects #
    # TODO can theoretically overflow if there a large number of effects (>6) at once
    y += 2
    x = 2
    for effect, active in player.effects.items():
        if active:
            print_string(con, x, y, f'*{effect.name[0]}', color=colors.red)
            x += 3

    # Equipment-derived stats #
    y += 1
    # Defensive Stats #
    surrounded = player.f.surrounded
    if surrounded == Surrounded.THREATENED:
        print_string(con, 3, y, '*THREATENED*', color=colors.orange)
    if surrounded == Surrounded.OVERWHELMED:
        print_string(con, 3, y, '*OVERWHELMED*', color=colors.red)

    print_string(con, 1, y + 1, f'STR: {player.f.strength}')
    color = colors.white if player.f.modded_defense >= player.f.defense else colors.dark_red
    print_string(con, 1, y + 2, f'DEF: %c{player.f.modded_defense}%c', color=color)

    color = colors.panel_stat_active if player.f.is_dashing else colors.panel_inactive
    print_string(con, 9, y + 1, f'DASHING', color=color)
    #
    if player.f.shield and player.f.shield.block_def:
        col1 = colors.panel_inactive if not player.f.is_blocking else colors.panel_stat_active
        col2 = 'dark_red' if player.f.shield.block_def > player.f.modded_block_def else f'{col1}'
        print_string(con, 9, y + 2, f'%{col1}%BLOCK:%% %{col2}%{player.f.modded_block_def}%%')

    # Weapon #
    y += 4
    if player.f.weapon_melee is not None:
        color = colors.panel_stat_active if player.f.weapon_melee.is_active_weapon(player) else colors.panel_inactive
        print_string(con, 1, y, f'%c{player.f.weapon_melee.name}%c', color=color)

    if player.f.weapon_ranged is not None:
        color = colors.panel_stat_active if player.f.weapon_ranged.is_active_weapon(player) else colors.panel_inactive
        x = 2 + len(player.f.weapon_melee.name) if player.f.weapon_melee is not None else 1
        print_string(con, x, y,
                     f'%c{player.f.weapon_ranged.name}%c',
                     color=color)

    if player.f.active_weapon is not None:
        print_string(con, 2, y+1,
                     f'ATK: {game.player.f.active_weapon.moveset.current_move}/{game.player.f.active_weapon.moveset.moves}')
        print_string(con, 2, y+2, f'DAM: {game.player.f.modded_dmg_potential[0]}-{game.player.f.modded_dmg_potential[-1]}')


        # Visualize targets for next attack
        x = 11
        print_string(con, x, y+1, f'TAR:')
        for i, line in enumerate(player.f.active_weapon.moveset.targets_gui):
            print_string(con, x + 4, y+i, ''.join(line))

    # # Quick Slots #
    # y = 14
    # draw_quickslots(con, y, game)

    con.blit(game.root, panel_x, panel_y, 0, 0, width, height)

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

            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                print_string(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

            # Draw creature name and stats #
            # Some symbols don't print properly with console_print, that's why it's split into put_char_ex and print
            if ent.pos == game.player.pos or (ent.pos == game.cursor.pos and game.state in (GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING)):
                symbol = '*'
            else:
                symbol = f'{ent.char}'
            tcod.console_put_char_ex(con, 1, y, symbol, ent.color, tcod.black)
            #wrapped_name = textwrap.wrap(f'{ent.full_name}', width - 3)
            wrapped_name = dynamic_wrap(f'{ent.full_name}', width - 3)

            for i, line in enumerate(wrapped_name):
                print_string(con, 3+i, y, line, color=ent.color)
                y += 2

    #tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)
    con.blit(game.root, panel_x, panel_y, 0, 0, width, height)

def render_enemy_panel(game, con, panel_x, panel_y, width, height, color):
    setup_console(con, caption='Enemies', borders=True, bordercolor=color)
    
    # check for monsters in FOV
    spotted = [ent for ent in game.npc_ents if ent.is_visible(game.fov_map) and ent.f.hp > 0]
    #spotted = [ent for ent in game.entities if ent.ai and ent.f.hp > 0 and ent.is_visible(game.fov_map)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width
            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                tcod.console_set_default_foreground(con, colors.white)
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                print_string(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

            char = '*' if ent.pos == game.cursor.pos and game.state in [GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING] else f'{ent.char}'

            # Draw creature name and stats #
            tcod.console_set_default_foreground(con, colors.gray)
            tcod.console_set_color_control(tcod.COLCTRL_1, ent.color, tcod.black)
            tcod.console_put_char_ex(con, 1, y, char, ent.color, tcod.black)
            print_string(con, 3, y, ent.full_name, color = ent.color)
            y += 1
            x = 1
            tcod.console_put_char_ex(con, x, y, chr(192), tcod.gray, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_2, ent.f.hp_color, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_3, ent.f.stamina_color, tcod.black)
            status_line = f'%c{ent.f.hp_string.title()}%c|%c{ent.f.stamina_string.title()}%c'\
                          % (tcod.COLCTRL_2, tcod.COLCTRL_STOP, tcod.COLCTRL_3, tcod.COLCTRL_STOP)
            for status, active in ent.f.effects.items(): # Todo does not consider number of status effects > width of panel
                if active:
                    status_line += f' %white%{status.name[0]}%%'

            print_string(con, x+1, y, f'{status_line}')

            y += 1

    con.blit(game.root, panel_x, panel_y, 0, 0, width, height)


def render_message_panel(message_log, title, con, panel_x, panel_y, width, height, game):
    setup_console(con, caption=title, borders=True)

    current_turn = game.turn

    y = 1
    for message in reversed(message_log.messages):
        if current_turn - message.turn <= 1:
            color_coefficient = 1.0
        elif current_turn - message.turn <= 2:
            color_coefficient = 0.6
        elif current_turn - message.turn <= 3:
            color_coefficient = 0.4
        else:
            color_coefficient = 0.2

        print_string(con, message_log.x, y, message.text, fgcolor=message.color, color_coefficient=color_coefficient)
        y += 1

    con.blit(game.root, panel_x, panel_y, 0, 0, width, height)
    #tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_status_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, fgcolor=colors.light_gray)
    draw_console_borders(con, color=colors.dark_gray)

    bar_width = round(width//3)
    draw_bar(con, 1, 1, bar_width, f'{game.player.f.hp_string}', int(game.player.f.hp), game.player.f.max_hp,
             game.player.f.hp_color, tcod.darkest_red)
    draw_bar(con, width-bar_width-1, 1, bar_width, f'{game.player.f.stamina_string}', int(game.player.f.stamina), game.player.f.max_stamina,
             game.player.f.stamina_color, colors.darkest_blue)

    draw_quickslots(con, r_cons.MSG_PANEL1_WIDTH, 0, game)

    tcod.console_put_char_ex(con, 0, 0, 195, colors.dark_gray, colors.black)
    tcod.console_put_char_ex(con, width-1, 0, 180, colors.dark_gray, colors.black)
    con.blit(game.map_panel, panel_x, panel_y, 0, 0, width, height)
    #tcod.console_print_frame(con, 0, 0, width, height) # TODO can safely be deleted?


def draw_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    panel.draw_rect(x, y, total_width, 1, 0, bg = back_color)
    #tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, 0, bg = bar_color)

    print_string(panel, int(x + total_width / 2), y, f'{name.title()}', alignment = tcod.CENTER, background=tcod.BKGND_NONE)


def draw_quickslots(con, x, y, game):

    player = game.player
    color = colors.white #colors.panel_inactive

    total_slots = player.qu_inventory.capacity
    width = 3 * total_slots # every slot needs 3 pixels

    start_x = x - total_slots # r_cons.BOTTOM_PANEL_WIDTH // 2 - width // 2
    #start_x = (cons.SIDE_PANEL_WIDTH // 2 - width // 2) + 2
    
    if total_slots > 0:
        o_x = start_x
        o_y = y
        # tcod.console_put_char_ex(con, o_x, o_y, 218, color, colors.black)
        # tcod.console_put_char_ex(con, o_x, o_y + 1, 179, color, colors.black)
        # tcod.console_put_char_ex(con, o_x, o_y + 2, 192, color, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y, 194, color, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y + 1, 179, color, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y + 2, 193, color, colors.black)
        o_x += 1
        for s in range(0,total_slots):
            tcod.console_put_char_ex(con, o_x, o_y, 196, color, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y + 1, ' ', color, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y + 2, 196, color, colors.black)
            o_x += 1
            #if s < total_slots-1:
            tcod.console_put_char_ex(con, o_x, o_y, 194, color, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y + 1, 179, color, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y + 2, 193, color, colors.black)
            # else:
            #     tcod.console_put_char_ex(con, o_x, o_y, 191, color, colors.black)
            #     tcod.console_put_char_ex(con, o_x, o_y + 1, 179, color, colors.black)
            #     tcod.console_put_char_ex(con, o_x, o_y + 2, 217, color, colors.black)
            o_x += 1

        o_x = start_x + 1
        for i, item in enumerate(player.qu_inventory): # Draw icons into slots
            tcod.console_put_char_ex(con, o_x, y, f'{i+1}', colors.white, colors.black)
            tcod.console_put_char_ex(con, o_x, y+1, f'{item.char}', item.color, colors.black)
            o_x += 2
