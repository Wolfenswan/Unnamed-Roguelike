#! python3
""" Constant variables """
import tcod

GAME_NAME = 'The Hive'
DEBUG = {
    'no_intro' : True,
    'invincibility': True,
    'reveal_map': False,
    'detailed_ent_info': True,
    'prevent_item_spawning': False, # also prevents containers
    'prevent_npc_spawning': False,
    'prevent_architecture_spawning': False, # excluding special objects (e.g. stairs)
}
LOGGING = {
    'debug': True,
    'runtime': False,
}

# DISPLAY SETTINGS
SCREEN_WIDTH = 76 # should be > 70 with Cheepicus 8x8x2
SCREEN_HEIGHT = 54
LIMIT_FPS = 30

FONT_DEFAULT = 'Cheepicus_8x8x2.png' # Recommended: Cheepicus_8x8x2.png
FONT_TCOD_LAYOUT = ['arial12x12.png','dejavu12x12_gs_tc.png','dejavu12x12_gs_tc.png','consolas10x10_gs_tc.png']

# DUNGEON SETTINGS #
DUNGEON_LOWEST_LEVEL = 10
DUNGEON_MIN_WIDTH = SCREEN_WIDTH * 0.8
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 1.2
DUNGEON_MIN_HEIGHT = SCREEN_HEIGHT * 0.8
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 1.2

# TODO should be relative in size to dungeon/room #
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 4

# NPC SETTINGS #
MONSTERS_DUNGEON_FACTOR = 5 # total rooms * this
MONSTERS_ROOM_LIMIT = 10 # room width * room height // this

# ITEM SETTINGS #
ITEMS_DUNGEON_FACTOR = 1.2 # total rooms * this
ITEMS_ROOM_LIMIT = 30 # room width * room height // this

# CONTAINER SETTINGS #
# TODO put in relation to max items?
CONTAINER_DUNGEON_FACTOR = 0.7 # total rooms * this
CONTAINER_ROOM_DIVISOR = 50 # room width * room height // this

# STATIC OBJECT SETTINGS #
#SOBJECTS_DUNGEON_FACTOR = 5 # total rooms times this (UNUSED)
SOBJECTS_ROOM_DIVISOR = 10  # room width * room height // this

# GAMEPLAY
ATK_EXERT_DIVISOR = 2 # attack power / this is the base amount of stamina this attack uses
DEFLECT_EXERT_MULTIPL = 1.5 # attack power * this is the amount of exertion a full armor deflection causes
DASH_EXERT_MULTIPL = 2.5 # Total AV * this

# FOV
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
FOV_RADIUS = 7
