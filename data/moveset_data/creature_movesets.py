from data.data_enums import Key, Mod

moveset_mandibles = {
    Key.DEFAULT: {
        Key.RANDOM: True,
        Key.VERBS: ('bite', 'gnaw at'),
    },
    1: {},
    2: {},
    3: {
        Key.VERB: 'nibble off',
        Mod.DMG_MULTIPL: 0.6
    },
    4: {
        Key.VERB: 'pierce',
        Mod.AV_MULTIPL: 0,
    }
}

moveset_mandibles_heavy = {
    **moveset_mandibles,
    Key.DEFAULT: {
        Key.RANDOM: True,
        Key.VERBS: ('bite', 'gnaw at'),
        Mod.BLOCK_STA_DMG_MULTIPL: 2
    },
}

moveset_claws = {
    Key.DEFAULT: {
        Key.VERBS: ('lash', 'claw', 'rip','rend'),
    },
    1: {},
}

moveset_claws_heavy = {
    **moveset_claws,
    1: {
        Mod.BLOCK_STA_DMG_MULTIPL: 2
    }
}

moveset_spit = {
    Key.DEFAULT: {
        Key.RANDOM: True,
        Key.VERBS: ('spit at', 'discharge at'),
    },
    1: {},
    2: {},
    3: {
        Mod.ARMOR_PIERCING_FLAT : 2,
        Key.VERB: 'corrode'
    },
}