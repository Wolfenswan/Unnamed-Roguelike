from data.data_enums import Key, Mod
from map.directions_util import RelativeDirection

col1 = '%dark_orange%'

moveset_sword = {
    1: {
       Key.DESCR: f'A {col1}swing%% from right to left, doing full damage.',
        Key.VERB: 'strike',
    },
    2: {
       Key.DESCR: f'A slightly {col1}weaker slash%% from the down left.',
        Key.VERB: 'slash',
        Mod.DMG_MULTIPL: 0.8,
        Mod.EXERT_MULTIPL: 0.8,
    },
    3: {
       Key.DESCR: f'A {col1}forceful thrust%% towards the enemies center.',
        Key.VERB: 'thrust at',
        Mod.DMG_MULTIPL: 1.25,
        Mod.EXERT_MULTIPL: 1.25,
    }
}
moveset_dagger = {
    1: {
        Key.DESCR: f'A {col1}quick stab%%, unnerving ones opponent.',
        Key.VERB: 'stab',
        Mod.DMG_MULTIPL: 0.85,
    },
    2: {
        Key.DESCR: f'A {col1}followup stab%% circumventing enemy armor.',
        Key.VERB: 'stab',
        Mod.DMG_MULTIPL: 0.8,
        Mod.ARMOR_PIERCING_FLAT: 1
    },
    3: {
        Key.DESCR: f'Another {col1}quick stab%%.',
        Key.VERB: 'stab',
        Mod.DMG_MULTIPL: 0.85,
    },
    4: {
        Key.DESCR: f'A {col1}deadly piercing strike%%.',
        Key.VERB: 'pierce',
        Mod.DMG_MULTIPL: 2,
        Mod.ARMOR_PIERCING_FLAT: 5
    },
}
moveset_spear = {
    1: {
       Key.DESCR: f'A {col1}weak stab%%, preparing further attacks.',
        Key.VERB: 'poke',
        Mod.DMG_MULTIPL: 0.75,
        Mod.EXERT_MULTIPL: 0.75,
    },
    2: {
       Key.DESCR: f"A {col1}standard thrust%%, utilizing the weapon's full potential.",
        Key.VERB: 'thrust at'
    },
    3: {
       Key.DESCR: f'A {col1}powerful thrust%%, piercing the target and possibly hitting something behind it.',
        Key.VERB: 'impale',
        Mod.DMG_MULTIPL: 1.25,
        Mod.EXERT_MULTIPL: 1.25,
        Key.EXTEND_ATTACK: [RelativeDirection.BEHIND]
    }
}
moveset_flail = {
Key.DEFAULT: {Key.VERBS: ('flail',),},
    1: {
       Key.DESCR: f'A {col1}weaker over-head swing%%, to get momentum.',
        Mod.DMG_MULTIPL: 0.5,
        Key.EXTEND_ATTACK: [RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    2: {
       Key.DESCR: f'A {col1}slightly stronger swing%%, speeding up the weapon.',
        Mod.DMG_MULTIPL: 0.85,
        Key.EXTEND_ATTACK: [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    3: {
        Key.DESCR: f"A {col1}standard swing%%, using the weapon's full potential.",
        Mod.DMG_MULTIPL: 1,
        Key.EXTEND_ATTACK: [RelativeDirection.RIGHT, RelativeDirection.LEFT, RelativeDirection.LEFT_BACK]
    },
    4: {
       Key.DESCR: f"A final {col1}overhead crush%% on a single head, ignoring shields.",
        Key.VERB: 'crush',
        Mod.DMG_MULTIPL: 1.25,
        Mod.EXERT_MULTIPL: 1.25,
        Mod.BLOCK_DEF_MULTIPL: 0,
    }
}
moveset_bow = {
    Key.DEFAULT: {Key.VERBS: ('shoot',),},
    1: {
       Key.DESCR: f"A quick but {col1}weaker draw%% to gauge the distance to the target.",
       Mod.DMG_MULTIPL: 0.5
    },
    2: {
       Key.DESCR: f"A {col1}standard draw%%, likely hitting the torso.",
    },
    3: {
       Key.DESCR: f"A followup, {col1}average shot%%, to prepare for the final target.",
    },
    4: {
       Key.DESCR: f"A {col1}devastating head shot%%, aimed right between the eyes.",
        Mod.DMG_MULTIPL: 2
    },
}