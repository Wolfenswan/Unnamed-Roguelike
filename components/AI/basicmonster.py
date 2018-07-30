from random import randint, choice

import tcod


class BasicMonster:
    def take_turn(self, game, fov_map):
        target = game.player
        game_map = game.map
        entities = game.entities

        results = []

        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.fighter.skills:
                monster.fighter.cooldown_skills()
                # TODO Use cooldown amount exceeding cooldown length to prioritze unused skills
                available_skills = monster.fighter.available_skills()
                if available_skills:
                    skill = choice(available_skills)
                    skill_results = skill.execute(game)
                    return results.extend(skill_results)

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