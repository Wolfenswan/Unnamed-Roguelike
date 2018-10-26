from data.data_keys import Key
from data.data_types import AttackType
from map.directions_util import RelativeDirection

col1 = '%dark_orange%'

moveset_sword = {
    1: {
       Key.DESCR: f'A {col1}swing%% from right to left, doing full damage.',
        Key.VERB: 'swings at',
    },
    2: {
       Key.DESCR: f'A slightly {col1}weaker slash%% from the down left.',
        Key.VERB: 'slashes',
        Key.DMG_MULTIPL: 0.8
    },
    3: {
       Key.DESCR: f'A {col1}forceful stab%% towards the enemies center.',
        Key.VERB: 'stabs',
        Key.DMG_MULTIPL: 1.25
    }
}

moveset_spear = {
    1: {
       Key.DESCR: f'A {col1}weak stab%% to prepare for further attacks.',
        Key.VERB: 'pokes',
        Key.DMG_MULTIPL: 0.75
    },
    2: {
       Key.DESCR: f"An {col1}standard thrust%%, using the weapon's full potential.",
        Key.VERB: 'thrusts at'
    },
    3: {
       Key.DESCR: f'A {col1}powerful thrust%%, piercing the target and hitting something behind it.',
        Key.VERB: 'forcefully thrusts through',
        Key.DMG_MULTIPL: 1.25,
        Key.EXTEND_ATTACK: [RelativeDirection.BEHIND]
    }
}

moveset_flail = {
Key.DEFAULT: {Key.VERBS: ('flails',),},
    1: {
       Key.DESCR: f'A {col1}weaker over-head swing%%, to get momentum.',
        Key.DMG_MULTIPL: 0.5,
        Key.EXTEND_ATTACK: [RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    2: {
       Key.DESCR: f'A {col1}slightly stronger swing%%, speeding up the weapon.',
        Key.DMG_MULTIPL: 0.85,
        Key.EXTEND_ATTACK: [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    3: {
       Key.DESCR: f"A {col1}standard swing%%, using the weapon's full potential.",
        Key.DMG_MULTIPL: 1,
        Key.EXTEND_ATTACK: [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    4: {
       Key.DESCR: f"A final {col1}overhead crush%% on a single head, ignoring shields.",
        Key.VERB: 'crushes',
        Key.DMG_MULTIPL: 1.25,
        Key.ATTACKTYPE: AttackType.QUICK,
    }
}


moveset_bow = {
    Key.DEFAULT: {Key.VERBS: ('shoots',),},
    1: {
       Key.DESCR: f"A quick but {col1}weaker draw%% to gauge the distance to the target.",
        Key.DMG_MULTIPL: 0.5
    },
    2: {
       Key.DESCR: f"A {col1}standard draw%%, likely hitting the torso.",
    },
    3: {
       Key.DESCR: f"A followup, {col1}average shot%%, to prepare for the final target.",
    },
    4: {
       Key.DESCR: f"A {col1}devastating head shot%%, aimed right between the eyes.",
        Key.DMG_MULTIPL: 2
    },
}


moveset_mandibles = {
    Key.DEFAULT: {
        Key.RANDOM: True,
        Key.VERBS: ('bites', 'gnaws at'),
    },
    1: {},
    2: {},
    3: {
        Key.VERB: 'nibbles at',
        Key.DMG_MULTIPL: 0.75
    }
}


moveset_claws = {
    Key.DEFAULT: {
        Key.VERBS: ('lashes', 'claws', 'rips','rends'),
    },
    1: {}
}


moveset_spit = {
    Key.DEFAULT: {
        Key.VERBS: ('spits at', 'discharges saliva at'),
    },
    1: {}
}