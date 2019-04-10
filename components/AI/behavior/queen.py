import logging
from game import Game
from gameobjects.special_entities import Egg

from map.game_map import GameMap


class Queen:
    def decide_action(self, target, game:Game):
        actor = self.owner
        game_map:GameMap = game.map
        distance = actor.distance_to_ent(target)
        # free_line = actor.free_line_to_ent(target, game)
        enough_friendlies_nearby = len(actor.entities_in_distance(entities=game.npc_ents, dist=3)) >= 3
        enough_friendlies_near_target = len(target.surrounding_enemies(game.npc_ents)) >= 1
        # enough_friendlies_in_area = len(actor.entities_in_distance(entities=game.npc_ents, dist=actor.fighter.vision)) >= 5

        results = []
        print(distance, enough_friendlies_nearby,enough_friendlies_near_target, len(game.entities))

        #logging.debug(f'{actor} is deciding on action against {target}')

        if distance >= 3: # If target is far enough away
            if not enough_friendlies_nearby:  # If not enough friendlies are present
                pos = actor.random_free_pos_in_dist(game)
                print(pos)
                if pos is not False:
                    egg = Egg(pos)
                    game.entities.append(egg)
                    return results
        elif distance >= 2:  # If target is not in melee range, but close
            if not enough_friendlies_near_target: # If target is getting too close, try putting an egg to obstruct it's path
                dir = actor.direction_to_ent(target)
                pos = (actor.x + dir[0], actor.y + dir[1])
                if not game_map.is_blocked(*pos, game.walk_blocking_ents):
                    egg = Egg(pos)
                    game.entities.append(egg)
                    return results

        # if no egg was laid, proceed to direct attack
        if distance >= 2:
            actor.fighter.active_weapon = actor.fighter.weapon_ranged
        else:
            actor.fighter.active_weapon = actor.fighter.weapon_melee

        results.extend(actor.fighter.attack_setup(target, game))

        return results