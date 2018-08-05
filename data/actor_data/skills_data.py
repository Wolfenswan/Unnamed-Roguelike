from components.skills import skill_charge_condition, skill_always_true, Skill

skills_data = {
    'skill_orc_charge_act' : {
        'name': 'Orc Charge Activation',
        'activate_condition': skill_charge_condition,
        'activate_condition_kwargs': {'min': 2, 'max': 6},
        'on_activate': Skill.skill_charge_activation,
        'on_activate_kwargs': {'distance': 5, 'delay':1},
        'cooldown_length': 6,
        'messages': ('The Orc prepares to charge!',)
        },
    'skill_orc_charge_exec' : {
        'name': 'Orc Charge Execution',
        'on_activate': Skill.skill_charge_execution,
        'activate_condition': skill_always_true,
        'cooldown_length': -1,
        'messages': ('The Orc charges forward!',)
        }
}