from config_files import colors

atkdmg_string_data = {
    'verbs': ('inflicting', 'causing', 'resulting in'),
    90: ('brutal', 'devastating'),
    65: ('severe', 'incredible'),
    45: ('heavy', 'strong'),
    25: ('moderate', 'average'),
    5: ('light', 'weak'),
    1: ('barely any', 'hardly any', 'trivial')
}

sta_color_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: colors.light_sea,
    60: colors.sea,
    30: colors.dark_sea,
    15: colors.darker_sea,
    1: colors.darkest_sea
}

stadmg_string_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: ('extreme', 'giant'),
    65: ('crass', 'heavy'),
    45: ('significant', 'unusual'),
    25: ('moderate', 'average'),
    5: ('light', 'low'),
    1: ('barely any', 'hardly any')
}

stadmg_color_data = {
    #'verbs': ('taking', 'exhausting', 'sapping'),
    90: sta_color_data[1],
    65: sta_color_data[15],
    30: sta_color_data[30],
    25: sta_color_data[60],
    5: colors.light_sea,
    1: sta_color_data[90]
}