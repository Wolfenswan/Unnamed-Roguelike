from abilities.conditions import AbilityCondition
from abilities.effects import AbilityEffect
from abilities.usage import AbilityUse

skills_data = {
    'skill_charge' : {
            'name': 'Charge Activation',
            'activate_condition': AbilityCondition.distance_to,
            'activate_condition_kwargs': {'min_dist': 2, 'max_dist': 6},
            'on_activate': AbilityUse.charge_prepare,
            'on_activate_kwargs': {'delay':1},
            'cooldown_length': 6
        },
    'skill_prime_expl' : {
            'name': 'Prime Detonation',
            'activate_condition': AbilityCondition.distance_to,
            'activate_condition_kwargs': {'min': 2, 'max': 6},
            'on_activate': AbilityEffect.explosion,
            'on_activate_kwargs': {'delay':1},
            'cooldown_length': 6
        },

}