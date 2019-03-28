from components.actors.fighter_util import Effect, Surrounded

status_modifiers_data = {
    Effect.DAZED: {
        'av_multipl' : 0.75,
        'dmg_multipl': 0.75,
        'skip_turn_chance': 15
    },
    Effect.STUNNED: {
        'av_multipl' : 0.5,
        'dmg_multipl' : 0,
        'skip_turn_chance': 100,
        'can_attack': False
    },

    Surrounded.THREATENED: {
        'av_multipl': 0.8
    },
    Surrounded.OVERWHELMED: {
        'av_multipl': 0.1
    }
}