import logging
from random import randint, choice

from game import Game
from gameobjects.util_functions import free_line_between_pos, distance_between_pos
from map.game_map import GameMap


class Ranged:
    """
    Simple behavior moves the npc straight towards the player, attack if next to them and use a skill if available.
    """

    def decide_action(self, target, game:Game):
        actor = self.owner.owner
        game_map:GameMap = game.map
        distance = actor.distance_to_ent(target)
        free_line = actor.free_line_to_ent(target, game)

        results = []

        logging.debug(f'{actor} is deciding on action against {target}')

        if distance <= 2:
            logging.debug(f'{actor} moves away from target, as distance({distance}) is too small')
            actor.move_away_from(target, game)
        elif distance * randint(1, 4) <= 4: # Small chance the actor might try to get away further
            logging.debug(f'{actor} moves away from target, after randomized distance({distance}) is under 4')
            actor.move_away_from(target, game)
        elif not free_line: # Entity will try to establish a clear line of sight to the target
            logging.debug(f'{actor} would attack but has no clear line to target')
            surrounding_pos = game_map.surrounding_pos(*actor.pos, dist=2)
            valid_pos = [pos for pos in surrounding_pos if not game_map.is_blocked(*pos, game.blocking_ents) and\
                        distance_between_pos(*pos, *target.pos) > 2\
                        and free_line_between_pos(*pos, *target.pos, game)]
            if len(valid_pos) > 0:
                pos = choice(valid_pos) # TODO an additional filter could be added to make sure a free line between actor and possible new pos exists
                logging.debug(f'{actor} is trying to move to {pos} to get a clear line to target')
                moved = actor.try_move(*actor.direction_to_pos(*pos), game)
                if moved is False: # if a pos was found but movement failed, attack anyway
                    logging.debug(f'{actor} could not move to pos, attacking')
                    results.extend(actor.fighter.attack_setup(target, game, melee=False))
            else: # if no pos with LOS was found nearby, attack anyway
                logging.debug(f'{actor} has not found a pos nearby with clear line to target, attacking')
                results.extend(actor.fighter.attack_setup(target, game, melee=False))
        else: # if distance is good and free los established, attack
            logging.debug(f'{actor} has clear line to target, attacking')
            results.extend(actor.fighter.attack_setup(target, game, melee=False))

        return results