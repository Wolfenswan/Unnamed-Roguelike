from data.data_types import AttackType
from map.directions_util import RelativeDirection

col1 = '%dark_orange%'

moveset_sword = {
    1: {
        'descr': f'A {col1}swing%% from right to left, doing full damage.',
        'verb': 'swings at',
    },
    2: {
        'descr': f'A slightly {col1}weaker slash%% from the down left.',
        'verb': 'slashes',
        'dmg_multipl': 0.8
    },
    3: {
        'descr': f'A {col1}forceful stab%% towards the enemies center.',
        'verb': 'stabs',
        'dmg_multipl': 1.25
    }
}

moveset_spear = {
    1: {
        'descr': f'A {col1}weak stab%% to prepare for further attacks.',
        'verb': 'pokes',
        'dmg_multipl': 0.75
    },
    2: {
        'descr': f"An {col1}standard thrust%%, using the weapon's full potential.",
        'verb': 'thrusts at'
    },
    3: {
        'descr': f'A {col1}powerful thrust%%, piercing the target and hitting something behind it.',
        'verb': 'forcefully thrusts through',
        'dmg_multipl': 1.25,
        'extend_attack': [RelativeDirection.BEHIND]
    }
}

moveset_flail = {
    'verbs': ('flails',),
    1: {
        'descr': f'A {col1}weaker over-head swing%%, to get momentum.',
        'dmg_multipl': 0.5,
        'extend_attack': [RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    2: {
        'descr': f'A {col1}slightly stronger swing%%, speeding up the weapon.',
        'dmg_multipl': 0.85,
        'extend_attack': [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    3: {
        'descr': f"A {col1}standard swing%%, using the weapon's full potential.",
        'dmg_multipl': 1,
        'extend_attack': [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    4: {
        'descr': f"A final {col1}overhead crush%% on a single head, ignoring shields.",
        'verb': 'crushes',
        'dmg_multipl': 1.25,
        'attack': AttackType.QUICK,
    }
}

moveset_mandibles = {
    'random' : True,
    'verbs': ('bites', 'gnaws at'),
    1: {},
    2: {},
    3: {
        'verb': 'nibbles at',
        'dmg_multipl': 0.75
    }
}


moveset_claws = {
    'verbs': ('lashes', 'claws', 'rips'),
    1: {}
}