from components.effects import Effect

"""
These dictionaries serve as reference to apply effects to useable items or skills.
"""

# TODO Key Enum
generic_projectile = {
        'targeted': True,
        'on_execution': Effect.projectile,
}

heal_self = {
        'effect_name': 'heal',
        'on_execution': Effect.direct_heal
}


heal_targeted = {
        **heal_self,
        **generic_projectile,
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
        'effect_verbs': ['burns', 'scorches'],
        'on_execution': Effect.explosion,
        'on_expl_hit': Effect.direct_damage
}


explosion_targeted = {
        **explosion,
        **generic_projectile,
        'on_proj_hit': Effect.explosion
}

incendiary_targeted = {
        **explosion,
        **generic_projectile,
        'on_proj_hit': Effect.explosion
        # 'on_proj_hit': Effect.explosion_incendiary
}

entangle = {
        'effect_name' : 'entangle',
        'effect_verbs': ['entangles','wraps'],
        'on_execution': Effect.entangle,
}


entangle_targeted = {
        **entangle,
        **generic_projectile,
        'on_proj_hit': Effect.entangle,
}