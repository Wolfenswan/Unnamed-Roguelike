import logging
from random import choice, randint


class Swarm:
    """ Swarming npcs will first check if they have friendlies nearby, before chasing down the player """

    def decide_move(self, target, game):
        game_map = game.map
        entities = game.entities
        npc = self.owner.owner

        results = []

        # Prepare the filters beforehand
        filter_kwargs = {'ai_only':True, 'filter_player':True}
        friendlies_nearby = len(npc.get_nearby_entities(game, dist=3, **filter_kwargs)) > 0
        friendlies_near_target = len(target.get_nearby_entities(game, dist=2, **filter_kwargs)) > 0
        friendlies_in_area = len(npc.get_nearby_entities(game, dist=npc.fighter.vision, **filter_kwargs)) > 0

        # 1. Check: Is Target either surrounded by friendlies or friendlies are next to self #
        if friendlies_nearby or friendlies_near_target:
            logging.debug(f'{npc} has friendly nearby and moves to player.')
            npc.move_astar(target, entities, game_map)
        # 2. Check: Are friendlies in vision range? #
        elif friendlies_in_area:
            nearest_ent = npc.get_nearby_entities(game, dist=npc.fighter.vision, **filter_kwargs)[0]
            logging.debug(f'{npc} is moving to friendly.')
            npc.move_astar(nearest_ent, entities, game_map)

        # 3. Check: If all else fails, try to flee #
        else: # TODO coin toss whether to cower or flee?
            logging.debug(f'{npc} is keeping distance from player.')
            npc.move_away_from(target, game)

        return results
    
    def decide_attack(self, target, game):
        game_map = game.map
        npc = self.owner.owner
        results = []

        # TODO should the ability to squeeze past be a skill?
        tiles = game_map.empty_tiles_near_ent(target, game)
        if tiles:
            tile = next((t for t in tiles if npc.distance_to_pos(*t) <= 2), None)
            if tile:
                npc.move_towards(*tile, game_map, game.entities)

            elif tile is None:
                tile = choice(tiles)
                if randint(0, 1): # TODO proper skill check later
                    tile = choice(tiles)
                    npc.x, npc.y = tile

        # Swarmer will attack after moving around the target #
        attack_results = npc.fighter.attack_setup(target, game)
        results.extend(attack_results)

        return results