from data.data_keys import Key

moveset_mandibles = {
    Key.DEFAULT: {
        Key.RANDOM: True,
        Key.VERBS: ('bites', 'gnaws at'),
    },
    1: {},
    2: {},
    3: {
        Key.VERB: 'nibbles at',
        Key.DMG_MULTIPL: 0.6
    },
    4: {
        Key.VERB: 'pierces',
        Key.AV_MULTIPL: 0,
    }
}
moveset_claws = {
    Key.DEFAULT: {
        Key.VERBS: ('lashes', 'claws', 'rips','rends'),
    },
    1: {},
}
moveset_spit = {
    Key.DEFAULT: {
        Key.VERBS: ('spits at', 'discharges saliva at'),
    },
    1: {}
}