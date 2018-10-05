from pprint import pprint
from random import randint

from gui.messages import Message, MessageCategory, MessageType
from rendering.render_animations import animate_projectile, animate_explosion


class AbilityEffect:

    @staticmethod
    def direct_damage(affected_ent = None, string='hit', **kwargs):
        # NOTE: Does currently not take any defenses into account.
        amount = randint(*kwargs.get('pwr'))

        if affected_ent is None:
            affected_ent = kwargs.get('user')

        results = []

        results.append({'message': Message(
            f'The {string} causes  %{affected_ent.fighter.hpdmg_color(amount)}%{affected_ent.fighter.hpdmg_string(amount)}%% damage to the {affected_ent.name}!',
            category=MessageCategory.COMBAT, type=MessageType.COMBAT_INFO)})
        results.extend(affected_ent.fighter.take_damage(amount))

        return results

    @staticmethod
    def direct_heal(affected_ent = None, **kwargs):
        amount = randint(*kwargs.get('pwr'))

        if affected_ent is None:
            affected_ent = kwargs.get('user')

        results = []

        if affected_ent.fighter.hp < affected_ent.fighter.max_hp:
            results.append({'message': Message(
                f'{affected_ent.name} heals for {affected_ent.fighter.hpdmg_string(amount)} effect!',
                category=MessageCategory.OBSERVATION, type=MessageType.COMBAT_INFO)})
        else:
            results.append({'message': Message(f'{affected_ent.name.title()} was already at full health.')})

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
        on_impact = kwargs.get('on_impact', None)
        effect_name = kwargs.get('effect_name', 'projectile')
        effect_verb = kwargs.get('effect_verb', 'hits')

        results = []

        animate_projectile(*user.pos, *target_pos, 0, game)  # TODO add color switch

        if on_impact is not None:
            ent = next((ent for ent in game.fighter_ents if ent.pos == target_pos), None)
            kwargs['affected_ent'] = ent
            kwargs['string'] = effect_name
            results.extend(on_impact(**kwargs))

        return results

    @staticmethod
    def explosion(**kwargs):
        game = kwargs['game']
        used_item = kwargs['used_item']
        center = kwargs.get('target_pos')
        radius = kwargs.get('radius',3)
        effect_name = kwargs.get('effect_name', 'explosion')
        effect_verb = kwargs.get('effect_verb', 'burns')
        projectile_color = kwargs.get('projectile_color', used_item.color)

        entities = [ent for ent in game.alive_ents if ent.distance_to_pos(*center) <= radius]
        results = []

        animate_explosion(*center, radius, game)  # TODO add color switch

        results.append(
            {'consumed': True,
             'message': Message(f'The {effect_name} {effect_verb} everything within {radius} tiles!')
             })

        for entity in entities:
            kwargs['affected_ent'] = entity
            kwargs['string'] = effect_name
            results.extend(AbilityEffect.direct_damage(**kwargs))

        return results