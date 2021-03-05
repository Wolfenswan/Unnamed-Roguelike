import logging
from random import randint
from typing import Callable, Dict, Set, Optional
from dataclasses import field, dataclass
from game import Game


@dataclass
class BaseSkill:
    name:str
    activate_conditions:Set[Callable]
    on_activate_kwargs: Dict = field(default_factory=dict)
    activate_condition_kwargs:Dict = field(default_factory=dict)
    cooldown_length : tuple = (0,0)
    cooldown:int = field(init=False, default=0)

    owner:Optional = None

    def __str__(self):
        return f'{self.name}:{id(self)} on {self.owner}. Cd: {self.cooldown}/{self.cooldown_length}'

    def __repr__(self):
        return f'{self.name}:{id(self)}(Owner: {self.owner})'

    def prepare(self, *args, **kwargs):
        # TODO add exception
        logging.debug(f'{self} is missing a custom prepare() method')

    def execute(self, *args, **kwargs):
        # TODO add exception
        logging.debug(f'{self} is missing a custom execute() method')

    def use(self, *args):
        results = []

        logging.debug(f'Using {self}.')
        if self.on_activate_kwargs.get('delay',1) > 0:
            skill_results = self.prepare(*args, **self.on_activate_kwargs)
        else:
            skill_results = self.execute(*args, **self.on_activate_kwargs)
        results.extend(skill_results)
        self.cooldown_skill(reset=True)
        return results

    @property
    def is_available(self):
        return self.cooldown == 0

    def is_active(self, target, game:Game):
        for cond in self.activate_conditions:
            check = cond(actor = self.owner, target = target, game = game, **self.activate_condition_kwargs)
            logging.debug(f'Condition {cond.__name__}: {check}')
            if not check:
                return False
        return True

    def cooldown_skill(self, reset=False):
        if reset:
            self.cooldown = randint(*self.cooldown_length)
        elif self.cooldown > 0:
            self.cooldown -= 1
        logging.debug(
            f'Cooling down {self}.')