import tcod

from config_files import colors
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_line, animate_move_to
from rendering.render_main import render_main_screen


class SkillUsage:

    @staticmethod
    def skill_charge_prepare(ent, *args, **kwargs):
        game = args[0]
        delay = kwargs['delay']
        results = []

        #dx, dy = ent.direction_to_ent(game.player)
        distance = ent.distance_to_ent(game.player)
        tx, ty = game.player.x, game.player.y

        ent.color_bg = colors.dark_red
        ent.turnplan.skip_turns(delay, game.turn)
        ent.turnplan.plan_turn(game.turn + delay + 1, {'planned_function': SkillUsage.skill_charge_execute,
                                                       'planned_function_args': (ent, tx, ty, game)})
        results.append({'message':Message(f'The {ent.name} prepares to rush forward.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    @staticmethod
    def skill_charge_execute(ent, dx, dy, game):
        # TODO follow a rough line towards the targets position, instead of only cardinal directions
        ent.color_bg = None # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message':Message(f'The {ent.name} charges forward!', category=MessageCategory.OBSERVATION, type=MessageType.COMBAT)})
        hit = animate_move_to(ent, dx, dy, game)
        #hit = animate_move_line(ent, game, dx, dy, distance)
        # TODO add power modifier to charged attacks
        if hit:
            if hit.fighter:
                results.extend(ent.fighter.attack(hit))
            elif hit.architecture:
                results.extend(ent.fighter.attack(ent))
        elif hit is False:   # If a wall is hit during the charge, damage the charging entity
            results.extend(ent.fighter.attack(ent))
        return results

class SkillConditions:

    @staticmethod
    def skill_charge_condition(game, actor, **kwargs):
        # TODO also a somewhat straight empty line
        player = game.player
        min, max = kwargs['min'], kwargs['max']
        if min < actor.distance_to_ent(player) < max:
            return True
        else:
            return False

    @staticmethod
    def skill_always_true():
        return True