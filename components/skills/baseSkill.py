import logging

from typing import Callable, Dict, Set

from dataclasses import field, dataclass

from game import Game


@dataclass
class BaseSkill:
    name:str
    activate_conditions:Set[Callable]
    on_activate_kwargs: Dict = field(default_factory=dict)
    activate_condition_kwargs:Dict = field(default_factory=dict)
    cooldown_length : int = 0
    cooldown:int = field(init=False, default=0)

    def __str__(self):
        return f'{self.name}:{id(self)} on {self.owner}'

    def __repr__(self):
        return f'{self.name}:{id(self)}(Owner: {self.owner})'

    def prepare(self, *args, **kwargs):
        # TODO add exception
        logging.debug(f'{self} is missing a custom prepare() method')

    def execute(self, *args, **kwargs):
        # TODO add exception
        logging.debug(f'{self} is missing a custom execute() method')

    def use(self, *args):
        actor = self.owner
        results = []

        logging.debug(f'Special attack for {actor}. Cooldown {self.cooldown} of {self.cooldown_length}')
        if self.on_activate_kwargs['delay'] > 0:
            skill_results = self.prepare(*args, **self.on_activate_kwargs)
        else:
            skill_results = self.execute(*args, **self.on_activate_kwargs)
        results.extend(skill_results)
        self.cooldown_skill(reset=True)
        return results

    @property
    def is_available(self):
        available = self.cooldown_length >= 0 and self.cooldown == 0
        return available

    def is_active(self, target, game:Game):
        for cond in self.activate_conditions:
            check = cond(actor = self.owner, target = target, game = game, **self.activate_condition_kwargs)
            logging.debug(f'Condition {cond.__name__}: {check}')
            if not check:
                return False
        return True

    def cooldown_skill(self, reset=False):
        if reset:
            self.cooldown = self.cooldown_length
        elif self.cooldown > 0:
            self.cooldown -= 1
        logging.debug(
            f'Cooled down {self}: {self.cooldown} of {self.cooldown_length}.')