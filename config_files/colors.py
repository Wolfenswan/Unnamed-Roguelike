"""selection of pre-defined colors"""
import tcod

# Dungeon
door = tcod.Color(153, 115, 0)
# light_fov = tcod.Color(127, 127, 127)
light_fov = tcod.Color(220, 195, 136)
dark_bg = (95, 95, 95)
dark_wall = tcod.Color(63, 63, 63)
dark_wall_fg = tcod.Color(95, 95, 95)
dark_ground = tcod.Color(31, 31, 31)
dark_ground_fg = tcod.Color(95, 95, 95)

# Entities
corpse = tcod.Color(127, 0, 0)

# custom
beige = tcod.Color(120, 100, 60)

# grey levels
black = tcod.Color(0, 0, 0)
darkest_grey = tcod.Color(31, 31, 31)

darker_grey = tcod.Color(63, 63, 63)
dark_grey = tcod.Color(95, 95, 95)
grey = tcod.Color(127, 127, 127)
light_grey = tcod.Color(159, 159, 159)
lighter_grey = tcod.Color(191, 191, 191)
lightest_grey = tcod.Color(223, 223, 223)
darkest_gray = tcod.Color(31, 31, 31)
darker_gray = tcod.Color(63, 63, 63)
dark_gray = tcod.Color(95, 95, 95)
gray = tcod.Color(127, 127, 127)
light_gray = tcod.Color(159, 159, 159)
lighter_gray = tcod.Color(191, 191, 191)
lightest_gray = tcod.Color(223, 223, 223)
white = tcod.Color(255, 255, 255)

# sepia
darkest_sepia = tcod.Color(31, 24, 15)
darker_sepia = tcod.Color(63, 50, 31)
dark_sepia = tcod.Color(94, 75, 47)
sepia = tcod.Color(127, 101, 63)
light_sepia = tcod.Color(158, 134, 100)
lighter_sepia = tcod.Color(191, 171, 143)
lightest_sepia = tcod.Color(222, 211, 195)

# standard s
red = tcod.Color(255, 0, 0)
flame = tcod.Color(255, 63, 0)
orange = tcod.Color(255, 127, 0)
amber = tcod.Color(255, 191, 0)
yellow = tcod.Color(255, 255, 0)
lime = tcod.Color(191, 255, 0)
chartreuse = tcod.Color(127, 255, 0)
green = tcod.Color(0, 255, 0)
sea = tcod.Color(0, 255, 127)
turquoise = tcod.Color(0, 255, 191)
cyan = tcod.Color(0, 255, 255)
sky = tcod.Color(0, 191, 255)
azure = tcod.Color(0, 127, 255)
blue = tcod.Color(0, 0, 255)
han = tcod.Color(63, 0, 255)
violet = tcod.Color(127, 0, 255)
purple = tcod.Color(191, 0, 255)
fuchsia = tcod.Color(255, 0, 255)
magenta = tcod.Color(255, 0, 191)
pink = tcod.Color(255, 0, 127)
crimson = tcod.Color(255, 0, 63)

# dark s
dark_red = tcod.Color(191, 0, 0)
dark_flame = tcod.Color(191, 47, 0)
dark_orange = tcod.Color(191, 95, 0)
dark_amber = tcod.Color(191, 143, 0)
dark_yellow = tcod.Color(191, 191, 0)
dark_lime = tcod.Color(143, 191, 0)
dark_chartreuse = tcod.Color(95, 191, 0)
dark_green = tcod.Color(0, 191, 0)
dark_sea = tcod.Color(0, 191, 95)
dark_turquoise = tcod.Color(0, 191, 143)
dark_cyan = tcod.Color(0, 191, 191)
dark_sky = tcod.Color(0, 143, 191)
dark_azure = tcod.Color(0, 95, 191)
dark_blue = tcod.Color(0, 0, 191)
dark_han = tcod.Color(47, 0, 191)
dark_violet = tcod.Color(95, 0, 191)
dark_purple = tcod.Color(143, 0, 191)
dark_fuchsia = tcod.Color(191, 0, 191)
dark_magenta = tcod.Color(191, 0, 143)
dark_pink = tcod.Color(191, 0, 95)
dark_crimson = tcod.Color(191, 0, 47)

# darker s
darker_red = tcod.Color(127, 0, 0)
darker_flame = tcod.Color(127, 31, 0)
darker_orange = tcod.Color(127, 63, 0)
darker_amber = tcod.Color(127, 95, 0)
darker_yellow = tcod.Color(127, 127, 0)
darker_lime = tcod.Color(95, 127, 0)
darker_chartreuse = tcod.Color(63, 127, 0)
darker_green = tcod.Color(0, 127, 0)
darker_sea = tcod.Color(0, 127, 63)
darker_turquoise = tcod.Color(0, 127, 95)
darker_cyan = tcod.Color(0, 127, 127)
darker_sky = tcod.Color(0, 95, 127)
darker_azure = tcod.Color(0, 63, 127)
darker_blue = tcod.Color(0, 0, 127)
darker_han = tcod.Color(31, 0, 127)
darker_violet = tcod.Color(63, 0, 127)
darker_purple = tcod.Color(95, 0, 127)
darker_fuchsia = tcod.Color(127, 0, 127)
darker_magenta = tcod.Color(127, 0, 95)
darker_pink = tcod.Color(127, 0, 63)
darker_crimson = tcod.Color(127, 0, 31)

# darkest s
darkest_red = tcod.Color(63, 0, 0)
darkest_flame = tcod.Color(63, 15, 0)
darkest_orange = tcod.Color(63, 31, 0)
darkest_amber = tcod.Color(63, 47, 0)
darkest_yellow = tcod.Color(63, 63, 0)
darkest_lime = tcod.Color(47, 63, 0)
darkest_chartreuse = tcod.Color(31, 63, 0)
darkest_green = tcod.Color(0, 63, 0)
darkest_sea = tcod.Color(0, 63, 31)
darkest_turquoise = tcod.Color(0, 63, 47)
darkest_cyan = tcod.Color(0, 63, 63)
darkest_sky = tcod.Color(0, 47, 63)
darkest_azure = tcod.Color(0, 31, 63)
darkest_blue = tcod.Color(0, 0, 63)
darkest_han = tcod.Color(15, 0, 63)
darkest_violet = tcod.Color(31, 0, 63)
darkest_purple = tcod.Color(47, 0, 63)
darkest_fuchsia = tcod.Color(63, 0, 63)
darkest_magenta = tcod.Color(63, 0, 47)
darkest_pink = tcod.Color(63, 0, 31)
darkest_crimson = tcod.Color(63, 0, 15)

# light s
light_red = tcod.Color(255, 114, 114)
light_flame = tcod.Color(255, 149, 114)
light_orange = tcod.Color(255, 184, 114)
light_amber = tcod.Color(255, 219, 114)
light_yellow = tcod.Color(255, 255, 114)
light_lime = tcod.Color(219, 255, 114)
light_chartreuse = tcod.Color(184, 255, 114)
light_green = tcod.Color(114, 255, 114)
light_sea = tcod.Color(114, 255, 184)
light_turquoise = tcod.Color(114, 255, 219)
light_cyan = tcod.Color(114, 255, 255)
light_sky = tcod.Color(114, 219, 255)
light_azure = tcod.Color(114, 184, 255)
light_blue = tcod.Color(114, 114, 255)
light_han = tcod.Color(149, 114, 255)
light_violet = tcod.Color(184, 114, 255)
light_purple = tcod.Color(219, 114, 255)
light_fuchsia = tcod.Color(255, 114, 255)
light_magenta = tcod.Color(255, 114, 219)
light_pink = tcod.Color(255, 114, 184)
light_crimson = tcod.Color(255, 114, 149)

# lighter s
lighter_red = tcod.Color(255, 165, 165)
lighter_flame = tcod.Color(255, 188, 165)
lighter_orange = tcod.Color(255, 210, 165)
lighter_amber = tcod.Color(255, 232, 165)
lighter_yellow = tcod.Color(255, 255, 165)
lighter_lime = tcod.Color(232, 255, 165)
lighter_chartreuse = tcod.Color(210, 255, 165)
lighter_green = tcod.Color(165, 255, 165)
lighter_sea = tcod.Color(165, 255, 210)
lighter_turquoise = tcod.Color(165, 255, 232)
lighter_cyan = tcod.Color(165, 255, 255)
lighter_sky = tcod.Color(165, 232, 255)
lighter_azure = tcod.Color(165, 210, 255)
lighter_blue = tcod.Color(165, 165, 255)
lighter_han = tcod.Color(188, 165, 255)
lighter_violet = tcod.Color(210, 165, 255)
lighter_purple = tcod.Color(232, 165, 255)
lighter_fuchsia = tcod.Color(255, 165, 255)
lighter_magenta = tcod.Color(255, 165, 232)
lighter_pink = tcod.Color(255, 165, 210)
lighter_crimson = tcod.Color(255, 165, 188)

# lightest s
lightest_red = tcod.Color(255, 191, 191)
lightest_flame = tcod.Color(255, 207, 191)
lightest_orange = tcod.Color(255, 223, 191)
lightest_amber = tcod.Color(255, 239, 191)
lightest_yellow = tcod.Color(255, 255, 191)
lightest_lime = tcod.Color(239, 255, 191)
lightest_chartreuse = tcod.Color(223, 255, 191)
lightest_green = tcod.Color(191, 255, 191)
lightest_sea = tcod.Color(191, 255, 223)
lightest_turquoise = tcod.Color(191, 255, 239)
lightest_cyan = tcod.Color(191, 255, 255)
lightest_sky = tcod.Color(191, 239, 255)
lightest_azure = tcod.Color(191, 223, 255)
lightest_blue = tcod.Color(191, 191, 255)
lightest_han = tcod.Color(207, 191, 255)
lightest_violet = tcod.Color(223, 191, 255)
lightest_purple = tcod.Color(239, 191, 255)
lightest_fuchsia = tcod.Color(255, 191, 255)
lightest_magenta = tcod.Color(255, 191, 239)
lightest_pink = tcod.Color(255, 191, 223)
lightest_crimson = tcod.Color(255, 191, 207)

# desaturated s
desaturated_red = tcod.Color(127, 63, 63)
desaturated_flame = tcod.Color(127, 79, 63)
desaturated_orange = tcod.Color(127, 95, 63)
desaturated_amber = tcod.Color(127, 111, 63)
desaturated_yellow = tcod.Color(127, 127, 63)
desaturated_lime = tcod.Color(111, 127, 63)
desaturated_chartreuse = tcod.Color(95, 127, 63)
desaturated_green = tcod.Color(63, 127, 63)
desaturated_sea = tcod.Color(63, 127, 95)
desaturated_turquoise = tcod.Color(63, 127, 111)
desaturated_cyan = tcod.Color(63, 127, 127)
desaturated_sky = tcod.Color(63, 111, 127)
desaturated_azure = tcod.Color(63, 95, 127)
desaturated_blue = tcod.Color(63, 63, 127)
desaturated_han = tcod.Color(79, 63, 127)
desaturated_violet = tcod.Color(95, 63, 127)
desaturated_purple = tcod.Color(111, 63, 127)
desaturated_fuchsia = tcod.Color(127, 63, 127)
desaturated_magenta = tcod.Color(127, 63, 111)
desaturated_pink = tcod.Color(127, 63, 95)
desaturated_crimson = tcod.Color(127, 63, 79)

# metallic
brass = tcod.Color(191, 151, 96)
copper = tcod.Color(197, 136, 124)
gold = tcod.Color(229, 191, 0)
silver = tcod.Color(203, 203, 203)

# miscellaneous
celadon = tcod.Color(172, 255, 175)
peach = tcod.Color(255, 159, 127)
