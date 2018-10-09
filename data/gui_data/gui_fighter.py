from components.actors.fighter_util import DamagePercentage, AttributePercentage
from config_files import colors

# HEALTH #
hp_string_data = {
    AttributePercentage.FULL : 'healthy',
    AttributePercentage.THREE_QUARTER : 'scratched',
    AttributePercentage.HALF : 'wounded',
    AttributePercentage.ONE_QUARTER : 'banged up',
    AttributePercentage.VERY_LOW : 'near death',
    AttributePercentage.EMPTY : 'dead'
}

hp_color_data = {
    AttributePercentage.FULL : colors.dark_green,#colors.green,
    AttributePercentage.THREE_QUARTER : colors.dark_chartreuse,
    AttributePercentage.HALF : colors.darker_red,
    AttributePercentage.ONE_QUARTER : colors.dark_red,
    AttributePercentage.VERY_LOW : colors.red,
    AttributePercentage.EMPTY : colors.red
}

hpdmg_string_data = {
    'verbs': ('inflicting', 'causing', 'doing'),
    DamagePercentage.VERY_HIGH: ('brutal', 'devastating'),
    DamagePercentage.HIGH: ('severe', 'heavy'),
    DamagePercentage.MODERATE: ('moderate', 'average'),
    DamagePercentage.LIGHT: ('light', 'weak'),
    DamagePercentage.VERY_LIGHT: ('minimal', 'miniscule', 'trivial'),
    DamagePercentage.NONE: ('no',)
}

hpdmg_color_data = {
    DamagePercentage.VERY_HIGH: hp_color_data[AttributePercentage.VERY_LOW],
    DamagePercentage.HIGH: hp_color_data[AttributePercentage.ONE_QUARTER],
    DamagePercentage.MODERATE: hp_color_data[AttributePercentage.HALF],
    DamagePercentage.LIGHT: hp_color_data[AttributePercentage.THREE_QUARTER],
    DamagePercentage.VERY_LIGHT: hp_color_data[AttributePercentage.THREE_QUARTER],
    DamagePercentage.NONE: hp_color_data[AttributePercentage.FULL]
}

# STAMINA #
sta_string_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    AttributePercentage.FULL : 'fit',
    AttributePercentage.THREE_QUARTER : 'active',
    AttributePercentage.HALF : 'strained',
    AttributePercentage.ONE_QUARTER : 'spent',
    AttributePercentage.VERY_LOW : 'exhausted',
    AttributePercentage.EMPTY : 'empty'
}

sta_color_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    AttributePercentage.FULL : colors.dark_sea,
    AttributePercentage.THREE_QUARTER : colors.darker_sea,
    AttributePercentage.HALF : colors.darker_cyan,
    AttributePercentage.ONE_QUARTER : colors.darkest_sea,
    AttributePercentage.VERY_LOW : colors.darkest_cyan,
    AttributePercentage.EMPTY : colors.darkest_cyan
}

stadmg_string_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    DamagePercentage.VERY_HIGH: ('extreme', 'massive'),
    DamagePercentage.HIGH: ('crass', 'heavy'),
    DamagePercentage.MODERATE: ('moderate', 'average'),
    DamagePercentage.LIGHT: ('light', 'low'),
    DamagePercentage.VERY_LIGHT: ('minimal', 'trivial'),
    DamagePercentage.NONE: ('no',)
}

stadmg_color_data = {
    DamagePercentage.VERY_HIGH: sta_color_data[AttributePercentage.VERY_LOW],
    DamagePercentage.HIGH: sta_color_data[AttributePercentage.ONE_QUARTER],
    DamagePercentage.MODERATE: sta_color_data[AttributePercentage.HALF],
    DamagePercentage.LIGHT: sta_color_data[AttributePercentage.THREE_QUARTER],
    DamagePercentage.VERY_LIGHT: sta_color_data[AttributePercentage.THREE_QUARTER],
    DamagePercentage.NONE: sta_color_data[AttributePercentage.FULL]
}