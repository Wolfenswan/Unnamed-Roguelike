from random import randint, choice

import tcod

from gameobjects.entity import EntityStates


class BasicMonster:
    def take_turn(self, game, fov_map):
        target = game.player
        game_map = game.map
        entities = game.entities

        results = []

        monster = self.owner

        # If monster is unable to move, reduce their turn delay
        if monster.state in [EntityStates.ENTITY_STUNNED, EntityStates.ENTITY_WAITING]:
            monster.delay_turns -= 1

        # If monster is not delaying, being turn evaluation #
        if monster.delay_turns == 0:
            monster.state = EntityStates.ENTITY_ACTIVE
            monster.color_bg = None # some special attacks modify a character's background color, this resets it

            # Check if monster is set to execute a skill after the delay #
            if monster.execute_after_delay is not None:
                skill_results = eval(monster.execute_after_delay)
                results.extend(skill_results)
                monster.execute_after_delay = None

            elif tcod.map_is_in_fov(fov_map, monster.x, monster.y):

                # Consider using a skill #
                if monster.skills:
                    monster.cooldown_skills() # Currently skills do not cool down if a monster is already stunned or waiting.
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

            else:
                dx, dy = randint(-1,1), randint(-1,1)
                x, y = monster.x + dx, monster.y + dy
                if not game_map.is_blocked(x, y):
                    monster.move(dx,dy)

        return results