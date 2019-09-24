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

        if randint(0,100) >= 40 and distance >= 1.5: # Initial chance to try laying an egg first, but only if target is outside melee range
            egg = None
            if distance >= 3: # If target is far enough away
                if not enough_friendlies_nearby:  # If not enough friendlies are present
                    pos = game_map.random_free_pos_near_ent(actor, game)
                    if pos is not False: # egg will spawn if good pos was found
                        egg = Summon(pos,'hatchling_egg')
            elif distance >= 2:  # If target is not in melee range, but close
                if not enough_friendlies_near_target: # If target is getting too close, try placing an egg to obstruct it's path
                    dir = actor.direction_to_ent(target)
                    pos = (actor.x + dir[0], actor.y + dir[1])
                    if not game_map.is_blocked(*pos, game.walk_blocking_ents):
                        egg = Summon(pos,'hatchling_egg')

            if egg is not None: # If an egg was laid, add it to the game's total entity list and finish the turn
                game.entities.append(egg)
                return results

        # Otherwise proceed to attack directly
        actor.ai.pick_weapon(target)
        results.extend(actor.f.attack_setup(target, game))

        return results