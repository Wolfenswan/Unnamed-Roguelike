from random import randint, choice

from gameobjects.entity import Entity

from components.combat.fighter_util import State
from gui.messages import Message, MessageCategory, MessageType
from rendering.render_animations import animate_projectile, animate_explosion


class Effect:
    """
    Effect-Class serves as a container for static methods.
    All Effect.-methods are result of player or npc interaction with the world either through skill or item usage.
    """

    @staticmethod
    def direct_damage(target = None, string='attack', ignore_def=False, **kwargs):
        # NOTE: Does currently not take any defenses into account.
        amount = randint(*kwargs.get('pwr'))
        if target is None:
            target = kwargs.get('user')

        results = []

        results.append({'message': Message(
            f'The {string} causes %{target.f.hpdmg_color(amount)}%{target.f.hpdmg_string(amount)}%% damage to {target.address}!',
            category=MessageCategory.COMBAT, type=MessageType.COMBAT_INFO)})
        results.extend(target.f.take_damage(amount))

        return results

    @staticmethod
    def direct_heal(**kwargs):
        target = kwargs.get('target')
        if target is None:
            target = kwargs.get('user')
        percentage = kwargs.get('percentage', False)
        if not percentage:
            amount = randint(*kwargs.get('pwr'))
        else:
            amount = target.f.max_hp/100 * randint(*kwargs.get('pwr'))

        if target is None:
            target = kwargs.get('user')

        results = []

        if not target.f.hp_full:
            results.append({'message': Message(
                f'{target.name} heals for {target.f.hpdmg_string(amount)} effect!',
                category=MessageCategory.OBSERVATION, type=MessageType.COMBAT_INFO)})
            target.f.heal(amount)
        else:
            results.append({'message': Message(f'{target.pronoun.title()} {target.state_verb_past} already at full health.')})

        return results

    @staticmethod
    def damage_by_radius(entity, string, **kwargs):
        # modify damage by radius, then apply
        pass

    @staticmethod
    def projectile(**kwargs):
        game = kwargs['game']
        user = kwargs['user']
        target_pos = kwargs.get('target_pos')
        on_hit = kwargs.get('on_proj_hit')
        # effect_name = kwargs.get('effect_name', 'projectile')
        # effect_verb = kwargs.get('effect_verb', 'hits')
        projectile = kwargs.get('projectile','*')
        color = kwargs['used_item'].color

        results = []

        animate_projectile(*user.pos, *target_pos, game, char=projectile,color=color)  # TODO add color switch

        kwargs['target'] = next((ent for ent in game.fighter_ents if ent.pos == target_pos), None)
        results.extend(on_hit(**kwargs))

        return results

    @staticmethod
    def explosion(**kwargs):
        game = kwargs['game']
        center = kwargs.get('target_pos')
        radius = kwargs.get('radius',3)
        on_hit = kwargs.get('on_expl_hit', Effect.direct_damage)
        effect_name = kwargs.get('effect_name', 'explosion')
        effect_verb = choice(kwargs.get('effect_verbs', ['burns', 'scorches']))

        entities = [ent for ent in game.alive_ents if ent.distance_to_pos(*center) <= radius]
        results = []

        animate_explosion(*center, game, radius)  # TODO add color switch

        results.append({'message': Message(f'The {effect_name} {effect_verb} everything within {radius} tiles!')})

        for entity in entities:
            kwargs['target'] = entity
            kwargs['string'] = effect_name
            if on_hit is not None:
                results.extend(on_hit(**kwargs)) # TODO damage_by_radius with damage falloff by distance from center

        return results


    @staticmethod
    def chained_explosion(**kwargs): # Just a Proof of Concept atm
        chain = 2
        results = []

        for i in range(chain):
            results.extend(Effect.explosion(**kwargs))

        return results

    @staticmethod
    def entangle(**kwargs):
        target = kwargs.get('target')
        duration = randint(*kwargs.get('pwr',(0,0)))

        if target is not None and target.f is not None:
            results = target.f.set_effect(State.ENTANGLED, True, duration, msg=True)
            return results

        return []