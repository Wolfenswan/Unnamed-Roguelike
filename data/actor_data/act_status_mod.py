from components.combat.fighter_util import State, Surrounded

status_modifiers_data = {
    State.DAZED: {
        'av_multipl' : 0.75,
        'dmg_multipl': 0.75,
        'skip_turn_chance': 15
    },
    State.STUNNED: {
        'av_multipl' : 0.5,
        'dmg_multipl' : 0,
        'skip_turn_chance': 100,
        'can_attack': False,
        'can_move': False
    },
    State.ENTANGLED: {
        'skip_turn_chance': 0,
        'can_move': False
    },
    State.IMMOBILE: {
        'can_move': False
    },

    Surrounded.FREE:{

    },
    Surrounded.THREATENED: {
        'av_multipl': 0.8
    },
    Surrounded.OVERWHELMED: {
        'av_multipl': 0.1
    }
}