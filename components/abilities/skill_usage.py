from config_files import colors
from gui.messages import Message, MessageCategory, MessageType
from rendering.render_animations import animate_move_to


class SkillUsage:

    @staticmethod
    def charge_prepare(ent, target, game, **kwargs):
        delay = kwargs['delay']
        results = []

        d_x, d_y = ent.direction_to_ent(target)
        tx, ty = target.x + d_x, target.y + d_y

        ent.color_bg = colors.dark_red
        ent.actionplan.add_to_queue(execute_in=delay, planned_function=SkillUsage.charge_execute,
                                    planned_function_args=(ent, tx, ty, game), fixed=True)
        #ent.actionplan.add_to_queue(delay, {'planned_function': SkillUsage.charge_execute,'planned_function_args': (ent, tx, ty, game)})
        results.append({'message':Message(f'The {ent.name} prepares to charge.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    @staticmethod
    def charge_execute(ent, tx, ty, game):
        # TODO attack_string should be defined in their own data file
        ent.color_bg = None # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message':Message(f'The {ent.name} charges forward!', category=MessageCategory.OBSERVATION, type=MessageType.COMBAT)})
        hit = animate_move_to(ent, tx, ty, game)
        if hit:
            if hit.fighter:
                results.extend(ent.fighter.attack_setup(hit, game, mod=2, attack_string='gores', ignore_moveset=True))
            elif hit.architecture:
                results.extend(ent.fighter.attack_setup(ent, game, mod=0.5, attack_string='rams', ignore_moveset=True))
        elif hit is False:   # If a wall is hit during the charge, damage the charging entity
            results.extend(ent.fighter.attack_setup(ent, game, mod=0.5, attack_string='rams', ignore_moveset=True))
        return results