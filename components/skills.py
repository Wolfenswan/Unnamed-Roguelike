import logging
from random import randint

from gui.messages import Message

class Skill:
    def __init__(self, on_activate=None, activate_condition=None, cooldown_length=None):
        self.on_activate = on_activate
        self.activate_condition = activate_condition
        self.cooldown_length = cooldown_length
        self.cooldown = cooldown_length

    def execute(self, game):
        actor = self.owner.owner
        logging.debug(f'Special attack for {actor}. Cooldown {self.cooldown} of {self.cooldown_length}')
        results = self.on_activate(actor)
        self.cooldown = 0
        return results

    def is_available(self, game):
        monster = self.owner.owner
        return self.cooldown >= self.cooldown_length and self.activate_condition(game, monster)


def skill_charge_activation(ent):
    results = []
    results.append({'message': Message(f'{ent.name} charges!')})
    return results

def skill_charge_condition(game, actor):
    player = game.player
    if actor.distance_to_ent(player) < 6:
        print('T')
        return True
    else:
        print('F')
        return False
