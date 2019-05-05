import logging
from random import randint

from game import Game
from gameobjects.special_entities import Summon

from map.game_map import GameMap


class Queen:
    def decide_action(self, target, game:Game):
        actor = self.owner
        game_map:GameMap = game.map
        distance = actor.distance_to_ent(target)
        # free_line = actor.free_line_to_ent(target, game)
        enough_friendlies_nearby = len(actor.entities_in_distance(entities=game.npc_ents, dist=3)) >= 3
        enough_friendlies_near_target = len(target.surrounding_enemies(game.npc_ents)) >= 1
        # enough_friendlies_in_area = len(actor.entities_in_distance(entities=game.npc_ents, dist=actor.f.vision)) >= 5

        results = []

        if randint(0,100) >= 20: #80% chance to try laying an egg first
            egg = None
            if distance >= 3: # If target is far enough away
                if not enough_friendlies_nearby:  # If not enough friendlies are present
                    #pos = actor.random_free_pos_in_dist(game)
                    pos = game_map.random_free_pos_near_ent(actor, game)
                    if pos is not False:
                        egg = Summon(pos,'hatchling_egg')
            elif distance >= 2:  # If target is not in melee range, but close
                if not enough_friendlies_near_target: # If target is getting too close, try putting an egg to obstruct it's path
                    dir = actor.direction_to_ent(target)
                    pos = (actor.x + dir[0], actor.y + dir[1])
                    if not game_map.is_blocked(*pos, game.walk_blocking_ents):
                        egg = Summon(pos,'hatchling_egg')

            if egg is not None: # If an egg was laid, add it to the game's total entity list and finish the action
                game.entities.append(egg)
                return results

        # With a 20% chance or if no egg was laid, proceed to attack directly
        if distance >= 2:   # First select the according weapon for the range
            actor.f.active_weapon = actor.f.weapon_ranged
        else:
            actor.f.active_weapon = actor.f.weapon_melee

        results.extend(actor.f.attack_setup(target, game))

        return results