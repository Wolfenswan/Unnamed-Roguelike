from random import choice


class StraightMover:
    def move_decision(self, game):
        target = game.player
        game_map = game.map
        entities = game.entities

        monster = self.owner.owner

        results = []

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

        return results