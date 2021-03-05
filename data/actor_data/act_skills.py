from components.combat.fighter_util import State
from components.effects import Effect
from components.skills.skillConditions import SkillCondition
from components.skills.skills import SkillCharge, SkillSlam, SkillExplodeSelf, SkillEntangle, SkillHatch
from data.data_enums import Key

"""
Each dictionary refers to a skill class and contains the parameters to customize the instance of each skill accordingly.
"""

skill_generic_charge = {
        Key.SKILL : SkillCharge,
        Key.NAME: 'Charge',
        Key.ACTIVATE_CONDITIONS : {SkillCondition.distance_to, SkillCondition.free_line_to_target},
        Key.ACTIVATE_CONDITION_KWARGS: {'min_dist': 2, 'max_dist': 5, 'ignore_ents' : True},
        Key.ON_ACTIVATE_KWARGS: {'delay':1},
        Key.COOLDOWN_LENGTH: (5,6)
    }

skill_quick_charge = {
        **skill_generic_charge,
        Key.COOLDOWN_LENGTH: (3,3)
    }

skill_generic_slam = {
    Key.SKILL : SkillSlam,
    Key.NAME: 'Slam',
    Key.ACTIVATE_CONDITIONS : {SkillCondition.distance_to},
    Key.ACTIVATE_CONDITION_KWARGS: {'min_dist': 1, 'max_dist': 1.5},
    Key.ON_ACTIVATE_KWARGS: {'delay':1},
    Key.COOLDOWN_LENGTH: (3,4)
}

skill_explode_self = {
    Key.SKILL: SkillExplodeSelf,
    Key.NAME : 'Explode',
    Key.ACTIVATE_CONDITIONS : {SkillCondition.distance_to},
    Key.ACTIVATE_CONDITION_KWARGS: {'min_dist': 1, 'max_dist': 5},
    Key.ON_ACTIVATE_KWARGS: {'delay_min':3, 'delay_max':5, 'radius':4, 'pwr':(20,30)},
    Key.COOLDOWN_LENGTH: (10,10)
}

skill_entangle = {
    Key.SKILL : SkillEntangle,
    Key.NAME : 'Entangle',
    Key.ACTIVATE_CONDITIONS : {SkillCondition.distance_to, SkillCondition.target_state},
    Key.ACTIVATE_CONDITION_KWARGS: {'min_dist': 1, 'max_dist': 1.5,'state': State.ENTANGLED, 'state_condition': False},
    Key.ON_ACTIVATE_KWARGS: {'delay':0},
    Key.COOLDOWN_LENGTH: (4,6)
}

skill_entangle_timed = {
    **skill_entangle,
    Key.ON_ACTIVATE_KWARGS: {'delay': 0, 'duration': 5},
    Key.COOLDOWN_LENGTH: (6,8)
    }

skill_hatch = {
    Key.SKILL: SkillHatch,
    Key.NAME : 'Hatch',
    Key.ACTIVATE_CONDITIONS : {SkillCondition.distance_to,},
    Key.ACTIVATE_CONDITION_KWARGS: {'min_dist': 0, 'max_dist': 8,},
    Key.ON_ACTIVATE_KWARGS: {'delay_min':1,'delay_max':3},
    Key.COOLDOWN_LENGTH: (1,2)
}