#! python3
""" Constant variables """
import tcod

DEBUG = False
GAME_NAME = 'RoguelikeTutReloaded'

# DISPLAY SETTINGS
SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40
LIMIT_FPS = 30

FONT_DEFAULT = 'Cheepicus_8x8x2.png'
FONT_TCOD_LAYOUT = ['arial12x12.png','dejavu12x12_gs_tc.png','dejavu12x12_gs_tc.png','consolas10x10_gs_tc.png']

# DUNGEON SETTINGS #
DUNGEON_LOWEST_LEVEL = 10
DUNGEON_MIN_WIDTH = MAP_SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 2
DUNGEON_MIN_HEIGHT = MAP_SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 2

# TODO Set this up so they are relative in size to dungeon/room #
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 4

# NPC SETTINGS #
MONSTERS_DUNGEON_FACTOR = 3 # total rooms * this
MONSTERS_ROOM_LIMIT = 15 # room width * room height // this

# ITEM SETTINGS #
ITEMS_DUNGEON_FACTOR = 0.5 # total rooms * this
ITEMS_ROOM_LIMIT = 50 # room width * room height // this

# CONTAINER SETTINGS #
# TODO put in relation to max items?
CONTAINER_DUNGEON_FACTOR = 1 # total rooms * this
CONTAINER_ROOM_DIVISOR = 30 # room width * room height // this

# STATIC OBJECT SETTINGS #
#SOBJECTS_DUNGEON_FACTOR = 5 # total rooms times this (UNUSED)
SOBJECTS_ROOM_DIVISOR = 20  # room width * room height // this

# Interaction
DASH_EXERT_MULTIPL = 3 # Total AV * this

# FOV
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
FOV_RADIUS = 7
