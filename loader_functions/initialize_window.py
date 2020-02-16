import tcod

from config_files import cfg
from rendering import render_constants as cons


def initialize_window(game):
    """ initializes everything relevant to game window """

    # Consoles #
    game.root = tcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    #game.root = tcod.console.Console(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    # game.con = tcod.console.Console(cons.SCREEN_WIDTH, cons.SCREEN_HEIGHT)
    game.map_panel = tcod.console.Console(cons.MAP_SCREEN_WIDTH, cons.MAP_SCREEN_HEIGHT)
    game.status_panel = tcod.console.Console(cons.STATUS_BAR_WIDTH, cons.STATUS_BAR_HEIGHT)
    game.top_right_panel = tcod.console.Console(cons.SIDE_PANEL_WIDTH, cons.PLAYER_PANEL_HEIGHT)
    game.center_right_panel = tcod.console.Console(cons.SIDE_PANEL_WIDTH, cons.COMBAT_PANEL_HEIGHT)
    game.lower_right_panel = tcod.console.Console(cons.SIDE_PANEL_WIDTH, cons.OBJECT_PANEL_HEIGHT)
    game.bottom_left_panel = tcod.console.Console(cons.MSG_PANEL1_WIDTH, cons.BOTTOM_PANEL_HEIGHT)
    game.bottom_center_panel = tcod.console.Console(cons.MSG_PANEL2_WIDTH, cons.BOTTOM_PANEL_HEIGHT)
