import tcod

from config_files import cfg


def initialize_window(game):
    """ initializes everything relevant to game window """

    # Consoles #
    game.con = tcod.console_new(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    game.map_panel = tcod.console_new(cfg.MAP_SCREEN_WIDTH, cfg.MAP_SCREEN_HEIGHT)
    game.status_panel = tcod.console_new(cfg.BOTTOM_PANELS_WIDTH, cfg.STATUS_PANEL_HEIGHT)
    game.top_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.PLAYER_PANEL_HEIGHT)
    game.center_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.COMBAT_PANEL_HEIGHT)
    game.lower_right_panel = tcod.console_new(cfg.SIDE_PANEL_WIDTH, cfg.OBJECT_PANEL_HEIGHT)
    game.bottom_left_panel = tcod.console_new(cfg.MSG_PANEL1_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
    game.bottom_center_panel = tcod.console_new(cfg.MSG_PANEL2_WIDTH, cfg.BOTTOM_PANELS_HEIGHT)
