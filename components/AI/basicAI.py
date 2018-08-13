from random import randint, choice

import tcod

from components.AI.movement.straightmover import StraightMover
from components.AI.movement.swarmmover import SwarmMover


class BasicAI:
    def __init__(self, movement = StraightMover()):
        self.movement = movement

        if movement:
            movement.owner = self

    def take_turn(self, game, fov_map):

        results = []
        target = game.player
        game_map = game.map
        entities = game.entities
        monster = self.owner

        # First check if anything has been planned for this turn #
        turn_plan = monster.turnplan.planned_turns.get(game.turn)
        if turn_plan:
            turn_plan_resuls = monster.turnplan.execute_plan(game.turn)
            results.extend(turn_plan_resuls)

        # Otherwise check if the monster can see the player #
        elif tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            monster.color_bg = None  # some special attacks modify a character's background color, this resets it

            #results.extend(self.movement.move_decision(game))
            # Consider using a skill #
            if monster.skills:
                monster.cooldown_skills()
                available_skills = monster.available_skills(game)
                if available_skills:
                    skill = choice(available_skills)
                    skill_results = skill.execute(game)
                    results.extend(skill_results)
                    return results

            if monster.distance_to_ent(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        # As last alternative, the monster will randomly move around #
        else:
            dx, dy = randint(-1, 1), randint(-1, 1)
            x, y = monster.x + dx, monster.y + dy
            if not game_map.is_blocked(x, y):
                monster.move(dx, dy)

        return results
