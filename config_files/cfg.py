#! python3
""" Constant variables """
import tcod

GAME_NAME = 'The Hive'
DEBUG = {
    'no_intro' : True,
    'invincibility': False,
    'reveal_map': False,
    'detailed_ent_info': False,
    'prevent_item_spawning': True, # also prevents containers
    'prevent_npc_spawning': False,
    'prevent_architecture_spawning': True, # excluding special objects (e.g. stairs)
}
LOGGING = {
    'debug': True,
    'runtime': True, # times functions
}

# DISPLAY SETTINGS
SCREEN_WIDTH = 76 # should be > 70 with Cheepicus 8x8x2
SCREEN_HEIGHT = 54
LIMIT_FPS = 30

FONT_DEFAULT = 'Cheepicus_8x8x2.png' # Recommended: Cheepicus_8x8x2.png
FONT_TCOD_LAYOUT = ['arial12x12.png','dejavu12x12_gs_tc.png','dejavu12x12_gs_tc.png','consolas10x10_gs_tc.png']

# DUNGEON SETTINGS #
DUNGEON_LOWEST_LEVEL = 6
DUNGEON_MIN_WIDTH = SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 2
DUNGEON_MIN_HEIGHT = SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 2

# NPC SETTINGS #
GROUPS_MIN_FACTOR = 0.5 # total rooms * this
GROUPS_MAX_FACTOR = 1 # total rooms * this
# MONSTERS_DUNGEON_FACTOR = 5 # total rooms * this
MONSTERS_ROOM_LIMIT = 10 # room width * room height // this

# ITEM SETTINGS #
ITEMS_DUNGEON_FACTOR = 0.75 # total rooms * this
ITEMS_ROOM_LIMIT = 0.25 # (room width * room height) * this

# CONTAINER SETTINGS #
# TODO put in relation to max items?
CONTAINER_DUNGEON_FACTOR = 0.7 # total rooms * this
CONTAINER_ROOM_FACTOR = 0.3 # (room width * room height) * this

# STATIC OBJECT SETTINGS #
#SOBJECTS_DUNGEON_FACTOR = 5 # total rooms times this (UNUSED)
SOBJECTS_ROOM_DIVISOR = 10  # room width * room height // this

# GAMEPLAY
ATK_EXERT_MULTIPL = 3 # attack power * this is the base amount of stamina this attack uses
DEFLECT_EXERT_MULTIPL = 1.5 # attack power * this is the amount of exertion a full armor deflection causes
DASH_EXERT_MULTIPL = 2.5 # Total AV * this

# FOV
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
FOV_RADIUS = 7
