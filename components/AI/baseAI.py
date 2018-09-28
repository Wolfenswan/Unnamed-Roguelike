from random import randint, choice

import tcod

from components.actors.status_modifiers import Presence
from data.actor_data.act_status_mod import status_modifiers_data
from gui.messages import Message


class BaseAI:
    def __init__(self, movement = None, attack=None):
        self.movement = movement

        if movement:
            self.movement.owner = self

        self.attack = attack

        if attack:
            self.attack.owner = self

    def take_turn(self, game, fov_map):

        results = []
        npc = self.owner
        presence = npc.fighter.presence
        target = game.player
        game_map = game.map

        # free_line = game.map.free_line_between_pos(target.x, target.y, npc.x, npc.y, game)
        # print(free_line)

        # Process action queue and planned action if applicable #
        planned_action_results = npc.actionplan.process_queue()
        if planned_action_results:
            results.extend(planned_action_results)
            return results

        if presence[Presence.STUNNED]:
            message = Message(f'PLACEHOLDER: {npc.name} is stunned and skipping turn.')
            results.append({'message': message})
            return results

        if presence[Presence.DAZED]:
            if randint(0,100) <= status_modifiers_data[Presence.DAZED]['skip_turn_chance']:
                message = Message(f'PLACEHOLDER: {npc.name} is dazed and skipping turn.')
                results.append({'message': message})
                return results

        if self.owner.fighter.stamina < self.owner.fighter.max_stamina / 10:
          # Switch to resting AI mode
          self.owner.fighter.recover(self.owner.fighter.max_stamina / 2)  # TODO Placeholder Stamina Management
          message = Message(f'PLACEHOLDER: {npc.name} is exhausted and skipping turn to rest.')
          results.append({'message': message})
          return results

        # First check if the npc can see the player #
        if tcod.map_is_in_fov(fov_map, npc.x, npc.y):
            npc.color_bg = None  # some special attacks modify a character's background color, this resets it

            # Consider using a skill #
            # TODO might be moved into behavior components later #
            if npc.skills:
                npc.cooldown_skills()
                available_skills = npc.available_skills(game)
                if available_skills:
                    skill = choice(available_skills)
                    skill_results = skill.execute(game)
                    results.extend(skill_results)
                    return results

            # If no skill is available, consider moving #
            if npc.distance_to_ent(target) >= 2:
                results.extend(self.movement.decide_move(target, game))

            # Or consider attack, if next to target #
            elif npc.distance_to_ent(target) < 2:
                results.extend(self.movement.decide_attack(target, game))

        # If NPC is hidden from FOV, move randomly #
        else:
            dx, dy = randint(-1, 1), randint(-1, 1)
            x, y = npc.x + dx, npc.y + dy
            if not game_map.is_wall(x, y):
                npc.move(dx, dy)

        return results

    def set_behavior(self, movement=None, attack=None):
        if movement:
            self.movement = movement
            self.movement.owner = self
        if attack:
            self.attack = attack
            self.attack.owner = self