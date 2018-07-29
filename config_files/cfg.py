#! python3
""" Constant variables """
import tcod

from config_files import colors

GAME_NAME = 'VermintideRL'

# Console
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 80
MAP_SCREEN_WIDTH = SCREEN_WIDTH
MAP_SCREEN_HEIGHT = SCREEN_HEIGHT - 10
LIMIT_FPS = 30

# Dungeon settings
DUNGEON_MIN_WIDTH = MAP_SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 2
DUNGEON_MIN_HEIGHT = MAP_SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 2
ROOM_MAX_SIZE = 18
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_MONSTERS = MAX_ROOMS/2 # Currently unused
MAX_ROOM_MONSTERS = 9      # TODO Adjust dynamically to room size
MAX_ROOM_ITEMS = 6
MAX_ROOM_STATICOBJECTS = 4

# GUI PANELS
PANELS_BORDER_COLOR = colors.dark_grey
PANELS_BORDER_COLOR_ACTIVE = colors.darker_red

# SIDE PANEL
SIDE_PANEL_WIDTH = SCREEN_WIDTH - MAP_SCREEN_WIDTH  # Difference between screen and map width
SIDE_PANEL_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH

# BOTTOM PANEL
BOTTOM_PANEL_HEIGHT = SCREEN_HEIGHT - MAP_SCREEN_HEIGHT  # Difference between screen and map height
BOTTOM_PANEL_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT
BOTTOM_PANEL_WIDTH = SCREEN_WIDTH

# Stat Panel
STAT_PANEL_HEIGHT = SCREEN_HEIGHT // 3
BAR_WIDTH = SIDE_PANEL_WIDTH - 2  # Width for the bars displaying health etc

# Inv Panel
INV_PANEL_HEIGHT_INACTIVE = SCREEN_HEIGHT - STAT_PANEL_HEIGHT - BOTTOM_PANEL_HEIGHT
INV_PANEL_HEIGHT_ACTIVE = SCREEN_HEIGHT - STAT_PANEL_HEIGHT

# Combat Panel (Enemy list & enemy details)
COMBAT_PANEL_WIDTH = BOTTOM_PANEL_WIDTH // 4

# Message panels
MSG_PANEL_WIDTH = (SCREEN_WIDTH - COMBAT_PANEL_WIDTH) // 2
MSG_WIDTH = SCREEN_WIDTH - 22 #MSG_PANEL_WIDTH - 2
MSG_HEIGHT = BOTTOM_PANEL_HEIGHT - 1
MSG_X = 22 # TODO Temporary testing value # offset for messages

# Message colors
MSG_COLOR_INFO_GAME = colors.turquoise
MSG_COLOR_INFO_GENERIC = colors.light_amber
MSG_COLOR_INFO_BAD = colors.dark_flame
MSG_COLOR_INFO_GOOD = colors.green
MSG_COLOR_FLUFF = colors.desaturated_red
MSG_COLOR_ALERT = colors.red

# Interaction
INVENTORY_WIDTH = 30

# FOV
FOV_ALGO = tcod.FOV_RESTRICTIVE
FOV_LIGHT_WALLS = True
FOV_RADIUS = 4
