import logging
from random import choice, randint


class Swarm:
    """ Swarming npcs will first check if they have friendlies nearby, before chasing down the player """

    def decide_action(self, target, game):
        actor = self.owner
        game_map = game.map
        distance = actor.distance_to_ent(target)
        friendlies_nearby = len(actor.entities_in_distance(entities=game.npc_ents, dist=3)) > 0
        friendlies_near_target = len(target.surrounding_enemies(game.npc_ents)) >= 1
        friendlies_in_area = len(actor.entities_in_distance(entities=game.npc_ents, dist=actor.f.vision)) > 0

        results = []

        if distance >= 2:
            # 1. Check: Is Target either already attacked by friendlies or friendlies are next to self #
            if friendlies_nearby or friendlies_near_target:
                logging.debug(f'{actor} has friendly nearby and moves to player.')
                actor.move_astar(target, game)
            # 2. Check: Are friendlies in vision range? #
            elif friendlies_in_area:
                nearest_ent = actor.entities_in_distance(dist=actor.f.vision, entities=game.npc_ents)[0]
                logging.debug(f'{actor} is moving to friendly.')
                actor.move_astar(nearest_ent, game)

            # 3. Check: If all else fails, try to flee #
            else:  # TODO coin toss whether to cower or flee?
                logging.debug(f'{actor} is keeping distance from player.')
                actor.move_away_from(target, game)
        else:
            if friendlies_near_target:
                # TODO should the ability to squeeze past be a skill?
                pos_list = game_map.all_free_pos_near_ent(target, game)
                if pos_list:
                    pos = next((pos for pos in pos_list if actor.distance_to_pos(*pos) <= 2), None)
                    if pos:
                        actor.move_towards(target, game)

                    elif pos is None:
                        if randint(0, 100) <= 65:  # TODO proper skill check later
                            pos = choice(pos_list)
                            actor.x, actor.y = pos

                # Swarmer may attack after moving around the target
                attack_results = actor.f.attack_setup(target, game)
                results.extend(attack_results)
            else:
                actor.move_away_from(target, game)

        return results