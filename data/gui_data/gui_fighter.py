from config_files import colors

# HEALTH #
hp_string_data = {
    90: 'healthy',
    60: 'scratched',
    30: 'wounded',
    1: 'near death',
    0: 'dead'
}

hp_color_data = {
    90: colors.dark_green,
    60: colors.darker_green,
    30: colors.dark_red,
    1: colors.darker_red,
    0: colors.darkest_red
}

hpdmg_string_data = {
    'verbs': ('inflicting', 'causing', 'doing'),
    90: ('brutal', 'devastating'),
    60: ('severe', 'incredible'),
    40: ('heavy', 'strong'),
    20: ('moderate', 'average'),
    5: ('light', 'weak'),
    1: ('minimal', 'miniscule', 'trivial')
}

hpdmg_color_data = {
    90: colors.red,
    60: hp_color_data[1],
    40: hp_color_data[30],
    20: hp_color_data[30],
    5: hp_color_data[60],
    1: hp_color_data[90]
}

# STAMINA #
sta_string_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: 'fit',
    60: 'active',
    40: 'strained',
    20: 'spent',
    0: 'exhausted'
}

sta_color_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: colors.light_sea,
    60: colors.sea,
    40: colors.dark_sea,
    20: colors.darker_sea,
    0: colors.darkest_sea
}

stadmg_string_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: ('extreme', 'giant'),
    60: ('crass', 'heavy'),
    40: ('significant', 'unusual'),
    20: ('moderate', 'average'),
    5: ('light', 'low'),
    1: ('minimal', 'miniscule', 'trivial')
}

stadmg_color_data = {
    90: sta_color_data[0],
    60: sta_color_data[20],
    40: sta_color_data[40],
    20: sta_color_data[60],
    5: colors.light_sea,
    1: sta_color_data[90]
}