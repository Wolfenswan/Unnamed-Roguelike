import logging
from random import choice

from config_files import colors
from gameobjects.entity import EntityStates
from gui.messages import Message

class Skill:
    def __init__(self, name = 'Skill', on_activate=None, on_activate_kwargs = {}, activate_condition=None, activate_condition_kwargs = {}, cooldown_length=None, messages=None, description=''):
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
        self.on_activate(actor, *args, **self.on_activate_kwargs)
        message = choice(self.messages)
        results.append({'message': Message(message)})
        self.cooldown_skill(reset=True)
        return results

    def is_available(self, game):
        actor = self.owner
        available = self.cooldown_length >= 0 and self.cooldown == 0 and self.activate_condition(game, actor, **self.activate_condition_kwargs)
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

# Skill Activation #

def skill_charge_activation(ent, *args, **kwargs):
    game = args[0]
    distance = kwargs['distance']
    # TODO cardinal direction instead of position
    # TODO Straight empty line to target
    target_x, target_y = game.player.x, game.player.y
    execute_string = f"monster.skills['skill_orc_charge_exec'].execute{target_x, target_y, distance}"
    ent.execute_after_delay = execute_string
    ent.state = EntityStates.ENTITY_WAITING
    ent.color_bg = colors.dark_red
    ent.delay_turns = 1

def skill_charge_execution(ent, *args, **kwargs):
    dx, dy = args[0], args[1]
    distance = args[2]
    # TODO x steps charge in cardinal direction
    ent.color_bg = colors.green

# Skill Conditions #

def skill_charge_condition(game, actor, **kwargs):
    player = game.player
    min, max = kwargs['min'], kwargs['max']
    if min < actor.distance_to_ent(player) < max:
        return True
    else:
        return False

def skill_always_true(*args):
    return True
