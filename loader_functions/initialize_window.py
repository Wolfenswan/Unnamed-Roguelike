import os

import tcod

from config_files import cfg

def initialize_window(game):
    """ initializes everything relevant to game window """

    # Set custom font #
    fonts = (
        'arial10x10',  # 0
        'arial12x12',  # 1,
        'consolas10x10_gs_tc', # 2
        'courier10x10_aa_tc',  # 3
        'lucida10x10_gs_tc',  # 4
        'prestige10x10_gs_tc',  # 5
        'dejavu12x12_gs_tc',  # 6
        'terminal8x8_gs_ro',  # 7
        'terminal10x10_gs_tc',  # 8
        'terminal12x12_gs_ro',  # 9 # FONT_LAYOUT_ASCII_INROW
        'terminal16x16_gs_ro',  # 10 # FONT_LAYOUT_ASCII_INROW
        'Cheepicus_8x8x2', # 11
        'Cheepicus_16x16', # 12
        '16x16_sm', # 13
    )
    font = fonts[11]+'.png'
    path = 'resources/fonts/'
    tcod.console_set_custom_font(os.path.join(path, font), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_ASCII_INROW)
    #tcod.console_set_custom_font(os.path.join(path, font), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.GAME_NAME, False)

    # Consoles #
    game.con = tcod.console_new(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    game.map_panel = tcod.console_new(cfg.MAP_SCREEN_WIDTH, cfg.MAP_SCREEN_HEIGHT) # TODO Currently unused
    game.status_panel = tcod.console_new(cfg.BOTTOM_PANELS_WIDTH, cfg.STATUS_PANEL_HEIGHT)
    game.top_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.PLAYER_PANEL_HEIGHT)
    game.center_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.COMBAT_PANEL_HEIGHT)
    game.lower_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.OBJECT_PANEL_HEIGHT)
    game.bottom_left_panel = tcod.console_new(cfg.MSG_PANEL1_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    game.bottom_center_panel = tcod.console_new(cfg.MSG_PANEL2_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)