import logging
from random import choice

from config_files import colors
from gui.messages import Message

class Skill:
    def __init__(self, name = 'Skill', on_activate=None, on_activate_kwargs = None, activate_condition=None, activate_condition_kwargs = None, cooldown_length=None, messages=None):
        self.name = name
        self.on_activate = on_activate
        self.on_activate_kwargs = {} if on_activate_kwargs is None else on_activate_kwargs
        self.activate_condition = {} if activate_condition is None else activate_condition
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

    @property
    def is_available(self):
        available = self.cooldown_length >= 0 and self.cooldown == 0
        return available

    def is_possible(self, target, game):
        return self.activate_condition(self.owner, target, game, **self.activate_condition_kwargs)

    def cooldown_skill(self, reset=False):
        if reset:
            self.cooldown = self.cooldown_length
        elif self.cooldown > 0:
            self.cooldown -= 1

        logging.debug(
            f'Cooled down {self.name} on {self.owner.name}: {self.cooldown} of {self.cooldown_length}.')