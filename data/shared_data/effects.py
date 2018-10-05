from abilities.effects import AbilityEffect

"""
These dictionaries serve as reference to apply effects to useable items or skills.
"""

heal = {
        'effect_name': 'heal',
        'on_execution': AbilityEffect.direct_heal
}


heal_targeted = {
        **heal,
        'targeted': True,
        'on_execution': AbilityEffect.projectile,
        'on_impact': AbilityEffect.direct_heal
}


dmg_targeted = {
        'targeted' : True,
        'effect_name': 'projectile',
        'on_execution': AbilityEffect.projectile,
        'on_impact': AbilityEffect.direct_damage
}


explosion = {
        'effect_name': 'explosion',
        'effect_verb': 'burns',
        'on_execution': AbilityEffect.explosion,
}


explosion_targeted = {
        **explosion,
        'targeted' : True,
        'on_execution': AbilityEffect.projectile,
        'on_impact': AbilityEffect.explosion
}