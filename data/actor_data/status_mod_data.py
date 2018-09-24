from components.actors.status_modifiers import Presence

status_modifiers_data = {
    Presence.DAZED: {
        'av_multipl' : 0.75,
        'dmg_multipl': 0.75,
        'skip_turn_chance': 15
    },
    Presence.STUNNED: {
        'av_multipl' : 0.5,
        'dmg_multipl' : 0,
        'skip_turn_chance': 100,
        'can_attack': False
    }
}