from config_files import colors
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_line, animate_move_to
from rendering.render_main import render_map_screen


class SkillUsage:

    @staticmethod
    def charge_prepare(ent, *args, **kwargs):
        game = args[0]
        delay = kwargs['delay']
        results = []

        tx, ty = game.player.x, game.player.y

        ent.color_bg = colors.dark_red
        ent.turnplan.skip_turns(delay, game.turn)
        ent.turnplan.plan_turn(game.turn + delay + 1, {'planned_function': SkillUsage.charge_execute,
                                                       'planned_function_args': (ent, tx, ty, game)})
        results.append({'message':Message(f'The {ent.name} prepares to rush forward.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    @staticmethod
    def charge_execute(ent, tx, ty, game):
        ent.color_bg = None # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message':Message(f'The {ent.name} charges forward!', category=MessageCategory.OBSERVATION, type=MessageType.COMBAT)})
        hit = animate_move_to(ent, tx, ty, game)
        #hit = animate_move_line(ent, game, dx, dy, distance)
        # TODO add power modifier to charged attacks
        if hit:
            if hit.fighter:
                results.extend(ent.fighter.attack(hit, mod=2))
            elif hit.architecture:
                results.extend(ent.fighter.attack(ent, mod=0.5))
        elif hit is False:   # If a wall is hit during the charge, damage the charging entity
            results.extend(ent.fighter.attack(ent, mod=0.5))
        return results

class SkillCondition:
    """
    TODO Add:
    Clear line to target
    """

    @staticmethod
    def can_see_player(actor, game, **kwargs):
        player = game.player
        return actor.distance_to_ent(player) <= actor.fighter.vision

    @staticmethod
    def free_line_to_player(actor, game, **kwargs):
        player = game.player
        game.map.free_line_between_tiles(actor.x, actor.y, player.x, player.y)

    @staticmethod
    def distance_to(actor, game, **kwargs):
        player = game.player
        min, max = kwargs['min_dist'], kwargs['max_dist']
        if min < actor.distance_to_ent(player) < max:
            return True
        else:
            return False

    @staticmethod
    def always_true():
        return True