from abilities.skills import SkillUsage, SkillConditions

skills_data = {
    'skill_charge_roach' : {
            'name': 'Charge Activation (Roach)',
            'activate_condition': SkillConditions.skill_charge_condition,
            'activate_condition_kwargs': {'min': 2, 'max': 6},
            'on_activate': SkillUsage.skill_charge_prepare,
            'on_activate_kwargs': {'distance': 5, 'delay':1},
            'cooldown_length': 6
        }
}