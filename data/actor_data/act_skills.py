from abilities.skills import SkillUsage, SkillCondition

skills_data = {
    'skill_charge' : {
            'name': 'Charge Activation',
            'activate_condition': SkillCondition.distance_to,
            'activate_condition_kwargs': {'min_dist': 2, 'max_dist': 6},
            'on_activate': SkillUsage.charge_prepare,
            'on_activate_kwargs': {'delay':1},
            'cooldown_length': 6
        },
    'skill_prime_expl' : {
            'name': 'Prime Detonation',
            'activate_condition': SkillCondition.distance_to,
            'activate_condition_kwargs': {'min': 2, 'max': 6},
            'on_activate': SkillUsage.charge_prepare,
            'on_activate_kwargs': {'delay':1},
            'cooldown_length': 6
        },

}