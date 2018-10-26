from components.effects import Effect

"""
These dictionaries serve as reference to apply effects to useable items or skills.
"""

# TODO Key Enum
heal = {
        'effect_name': 'heal',
        'on_execution': Effect.direct_heal
}


heal_targeted = {
        **heal,
        'targeted': True,
        'on_execution': Effect.projectile,
        'on_proj_hit': Effect.direct_heal
}


dmg_targeted = {
        'targeted' : True,
        'effect_name': 'projectile',
        'on_execution': Effect.projectile,
        'on_proj_hit': Effect.direct_damage
}


explosion = {
        'effect_name': 'explosion',
        'effect_verb': 'burns',
        'on_execution': Effect.explosion,
        'on_expl_hit': Effect.direct_damage
}


explosion_targeted = {
        **explosion,
        'targeted' : True,
        'on_execution': Effect.projectile,
        'on_proj_hit': Effect.explosion
}