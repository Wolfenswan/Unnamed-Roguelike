from components.combat.fighter_util import State, Surrounded
from data.data_enums import Mod

status_modifiers_data = {
    State.DAZED: {
        Mod.AV_MULTIPL : 0.75,
        Mod.DMG_MULTIPL: 0.75,
        Mod.SKIP_TURN_CHANCE: 15
    },
    State.STUNNED: {
        Mod.AV_MULTIPL : 0.5,
        Mod.DMG_MULTIPL : 0,
        Mod.SKIP_TURN_CHANCE: 100,
        Mod.CAN_ATTACK: False,
        Mod.CAN_MOVE: False
    },
    State.ENTANGLED: {
        Mod.SKIP_TURN_CHANCE: 0,
        Mod.CAN_MOVE: False
    },
    State.IMMOBILE: {
        Mod.CAN_MOVE: False
    },

    Surrounded.FREE:{},
    Surrounded.THREATENED: {
        Mod.AV_MULTIPL : 0.7
    },
    Surrounded.OVERWHELMED: {
         Mod.AV_MULTIPL : 0.1
    }
}