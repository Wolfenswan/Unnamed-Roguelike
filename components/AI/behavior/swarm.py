import logging
from random import choice, randint


class Swarm:
    """ Swarming npcs will first check if they have friendlies nearby, before chasing down the player """

    def decide_move(self, target, game):
        npc = self.owner.owner

        results = []

        # Prepare the filters beforehand
        friendlies_nearby = len(npc.entities_in_distance(entities=game.npc_ents,dist=3)) > 0
        friendlies_near_target = len(target.surrounding_enemies(game.npc_ents)) > 1
        friendlies_in_area = len(npc.entities_in_distance(entities=game.npc_ents, dist=npc.fighter.vision)) > 0

        # 1. Check: Is Target either surrounded by friendlies or friendlies are next to self #
        if friendlies_nearby or friendlies_near_target:
            logging.debug(f'{npc} has friendly nearby and moves to player.')
            npc.move_astar(target, game)
        # 2. Check: Are friendlies in vision range? #
        elif friendlies_in_area:
            nearest_ent = npc.entities_in_distance(dist=npc.fighter.vision, entities=game.npc_ents)[0]
            logging.debug(f'{npc} is moving to friendly.')
            npc.move_astar(nearest_ent, game)

        # 3. Check: If all else fails, try to flee #
        else: # TODO coin toss whether to cower or flee?
            logging.debug(f'{npc} is keeping distance from player.')
            npc.move_away_from(target, game)

        return results
    
    def decide_attack(self, target, game):
        game_map = game.map
        npc = self.owner.owner
        results = []

        friendlies_near_target = len(target.surrounding_enemies(game.npc_ents)) > 1

        if friendlies_near_target:
            # TODO should the ability to squeeze past be a skill?
            pos_list = game_map.empty_pos_near_ent(target, game)
            if pos_list:
                pos = next((pos for pos in pos_list if npc.distance_to_pos(*pos) <= 2), None)
                if pos:
                    npc.move_towards(target, game)

                elif pos is None:
                    if randint(0, 100) <= 65: # TODO proper skill check later
                        pos = choice(pos_list)
                        npc.x, npc.y = pos

            # Swarmer may attack after moving around the target #
            attack_results = npc.fighter.attack_setup(target, game)
        else:
            attack_results = self.decide_move(target, game)

        results.extend(attack_results)
        return results