import logging
from random import randint, choice
from typing import Union, Optional

from dataclasses import dataclass

from components.actors.fighter_util import State
from data.actor_data.act_status_mod import status_modifiers_data
from gui.messages import Message


@dataclass
class BaseAI:
    behavior : Optional = None

    def take_turn(self, game, fov_map):
        results = []
        npc = self.owner
        presence = npc.fighter.effects
        target = game.player
        game_map = game.map

        logging.debug(f'{npc} is taking turn #{game.turn}')

        # free_line = game.map.free_line_between_pos(target.x, target.y, npc.x, npc.y, game)

        # First check if turn is entirely skipped
        if presence[State.STUNNED]:
            message = Message(f'PLACEHOLDER: {npc.name} is stunned and skipping turn.')
            results.append({'message': message})
            return results

        if presence[State.DAZED]:
            if randint(0,100) <= status_modifiers_data[State.DAZED]['skip_turn_chance']:
                message = Message(f'PLACEHOLDER: {npc.name} is dazed and skipping turn.')
                results.append({'message': message})
                return results

        # Process action queue and planned action if applicable, skipping the rest of the turn #
        planned_action_results = npc.actionplan.process_queue()
        if planned_action_results:
            results.extend(planned_action_results)
            return results

        if npc.fighter.stamina < npc.fighter.max_stamina / 10:
          # Switch to resting AI mode
          npc.fighter.recover(npc.fighter.max_stamina / 2)  # TODO Placeholder Stamina Management
          message = Message(f'PLACEHOLDER: {npc.name} is exhausted and skipping turn to rest.')
          results.append({'message': message})
          return results

        # First check if the npc can see the player #
        if npc.is_visible(fov_map): #tcod.map_is_in_fov(fov_map, npc.x, npc.y):
            # Consider using a skill #
            # TODO might be merged into behavior components later #
            if npc.skills:
                npc.skills.cooldown()
                if npc.skills.available:
                    possible_skills = npc.skills.active(target, game)
                    if possible_skills:
                        skill = choice(possible_skills)
                        skill_results = skill.use(target, game)
                        results.extend(skill_results)
                        return results

            # If no skill is available or was used, decide on an action, based on behavior #
            if self.behavior is not None:
                results.extend(self.behavior.decide_action(target, game))

        # If NPC is hidden from FOV, move randomly #
        # TODO test perfomance impact
        elif npc.can_move:
            dx, dy = randint(-1, 1), randint(-1, 1)
            x, y = npc.x + dx, npc.y + dy
            if not game_map.is_wall(x, y):
                npc.move(dx, dy)

        return results


    def set_behavior(self, behavior):
        self.behavior = behavior()
        self.behavior.owner = self.owner