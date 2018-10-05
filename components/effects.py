import tcod

from gui.messages import Message, MessageCategory, MessageType
from rendering.render_animations import animate_projectile, animate_explosion


class Effects:

    @staticmethod
    def explosion(**kwargs):
        game = kwargs['game']
        user = kwargs['user']
        used_item = kwargs['used_item']
        target_pos = kwargs.get('target_pos')
        damage = kwargs.get('dmg')
        radius = kwargs.get('radius')
        projectile_color = kwargs.get('projectil_color', used_item.color)

        fov_map = game.fov_map
        entities = game.alive_ents

        results = []

        animate_projectile(*user.pos, *target_pos, 0, game) # TODO add color switch
        animate_explosion(*target_pos, radius, game) # TODO add color switch

        if not tcod.map_is_in_fov(fov_map, *target_pos):
            results.append(
                {'consumed': False, 'message': Message('You cannot target a tile outside your field of view.')})
            return results

        results.append(
            {'consumed': True,
             'message': Message(f'The {used_item.name} explodes, burning everything within {radius} tiles!')
             })

        for entity in entities:
            if entity.distance_to_pos(*target_pos) <= radius:
                results.append({'message': Message(f'The {entity.name} takes %{entity.fighter.hpdmg_color(damage)}%{entity.fighter.hpdmg_string(damage)}%% damage!', category=MessageCategory.COMBAT, type=MessageType.COMBAT_INFO)})
                results.extend(entity.fighter.take_damage(damage))

        return results