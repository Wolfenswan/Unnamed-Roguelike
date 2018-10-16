from components.skills.skillConditions import SkillCondition
from components.effects import Effect
from components.skills.skills import SkillCharge, SkillSlam

"""
Each dictionary refers to a skill class and contains the parameters to customize the instance of each skill accordingly.
"""

skill_generic_charge = {
        'skill' : SkillCharge,
        'name': 'Charge',
        'activate_condition_kwargs': {'min_dist': 2, 'max_dist': 6},
        'on_activate_kwargs': {'delay':1},
        'cooldown_length': 6
    }

skill_quick_charge = {
        **skill_generic_charge,
        'cooldown_length': 3
    }

skill_generic_slam = {
    'skill' : SkillSlam,
    'name': 'Slam',
    'activate_condition_kwargs': {'min_dist': 1, 'max_dist': 1.5},
    'on_activate_kwargs': {'delay':1},
    'cooldown_length': 4
}

skill_prime = {
        'skill': SkillExplode,
        'activate_condition_kwargs': {'min_dist': 1, 'max_dist': 5},
        'on_activate': Effect.explosion,
        'on_activate_kwargs': {'delay':1},
        'cooldown_length': 6
}