moveset_sword = {
    1: {
        'descr': 'A swing from right to left, doing full damage.',
        'string': 'swings at',
    },
    2: {
        'descr': 'A slightly weaker slash from the down left.',
        'string': 'slashes',
        'dmg_mod': 0.8
    },
    3: {
        'descr': 'A forceful stab towards the enemies center.',
        'string': 'stabs',
        'dmg_mod': 1.25
    }
}

moveset_spear = {
    1: {
        'descr': 'A weak stab to prepare for further attacks.',
        'string': 'pokes',
        'dmg_mod': 0.75
    },
    2: {
        'descr': 'An accurate thrust, using the weapon\'s full potential.',
        'string': 'accurately thrusts at'
    },
    3: {
        'descr': 'A powerful thrust, piercing the target and potentially hitting someone behind it.',
        'string': 'forcefully thrusts through',
        'dmg_mod': 1.25,
        'extra_hits': {'target_behind': True}
    }
}