from components.skills import skill_charge_activation, skill_charge_condition, skill_charge_execution, skill_always_true

skills_data = {
    'skill_orc_charge_act' : {
        'name': 'Orc Charge Activation',
        'on_activate': skill_charge_activation,
        'on_activate_kwargs': {'distance': 5},
        'activate_condition': skill_charge_condition,
        'activate_condition_kwargs': {'min':2, 'max':6},
        'cooldown_length': 6,
        'messages': ('The Orc prepares to charge!',)
        },
    'skill_orc_charge_exec' : {
        'name': 'Orc Charge Execution',
        'on_activate': skill_charge_execution,
        'activate_condition': skill_always_true,
        'cooldown_length': -1,
        'messages': ('The Orc charges forward!',)
        }
}