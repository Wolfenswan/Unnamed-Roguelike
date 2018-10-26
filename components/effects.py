from random import randint

from gui.messages import Message, MessageCategory, MessageType
from rendering.render_animations import animate_projectile, animate_explosion


class Effect:

    @staticmethod
    def direct_damage(affected_ent = None, string='hit', **kwargs):
        # NOTE: Does currently not take any defenses into account.
        amount = randint(*kwargs.get('pwr'))
        if affected_ent is None:
            affected_ent = kwargs.get('user')

        results = []

        results.append({'message': Message(
            f'The {string} causes %{affected_ent.fighter.hpdmg_color(amount)}%{affected_ent.fighter.hpdmg_string(amount)}%% damage to {affected_ent.address}!',
            category=MessageCategory.COMBAT, type=MessageType.COMBAT_INFO)})
        results.extend(affected_ent.fighter.take_damage(amount))

        return results

    @staticmethod
    def direct_heal(affected_ent = None, **kwargs):
        amount = randint(*kwargs.get('pwr'))

        if affected_ent is None:
            affected_ent = kwargs.get('user')

        results = []

        if not affected_ent.fighter.hp_full:
            results.append({'message': Message(
                f'{affected_ent.name} heals for {affected_ent.fighter.hpdmg_string(amount)} effect!',
                category=MessageCategory.OBSERVATION, type=MessageType.COMBAT_INFO)})
            affected_ent.fighter.heal(amount)
        else:
            results.append({'message': Message(f'{affected_ent.pronoun.title()} {affected_ent.state_verb_past} already at full health.')})

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
        effect_name = kwargs.get('effect_name', 'projectile')
        effect_verb = kwargs.get('effect_verb', 'hits')

        results = []

        animate_projectile(*user.pos, *target_pos, game)  # TODO add color switch

        if on_hit is not None:
            ent = next((ent for ent in game.fighter_ents if ent.pos == target_pos), None)
            kwargs['affected_ent'] = ent
            kwargs['string'] = effect_name
            results.extend(on_hit(**kwargs))

        return results

    @staticmethod
    def explosion(**kwargs):
        game = kwargs['game']
        center = kwargs.get('target_pos')
        radius = kwargs.get('radius',3)
        on_hit = kwargs.get('on_expl_hit', Effect.direct_damage)
        effect_name = kwargs.get('effect_name', 'explosion')
        effect_verb = kwargs.get('effect_verb', 'burns')

        entities = [ent for ent in game.alive_ents if ent.distance_to_pos(*center) <= radius]
        results = []

        animate_explosion(*center, radius, game)  # TODO add color switch

        results.append({'message': Message(f'The {effect_name} {effect_verb} everything within {radius} tiles!')})

        for entity in entities:
            kwargs['affected_ent'] = entity
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