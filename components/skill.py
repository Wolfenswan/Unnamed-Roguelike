import logging
from random import choice

from config_files import colors
from gui.messages import Message

class Skill:
    def __init__(self, name = 'Skill', on_activate=None, on_activate_kwargs = {}, activate_condition=None, activate_condition_kwargs = {}, cooldown_length=None, messages=None):
        self.name = name
        self.on_activate = on_activate
        self.on_activate_kwargs = on_activate_kwargs
        self.activate_condition = activate_condition
        self.activate_condition_kwargs = activate_condition_kwargs
        self.cooldown_length = cooldown_length
        self.cooldown = 0
        self.messages = messages

    def execute(self, *args):
        actor = self.owner
        results = []

        logging.debug(f'Special attack for {actor}. Cooldown {self.cooldown} of {self.cooldown_length}')
        activation_results = self.on_activate(actor, *args, **self.on_activate_kwargs)
        results.extend(activation_results)
        self.cooldown_skill(reset=True)
        return results

    def is_available(self, game):
        actor = self.owner
        available = self.cooldown_length >= 0 and self.cooldown == 0 and self.activate_condition(actor, game, **self.activate_condition_kwargs)
        return available

    # def is_available_alt(self, game):
    #     # alternative method, currently unused, needs string for skill_activate_condition instead of function
    #     monster = self.owner.owner
    #     condition = eval(self.activate_condition)
    #     if self.cooldown <= self.cooldown_length and condition:
    #         return True
    #     else:
    #         return False

    def cooldown_skill(self, reset=False):
        if reset:
            self.cooldown = self.cooldown_length
        elif self.cooldown > 0:
            self.cooldown -= 1

        logging.debug(
            f'Cooled down {self.name} on {self.owner.name}: {self.cooldown} of {self.cooldown_length}.')