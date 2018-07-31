from config_files import colors

WP_CHAR = '\\'
WP_COLOR = colors.turquoise
WP_EQUIP = 'arms'  # which extremity the item is equipped to
WP_TYPE = 'weapon'  # which slot it will take

wp_swords_data = {
    'sword_rusty': {
        'name': 'Rusty Sword',
        'descr': 'You are not sure if this sword has seen better days, or if time simply has caught up to shoddy craftsmanship.',
        'chance': 100,
        'dlvls': range(1,99),
        "char": WP_CHAR,
        "color": WP_COLOR,
        'e_to': WP_EQUIP,
        'e_type': WP_TYPE,
        'dmg_range': (2, 5)
    }
}
