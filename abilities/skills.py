import tcod

from config_files import colors
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animation import animate_move
from rendering.render_main import render_main_screen


class SkillUsage:

    @staticmethod
    def skill_charge_prepare(ent, *args, **kwargs):
        game = args[0]
        distance = kwargs['distance']
        delay = kwargs['delay']
        results = []
        # TODO Condition: Straight empty line to target
        dx, dy = ent.direction_to_ent(game.player)

        ent.color_bg = colors.dark_red
        ent.turnplan.skip_turns(delay, game.turn)
        ent.turnplan.plan_turn(game.turn + delay + 1, {'planned_function': SkillUsage.skill_charge_execute,
                                                       'planned_function_args': (ent, game, dx, dy, distance)})
        results.append({'message':Message(f'The {ent.name} prepares to rush forward.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    @staticmethod
    def skill_charge_execute(ent, game, dx, dy, distance):
        results = []
        results.append({'message':Message(f'The {ent.name} charges forward!', category=MessageCategory.OBSERVATION, type=MessageType.COMBAT)})
        ent.color_bg = colors.green
        # TODO - charging monsters cover too distance, why?
        hit = animate_move(ent, game, dx, dy, distance)
        print(hit)
        if hit:
            results.extend(ent.fighter.attack(hit))
        # for i in range(distance):   # TODO Animation; maybe break up in several large steps over n turns?
        #     blocked = ent.try_move(game, dx, dy)
        #     print(i, distance, dx, dy, ent.direction_to_ent(game.player))
        #     if blocked:
        #         print(blocked)
        #         ent.fighter.attack(blocked)
        #         break

        return results

class SkillConditions:

    @staticmethod
    def skill_charge_condition(game, actor, **kwargs):
        player = game.player
        min, max = kwargs['min'], kwargs['max']
        if min < actor.distance_to_ent(player) < max:
            return True
        else:
            return False

    @staticmethod
    def skill_always_true():
        return True