import logging


class SwarmMover:
    def move_decision(self, game):
        """ Swarming monsters will first check if they have friendlies nearby, before chasing down the player """
        target = game.player
        game_map = game.map
        entities = game.entities

        monster = self.owner.owner

        # make sure there's at least > 1 friendly monster nearby
        kwargs = {'ai_only':True, 'filter_player':True}
        if len(monster.get_nearby_entities(game, dist=2, **kwargs)) or len(target.get_nearby_entities(game, dist=2, **kwargs)):
            logging.debug(f'{monster} has friendly nearby and moves to player.')
            monster.move_astar(target, entities, game_map)

        # if not, move towards nearest friendlies in vision range
        #kwargs2 = {'ai_only': True, 'filter_player': True, 'dist': monster.vision}
        #nearby_ents = monster.get_nearby_entities(game, **kwargs2)
        elif len(monster.get_nearby_entities(game, dist=monster.fighter.vision, **kwargs)) > 0:
            nearest_ent = monster.get_nearby_entities(game, dist=monster.fighter.vision, **kwargs)[0]
            logging.debug(f'{monster} is moving to friendly.')
            monster.move_astar(nearest_ent, entities, game_map)

        # if there are none, keep distance from player
        else:
            logging.debug(f'{monster} is keeping distance from player.')
            monster.move_away_from(target)

        # TODO attacks, special moves

        return []