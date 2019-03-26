import os

import tcod

from config_files import cfg


def all_fonts():
    fonts = []
    path = 'resources/fonts/'
    for font in os.listdir(os.fsencode(path)):
        fonts.append(os.fsdecode(font))

    return fonts


def initialize_font(font = cfg.FONT_DEFAULT):
    path = 'resources/fonts/'
    layout = tcod.FONT_LAYOUT_TCOD if font in cfg.FONT_TCOD_LAYOUT else tcod.FONT_LAYOUT_ASCII_INROW
    tcod.console_set_custom_font(os.path.join(path, font), tcod.FONT_TYPE_GREYSCALE | layout)
    tcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.GAME_NAME, tcod.console_is_fullscreen())